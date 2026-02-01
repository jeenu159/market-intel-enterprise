# MarketIntel Enterprise AI Platform

## 🚀 Overview
MarketIntel is a scalable, microservices-based AI platform designed to ingest, classify, and analyze financial news in real-time. It leverages a decoupled architecture to ensure high availability and independent scaling of inference and ingestion layers.

## 🏗 Architecture
- **Ingestion Service:** FastAPI + HTTPX + SQLAlchemy (Async I/O)
- **Inference Service:** FastAPI + Scikit-Learn (ML Model Serving)
- **Database:** PostgreSQL 15
- **Infrastructure:** Docker & Docker Compose (Local), Kubernetes (Cloud - In Progress)

## 🛠 Tech Stack
- **Languages:** Python 3.10
- **Frameworks:** FastAPI, Uvicorn
- **DevOps:** Docker, Docker Compose, GitHub Actions
- **ML:** Scikit-Learn (TF-IDF + Logistic Regression)
