FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs chromium libreoffice fonts-dejavu fonts-liberation

ENV LANG=C.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json .
RUN npm install

COPY app/ ./app/
COPY renderer/ ./renderer/

EXPOSE $PORT

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "$PORT"]