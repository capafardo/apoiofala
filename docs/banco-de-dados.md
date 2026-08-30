# Banco de Dados - CAA-Lab

## 1. Engine e Armazenamento

- **Engine MVP:** SQLite com suporte a WAL (Write-Ahead Logging) e chaves estrangeiras ativadas.
- **Localização:** `data/caa_lab.db` (armazenado em volume persistente).
- **Abstração:** SQLAlchemy 2.0 ORM com padrão Repository, permitindo migração futura transparente para PostgreSQL.

## 2. Entidades Principais

- **User (Usuários):** `id`, `username`, `password_hash`, `role` (admin, professional, user), `created_at`, `is_active`.
- **Profile (Perfis de Paciente/Criança):** `id`, `user_id`, `name`, `symbol_size`, `symbols_per_page`, `contrast_mode`, `voice_speed`, `theme_color`.
- **Category (Categorias de Símbolos):** `id`, `name`, `icon`, `color`, `order_index`, `is_active`.
- **Symbol (Pictogramas):** `id`, `category_id`, `name`, `text_label`, `image_path`, `spoken_text`, `order_index`, `is_active`.
- **QuickPhrase (Frases Rápidas):** `id`, `profile_id`, `category_id`, `text`, `icon`, `order_index`, `is_active`.
- **UsageMetric (Métricas Técnicas Anônimas):** `id`, `profile_id`, `category_id`, `action_type`, `timestamp`.
