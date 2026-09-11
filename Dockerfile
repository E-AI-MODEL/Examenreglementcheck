FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y tesseract-ocr tesseract-ocr-nld \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd --create-home --uid 10001 checker \
    && mkdir -p runtime/runs runtime/uploads \
    && chown -R checker:checker /app

USER checker
EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import json,urllib.request; assert json.load(urllib.request.urlopen('http://127.0.0.1:8765/api/health',timeout=3))['ok']"

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8765"]

