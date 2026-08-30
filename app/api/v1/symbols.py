"""
Rotas para Catálogo de Pictogramas e Símbolos e Personalização por Perfil.
"""

from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.symbol import Symbol
from app.models.profile_symbol import ProfileSymbol
from app.schemas.symbol import SymbolResponse, SymbolCreate, SymbolUpdate
from app.api.deps import require_professional_or_admin

router = APIRouter(prefix="/symbols", tags=["Símbolos"])


class ProfileCategorySymbolsUpdate(BaseModel):
    symbol_ids: List[int]


@router.get("/library", response_model=List[SymbolResponse], summary="Biblioteca geral de símbolos")
async def get_library_symbols(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Retorna todos os símbolos disponíveis na biblioteca global do sistema."""
    query = db.query(Symbol).filter(Symbol.is_active.is_(True))
    if search:
        pattern = f"%{search.strip().lower()}%"
        query = query.filter(
            Symbol.name.ilike(pattern) | Symbol.text_label.ilike(pattern)
        )
    return query.order_by(Symbol.name.asc()).all()


@router.get("", response_model=List[SymbolResponse], summary="Listar símbolos")
async def list_symbols(
    category_id: Optional[int] = None,
    profile_id: Optional[int] = None,
    search: Optional[str] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    """Retorna símbolos filtrados por categoria, considerando customização por perfil."""
    # Se category_id e profile_id forem passados, verificar se o perfil possui prancha personalizada
    if category_id is not None and profile_id is not None:
        custom_links = (
            db.query(ProfileSymbol)
            .filter(
                ProfileSymbol.profile_id == profile_id,
                ProfileSymbol.category_id == category_id,
                ProfileSymbol.is_active.is_(True),
            )
            .order_by(ProfileSymbol.order_index.asc())
            .all()
        )
        if custom_links:
            symbol_ids = [link.symbol_id for link in custom_links]
            # Carregar símbolos na ordem definida
            symbols = db.query(Symbol).filter(Symbol.id.in_(symbol_ids)).all()
            sym_dict = {s.id: s for s in symbols}
            ordered_symbols = [sym_dict[sid] for sid in symbol_ids if sid in sym_dict]
            if search:
                s_lower = search.strip().lower()
                ordered_symbols = [
                    s for s in ordered_symbols
                    if s_lower in s.name.lower() or s_lower in s.text_label.lower()
                ]
            return ordered_symbols

    query = db.query(Symbol)

    if not include_inactive:
        query = query.filter(Symbol.is_active.is_(True))

    if category_id is not None:
        query = query.filter(Symbol.category_id == category_id)

    if search:
        search_pattern = f"%{search.strip().lower()}%"
        query = query.filter(
            Symbol.name.ilike(search_pattern) | Symbol.text_label.ilike(search_pattern)
        )

    return query.order_by(Symbol.order_index.asc(), Symbol.name.asc()).all()


@router.post(
    "/profiles/{profile_id}/categories/{category_id}/assign",
    summary="Associar múltiplos símbolos à categoria de um perfil (Drag and Drop)",
)
async def assign_symbols_to_profile_category(
    profile_id: int,
    category_id: int,
    payload: ProfileCategorySymbolsUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Substitui ou adiciona símbolos à prancha daquela categoria para o perfil da criança."""
    # Remover associações anteriores dessa categoria para esse perfil
    db.query(ProfileSymbol).filter(
        ProfileSymbol.profile_id == profile_id,
        ProfileSymbol.category_id == category_id,
    ).delete()

    # Inserir novos símbolos na ordem indicada
    for idx, sid in enumerate(payload.symbol_ids):
        link = ProfileSymbol(
            profile_id=profile_id,
            symbol_id=sid,
            category_id=category_id,
            order_index=idx + 1,
            is_active=True,
        )
        db.add(link)

    db.commit()
    return {
        "status": "ok",
        "message": f"{len(payload.symbol_ids)} símbolos atribuídos à categoria com sucesso",
    }


@router.post(
    "/profiles/{profile_id}/categories/{category_id}/add",
    summary="Adicionar um ou mais símbolos à categoria existente de um perfil",
)
async def add_symbols_to_profile_category(
    profile_id: int,
    category_id: int,
    payload: ProfileCategorySymbolsUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Adiciona símbolos adicionais sem apagar os já existentes."""
    existing_links = db.query(ProfileSymbol).filter(
        ProfileSymbol.profile_id == profile_id,
        ProfileSymbol.category_id == category_id,
    ).all()
    existing_symbol_ids = {l.symbol_id for l in existing_links}
    next_order = len(existing_links) + 1

    # Se ainda não havia customização, copiar os padrões da categoria primeiro
    if not existing_links:
        default_symbols = db.query(Symbol).filter(
            Symbol.category_id == category_id,
            Symbol.is_active.is_(True)
        ).order_by(Symbol.order_index.asc()).all()
        for idx, ds in enumerate(default_symbols):
            db.add(ProfileSymbol(
                profile_id=profile_id,
                symbol_id=ds.id,
                category_id=category_id,
                order_index=idx + 1,
                is_active=True,
            ))
            existing_symbol_ids.add(ds.id)
        next_order = len(default_symbols) + 1

    added_count = 0
    for sid in payload.symbol_ids:
        if sid not in existing_symbol_ids:
            db.add(ProfileSymbol(
                profile_id=profile_id,
                symbol_id=sid,
                category_id=category_id,
                order_index=next_order,
                is_active=True,
            ))
            existing_symbol_ids.add(sid)
            next_order += 1
            added_count += 1

    db.commit()
    return {"status": "ok", "added": added_count}


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
