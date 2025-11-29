# Usa una imagen base oficial de Python como base
FROM python:3.9-slim

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los requisitos y el archivo de aplicación
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY app/ app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
