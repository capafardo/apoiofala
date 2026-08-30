# Arquitetura do Sistema - CAA-Lab

## 1. Visão Geral

O **CAA-Lab** foi projetado para operar com autonomia máxima em rede local fechada em estações Ubuntu Linux.

```text
               ESTAÇÃO LOCAL / REDE LOCAL
┌────────────────────────────────────────────────────────┐
│                   NAVEGADOR LOCAL                      │
│   HTML5 / CSS3 / JS Modular (Web Speech API TTS)       │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP / JSON (:8000)
┌───────────────────────────▼────────────────────────────┐
│              CONTAINER CAA-LAB (FastAPI)               │
│   - Uvicorn Server                                     │
│   - Application Core / API Routers                     │
│   - Services & Speech Abstraction Layer                │
│   - Repository Data Layer                              │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    STORAGE LOCAL                       │
│   - SQLite DB (data/caa_lab.db)                        │
│   - Assets / Pictogramas (assets/pictograms/)          │
└────────────────────────────────────────────────────────┘
```

## 2. Componentes

- **Backend (Python 3.11+ / FastAPI):**
  - Servidor assíncrono de alto desempenho com tipagem estrita (Pydantic v2).
  - Camada de abstração de dados (Repository Pattern) isolando o SQLAlchemy.
  - Abstração `SpeechService` com provedor local e extensibilidade.
- **Frontend (Web Offline):**
  - Interface baseada em padrões abertos, acessível por touch, mouse e teclado.
  - Variáveis CSS nativas para alternância instantânea entre temas padrão e alto contraste.
- **Armazenamento:**
  - SQLite persistido via volume Docker em `data/`.
  - Migrável futuramente para PostgreSQL sem refatoração de regras de negócio.

## 3. Portas e Rede

- **Porta padrão da aplicação:** `8000` (configurável via `PORT` no `.env`).
- **Comunicação externa:** Zero conexões para internet externa em runtime no perfil criança.
