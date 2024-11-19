# Utilizar una imagen base más ligera
FROM python:3.9-slim

# Instalación de dependencias esenciales
RUN apt-get update && \
    apt-get install -y \
    firefox-esr \
    wget \
    curl \
    unzip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instalación de geckodriver (versión específica v0.33.0)
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.33.0-linux64.tar.gz

# Añadir los archivos de la aplicación al contenedor
WORKDIR /app
COPY . .

# Instalación de dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Permitir ejecución del script principal
RUN chmod +x /app/main.py

# Configurar PATH para geckodriver (asegurarse de que está en el PATH)
ENV PATH="/usr/local/bin:${PATH}"

# Comando para ejecutar el script
ENTRYPOINT ["python3", "/app/main.py"]
