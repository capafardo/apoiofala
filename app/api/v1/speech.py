"""
Rotas para Síntese de Voz (TTS).
"""

import shutil
import subprocess

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel

from app.services.speech import speech_service
from app.services import neural_tts

router = APIRouter(prefix="/speech", tags=["Síntese de Voz"])


class SpeechRequest(BaseModel):
    text: str
    language: str = "pt-BR"
    speed: float = 1.0


@router.post("/synthesize", summary="Solicitar síntese de voz para frase ou símbolo")
async def synthesize_speech(req: SpeechRequest):
    """Processa requisição de síntese de voz usando a camada abstrata SpeechService."""
    return speech_service.synthesize_text(
        text=req.text,
        language=req.language,
        speed=req.speed,
    )


@router.get(
    "/tts",
    summary="Sintetizar texto em áudio (voz neural Microsoft; fallback espeak-ng offline)",
)
async def text_to_speech(
    text: str = Query(..., min_length=1, max_length=500, description="Texto a ser falado"),
    speed: float = Query(1.0, ge=0.5, le=2.0, description="Velocidade relativa da fala (0.5 a 2.0)"),
    language: str = Query("pt-BR", description="Idioma desejado (pt-BR por padrão)"),
    engine: str = Query(
        "auto",
        pattern="^(auto|neural|espeak)$",
        description="Motor de síntese: auto (neural→espeak), neural (apenas online) ou espeak (offline)",
    ),
):
    """
    Gera o áudio da fala com voz **neural da Microsoft** (via edge-tts, gratuito
    e sem chave de API), com cache em disco para resposta instantânea.

    Sem conectividade com o serviço da Microsoft (ou com `engine=espeak`), usa o
    espeak-ng local — 100% offline — garantindo que o som sempre funcione.
    """
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Texto vazio para sintetizar")

    engine = (engine or "auto").lower()

    # Motor espeak legado (offline puro), quando solicitado explicitamente
    if engine == "espeak":
        return _synthesize_with_espeak(text, language, speed)

    # Motor neural (auto ou neural): edge-tts com fallback espeak em 'auto'
    try:
        audio, media_type, used = await neural_tts.synthesize_async(text, language, speed)
        if used == "edge-neural":
            return Response(
                content=audio,
                media_type=media_type,
                headers={"X-TTS-Engine": "edge-neural", "X-TTS-Voice": "microsoft"},
            )
        if engine == "neural":
            raise HTTPException(
                status_code=503,
                detail="Serviço neural indisponível e fallback desativado",
            )
        # 'auto': usa o resultado do fallback espeak
        return Response(content=audio, media_type=media_type, headers={"X-TTS-Engine": used})
    except HTTPException:
        raise
    except Exception as exc:
        if engine == "neural":
            raise HTTPException(
                status_code=503,
                detail=f"Serviço de voz neural indisponível: {exc}",
            )
        # 'auto': tenta o espeak local como último recurso
        return _synthesize_with_espeak(text, language, speed)


def _synthesize_with_espeak(text: str, language: str, speed: float) -> Response:
    """Síntese offline legada com espeak-ng (WAV)."""
    espeak = shutil.which("espeak-ng") or shutil.which("espeak")
    if not espeak:
        raise HTTPException(
            status_code=503,
            detail="Sintetizador espeak-ng não encontrado no sistema.",
        )

    lang = (language or "pt-BR").lower()
    voice = "pt-br" if lang.startswith("pt") else lang
    wpm = max(80, min(450, int(round(175 * speed))))

    try:
        proc = subprocess.run(
            [espeak, "-v", voice, "-s", str(wpm), "--stdout", text],
            capture_output=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Tempo esgotado na síntese de voz")

    if proc.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao sintetizar o texto (código {proc.returncode})",
        )

    return Response(
        content=proc.stdout,
        media_type="audio/wav",
        headers={"X-TTS-Engine": "espeak-ng"},
    )
