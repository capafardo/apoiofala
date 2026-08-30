"""
Schemas Pydantic para Frases Rápidas.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class QuickPhraseBase(BaseModel):
    text: str
    spoken_text: Optional[str] = None
    icon: str = "message-circle"
    order_index: int = 0
    is_active: bool = True
    profile_id: Optional[int] = None
    category_id: Optional[int] = None


class QuickPhraseCreate(QuickPhraseBase):
    pass


class QuickPhraseUpdate(BaseModel):
    text: Optional[str] = None
    spoken_text: Optional[str] = None
    icon: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class QuickPhraseResponse(QuickPhraseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
