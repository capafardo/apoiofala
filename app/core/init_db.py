"""
Inicialização e Seed do Banco de Dados.
"""

from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.profile import Profile, SymbolSize, ContrastMode
from app.models.category import Category


def init_db(db: Session = None) -> None:
    """Cria tabelas e insere dados padrão de inicialização se não existirem."""
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)

    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        # 1. Usuário Administrador Padrão
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                full_name="Administrador do Sistema",
                password_hash=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

        # 2. Usuário Profissional Padrão
        prof_user = db.query(User).filter(User.username == "terapeuta").first()
        if not prof_user:
            prof_user = User(
                username="terapeuta",
                full_name="Terapeuta / Fonoaudiólogo",
                password_hash=get_password_hash("terapeuta123"),
                role=UserRole.PROFESSIONAL,
                is_active=True,
            )
            db.add(prof_user)
            db.commit()
            db.refresh(prof_user)

        # 3. Usuário / Perfil Padrão de Criança (ex: João Pedro, conforme imagem de referência)
        child_user = db.query(User).filter(User.username == "joaopedro").first()
        if not child_user:
            child_user = User(
                username="joaopedro",
                full_name="João Pedro",
                password_hash=get_password_hash("joao123"),
                role=UserRole.USER,
                is_active=True,
            )
            db.add(child_user)
            db.commit()
            db.refresh(child_user)

        # Perfil associado a João Pedro
        default_profile = db.query(Profile).filter(Profile.name == "João Pedro").first()
        if not default_profile:
            default_profile = Profile(
                user_id=child_user.id,
                name="João Pedro",
                symbol_size=SymbolSize.MEDIUM,
                symbols_per_page=12,
                theme_color="blue",
                contrast_mode=ContrastMode.NORMAL,
                voice_speed=1.0,
                voice_pitch=1.0,
                complexity_level=1,
            )
            db.add(default_profile)
            db.commit()

        # 4. Categorias Padrão
        default_categories = [
            {"name": "Início", "slug": "inicio", "icon": "home", "color": "#3b82f6", "order_index": 1},
            {"name": "Comunicar", "slug": "comunicar", "icon": "message-circle", "color": "#10b981", "order_index": 2},
            {"name": "Frases rápidas", "slug": "frases-rapidas", "icon": "star", "color": "#f59e0b", "order_index": 3},
            {"name": "Sentimentos", "slug": "sentimentos", "icon": "heart", "color": "#ef4444", "order_index": 4},
            {"name": "Necessidades", "slug": "necessidades", "icon": "help-circle", "color": "#8b5cf6", "order_index": 5},
            {"name": "Comida e bebida", "slug": "comida-bebida", "icon": "coffee", "color": "#ec4899", "order_index": 6},
            {"name": "Pessoas", "slug": "pessoas", "icon": "users", "color": "#06b6d4", "order_index": 7},
            {"name": "Lugares", "slug": "lugares", "icon": "map-pin", "color": "#14b8a6", "order_index": 8},
            {"name": "Brincar", "slug": "brincar", "icon": "smile", "color": "#f97316", "order_index": 9},
            {"name": "Mais", "slug": "mais", "icon": "more-horizontal", "color": "#6b7280", "order_index": 10},
        ]

        for cat_data in default_categories:
            cat = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not cat:
                cat = Category(
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    icon=cat_data["icon"],
                    color=cat_data["color"],
                    order_index=cat_data["order_index"],
                    is_active=True,
                )
                db.add(cat)

        db.commit()

    finally:
        if close_db:
            db.close()
