"""Testes de integração para perfis e configurações."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_list_and_update_profile():
    """Valida listagem e atualização de preferências do perfil."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Login como terapeuta
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"username": "terapeuta", "password": "terapeuta123"},
        )
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Obter perfis
        res = await client.get("/api/v1/profiles", headers=headers)
        assert res.status_code == 200
        profiles = res.json()
        assert len(profiles) >= 1
        profile_id = profiles[0]["id"]

        # Atualizar perfil
        update_data = {
            "symbol_size": "grande",
            "symbols_per_page": 20,
            "voice_speed": 1.2,
        }
        put_res = await client.put(
            f"/api/v1/profiles/{profile_id}",
            json=update_data,
            headers=headers,
        )
        assert put_res.status_code == 200
        updated = put_res.json()
        assert updated["symbol_size"] == "grande"
        assert updated["symbols_per_page"] == 20
        assert updated["voice_speed"] == 1.2
