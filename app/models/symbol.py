"""
Modelo de Símbolo / Pictograma do CAA-Lab.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=True)
    
    name = Column(String(100), index=True, nullable=False)
    text_label = Column(String(100), nullable=False)
    image_path = Column(String(255), nullable=False)
    spoken_text = Column(String(255), nullable=True)
    
    bg_color = Column(String(30), nullable=True)
    border_color = Column(String(30), nullable=True)
    
    order_index = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    category = relationship("Category", back_populates="symbols")
    profile = relationship("Profile", back_populates="custom_symbols")
