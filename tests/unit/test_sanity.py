"""Teste de sanidade inicial para validação do ambiente de testes."""

import pytest
import app


def test_package_version():
    """Verifica se o pacote app expõe versão válida."""
    assert hasattr(app, "__version__")
    assert isinstance(app.__version__, str)
