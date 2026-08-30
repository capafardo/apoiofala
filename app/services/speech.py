"""
Serviço de Síntese de Voz (TTS) - Abstração e Provedores Locais.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.core.config import settings


class BaseSpeechProvider(ABC):
    """Interface abstrata para provedores de síntese de voz."""

    @abstractmethod
    def synthesize(self, text: str, language: str = "pt-BR", speed: float = 1.0) -> Dict[str, Any]:
        """Processa a solicitação de síntese de voz."""
        pass


class WebSpeechLocalProvider(BaseSpeechProvider):
    """
    Provedor padrão para execução direta via Web Speech API do navegador.
    100% offline, latência zero, suporta português nativo.
    """

    def synthesize(self, text: str, language: str = "pt-BR", speed: float = 1.0) -> Dict[str, Any]:
        return {
            "provider": "web_speech_api",
            "text": text,
            "language": language or settings.DEFAULT_LANGUAGE,
            "speed": speed or settings.DEFAULT_VOICE_RATE,
            "mode": "client_side",
            "status": "ready",
        }


class SpeechService:
    """Gerenciador central do serviço de voz."""

    def __init__(self, provider: Optional[BaseSpeechProvider] = None):
        self.provider = provider or WebSpeechLocalProvider()

    def set_provider(self, provider: BaseSpeechProvider):
        self.provider = provider

    def synthesize_text(self, text: str, language: str = "pt-BR", speed: float = 1.0) -> Dict[str, Any]:
        if not text or not text.strip():
            return {"status": "error", "message": "Texto vazio para sintetizar"}
        return self.provider.synthesize(text.strip(), language=language, speed=speed)


# Instância singleton padrão do serviço
speech_service = SpeechService()
