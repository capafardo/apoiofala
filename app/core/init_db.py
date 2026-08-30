"""
Inicialização, Migrações Automáticas e Seed do Banco de Dados do CAA-Lab.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.profile import Profile, SymbolSize, ContrastMode
from app.models.category import Category
from app.models.symbol import Symbol
from app.models.quick_phrase import QuickPhrase
from app.models.profile_symbol import ProfileSymbol
from scripts.generate_pictograms import ensure_pictograms


def migrate_schema(db: Session):
    """Executa migrações automáticas de colunas para garantir compatibilidade."""
    try:
        # Verificar se colunas de apelido existem na tabela profiles
        result = db.execute(text("PRAGMA table_info(profiles);")).fetchall()
        columns = [row[1] for row in result]

        if "child_nickname" not in columns:
            db.execute(text("ALTER TABLE profiles ADD COLUMN child_nickname VARCHAR(100);"))
        if "guardian_nickname" not in columns:
            db.execute(text("ALTER TABLE profiles ADD COLUMN guardian_nickname VARCHAR(100);"))
        db.commit()
    except Exception as e:
        db.rollback()


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
        # Executar migrações se necessário
        migrate_schema(db)

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

        # 3. Perfis Padrão de Demonstração (com nicknames de criança e responsável)
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

        # Perfil 1: João Pedro (Mãe: Ana)
        default_profile = db.query(Profile).filter(Profile.name == "João Pedro").first()
        if not default_profile:
            default_profile = Profile(
                user_id=child_user.id,
                name="João Pedro",
                child_nickname="Joãozinho",
                guardian_nickname="Mãe Ana",
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

        # Perfil 2: Maria Clara (Acompanhante: Carla)
        maria_profile = db.query(Profile).filter(Profile.name == "Maria Clara").first()
        if not maria_profile:
            maria_profile = Profile(
                user_id=child_user.id,
                name="Maria Clara",
                child_nickname="Clarinha",
                guardian_nickname="Tia Carla (Acompanhante)",
                symbol_size=SymbolSize.LARGE,
                symbols_per_page=6,
                theme_color="pink",
                contrast_mode=ContrastMode.NORMAL,
                voice_speed=0.9,
                voice_pitch=1.1,
                complexity_level=1,
            )
            db.add(maria_profile)
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

        # 5. Símbolos Padrão Ricos para TODAS as categorias
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

            # Frases Rápidas (Símbolos representando atalhos)
            {"cat": "frases-rapidas", "name": "quero ir para casa", "label": "ir p/ casa", "img": "/static/pictograms/casa.svg", "spoken": "Eu quero ir para casa.", "bg": "#fef9c3", "order": 1},
            {"cat": "frases-rapidas", "name": "estou com fome", "label": "com fome", "img": "/static/pictograms/comer.svg", "spoken": "Estou com fome.", "bg": "#ffedd5", "order": 2},
            {"cat": "frases-rapidas", "name": "preciso de ajuda", "label": "preciso ajuda", "img": "/static/pictograms/ajuda.svg", "spoken": "Preciso de ajuda.", "bg": "#fee2e2", "order": 3},
            {"cat": "frases-rapidas", "name": "não entendi", "label": "não entendi", "img": "/static/pictograms/nao.svg", "spoken": "Não entendi.", "bg": "#e0f2fe", "order": 4},
            {"cat": "frases-rapidas", "name": "quero ir ao banheiro", "label": "ir ao banheiro", "img": "/static/pictograms/banheiro.svg", "spoken": "Quero ir ao banheiro.", "bg": "#e0f2fe", "order": 5},
            {"cat": "frases-rapidas", "name": "estou com sede", "label": "com sede", "img": "/static/pictograms/agua.svg", "spoken": "Estou com sede.", "bg": "#dcfce7", "order": 6},

            # Comunicar
            {"cat": "comunicar", "name": "sim", "label": "sim", "img": "/static/pictograms/sim.svg", "spoken": "sim", "bg": "#dcfce7", "order": 1},
            {"cat": "comunicar", "name": "não", "label": "não", "img": "/static/pictograms/nao.svg", "spoken": "não", "bg": "#fee2e2", "order": 2},
            {"cat": "comunicar", "name": "olá", "label": "olá", "img": "/static/pictograms/ola.svg", "spoken": "olá", "bg": "#fef9c3", "order": 3},
            {"cat": "comunicar", "name": "tchau", "label": "tchau", "img": "/static/pictograms/tchau.svg", "spoken": "tchau", "bg": "#ffedd5", "order": 4},
            {"cat": "comunicar", "name": "por favor", "label": "por favor", "img": "/static/pictograms/por-favor.svg", "spoken": "por favor", "bg": "#e0f2fe", "order": 5},
            {"cat": "comunicar", "name": "obrigado", "label": "obrigado", "img": "/static/pictograms/obrigado.svg", "spoken": "obrigado", "bg": "#dcfce7", "order": 6},
            {"cat": "comunicar", "name": "desculpa", "label": "desculpa", "img": "/static/pictograms/desculpa.svg", "spoken": "desculpa", "bg": "#fef9c3", "order": 7},
            {"cat": "comunicar", "name": "conversar", "label": "conversar", "img": "/static/pictograms/conversar.svg", "spoken": "conversar", "bg": "#e0f2fe", "order": 8},
            {"cat": "comunicar", "name": "repetir", "label": "repetir", "img": "/static/pictograms/repetir.svg", "spoken": "repetir", "bg": "#f3e8ff", "order": 9},
            {"cat": "comunicar", "name": "esperar", "label": "esperar", "img": "/static/pictograms/esperar.svg", "spoken": "esperar", "bg": "#fef9c3", "order": 10},
            {"cat": "comunicar", "name": "parar", "label": "parar", "img": "/static/pictograms/parar.svg", "spoken": "parar", "bg": "#fee2e2", "order": 11},
            {"cat": "comunicar", "name": "ajuda", "label": "ajuda", "img": "/static/pictograms/ajuda.svg", "spoken": "ajuda", "bg": "#ffedd5", "order": 12},

            # Necessidades
            {"cat": "necessidades", "name": "banheiro", "label": "banheiro", "img": "/static/pictograms/banheiro.svg", "spoken": "banheiro", "bg": "#e0f2fe", "order": 1},
            {"cat": "necessidades", "name": "xixi", "label": "xixi", "img": "/static/pictograms/xixi.svg", "spoken": "xixi", "bg": "#fef9c3", "order": 2},
            {"cat": "necessidades", "name": "cocô", "label": "cocô", "img": "/static/pictograms/coco.svg", "spoken": "cocô", "bg": "#ffedd5", "order": 3},
            {"cat": "necessidades", "name": "água", "label": "água", "img": "/static/pictograms/agua.svg", "spoken": "água", "bg": "#e0f2fe", "order": 4},
            {"cat": "necessidades", "name": "comer", "label": "comer", "img": "/static/pictograms/comer.svg", "spoken": "comer", "bg": "#fef9c3", "order": 5},
            {"cat": "necessidades", "name": "dormir", "label": "dormir", "img": "/static/pictograms/dormir.svg", "spoken": "dormir", "bg": "#e0f2fe", "order": 6},
            {"cat": "necessidades", "name": "dor", "label": "dor", "img": "/static/pictograms/dor.svg", "spoken": "dor", "bg": "#fee2e2", "order": 7},
            {"cat": "necessidades", "name": "remédio", "label": "remédio", "img": "/static/pictograms/remedio.svg", "spoken": "remédio", "bg": "#ffedd5", "order": 8},
            {"cat": "necessidades", "name": "frio", "label": "frio", "img": "/static/pictograms/frio.svg", "spoken": "frio", "bg": "#e0f2fe", "order": 9},
            {"cat": "necessidades", "name": "calor", "label": "calor", "img": "/static/pictograms/calor.svg", "spoken": "calor", "bg": "#ffedd5", "order": 10},
            {"cat": "necessidades", "name": "banho", "label": "banho", "img": "/static/pictograms/banho.svg", "spoken": "banho", "bg": "#e0f2fe", "order": 11},
            {"cat": "necessidades", "name": "escovar dentes", "label": "escovar dentes", "img": "/static/pictograms/escovar-dentes.svg", "spoken": "escovar os dentes", "bg": "#dcfce7", "order": 12},
            {"cat": "necessidades", "name": "trocar roupa", "label": "trocar roupa", "img": "/static/pictograms/trocar-roupa.svg", "spoken": "trocar de roupa", "bg": "#dcfce7", "order": 13},
            {"cat": "necessidades", "name": "cansado", "label": "cansado", "img": "/static/pictograms/cansado.svg", "spoken": "estou cansado", "bg": "#fef9c3", "order": 14},

            # Pessoas
            {"cat": "pessoas", "name": "eu", "label": "eu", "img": "/static/pictograms/eu.svg", "spoken": "eu", "bg": "#dcfce7", "order": 1},
            {"cat": "pessoas", "name": "mãe", "label": "mãe", "img": "/static/pictograms/mae.svg", "spoken": "mãe", "bg": "#ffedd5", "order": 2},
            {"cat": "pessoas", "name": "pai", "label": "pai", "img": "/static/pictograms/pai.svg", "spoken": "pai", "bg": "#e0f2fe", "order": 3},
            {"cat": "pessoas", "name": "irmão", "label": "irmão", "img": "/static/pictograms/irmao.svg", "spoken": "irmão", "bg": "#dcfce7", "order": 4},
            {"cat": "pessoas", "name": "irmã", "label": "irmã", "img": "/static/pictograms/irma.svg", "spoken": "irmã", "bg": "#fee2e2", "order": 5},
            {"cat": "pessoas", "name": "vovô", "label": "vovô", "img": "/static/pictograms/avo-m.svg", "spoken": "vovô", "bg": "#f1f5f9", "order": 6},
            {"cat": "pessoas", "name": "vovó", "label": "vovó", "img": "/static/pictograms/avo-f.svg", "spoken": "vovó", "bg": "#f3e8ff", "order": 7},
            {"cat": "pessoas", "name": "amigo", "label": "amigo", "img": "/static/pictograms/amigo.svg", "spoken": "amigo", "bg": "#fef9c3", "order": 8},
            {"cat": "pessoas", "name": "professor", "label": "professor", "img": "/static/pictograms/professor.svg", "spoken": "professor", "bg": "#ffedd5", "order": 9},
            {"cat": "pessoas", "name": "terapeuta", "label": "terapeuta", "img": "/static/pictograms/terapeuta.svg", "spoken": "terapeuta", "bg": "#e0f2fe", "order": 10},
            {"cat": "pessoas", "name": "família", "label": "família", "img": "/static/pictograms/familia.svg", "spoken": "família", "bg": "#fef9c3", "order": 11},

            # Lugares
            {"cat": "lugares", "name": "casa", "label": "casa", "img": "/static/pictograms/casa.svg", "spoken": "casa", "bg": "#fef9c3", "order": 1},
            {"cat": "lugares", "name": "escola", "label": "escola", "img": "/static/pictograms/escola.svg", "spoken": "escola", "bg": "#dcfce7", "order": 2},
            {"cat": "lugares", "name": "parque", "label": "parque", "img": "/static/pictograms/parque.svg", "spoken": "parque", "bg": "#dcfce7", "order": 3},
            {"cat": "lugares", "name": "hospital", "label": "hospital", "img": "/static/pictograms/hospital.svg", "spoken": "hospital", "bg": "#fee2e2", "order": 4},
            {"cat": "lugares", "name": "quarto", "label": "quarto", "img": "/static/pictograms/quarto.svg", "spoken": "quarto", "bg": "#e0f2fe", "order": 5},
            {"cat": "lugares", "name": "cozinha", "label": "cozinha", "img": "/static/pictograms/cozinha.svg", "spoken": "cozinha", "bg": "#f1f5f9", "order": 6},
            {"cat": "lugares", "name": "sala", "label": "sala", "img": "/static/pictograms/sala.svg", "spoken": "sala", "bg": "#f3e8ff", "order": 7},
            {"cat": "lugares", "name": "rua", "label": "rua", "img": "/static/pictograms/rua.svg", "spoken": "rua", "bg": "#f1f5f9", "order": 8},
            {"cat": "lugares", "name": "mercado", "label": "mercado", "img": "/static/pictograms/mercado.svg", "spoken": "mercado", "bg": "#e0f2fe", "order": 9},
            {"cat": "lugares", "name": "praia", "label": "praia", "img": "/static/pictograms/praia.svg", "spoken": "praia", "bg": "#fef9c3", "order": 10},

            # Brincar
            {"cat": "brincar", "name": "bola", "label": "bola", "img": "/static/pictograms/bola.svg", "spoken": "bola", "bg": "#f1f5f9", "order": 1},
            {"cat": "brincar", "name": "boneca", "label": "boneca", "img": "/static/pictograms/boneca.svg", "spoken": "boneca", "bg": "#ffedd5", "order": 2},
            {"cat": "brincar", "name": "carrinho", "label": "carrinho", "img": "/static/pictograms/carrinho.svg", "spoken": "carrinho", "bg": "#fee2e2", "order": 3},
            {"cat": "brincar", "name": "blocos", "label": "blocos", "img": "/static/pictograms/blocos.svg", "spoken": "blocos de montar", "bg": "#fef9c3", "order": 4},
            {"cat": "brincar", "name": "desenhar", "label": "desenhar", "img": "/static/pictograms/desenhar.svg", "spoken": "desenhar", "bg": "#dcfce7", "order": 5},
            {"cat": "brincar", "name": "quebra-cabeça", "label": "quebra-cabeça", "img": "/static/pictograms/quebra-cabeca.svg", "spoken": "quebra-cabeça", "bg": "#e0f2fe", "order": 6},
            {"cat": "brincar", "name": "tablet", "label": "tablet", "img": "/static/pictograms/tablet.svg", "spoken": "tablet", "bg": "#f1f5f9", "order": 7},
            {"cat": "brincar", "name": "música", "label": "música", "img": "/static/pictograms/musica.svg", "spoken": "música", "bg": "#f3e8ff", "order": 8},
            {"cat": "brincar", "name": "correr", "label": "correr", "img": "/static/pictograms/correr.svg", "spoken": "correr", "bg": "#e0f2fe", "order": 9},
            {"cat": "brincar", "name": "brincar", "label": "brincar", "img": "/static/pictograms/brincar.svg", "spoken": "brincar", "bg": "#fef9c3", "order": 10},

            # Mais
            {"cat": "mais", "name": "mais", "label": "mais", "img": "/static/pictograms/mais.svg", "spoken": "mais", "bg": "#f3e8ff", "order": 1},
            {"cat": "mais", "name": "menos", "label": "menos", "img": "/static/pictograms/menos.svg", "spoken": "menos", "bg": "#f3e8ff", "order": 2},
            {"cat": "mais", "name": "rápido", "label": "rápido", "img": "/static/pictograms/rapido.svg", "spoken": "rápido", "bg": "#fef9c3", "order": 3},
            {"cat": "mais", "name": "devagar", "label": "devagar", "img": "/static/pictograms/devagar.svg", "spoken": "devagar", "bg": "#dcfce7", "order": 4},
            {"cat": "mais", "name": "agora", "label": "agora", "img": "/static/pictograms/agora.svg", "spoken": "agora", "bg": "#e0f2fe", "order": 5},
            {"cat": "mais", "name": "depois", "label": "depois", "img": "/static/pictograms/depois.svg", "spoken": "depois", "bg": "#dcfce7", "order": 6},
            {"cat": "mais", "name": "grande", "label": "grande", "img": "/static/pictograms/grande.svg", "spoken": "grande", "bg": "#e0f2fe", "order": 7},
            {"cat": "mais", "name": "pequeno", "label": "pequeno", "img": "/static/pictograms/pequeno.svg", "spoken": "pequeno", "bg": "#fee2e2", "order": 8},
            {"cat": "mais", "name": "bonito", "label": "bonito", "img": "/static/pictograms/bonito.svg", "spoken": "bonito", "bg": "#fef9c3", "order": 9},
            {"cat": "mais", "name": "abrir", "label": "abrir", "img": "/static/pictograms/abrir.svg", "spoken": "abrir", "bg": "#ffedd5", "order": 10},
            {"cat": "mais", "name": "fechar", "label": "fechar", "img": "/static/pictograms/fechar.svg", "spoken": "fechar", "bg": "#ffedd5", "order": 11},

            # Comida e Bebida
            {"cat": "comida-bebida", "name": "água", "label": "água", "img": "/static/pictograms/agua.svg", "spoken": "água", "bg": "#e0f2fe", "order": 1},
            {"cat": "comida-bebida", "name": "suco", "label": "suco", "img": "/static/pictograms/suco.svg", "spoken": "suco", "bg": "#ffedd5", "order": 2},
            {"cat": "comida-bebida", "name": "leite", "label": "leite", "img": "/static/pictograms/leite.svg", "spoken": "leite", "bg": "#f1f5f9", "order": 3},
            {"cat": "comida-bebida", "name": "pão", "label": "pão", "img": "/static/pictograms/pao.svg", "spoken": "pão", "bg": "#fef9c3", "order": 4},
            {"cat": "comida-bebida", "name": "arroz", "label": "arroz", "img": "/static/pictograms/arroz.svg", "spoken": "arroz", "bg": "#f8fafc", "order": 5},
            {"cat": "comida-bebida", "name": "feijão", "label": "feijão", "img": "/static/pictograms/feijao.svg", "spoken": "feijão", "bg": "#ffedd5", "order": 6},
            {"cat": "comida-bebida", "name": "carne", "label": "carne", "img": "/static/pictograms/carne.svg", "spoken": "carne", "bg": "#fee2e2", "order": 7},
            {"cat": "comida-bebida", "name": "fruta", "label": "fruta", "img": "/static/pictograms/fruta.svg", "spoken": "fruta", "bg": "#dcfce7", "order": 8},
            {"cat": "comida-bebida", "name": "beber", "label": "beber", "img": "/static/pictograms/beber.svg", "spoken": "beber", "bg": "#e0f2fe", "order": 9},
            {"cat": "comida-bebida", "name": "comer", "label": "comer", "img": "/static/pictograms/comer.svg", "spoken": "comer", "bg": "#fef9c3", "order": 10},

            # Sentimentos
            {"cat": "sentimentos", "name": "feliz", "label": "feliz", "img": "/static/pictograms/feliz.svg", "spoken": "estou feliz", "bg": "#fef9c3", "order": 1},
            {"cat": "sentimentos", "name": "triste", "label": "triste", "img": "/static/pictograms/triste.svg", "spoken": "estou triste", "bg": "#e0f2fe", "order": 2},
            {"cat": "sentimentos", "name": "dor", "label": "dor", "img": "/static/pictograms/dor.svg", "spoken": "estou com dor", "bg": "#fee2e2", "order": 3},
            {"cat": "sentimentos", "name": "cansado", "label": "cansado", "img": "/static/pictograms/cansado.svg", "spoken": "estou cansado", "bg": "#fef9c3", "order": 4},
            {"cat": "sentimentos", "name": "gosto", "label": "gosto", "img": "/static/pictograms/gosto.svg", "spoken": "eu gosto", "bg": "#dcfce7", "order": 5},
            {"cat": "sentimentos", "name": "não gosto", "label": "não gosto", "img": "/static/pictograms/nao-gosto.svg", "spoken": "não gosto", "bg": "#fee2e2", "order": 6},
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

        # 6. Frases Rápidas Padrão
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
