"""
Schemas Pydantic para Métricas Técnicas de Uso.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict


class MetricEventCreate(BaseModel):
    action_type: str
    reference_id: Optional[str] = None
    profile_id: Optional[int] = None
    category_id: Optional[int] = None


class MetricEventResponse(MetricEventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime


class MetricSummaryResponse(BaseModel):
    total_active_users: int
    total_messages_today: int
    total_touches_today: int
    total_favorite_phrases: int
    usage_by_category: Dict[str, int]
    top_used_messages: List[Dict[str, Any]]
