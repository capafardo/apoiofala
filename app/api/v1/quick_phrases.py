"""
Rotas para Frases Rápidas.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.quick_phrase import QuickPhrase
from app.schemas.quick_phrase import (
    QuickPhraseResponse,
    QuickPhraseCreate,
    QuickPhraseUpdate,
)
from app.api.deps import require_professional_or_admin

router = APIRouter(prefix="/quick-phrases", tags=["Frases Rápidas"])


@router.get("", response_model=List[QuickPhraseResponse], summary="Listar frases rápidas")
async def list_quick_phrases(
    profile_id: Optional[int] = None,
    category_id: Optional[int] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    """Retorna frases rápidas ordenadas."""
    query = db.query(QuickPhrase)
    if not include_inactive:
        query = query.filter(QuickPhrase.is_active.is_(True))
    if profile_id is not None:
        query = query.filter(
            (QuickPhrase.profile_id == profile_id) | (QuickPhrase.profile_id.is_(None))
        )
    if category_id is not None:
        query = query.filter(QuickPhrase.category_id == category_id)

    return query.order_by(QuickPhrase.order_index.asc(), QuickPhrase.id.asc()).all()


@router.post(
    "",
    response_model=QuickPhraseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar frase rápida (Profissional/Admin)",
)
async def create_quick_phrase(
    phrase_in: QuickPhraseCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Cadastra uma nova frase rápida."""
    qp = QuickPhrase(**phrase_in.model_dump())
    db.add(qp)
    db.commit()
    db.refresh(qp)
    return qp


@router.put(
    "/{phrase_id}",
    response_model=QuickPhraseResponse,
    summary="Atualizar frase rápida",
)
async def update_quick_phrase(
    phrase_id: int,
    phrase_in: QuickPhraseUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Atualiza dados de uma frase rápida."""
    qp = db.query(QuickPhrase).filter(QuickPhrase.id == phrase_id).first()
    if not qp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frase rápida não encontrada",
        )

    for field, value in phrase_in.model_dump(exclude_unset=True).items():
        setattr(qp, field, value)

    db.commit()
    db.refresh(qp)
    return qp


@router.delete(
    "/{phrase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover frase rápida",
)
async def delete_quick_phrase(
    phrase_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Remove uma frase rápida."""
    qp = db.query(QuickPhrase).filter(QuickPhrase.id == phrase_id).first()
    if not qp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frase rápida não encontrada",
        )
    db.delete(qp)
    db.commit()
    return None
