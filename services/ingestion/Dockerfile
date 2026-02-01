FROM python:3.10-slim

WORKDIR /app

# 1. Install System Dependencies for Postgres
# "rm -rf ..." cleans up the apt cache to keep the image small (Best Practice)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy Source Code
COPY ./src ./src

# 4. Run the App
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]