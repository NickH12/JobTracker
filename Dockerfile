FROM python:3.11-slim

WORKDIR /code

# System packages needed to build psycopg2/cryptography/bcrypt wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching -
# this layer only rebuilds when requirements.txt changes, not on every code change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Run migrations, then start the API server.
# In production you'd typically run migrations as a separate step/job,
# but for a small project this keeps things simple and reliable.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]