FROM python:3.11-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-common \
    chromium-sandbox \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    fonts-liberation \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Chrome binary path (ÖNEMLİ)
ENV CHROME_BIN=/usr/bin/chromium
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
