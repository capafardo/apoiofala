"""
Modelo de Perfil de Paciente / Criança do CAA-Lab.
"""

from datetime import datetime, timezone
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base


class SymbolSize(str, enum.Enum):
    SMALL = "pequeno"
    MEDIUM = "medio"
    LARGE = "grande"


class ContrastMode(str, enum.Enum):
    NORMAL = "normal"
    HIGH_CONTRAST = "alto_contraste"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    
    # Identificação da Criança e Responsável / Acompanhante
    child_nickname = Column(String(100), nullable=True)
    guardian_nickname = Column(String(100), nullable=True)
    
    # Configurações visuais e de acessibilidade
    symbol_size = Column(Enum(SymbolSize), default=SymbolSize.MEDIUM, nullable=False)
    symbols_per_page = Column(Integer, default=12, nullable=False)
    theme_color = Column(String(30), default="blue", nullable=False)
    contrast_mode = Column(Enum(ContrastMode), default=ContrastMode.NORMAL, nullable=False)
    
    # Configurações de síntese de voz
    voice_speed = Column(Float, default=1.0, nullable=False)
    voice_pitch = Column(Float, default=1.0, nullable=False)
    voice_name = Column(String(100), nullable=True)
    
    # Nível de complexidade (1: básico, 2: intermediário, 3: avançado)
    complexity_level = Column(Integer, default=1, nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="profiles")
    quick_phrases = relationship("QuickPhrase", back_populates="profile", cascade="all, delete-orphan")
    custom_symbols = relationship("Symbol", back_populates="profile", cascade="all, delete-orphan")
    profile_symbols = relationship("ProfileSymbol", back_populates="profile", cascade="all, delete-orphan")
