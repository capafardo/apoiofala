"""Testes de integração para símbolos e busca."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_list_symbols():
    """Valida listagem de símbolos."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/symbols")
        assert res.status_code == 200
        symbols = res.json()
        assert len(symbols) >= 15
        names = [s["name"] for s in symbols]
        assert "eu" in names
        assert "quero" in names
        assert "beber" in names


@pytest.mark.asyncio
async def test_filter_symbols_by_category():
    """Valida filtro por categoria."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Obter categoria de comida e bebida
        cats_res = await client.get("/api/v1/categories")
        food_cat = next(c for c in cats_res.json() if c["slug"] == "comida-bebida")

        res = await client.get(f"/api/v1/symbols?category_id={food_cat['id']}")
        assert res.status_code == 200
        symbols = res.json()
        assert len(symbols) >= 8
        labels = [s["text_label"] for s in symbols]
        assert "água" in labels
        assert "leite" in labels


@pytest.mark.asyncio
async def test_search_symbols():
    """Valida busca textual por símbolo."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/symbols?search=casa")
        assert res.status_code == 200
        symbols = res.json()
        assert len(symbols) >= 1
        assert symbols[0]["name"] == "casa"
