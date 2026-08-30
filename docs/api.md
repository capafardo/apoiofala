# Especificação da API REST - CAA-Lab

## 1. Visão Geral

A API REST do **CAA-Lab** é servida pelo FastAPI e expõe endpoints estruturados para gestão de símbolos, pranchas personalizadas, perfis, frases rápidas, autenticação e métricas não invasivas.

A documentação interativa OpenAPI está disponível em `/docs` e `/redoc` em ambiente local.

---

## 2. Catálogo de Endpoints

### 🔍 Diagnóstico e Sistema

#### `GET /health`
* **Descrição:** Retorna o status de integridade do serviço.
* **Resposta (200 OK):**
```json
{
  "status": "ok"
}
```

#### `GET /ready`
* **Descrição:** Informações sobre o ambiente e prontidão do serviço.
* **Resposta (200 OK):**
```json
{
  "status": "ready",
  "app": "CAA-Lab",
  "version": "0.1.0",
  "env": "development"
}
```

---

### 🔐 Autenticação (`/api/v1/auth`)

#### `POST /api/v1/auth/login`
* **Descrição:** Autentica o usuário (Admin, Profissional ou Criança) e emite token JWT e cookie HttpOnly.
* **Payload:**
```json
{
  "username": "terapeuta",
  "password": "terapeuta123"
}
```
* **Resposta (200 OK):**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "username": "terapeuta",
    "full_name": "Terapeuta / Fonoaudiólogo",
    "role": "professional",
    "is_active": true
  }
}
```

#### `GET /api/v1/auth/me`
* **Descrição:** Retorna os dados do usuário autenticado no momento.
* **Headers:** `Authorization: Bearer <TOKEN>`

---

### 🎨 Símbolos e Pranchas (`/api/v1/symbols`)

#### `GET /api/v1/symbols/library`
* **Descrição:** Retorna todos os pictogramas disponíveis na biblioteca central offline do sistema.
* **Query Params:** `search` (opcional).

#### `GET /api/v1/symbols`
* **Descrição:** Retorna símbolos filtrados. Quando `profile_id` e `category_id` são informados, carrega a prancha personalizada daquela criança; caso não haja customização, retorna os símbolos padrão da categoria.
* **Query Params:**
  * `category_id` (int, opcional)
  * `profile_id` (int, opcional)
  * `search` (string, opcional)

#### `POST /api/v1/symbols/profiles/{profile_id}/categories/{category_id}/assign`
* **Descrição:** Substitui a lista de símbolos de uma categoria para o perfil da criança (usado na reorganização completa da prancha).
* **Payload:**
```json
{
  "symbol_ids": [1, 5, 8, 12]
}
```

#### `POST /api/v1/symbols/profiles/{profile_id}/categories/{category_id}/add`
* **Descrição:** Adiciona um ou mais símbolos (via Drag-and-Drop) à prancha da categoria da criança sem apagar os já existentes.
* **Payload:**
```json
{
  "symbol_ids": [3, 7]
}
```

---

### 🧒 Perfis e Personalização (`/api/v1/profiles`)

#### `GET /api/v1/profiles`
* **Descrição:** Lista todos os perfis de crianças/pacientes cadastrados.

#### `POST /api/v1/profiles`
* **Descrição:** Cadastra um novo perfil de criança com apelidos.
* **Payload:**
```json
{
  "name": "João Pedro da Silva",
  "child_nickname": "Joãozinho",
  "guardian_nickname": "Mãe Ana",
  "symbol_size": "medio",
  "symbols_per_page": 12,
  "theme_color": "blue",
  "contrast_mode": "normal",
  "voice_speed": 1.0
}
```

#### `PUT /api/v1/profiles/{id}`
* **Descrição:** Atualiza dados e preferências visuais ou de voz de um perfil.

---

### 📂 Categorias (`/api/v1/categories`)

#### `GET /api/v1/categories`
* **Descrição:** Retorna a lista ordenada de categorias de símbolos ativas.

---

### ⭐ Frases Rápidas (`/api/v1/quick-phrases`)

#### `GET /api/v1/quick-phrases`
* **Descrição:** Retorna as frases rápidas ativas associadas ao perfil informado.

---

### 📊 Métricas Técnicas (`/api/v1/metrics`)

#### `POST /api/v1/metrics/event`
* **Descrição:** Registra um evento técnico anônimo (toque em pictograma, troca de categoria, reprodução de frase).

#### `GET /api/v1/metrics/summary`
* **Descrição:** Retorna dados agregados e anônimos para o dashboard do Modo Profissional.
