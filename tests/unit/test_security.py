"""Testes unitários para utilitários de segurança e JWT."""

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_password_hashing():
    """Valida que o hash não armazena senha em texto puro e verifica corretamente."""
    password = "senhaSegura123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert verify_password(password, hashed) is True
    assert verify_password("senhaErrada", hashed) is False


def test_jwt_token_cycle():
    """Valida geração e decodificação de JWT."""
    username = "joaopedro"
    role = "user"
    token = create_access_token(subject=username, role=role)

    assert isinstance(token, str)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == username
    assert payload.get("role") == role
