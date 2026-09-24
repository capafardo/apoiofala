"""
Provedor de TTS Neuronal (Microsoft Edge / Azure Neural Voices via edge-tts).

Usa o serviço de TTS do Microsoft Edge gratuitamente, sem chave de API,
produzindo vozes naturais (ex.: pt-BR-FranciscaNeural) muito superiores ao
espeak-ng. O resultado (MP3 24 kHz) é armazenado em cache em disco para
resposta instantânea em repetições e uso reduzido da rede.

Fallback: quando não há conectividade com a Microsoft, a síntese cai para o
espeak-ng local (100% offline), garantindo o princípio fail-safe do projeto.
"""

import asyncio
import hashlib
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple

from app.core.config import settings

try:
    import edge_tts

    EDGE_TTS_AVAILABLE = True
except ImportError:  # pragma: no cover - dependência opcional
    edge_tts = None
    EDGE_TTS_AVAILABLE = False

# Vozes neuronais pt-BR da Microsoft (qualidade natural, uso gratuito via Edge)
VOICE_PT_BR_FEMALE = "pt-BR-FranciscaNeural"
VOICE_PT_BR_MALE = "pt-BR-AntonioNeural"

# Mapeia idiomas suportados para as vozes neuronais correspondentes
LANGUAGE_VOICES = {
    "pt-br": VOICE_PT_BR_FEMALE,
    "pt": VOICE_PT_BR_FEMALE,
    "en-us": "en-US-AriaNeural",
    "en": "en-US-AriaNeural",
    "es-es": "es-ES-ElviraNeural",
    "es": "es-ES-ElviraNeural",
}

# Timeout da síntese online (segundos) — mantido baixo (3s) para resposta ágil sem travar offline
SYNTH_TIMEOUT_S = 3

# Circuit breaker para operação offline: após falha de rede, não tenta novamente por 60s
_LAST_NETWORK_FAILURE = 0.0
_CIRCUIT_BREAKER_SECONDS = 60.0


def _cache_dir() -> Path:
    """Diretório de cache de áudio sintetizado (persistente)."""
    d = settings.ASSETS_DIR / "audio" / "tts-cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _voice_for_language(language: str) -> str:
    """Escolhe a voz neuronal adequada ao idioma solicitado."""
    lang = (language or settings.DEFAULT_LANGUAGE).lower().replace("_", "-")
    return LANGUAGE_VOICES.get(lang, VOICE_PT_BR_FEMALE)


def _cache_path(text: str, voice: str, rate: str) -> Path:
    """Caminho determinístico no cache para (texto, voz, velocidade)."""
    key = hashlib.sha1(f"{voice}|{rate}|{text}".encode("utf-8")).hexdigest()
    return _cache_dir() / f"{key}.mp3"


def _rate_percent(speed: float) -> str:
    """Converte o fator relativo (0.5–2.0) no formato '+N%' do edge-tts."""
    pct = int(round((speed - 1.0) * 100))
    return f"{'+' if pct >= 0 else ''}{pct}%"


def _should_try_online() -> bool:
    """Verifica se devemos tentar síntese online na Microsoft."""
    if not EDGE_TTS_AVAILABLE:
        return False
    if getattr(settings, "TTS_OFFLINE_MODE", False):
        return False
    # Circuit breaker: evita travar a interface com timeouts se a rede estiver fora
    if time.monotonic() - _LAST_NETWORK_FAILURE < _CIRCUIT_BREAKER_SECONDS:
        return False
    return True


def is_available() -> bool:
    """Indica se o provedor neuronal pode ser utilizado neste ambiente."""
    return _should_try_online()


async def _synthesize_online(text: str, voice: str, rate: str) -> bytes:
    """Síntese via serviço do Microsoft Edge (retorna MP3)."""
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    chunks: list[bytes] = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            chunks.append(chunk["data"])
    if not chunks:
        raise RuntimeError("Serviço de TTS neuronal não retornou áudio")
    return b"".join(chunks)


def _synthesize_espeak(text: str, language: str, speed: float) -> Tuple[bytes, str]:
    """Fallback offline com espeak-ng (retorna WAV)."""
    espeak = shutil.which("espeak-ng") or shutil.which("espeak")
    if not espeak:
        raise RuntimeError("Sintetizador espeak-ng não encontrado no sistema")

    lang = (language or settings.DEFAULT_LANGUAGE).lower()
    voice = "pt-br" if lang.startswith("pt") else lang
    wpm = max(80, min(450, int(round(175 * speed))))

    proc = subprocess.run(
        [espeak, "-v", voice, "-s", str(wpm), "--stdout", text],
        capture_output=True,
        timeout=30,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Falha na síntese espeak-ng (código {proc.returncode})")
    return proc.stdout, "audio/wav"


def synthesize(text: str, language: str = "pt-BR", speed: float = 1.0) -> Tuple[bytes, str, str]:
    """
    Sintetiza `text` com voz neuronal da Microsoft (cache em disco).

    Retorna (conteúdo_áudio, media_type, motor_usado) em que motor_usado é
    'edge-neural' ou 'espeak-ng' (fallback offline).
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Texto vazio para sintetizar")

    voice = _voice_for_language(language)
    rate = _rate_percent(speed)
    cache_file = _cache_path(text, voice, rate)

    # 1. Cache em disco: resposta instantânea sem rede
    if cache_file.is_file() and cache_file.stat().st_size > 0:
        return cache_file.read_bytes(), "audio/mpeg", "edge-neural"

    # 2. Síntese online (Microsoft Edge) com limite de tempo e circuit-breaker
    if _should_try_online():
        try:
            async def _run() -> bytes:
                return await asyncio.wait_for(
                    _synthesize_online(text, voice, rate), timeout=SYNTH_TIMEOUT_S
                )

            audio = asyncio.run(_run())
            cache_file.write_bytes(audio)
            return audio, "audio/mpeg", "edge-neural"
        except Exception:
            global _LAST_NETWORK_FAILURE
            _LAST_NETWORK_FAILURE = time.monotonic()
            pass  # cai imediatamente para o fallback offline

    # 3. Fallback 100% offline (espeak-ng)
    audio, media_type = _synthesize_espeak(text, language, speed)
    return audio, media_type, "espeak-ng"


async def synthesize_async(
    text: str, language: str = "pt-BR", speed: float = 1.0
) -> Tuple[bytes, str, str]:
    """Versão assíncrona de `synthesize` (evita bloquear o event loop)."""
    return await asyncio.to_thread(synthesize, text, language, speed)
