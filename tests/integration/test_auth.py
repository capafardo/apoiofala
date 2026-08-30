"""Testes de integração para rotas de autenticação."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_database():
    """Garante banco populado para testes."""
    init_db()


@pytest.mark.asyncio
async def test_login_success_admin():
    """Valida login com credenciais válidas do admin."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "admin"
        assert data["user"]["role"] == "admin"


@pytest.mark.asyncio
async def test_login_invalid_password():
    """Valida rejeição de senha incorreta."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "senhaInvalida"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authenticated():
    """Valida endpoint /me com token JWT válido."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"username": "joaopedro", "password": "joao123"},
        )
        token = login_res.json()["access_token"]

        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "joaopedro"
        assert data["role"] == "user"


@pytest.mark.asyncio
async def test_admin_register_new_user():
    """Valida que administrador pode cadastrar novos usuários."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        admin_login = await client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        admin_token = admin_login.json()["access_token"]

        new_user_data = {
            "username": "novousuario",
            "full_name": "Novo Usuário Teste",
            "password": "senhaNova123!",
            "role": "user",
        }
        res = await client.post(
            "/api/v1/auth/register",
            json=new_user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 201
        data = res.json()
        assert data["username"] == "novousuario"


@pytest.mark.asyncio
async def test_user_cannot_register_others():
    """Valida que usuário comum é bloqueado (403) ao tentar cadastrar novos usuários."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        user_login = await client.post(
            "/api/v1/auth/login",
            json={"username": "joaopedro", "password": "joao123"},
        )
        user_token = user_login.json()["access_token"]

        res = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "hacker",
                "full_name": "Invasor",
                "password": "123",
                "role": "admin",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert res.status_code == 403
