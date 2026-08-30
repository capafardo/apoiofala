"""
Rotas para Perfis de Criança/Paciente e Personalização.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.profile import Profile
from app.schemas.profile import ProfileResponse, ProfileCreate, ProfileUpdate
from app.api.deps import get_current_active_user, require_professional_or_admin

router = APIRouter(prefix="/profiles", tags=["Perfis"])


@router.get("", response_model=List[ProfileResponse], summary="Listar perfis")
async def list_profiles(
    db: Session = Depends(get_db),
    _user=Depends(get_current_active_user),
):
    """Retorna lista de todos os perfis cadastrados."""
    return db.query(Profile).order_by(Profile.name.asc()).all()


@router.get("/{profile_id}", response_model=ProfileResponse, summary="Obter perfil por ID")
async def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_active_user),
):
    """Retorna dados e configurações do perfil."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil não encontrado",
        )
    return profile


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar perfil (Profissional/Admin)",
)
async def create_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Cria um novo perfil de criança/paciente."""
    profile = Profile(**profile_in.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.put(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Atualizar configurações do perfil",
)
async def update_profile(
    profile_id: int,
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Atualiza configurações de tamanho de símbolos, contraste, tema ou voz do perfil."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil não encontrado",
        )

    for field, value in profile_in.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
