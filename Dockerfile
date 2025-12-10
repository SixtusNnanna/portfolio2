# Ultra-light CPU-only image — under 2GB (Railway free tier loves it)
FROM python:3.11-slim

WORKDIR /app

# Install only what we need (no heavy GPU stuff)
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Copy code
COPY . .

# Install ONLY CPU versions + lightweight models
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    sqlalchemy[asyncio] \
    asyncpg \
    psycopg2-binary \
    python-multipart \
    requests \
    cloudinary \
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]