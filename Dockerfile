# Etapa 1: build das dependências
FROM python:3.11-slim AS builder

# Instalar dependências do sistema necessárias para weasyprint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*    

WORKDIR /app

# Copiar arquivos de configuração
COPY pyproject.toml .

# Instalar dependências no ambiente isolado
RUN pip install --upgrade pip setuptools wheel \
    && pip install . --no-cache-dir

# Etapa 2: imagem final
FROM python:3.11-slim

WORKDIR /app

# Copiar dependências já instaladas
COPY --from=builder /usr/local /usr/local

# Copiar código da aplicação
COPY . .

# Expor porta padrão do Streamlit
EXPOSE 8501

# Comando padrão para rodar a aplicação
CMD ["streamlit", "run", "01_📃_Analisador_de_Currículos.py", "--server.port=8501", "--server.address=0.0.0.0"]
