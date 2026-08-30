# Catálogo e Estratégia de Testes - CAA-Lab

## 1. Estrutura da Suite de Testes

A suite de testes utiliza `pytest` e `pytest-asyncio` com cliente assíncrono `httpx.AsyncClient` para simular requisições HTTP reais contra a aplicação FastAPI.

Total de testes automatizados: **28 testes** (100% aprovados).

---

## 2. Detalhamento dos Testes

### 🧪 Testes Unitários (`tests/unit/`)
* `test_sanity.py`:
  * `test_package_version`: Valida integridade do pacote e versão exposta.
* `test_config.py`:
  * `test_settings_defaults`: Valida valores padrão de porta, banco SQLite, idioma e caminhos.
* `test_security.py`:
  * `test_password_hashing`: Valida segurança do hash `bcrypt` e proteção contra texto puro.
  * `test_jwt_token_cycle`: Valida ciclo de codificação, expiração e decodificação do JWT.
* `test_speech.py`:
  * `test_speech_service_synthesis`: Valida contrato de resposta do `SpeechService`.
  * `test_speech_empty_text`: Valida tratamento de mensagens vazias.

---

### 🌐 Testes de Integração (`tests/integration/`)
* `test_health.py`:
  * `test_health_check_endpoint`: Testa `GET /health` (`{"status": "ok"}`).
  * `test_ready_check_endpoint`: Testa `GET /ready`.
* `test_auth.py`:
  * `test_login_success_admin`: Login bem-sucedido com emissão de token JWT.
  * `test_login_invalid_password`: Rejeição de senha inválida com 401 Unauthorized.
  * `test_get_me_authenticated`: Obtenção dos dados do usuário logado via `/api/v1/auth/me`.
  * `test_admin_register_new_user`: Cadastro de novos usuários por administradores.
  * `test_user_cannot_register_others`: Bloqueio (403 Forbidden) para criação de usuários por perfis comuns.
* `test_database.py`:
  * `test_database_seed_integrity`: Valida criação das tabelas e seed de dados iniciais.
* `test_categories.py`:
  * `test_list_categories`: Valida listagem das 10 categorias essenciais.
* `test_symbols.py`:
  * `test_list_symbols`: Valida listagem geral de símbolos.
  * `test_filter_symbols_by_category`: Valida filtro por categoria específica.
  * `test_search_symbols`: Valida busca textual por termos (ex: *"casa"*).
* `test_profiles.py`:
  * `test_list_and_update_profile`: Valida consulta e atualização de configurações visuais e de voz.
* `test_profile_customization.py`:
  * `test_all_categories_have_symbols`: Garante que nenhuma das 10 categorias esteja vazia.
  * `test_get_library_symbols`: Valida acesso à biblioteca geral de pictogramas (+50 itens).
  * `test_create_profile_with_nicknames`: Valida criação de perfil com apelido da criança e da mãe/acompanhante.
  * `test_drag_and_drop_assign_symbols_to_profile_category`: Valida fluxo de personalização de pranchas por drag-and-drop.
* `test_quick_phrases.py`:
  * `test_list_quick_phrases`: Valida listagem de frases frequentes pré-configuradas.
* `test_metrics.py`:
  * `test_record_and_summary_metrics`: Valida registro de eventos e resumo consolidado não invasivo.
* `test_web_routes.py`:
  * `test_index_page_returns_html`: Valida carregamento da interface do Modo Criança (`GET /`).
  * `test_professional_page_returns_html`: Valida carregamento do painel profissional (`GET /profissional`).
  * `test_static_assets_available`: Valida disponibilidade estática de CSS e SVGs locais.

---

## 3. Como Executar os Testes

```bash
# Executar todos os testes
.venv/bin/pytest

# Executar com saída detalhada
.venv/bin/pytest -v
```
