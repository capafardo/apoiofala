"""
Modelo de Frase Rápida do CAA-Lab.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class QuickPhrase(Base):
    __tablename__ = "quick_phrases"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    text = Column(String(255), nullable=False)
    spoken_text = Column(String(255), nullable=True)
    icon = Column(String(50), default="message-circle", nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    profile = relationship("Profile", back_populates="quick_phrases")
    category = relationship("Category", back_populates="quick_phrases")
