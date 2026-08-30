"""
Rotas para Categorias de Símbolos.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from app.api.deps import require_professional_or_admin

router = APIRouter(prefix="/categories", tags=["Categorias"])


@router.get("", response_model=List[CategoryResponse], summary="Listar categorias ativas")
async def list_categories(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    """Retorna lista ordenada de categorias."""
    query = db.query(Category)
    if not include_inactive:
        query = query.filter(Category.is_active.is_(True))
    return query.order_index(Category.order_index.asc()).all() if hasattr(query, "order_index") else query.order_by(Category.order_index.asc()).all()


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar categoria (Profissional/Admin)",
)
async def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Cria uma nova categoria de símbolos."""
    existing = db.query(Category).filter(
        (Category.name == cat_in.name) | (Category.slug == cat_in.slug)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria com este nome ou identificador já existe",
        )

    category = Category(**cat_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Atualizar categoria",
)
async def update_category(
    category_id: int,
    cat_in: CategoryUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_professional_or_admin),
):
    """Atualiza dados de uma categoria."""
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada",
        )

    for field, value in cat_in.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)

    db.commit()
    db.refresh(cat)
    return cat
