# Plano e Estratégia de Testes - CAA-Lab

## 1. Níveis de Teste

- **Testes Unitários (`tests/unit/`):** Validação isolada de schemas Pydantic, hashing de senhas, lógica de serviços e abstrações.
- **Testes de Integração (`tests/integration/`):** Testes de rotas da API com cliente HTTP assíncrono (`TestClient` / `httpx`) e banco SQLite em memória.
- **Testes E2E / Aceitação (`tests/e2e/`):** Fluxos completos de autenticação, montagem de frases e operação do sistema.

## 2. Execução

```bash
pytest
```
