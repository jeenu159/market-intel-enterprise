FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY ./src ./src
# Note: We do NOT copy the models folder here because we mounted it in docker-compose
# This keeps the image small.

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]