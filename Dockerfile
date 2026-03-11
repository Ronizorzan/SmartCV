# Usa uma imagem oficial do Python, versão slim para ser mais leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Atualiza os pacotes e instala TODAS as dependências nativas exigidas pelo WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libglib2.0-0 \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos para dentro do contêiner
COPY pyproject.toml .

# Instala as dependências do Python
RUN pip install --no-cache-dir .

# Copia todo o resto do seu código para o contêiner
COPY . .

# Expõe a porta padrão que o Streamlit usa
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "01_📃_Analisador_de_Currículos.py", "--server.port=8501", "--server.address=0.0.0.0"]
