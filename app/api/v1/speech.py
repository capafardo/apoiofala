"""
Rotas para Síntese de Voz (TTS).
"""

from pydantic import BaseModel
from fastapi import APIRouter
from app.services.speech import speech_service

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
