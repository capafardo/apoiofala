"""Testes unitários para configurações do sistema."""

from app.core.config import settings


def test_settings_defaults():
    """Valida configurações padrão essenciais."""
    assert settings.APP_NAME == "CAA-Lab"
    assert settings.PORT == 8000
    assert "sqlite" in settings.DATABASE_URL
    assert settings.DEFAULT_LANGUAGE == "pt-BR"
