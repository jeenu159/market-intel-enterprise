import httpx
import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from .database import SessionLocal, NewsArticle, init_db

app = FastAPI()

# Configuration
INFERENCE_URL = os.getenv("INFERENCE_URL", "http://inference:8001/predict")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# --- 1. Startup Logic ---
@app.on_event("startup")
def startup_event():
    # When the service starts, create the DB tables if they don't exist
    init_db()

# --- 2. Data Models (Pydantic) ---
# This ensures we only accept valid data
class ArticleRequest(BaseModel):
    title: str
    content: str
    source: str = "Manual Input"
    published_at: datetime = None

# --- 3. The "Worker" Function ---
async def process_article(article: ArticleRequest):
    """
    This runs in the background. It calls the AI and saves to DB.
    """
    # Step A: Call the Inference Service (The Brain)
    category = "Uncategorized"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                INFERENCE_URL, 
                json={"text": article.content},
                timeout=10.0 # Always set timeouts in production!
            )
            if response.status_code == 200:
                category = response.json().get("category", "Error")
            else:
                print(f"⚠️ Inference Error: {response.text}")
    except Exception as e:
        print(f"❌ Could not contact Inference Service: {e}")

    # Step B: Save to Database
    try:
        db = SessionLocal()
        new_article = NewsArticle(
            title=article.title,
            content=article.content,
            category=category,
            source=article.source,
            published_at=article.published_at or datetime.now()
        )
        db.add(new_article)
        db.commit() # Save changes
        db.refresh(new_article) # Reload to get the new ID
        db.close()
        print(f"✅ Saved Article ID {new_article.id} as [{category}]")
    except Exception as e:
        print(f"❌ Database Error: {e}")

# --- 4. The API Endpoint ---
@app.post("/ingest")
async def ingest_article(article: ArticleRequest, background_tasks: BackgroundTasks):
    """
    Receives an article and schedules it for processing.
    Returns immediately so the user doesn't wait.
    """
    background_tasks.add_task(process_article, article)
    return {"status": "Accepted", "message": "Article is being processed in background"}

@app.get("/health")
def health_check():
    return {"status": "Ingestion Service Ready"}