"""
Rotas de Autenticação e Gestão de Sessão.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
)
from app.api.deps import get_current_active_user, require_admin

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse, summary="Autenticação de usuário")
async def login(
    login_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """Autentica usuário com username e senha, retornando token JWT e cookie."""
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta inativa",
        )

    token = create_access_token(subject=user.username, role=user.role.value)

    # Configurar cookie httpOnly para conveniência no navegador
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,  # 24 horas
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/logout", summary="Encerramento de sessão")
async def logout(response: Response):
    """Limpa o cookie de sessão."""
    response.delete_cookie("access_token")
    return {"message": "Sessão encerrada com sucesso"}


@router.get("/me", response_model=UserResponse, summary="Dados do usuário atual")
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Retorna os dados do usuário autenticado no momento."""
    return current_user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastro de novo usuário (Admin)",
)
async def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """Cadastra um novo usuário no sistema (requer perfil de Administrador)."""
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já cadastrado",
        )

    hashed_pw = get_password_hash(user_in.password)
    new_user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        password_hash=hashed_pw,
        role=user_in.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
