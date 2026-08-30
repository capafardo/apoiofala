"""
Modelo de Associação de Símbolos por Perfil e Categoria (Prancha Personalizada).
"""

from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProfileSymbol(Base):
    __tablename__ = "profile_symbols"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    profile = relationship("Profile", back_populates="profile_symbols")
    symbol = relationship("Symbol")
    category = relationship("Category")
