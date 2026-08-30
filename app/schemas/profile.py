"""
Schemas Pydantic para Perfis de Criança/Paciente.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.profile import SymbolSize, ContrastMode


class ProfileBase(BaseModel):
    name: str
    symbol_size: SymbolSize = SymbolSize.MEDIUM
    symbols_per_page: int = 12
    theme_color: str = "blue"
    contrast_mode: ContrastMode = ContrastMode.NORMAL
    voice_speed: float = 1.0
    voice_pitch: float = 1.0
    voice_name: Optional[str] = None
    complexity_level: int = 1


class ProfileCreate(ProfileBase):
    user_id: Optional[int] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    symbol_size: Optional[SymbolSize] = None
    symbols_per_page: Optional[int] = None
    theme_color: Optional[str] = None
    contrast_mode: Optional[ContrastMode] = None
    voice_speed: Optional[float] = None
    voice_pitch: Optional[float] = None
    voice_name: Optional[str] = None
    complexity_level: Optional[int] = None


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
