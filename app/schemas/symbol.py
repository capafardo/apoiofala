"""
Schemas Pydantic para Pictogramas / Símbolos.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class SymbolBase(BaseModel):
    category_id: int
    name: str
    text_label: str
    image_path: str
    spoken_text: Optional[str] = None
    bg_color: Optional[str] = None
    border_color: Optional[str] = None
    order_index: int = 0
    is_active: bool = True
    profile_id: Optional[int] = None


class SymbolCreate(SymbolBase):
    pass


class SymbolUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    text_label: Optional[str] = None
    image_path: Optional[str] = None
    spoken_text: Optional[str] = None
    bg_color: Optional[str] = None
    border_color: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None


class SymbolResponse(SymbolBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
