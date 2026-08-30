"""Testes de integração para personalização de pranchas e criação de perfis com apelidos."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_all_categories_have_symbols():
    """Valida se todas as categorias (Comunicar, Necessidades, Pessoas, Lugares, Brincar, Mais, etc.) contêm símbolos."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        cats_res = await client.get("/api/v1/categories")
        categories = cats_res.json()
        assert len(categories) >= 10

        for cat in categories:
            res = await client.get(f"/api/v1/symbols?category_id={cat['id']}")
            assert res.status_code == 200
            symbols = res.json()
            assert len(symbols) > 0, f"Categoria '{cat['name']}' ({cat['slug']}) está sem símbolos!"


@pytest.mark.asyncio
async def test_get_library_symbols():
    """Valida retorno da biblioteca geral de símbolos."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/symbols/library")
        assert res.status_code == 200
        library = res.json()
        assert len(library) >= 50


@pytest.mark.asyncio
async def test_create_profile_with_nicknames():
    """Valida criação de perfil com apelido da criança e apelido da mãe/acompanhante."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Login profissional
        login = await client.post(
            "/api/v1/auth/login",
            json={"username": "terapeuta", "password": "terapeuta123"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        profile_data = {
            "name": "Leonardo Santos",
            "child_nickname": "Leo",
            "guardian_nickname": "Mãe Juliana",
            "symbol_size": "grande",
            "symbols_per_page": 6,
            "voice_speed": 1.1,
        }
        res = await client.post("/api/v1/profiles", json=profile_data, headers=headers)
        assert res.status_code == 201
        created = res.json()
        assert created["child_nickname"] == "Leo"
        assert created["guardian_nickname"] == "Mãe Juliana"
        assert created["symbol_size"] == "grande"


@pytest.mark.asyncio
async def test_drag_and_drop_assign_symbols_to_profile_category():
    """Valida atribuição e customização de símbolos para uma categoria de um perfil específico."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        login = await client.post(
            "/api/v1/auth/login",
            json={"username": "terapeuta", "password": "terapeuta123"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Obter perfis e categorias
        profiles = (await client.get("/api/v1/profiles", headers=headers)).json()
        categories = (await client.get("/api/v1/categories")).json()
        library = (await client.get("/api/v1/symbols/library")).json()

        profile_id = profiles[0]["id"]
        category_id = categories[0]["id"]

        # Selecionar 3 símbolos da biblioteca
        selected_ids = [library[0]["id"], library[1]["id"], library[2]["id"]]

        # Atribuir via endpoint de drag & drop
        assign_res = await client.post(
            f"/api/v1/symbols/profiles/{profile_id}/categories/{category_id}/assign",
            json={"symbol_ids": selected_ids},
            headers=headers,
        )
        assert assign_res.status_code == 200
        assert assign_res.json()["status"] == "ok"

        # Verificar se ao buscar símbolos do perfil para aquela categoria, retornam exatamente os 3 atribuídos
        sym_res = await client.get(
            f"/api/v1/symbols?category_id={category_id}&profile_id={profile_id}"
        )
        assert sym_res.status_code == 200
        custom_symbols = sym_res.json()
        assert len(custom_symbols) == 3
        custom_ids = [s["id"] for s in custom_symbols]
        assert custom_ids == selected_ids
