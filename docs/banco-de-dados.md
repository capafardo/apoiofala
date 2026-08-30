# Modelagem e Banco de Dados - CAA-Lab

## 1. Visão Geral da Persistência

- **Engine:** SQLite 3 com suporte a modo WAL (*Write-Ahead Logging*) e integridade referencial ativa (`PRAGMA foreign_keys=ON;`).
- **Abstração:** SQLAlchemy 2.0 ORM com padrão Repository, permitindo migração futura simplificada para PostgreSQL.
- **Localização:** `./data/caa_lab.db` (armazenado em volume Docker persistente).

---

## 2. Diagrama Entidade-Relacionamento (Conceitual)

```text
┌──────────────┐          ┌────────────────┐          ┌─────────────────┐
│     User     │ 1      N │    Profile     │ 1      N │  ProfileSymbol  │
│--------------│──────────│----------------│──────────│-----------------│
│ id (PK)      │          │ id (PK)        │          │ id (PK)         │
│ username     │          │ user_id (FK)   │          │ profile_id (FK) │
│ password_hash│          │ name           │          │ symbol_id (FK)  │
│ role         │          │ child_nickname │          │ category_id (FK)│
│ is_active    │          │ guardian_nick..│          │ order_index     │
└──────────────┘          │ symbol_size    │          └────────┬────────┘
                          │ symbols_per_pg │                   │
                          │ voice_speed    │                   │ N
                          └───────┬────────┘                   │
                                  │ 1                          │
                                  │ N                          │ 1
┌──────────────┐          ┌───────▼────────┐          ┌────────▼────────┐
│   Category   │ 1      N │  QuickPhrase   │          │     Symbol      │
│--------------│──────────│----------------│          │-----------------│
│ id (PK)      │          │ id (PK)        │          │ id (PK)         │
│ name         │          │ profile_id (FK)│          │ category_id (FK)│
│ slug         │          │ category_id(FK)│          │ name            │
│ icon         │          │ text           │          │ text_label      │
│ color        │          │ spoken_text    │          │ image_path      │
│ order_index  │          │ order_index    │          │ spoken_text     │
└──────────────┘          └────────────────┘          │ bg_color        │
                                                      │ order_index     │
                                                      └─────────────────┘
```

---

## 3. Descrição Detalhada das Tabelas

### `users`
* `id` (INTEGER, PK): Identificador único do usuário.
* `username` (VARCHAR(64), UNIQUE, INDEX): Login de acesso.
* `full_name` (VARCHAR(128)): Nome completo.
* `password_hash` (VARCHAR(255)): Hash bcrypt da senha.
* `role` (ENUM: 'admin', 'professional', 'user'): Papel de permissão.
* `is_active` (BOOLEAN): Status da conta.
* `created_at` / `updated_at` (DATETIME): Registro temporal.

### `profiles`
* `id` (INTEGER, PK): Identificador do perfil.
* `user_id` (INTEGER, FK -> users.id, CASCADE, Nullable): Conta de usuário associada.
* `name` (VARCHAR(100)): Nome completo da criança.
* `child_nickname` (VARCHAR(100)): Apelido carinhoso/abreviado da criança (ex: *Joãozinho*).
* `guardian_nickname` (VARCHAR(100)): Apelido da mãe ou acompanhante (ex: *Mãe Ana*).
* `symbol_size` (ENUM: 'pequeno', 'medio', 'grande'): Tamanho visual dos cartões.
* `symbols_per_page` (INTEGER): Limite de itens por página (ex: 6, 12, 20).
* `contrast_mode` (ENUM: 'normal', 'alto_contraste'): Modo de contraste.
* `theme_color` (VARCHAR(30)): Cor tema da interface.
* `voice_speed` (FLOAT): Multiplicador de velocidade da síntese de voz (0.5 a 2.0).

### `categories`
* `id` (INTEGER, PK): Identificador da categoria.
* `name` (VARCHAR(100)): Nome legível (ex: *Comunicar, Necessidades, Brincar*).
* `slug` (VARCHAR(100), UNIQUE, INDEX): Identificador URL-safe.
* `icon` (VARCHAR(50)): Ícone representativo.
* `color` (VARCHAR(30)): Cor temática em hexadecimal.
* `order_index` (INTEGER): Ordem de exibição na barra lateral.
* `is_active` (BOOLEAN): Status de ativação.

### `symbols`
* `id` (INTEGER, PK): Identificador do pictograma.
* `category_id` (INTEGER, FK -> categories.id): Categoria padrão do símbolo.
* `profile_id` (INTEGER, FK -> profiles.id, Nullable): Perfil customizado (se exclusivo).
* `name` (VARCHAR(100), INDEX): Nome técnico do símbolo.
* `text_label` (VARCHAR(100)): Rótulo textual exibido abaixo da imagem.
* `image_path` (VARCHAR(255)): Caminho para o arquivo vetorial SVG offline.
* `spoken_text` (VARCHAR(255), Nullable): Frase ou palavra falada pelo sintetizador.
* `bg_color` (VARCHAR(30), Nullable): Cor de fundo suave do cartão.
* `order_index` (INTEGER): Ordem na grade.
* `is_active` (BOOLEAN): Status do símbolo.

### `profile_symbols`
* `id` (INTEGER, PK): Identificador do vínculo.
* `profile_id` (INTEGER, FK -> profiles.id, CASCADE): Perfil da criança.
* `symbol_id` (INTEGER, FK -> symbols.id, CASCADE): Pictograma incluído na prancha.
* `category_id` (INTEGER, FK -> categories.id, CASCADE): Categoria onde o símbolo foi posicionado.
* `order_index` (INTEGER): Ordem específica dentro da categoria para este perfil.
* `is_active` (BOOLEAN): Ativação.

### `quick_phrases`
* `id` (INTEGER, PK): Identificador da frase.
* `profile_id` (INTEGER, FK -> profiles.id, CASCADE, Nullable): Perfil associado.
* `text` (VARCHAR(255)): Texto da frase.
* `spoken_text` (VARCHAR(255)): Áudio falado.
* `icon` (VARCHAR(50)): Ícone visual.
* `order_index` (INTEGER): Ordem na lista lateral.

### `usage_metrics`
* `id` (INTEGER, PK): Identificador do evento.
* `profile_id` (INTEGER, FK -> profiles.id, SET NULL, Nullable): Perfil anônimo.
* `category_id` (INTEGER, FK -> categories.id, SET NULL, Nullable): Categoria acessada.
* `action_type` (VARCHAR(50)): Tipo de ação (*touch_symbol, change_category, speak_message, quick_phrase*).
* `reference_id` (VARCHAR(100), Nullable): Identificador do elemento.
* `timestamp` (DATETIME): Data e hora do registro técnico.
