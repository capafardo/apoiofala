"""
Aplicação Principal - CAA-Lab
Comunicação Aumentativa e Alternativa
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.init_db import init_db

# Importação dos Roteadores da API
from app.api.v1.auth import router as auth_router
from app.api.v1.categories import router as categories_router
from app.api.v1.symbols import router as symbols_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.quick_phrases import router as quick_phrases_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.speech import router as speech_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida da aplicação (startup e shutdown)."""
    # Garantir criação de diretórios essenciais
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.ASSETS_DIR / "pictograms", exist_ok=True)
    os.makedirs(settings.ASSETS_DIR / "audio", exist_ok=True)
    os.makedirs(settings.ASSETS_DIR / "uploads", exist_ok=True)
    os.makedirs(settings.STATIC_DIR / "css", exist_ok=True)
    os.makedirs(settings.STATIC_DIR / "js", exist_ok=True)
    os.makedirs(settings.STATIC_DIR / "pictograms", exist_ok=True)
    os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)

    # Inicializar banco de dados e dados padrão
    init_db()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Aplicação Web de Comunicação Aumentativa e Alternativa (CAA) para Rede Local",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG or settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.DEBUG or settings.APP_ENV != "production" else None,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adiciona headers de segurança às respostas HTTP."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# CORS configurado para ambiente local fechado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos e assets locais
if os.path.exists(settings.STATIC_DIR):
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

if os.path.exists(settings.ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=str(settings.ASSETS_DIR)), name="assets")

# Registro de Roteadores da API v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(symbols_router, prefix="/api/v1")
app.include_router(profiles_router, prefix="/api/v1")
app.include_router(quick_phrases_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(speech_router, prefix="/api/v1")


# Rotas de Interface Web (Frontend)
@app.get("/", response_class=HTMLResponse, tags=["Interface Web"], summary="Modo Criança (Prancha de Comunicação)")
async def index():
    """Página principal com o Modo Criança."""
    template_path = settings.TEMPLATES_DIR / "index.html"
    if os.path.exists(template_path):
        return FileResponse(template_path)
    return HTMLResponse("<h1>CAA-Lab em inicialização...</h1>")


@app.get("/profissional", response_class=HTMLResponse, tags=["Interface Web"], summary="Modo Profissional")
async def professional_dashboard():
    """Painel do profissional e terapeuta."""
    template_path = settings.TEMPLATES_DIR / "profissional.html"
    if os.path.exists(template_path):
        return FileResponse(template_path)
    return HTMLResponse("<h1>Painel Profissional não encontrado</h1>")


# Rotas de Diagnóstico
@app.get("/health", tags=["Diagnóstico"], summary="Healthcheck da aplicação")
async def health_check():
    """Retorna o status de saúde da aplicação."""
    return {"status": "ok"}


@app.get("/ready", tags=["Diagnóstico"], summary="Readiness check da aplicação")
async def readiness_check():
    """Verifica se a aplicação está pronta para receber tráfego."""
    return {
        "status": "ready",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "env": settings.APP_ENV,
    }
