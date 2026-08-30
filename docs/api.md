# API REST - CAA-Lab

## 1. Visão Geral

A API é servida pelo FastAPI e fornece documentação OpenAPI interativa em `/docs` e `/redoc`.

## 2. Endpoints do Sistema

### Diagnóstico & Sistema
- `GET /health`: Healthcheck da aplicação (`{"status": "ok"}`).
- `GET /ready`: Readiness check (banco e serviços disponíveis).

### Autenticação & Usuários
- `POST /api/v1/auth/login`: Autenticação e obtenção de token/sessão.
- `GET /api/v1/auth/me`: Dados do usuário autenticado.
- `GET /api/v1/users`: Listagem de usuários (Admin/Profissional).
- `POST /api/v1/users`: Criação de usuário.

### Perfis & Personalização
- `GET /api/v1/profiles`: Listagem de perfis cadastrados.
- `GET /api/v1/profiles/{id}`: Obter detalhes e configurações do perfil.
- `PUT /api/v1/profiles/{id}`: Atualizar configurações visuais/voz do perfil.

### Categorias & Pictogramas
- `GET /api/v1/categories`: Listagem de categorias ativas.
- `POST /api/v1/categories`: Criar nova categoria.
- `GET /api/v1/symbols`: Listagem de pictogramas (com filtro por categoria/busca).
- `POST /api/v1/symbols`: Cadastrar novo pictograma.
- `PUT /api/v1/symbols/{id}`: Atualizar pictograma.

### Frases Rápidas
- `GET /api/v1/quick-phrases`: Listagem de frases rápidas do perfil.
- `POST /api/v1/quick-phrases`: Cadastrar nova frase rápida.

### Métricas Técnicas
- `GET /api/v1/metrics/summary`: Resumo consolidado não invasivo de métricas de uso.
- `POST /api/v1/metrics/event`: Registrar evento técnico (toque, categoria).
