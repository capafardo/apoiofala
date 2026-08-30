"""
Modelo de Métrica de Uso Técnico Anônima do CAA-Lab.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base


class UsageMetric(Base):
    __tablename__ = "usage_metrics"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    action_type = Column(String(50), nullable=False)  # touch_symbol, speak_message, quick_phrase, change_category
    reference_id = Column(String(100), nullable=True)  # ex: symbol_id ou category_id
    
    timestamp = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
