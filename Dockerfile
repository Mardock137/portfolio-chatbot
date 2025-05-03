# --- Dockerfile ---
    FROM python:3.11-slim

    # Evita richieste interattive in build
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # Copio requirements e installo
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copio solo il codice che serve
    COPY src/ ./src/
    
    # Porta che Cloud Run espone
    ENV PORT 8080
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
    