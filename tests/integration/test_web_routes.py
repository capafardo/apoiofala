"""Testes de integração para as rotas web e arquivos estáticos."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_index_page_returns_html():
    """Valida se GET / retorna a prancha do Modo Criança."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/")
        assert res.status_code == 200
        assert "CAA-Lab" in res.text
        assert "MODO CRIANÇA" in res.text
        assert "MINHA MENSAGEM" in res.text


@pytest.mark.asyncio
async def test_professional_page_returns_html():
    """Valida se GET /profissional retorna o painel profissional."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/profissional")
        assert res.status_code == 200
        assert "Modo Profissional" in res.text
        assert "Painel" in res.text


@pytest.mark.asyncio
async def test_static_assets_available():
    """Valida se CSS e pictogramas estáticos são servidos."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        css_res = await client.get("/static/css/style.css")
        assert css_res.status_code == 200

        svg_res = await client.get("/static/pictograms/eu.svg")
        assert svg_res.status_code == 200
        assert "<svg" in svg_res.text
