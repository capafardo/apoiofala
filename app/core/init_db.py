"""
Inicialização e Seed do Banco de Dados e Assets do CAA-Lab.
"""

from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.profile import Profile, SymbolSize, ContrastMode
from app.models.category import Category
from app.models.symbol import Symbol
from app.models.quick_phrase import QuickPhrase
from scripts.generate_pictograms import ensure_pictograms


def init_db(db: Session = None) -> None:
    """Cria tabelas e insere dados padrão de inicialização se não existirem."""
    # Garantir criação e presença dos arquivos de pictograma offline
    ensure_pictograms()

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

        # 3. Usuário / Perfil Padrão de Criança (ex: João Pedro)
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
            db.refresh(default_profile)

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

        cat_map = {}
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
                db.refresh(cat)
            cat_map[cat.slug] = cat

        # 5. Símbolos Padrão de Demonstração (Modo Criança e Vocabulário)
        symbols_seed = [
            # Início
            {"cat": "inicio", "name": "eu", "label": "eu", "img": "/static/pictograms/eu.svg", "spoken": "eu", "bg": "#dcfce7", "order": 1},
            {"cat": "inicio", "name": "quero", "label": "quero", "img": "/static/pictograms/quero.svg", "spoken": "quero", "bg": "#dcfce7", "order": 2},
            {"cat": "inicio", "name": "beber", "label": "beber", "img": "/static/pictograms/beber.svg", "spoken": "beber", "bg": "#fef9c3", "order": 3},
            {"cat": "inicio", "name": "banheiro", "label": "banheiro", "img": "/static/pictograms/banheiro.svg", "spoken": "banheiro", "bg": "#e0f2fe", "order": 4},
            {"cat": "inicio", "name": "gosto", "label": "gosto", "img": "/static/pictograms/gosto.svg", "spoken": "gosto", "bg": "#fef9c3", "order": 5},
            {"cat": "inicio", "name": "comer", "label": "comer", "img": "/static/pictograms/comer.svg", "spoken": "comer", "bg": "#fef9c3", "order": 6},
            {"cat": "inicio", "name": "ir", "label": "ir", "img": "/static/pictograms/ir.svg", "spoken": "ir", "bg": "#e0f2fe", "order": 7},
            {"cat": "inicio", "name": "não", "label": "não", "img": "/static/pictograms/nao.svg", "spoken": "não", "bg": "#fee2e2", "order": 8},
            {"cat": "inicio", "name": "ajuda", "label": "ajuda", "img": "/static/pictograms/ajuda.svg", "spoken": "ajuda", "bg": "#fef9c3", "order": 9},
            {"cat": "inicio", "name": "mais", "label": "mais", "img": "/static/pictograms/mais.svg", "spoken": "mais", "bg": "#f3e8ff", "order": 10},
            {"cat": "inicio", "name": "mãe", "label": "mãe", "img": "/static/pictograms/mae.svg", "spoken": "mãe", "bg": "#ffedd5", "order": 11},
            {"cat": "inicio", "name": "pai", "label": "pai", "img": "/static/pictograms/pai.svg", "spoken": "pai", "bg": "#e0f2fe", "order": 12},
            {"cat": "inicio", "name": "casa", "label": "casa", "img": "/static/pictograms/casa.svg", "spoken": "casa", "bg": "#fef9c3", "order": 13},
            {"cat": "inicio", "name": "escola", "label": "escola", "img": "/static/pictograms/escola.svg", "spoken": "escola", "bg": "#dcfce7", "order": 14},
            {"cat": "inicio", "name": "brincar", "label": "brincar", "img": "/static/pictograms/brincar.svg", "spoken": "brincar", "bg": "#f3e8ff", "order": 15},

            # Comida e Bebida
            {"cat": "comida-bebida", "name": "água", "label": "água", "img": "/static/pictograms/agua.svg", "spoken": "água", "bg": "#e0f2fe", "order": 1},
            {"cat": "comida-bebida", "name": "suco", "label": "suco", "img": "/static/pictograms/suco.svg", "spoken": "suco", "bg": "#ffedd5", "order": 2},
            {"cat": "comida-bebida", "name": "leite", "label": "leite", "img": "/static/pictograms/leite.svg", "spoken": "leite", "bg": "#f1f5f9", "order": 3},
            {"cat": "comida-bebida", "name": "pão", "label": "pão", "img": "/static/pictograms/pao.svg", "spoken": "pão", "bg": "#fef9c3", "order": 4},
            {"cat": "comida-bebida", "name": "arroz", "label": "arroz", "img": "/static/pictograms/arroz.svg", "spoken": "arroz", "bg": "#f8fafc", "order": 5},
            {"cat": "comida-bebida", "name": "feijão", "label": "feijão", "img": "/static/pictograms/feijao.svg", "spoken": "feijão", "bg": "#ffedd5", "order": 6},
            {"cat": "comida-bebida", "name": "carne", "label": "carne", "img": "/static/pictograms/carne.svg", "spoken": "carne", "bg": "#fee2e2", "order": 7},
            {"cat": "comida-bebida", "name": "fruta", "label": "fruta", "img": "/static/pictograms/fruta.svg", "spoken": "fruta", "bg": "#dcfce7", "order": 8},

            # Sentimentos
            {"cat": "sentimentos", "name": "feliz", "label": "feliz", "img": "/static/pictograms/feliz.svg", "spoken": "feliz", "bg": "#fef9c3", "order": 1},
            {"cat": "sentimentos", "name": "triste", "label": "triste", "img": "/static/pictograms/triste.svg", "spoken": "triste", "bg": "#e0f2fe", "order": 2},
        ]

        for s_data in symbols_seed:
            cat = cat_map.get(s_data["cat"])
            if cat:
                sym = db.query(Symbol).filter(
                    Symbol.category_id == cat.id,
                    Symbol.name == s_data["name"]
                ).first()
                if not sym:
                    sym = Symbol(
                        category_id=cat.id,
                        name=s_data["name"],
                        text_label=s_data["label"],
                        image_path=s_data["img"],
                        spoken_text=s_data["spoken"],
                        bg_color=s_data["bg"],
                        order_index=s_data["order"],
                        is_active=True,
                    )
                    db.add(sym)

        # 6. Frases Rápidas Padrão (conforme inspiracao-design.png)
        quick_phrases_seed = [
            {"text": "Eu quero ir para casa.", "spoken": "Eu quero ir para casa.", "icon": "home", "order": 1},
            {"text": "Estou com fome.", "spoken": "Estou com fome.", "icon": "coffee", "order": 2},
            {"text": "Preciso de ajuda.", "spoken": "Preciso de ajuda.", "icon": "help-circle", "order": 3},
            {"text": "Não entendi.", "spoken": "Não entendi.", "icon": "alert-circle", "order": 4},
        ]

        for qp_data in quick_phrases_seed:
            qp = db.query(QuickPhrase).filter(
                QuickPhrase.profile_id == default_profile.id,
                QuickPhrase.text == qp_data["text"]
            ).first()
            if not qp:
                qp = QuickPhrase(
                    profile_id=default_profile.id,
                    text=qp_data["text"],
                    spoken_text=qp_data["spoken"],
                    icon=qp_data["icon"],
                    order_index=qp_data["order"],
                    is_active=True,
                )
                db.add(qp)

        db.commit()

    finally:
        if close_db:
            db.close()
