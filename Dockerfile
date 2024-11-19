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

# Instalación de geckodriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")') && \
    wget -q https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

# Instalación de Selenium
RUN pip install selenium

# Añadir los archivos de la aplicación al contenedor
WORKDIR /app
COPY . .

# Permitir ejecución del script principal
RUN chmod +x /app/main.py

# Comando para ejecutar el script
ENTRYPOINT ["python3", "main.py"]