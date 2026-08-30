"""
Schemas Pydantic para Categorias.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: str = "folder"
    color: str = "#3b82f6"
    order_index: int = 0
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
