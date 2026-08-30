"""
Modelo de Categoria de Símbolos do CAA-Lab.
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    icon = Column(String(50), default="folder", nullable=False)
    color = Column(String(30), default="#3b82f6", nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    symbols = relationship("Symbol", back_populates="category", cascade="all, delete-orphan")
    quick_phrases = relationship("QuickPhrase", back_populates="category")
