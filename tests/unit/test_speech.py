"""Testes unitários para abstração do SpeechService."""

from app.services.speech import speech_service, WebSpeechLocalProvider


def test_speech_service_synthesis():
    """Valida retorno padronizado do sintetizador local."""
    result = speech_service.synthesize_text("Eu quero água.")
    assert result["status"] == "ready"
    assert result["text"] == "Eu quero água."
    assert result["language"] == "pt-BR"
    assert result["mode"] == "client_side"


def test_speech_empty_text():
    """Valida tratamento de texto vazio."""
    result = speech_service.synthesize_text("")
    assert result["status"] == "error"
