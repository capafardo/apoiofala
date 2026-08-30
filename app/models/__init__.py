"""
Exportação centralizada de todos os modelos SQLAlchemy.
"""

from app.models.user import User, UserRole
from app.models.profile import Profile, SymbolSize, ContrastMode
from app.models.category import Category
from app.models.symbol import Symbol
from app.models.quick_phrase import QuickPhrase
from app.models.metric import UsageMetric
from app.models.profile_symbol import ProfileSymbol

__all__ = [
    "User",
    "UserRole",
    "Profile",
    "SymbolSize",
    "ContrastMode",
    "Category",
    "Symbol",
    "QuickPhrase",
    "UsageMetric",
    "ProfileSymbol",
]
