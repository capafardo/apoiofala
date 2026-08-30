"""Testes de integridade do banco de dados e modelos."""

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.profile import Profile
from app.models.category import Category


def test_database_seed_integrity():
    """Verifica se o seed inicial populou as tabelas com integridade relacional."""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        assert admin is not None
        assert admin.role == UserRole.ADMIN

        joao = db.query(User).filter(User.username == "joaopedro").first()
        assert joao is not None
        assert len(joao.profiles) > 0
        assert joao.profiles[0].name == "João Pedro"

        categories = db.query(Category).all()
        assert len(categories) >= 10
    finally:
        db.close()
