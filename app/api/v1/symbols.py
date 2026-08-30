"""
Rotas para Catálogo de Pictogramas e Símbolos.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.symbol import Symbol
from app.schemas.symbol import SymbolResponse, SymbolCreate, SymbolUpdate
from app.api.deps import require_professional_or_admin

router = APIRouter(prefix="/symbols", tags=["Símbolos"])


@router.get("", response_model=List[SymbolResponse], summary="Listar símbolos")
async def list_symbols(
    category_id: Optional[int] = None,
    profile_id: Optional[int] = None,
    search: Optional[str] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    """Retorna símbolos filtrados por categoria, perfil ou termo de busca."""
    query = db.query(Symbol)

    if not include_inactive:
        query = query.filter(Symbol.is_active.is_(True))

    if category_id is not None:
        query = query.filter(Symbol.category_id == category_id)

    if profile_id is not None:
        # Retorna símbolos globais (profile_id is None) OU customizados para este perfil
        query = query.filter(
            (Symbol.profile_id.is_(None)) | (Symbol.profile_id == profile_id)
        )

    if search:
        search_pattern = f"%{search.strip().lower()}%"
        query = query.filter(
            Symbol.name.ilike(search_pattern) | Symbol.text_label.ilike(search_pattern)
        )

    return query.order_by(Symbol.order_index.asc(), Symbol.name.asc()).all()


@router.get("/{symbol_id}", response_model=SymbolResponse, summary="Obter símbolo por ID")
async def get_symbol(symbol_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes de um símbolo específico."""
    sym = db.query(Symbol).filter(Symbol.id == symbol_id).first()
    if not sym:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Símbolo não encontrado",
        )
    return sym


@router.post(
    "",
    response_model=SymbolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo símbolo (Profissional/Admin)",
)
async def create_symbol(
    sym_in: SymbolCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Cadastra um novo pictograma no sistema."""
    symbol = Symbol(**sym_in.model_dump())
    db.add(symbol)
    db.commit()
    db.refresh(symbol)
    return symbol


@router.put(
    "/{symbol_id}",
    response_model=SymbolResponse,
    summary="Atualizar símbolo",
)
async def update_symbol(
    symbol_id: int,
    sym_in: SymbolUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Atualiza dados ou ativação de um pictograma."""
    sym = db.query(Symbol).filter(Symbol.id == symbol_id).first()
    if not sym:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Símbolo não encontrado",
        )

    for field, value in sym_in.model_dump(exclude_unset=True).items():
        setattr(sym, field, value)

    db.commit()
    db.refresh(sym)
    return sym


@router.delete(
    "/{symbol_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover símbolo",
)
async def delete_symbol(
    symbol_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Remove um pictograma do sistema."""
    sym = db.query(Symbol).filter(Symbol.id == symbol_id).first()
    if not sym:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Símbolo não encontrado",
        )
    db.delete(sym)
    db.commit()
    return None
