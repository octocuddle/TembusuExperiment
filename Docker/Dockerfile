FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install requirements first for caching
COPY ./app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the FastAPI app
COPY ./app ./app

# Run uvicorn using the full module path
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
