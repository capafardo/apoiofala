# Operação e Implantação - CAA-Lab

## 1. Inicialização Rápida

Para iniciar a aplicação em qualquer estação Ubuntu com Docker instalado:

```bash
./iniciar.sh
```

O script cuidará de:
1. Validar a presença do Docker e Docker Compose;
2. Configurar o arquivo de variáveis de ambiente (`.env`);
3. Criar os diretórios locais necessários (`data/`, `assets/`);
4. Subir os containers e aguardar a validação do healthcheck (`/health`);
5. Abrir a interface web no navegador padrão da estação (`xdg-open`).

## 2. Execução em Ambiente de Desenvolvimento

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
