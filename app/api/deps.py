"""
Dependências de injeção para FastAPI (banco, autenticação e permissões).
"""

from typing import List, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_token_from_request(
    request: Request,
    token_header: Optional[str] = Depends(oauth2_scheme),
) -> Optional[str]:
    """Extrai o token JWT do header Authorization ou de cookie de sessão."""
    if token_header:
        return token_header
    # Fallback para cookie de sessão
    return request.cookies.get("access_token")


async def get_current_user(
    token: Optional[str] = Depends(get_token_from_request),
    db: Session = Depends(get_db),
) -> User:
    """Extrai e valida o usuário a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    username: str = payload.get("sub")
    if not username:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Garante que o usuário atual está ativo."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo no sistema",
        )
    return current_user


def require_roles(allowed_roles: List[UserRole]):
    """Fábrica de dependências para restrição baseada em papéis/roles."""

    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso não autorizado para o perfil do usuário",
            )
        return current_user

    return role_checker


require_admin = require_roles([UserRole.ADMIN])
require_professional_or_admin = require_roles([UserRole.ADMIN, UserRole.PROFESSIONAL])
