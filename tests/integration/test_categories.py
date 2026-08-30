"""Testes de integração para categorias de símbolos."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_list_categories():
    """Valida listagem de categorias cadastradas."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/categories")
        assert res.status_code == 200
        categories = res.json()
        assert len(categories) >= 10
        slugs = [c["slug"] for c in categories]
        assert "inicio" in slugs
        assert "comida-bebida" in slugs
        assert "sentimentos" in slugs
