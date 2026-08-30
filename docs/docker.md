# Docker e Infraestrutura - CAA-Lab

## 1. Containers e Volumes

- **Container Web/App:** Executa a aplicação FastAPI via Uvicorn.
- **Volumes Persistentes:**
  - `./data:/app/data` (banco de dados SQLite e configurações)
  - `./assets:/app/assets` (pictogramas e arquivos de áudio)
- **Rede:** Rede interna Docker bridge isolada sem necessidade de bind externo além da porta configurada.
- **Healthcheck:** Monitora o endpoint `GET /health` a cada 15 segundos.
