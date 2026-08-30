"""Testes de integração para frases rápidas."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_list_quick_phrases():
    """Valida listagem de frases rápidas."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/quick-phrases")
        assert res.status_code == 200
        phrases = res.json()
        assert len(phrases) >= 4
        texts = [p["text"] for p in phrases]
        assert "Eu quero ir para casa." in texts
        assert "Estou com fome." in texts
