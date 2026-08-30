# Segurança e Privacidade (LGPD) - CAA-Lab

## 1. Diretrizes Fundamentais

- **Isolamento de Dados:** Todo armazenamento é 100% local (`data/`).
- **Minimização de Dados:** Não são coletadas informações desnecessárias; mensagens particulares da criança não são persistidas em logs ou métricas.
- **Armazenamento de Senhas:** Senhas de usuários e profissionais são armazenadas com hash criptográfico forte (`bcrypt`).
- **Segurança HTTP:** Headers de segurança configurados (`X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` local).
- **Sem Telemetria Externa:** Zero chamadas a rastreadores, analytics ou serviços de terceiros.
