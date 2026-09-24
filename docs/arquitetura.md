# Arquitetura do Sistema - CAA-Lab

## 1. Visão Geral

O **CAA-Lab** foi projetado para operar com autonomia máxima em rede local fechada em estações Ubuntu Linux (estando preparado tanto para ambiente de desenvolvimento quanto para implantação em laboratório).

```text
               ESTAÇÃO LOCAL / REDE LOCAL (Ubuntu)
┌────────────────────────────────────────────────────────────────────────┐
│                        NAVEGADOR LOCAL                                 │
│  - Modo Criança: Prancha tátil, Construtor de frases, Frases rápidas   │
│  - Modo Profissional: Drag-and-Drop, Gestão de Perfis, Dashboard       │
│  - Web Speech API: Síntese de voz em português local e offline         │
│  - Acessibilidade: Alto Contraste, Font Scaling (A-/A+), Teclado       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (:8000)
┌───────────────────────────────────▼────────────────────────────────────┐
│                    CONTAINER CAA-LAB (FastAPI)                         │
│  - Servidor Uvicorn Assíncrono                                         │
│  - Core / Security (Bcrypt, JWT, Security Headers)                     │
│  - API Routers: /auth, /symbols, /profiles, /categories, /metrics, etc.│
│  - Camada de Serviços e Abstração SpeechService                        │
│  - Camada Repository / SQLAlchemy 2.0                                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                         STORAGE LOCAL                                  │
│  - SQLite 3 DB (WAL mode, Foreign Keys) em data/caa_lab.db             │
│  - Biblioteca Vetorial de Pictogramas (80+ SVGs) em assets/ e static/  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes Principais

### A. Frontend (Offline-First Vanilla Modular)
- **Zero CDNs ou Fontes Externas:** Todas as fontes e símbolos são embutidos e servidos localmente.
- **Camada de Áudio (`speech.js`):** Utiliza a Web Speech API nativa do sistema operacional/navegador para síntese imediata de voz em português.
- **Módulo Drag & Drop (`admin.js`):** Suporta multisseleção e movimentação de símbolos em lote da biblioteca para categorias do perfil da criança.
- **Seletor de Perfil Ativo:** Alterna instantaneamente as pranchas e configurações no Modo Criança.

### B. Backend (FastAPI / Python 3.11+)
- **Estrutura Assíncrona:** Alta performance e baixo consumo de memória.
- **Tipagem Estrita com Pydantic v2:** Validação robusta de todos os payloads de entrada e saída.
- **Abstração de TTS (`SpeechService`):** Desacopla o mecanismo de síntese. No backend, a rota `/speech/tts` usa voz neural da Microsoft (edge-tts, gratuita) com cache em disco e fallback espeak-ng 100% offline.

### C. Persistência de Dados
- **SQLite 3 Local com WAL:** Garante alta concorrência de leitura e escrita sem corrupção.
- **Isolamento por Perfil (`ProfileSymbol`):** Permite que cada criança tenha sua própria organização de vocabulário.

---

## 3. Segurança e Rede
- **Porta Padrão:** `8000` (configurável via variável de ambiente `PORT`).
- **Comunicação Segura:** Headers HTTP `nosniff`, `SAMEORIGIN`, `XSS-Protection`.
- **Minimização de Dados:** Dados conversacionais privados da criança não são salvos em logs.
