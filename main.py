import os
import logging
import requests
import pandas as pd
import joblib  # <--- New Friend
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# 1. Setup
load_dotenv()
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. Database Connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

def fetch_news():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=(technology OR business OR health)&pageSize=50&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])
        logging.info(f"Successfully fetched {len(articles)} articles.")
        return articles
    except Exception as e:
        logging.error(f"API Request failed: {e}")
        return []

def run_pipeline():
    logging.info("Starting AI Data Pipeline...")
    
    # A. Load the AI Brain
    # Note: These files must exist in the same folder!
    try:
        model = joblib.load('market_intel_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        logging.info("AI Model loaded successfully.")
    except Exception as e:
        logging.error(f"Could not load AI model: {e}")
        return

    # B. Fetch Data
    raw_articles = fetch_news()
    if not raw_articles:
        return

    # C. Process Data
    processed_data = []
    for art in raw_articles:
        title = art.get('title', '')
        description = art.get('description', '') or ''
        full_text = f"{title} {description}"
        
        # --- THE AI MAGIC HAPPENS HERE ---
        # 1. Convert text to numbers
        vec_input = vectorizer.transform([full_text])
        # 2. Predict category
        category = model.predict(vec_input)[0]
        # ---------------------------------

        processed_data.append({
            'title': title,
            'content': description,
            'published_at': art.get('publishedAt'),
            'source': art.get('source', {}).get('name'),
            'category': category,  # <--- New Field
            'ingested_at': datetime.now()
        })
    
    df = pd.DataFrame(processed_data)
    
    # D. Save to AWS RDS
    try:
        engine = create_engine(DATABASE_URI)
        # 'if_exists="append"' adds new rows
        # We don't need to manually run SQL ALTER TABLE; Pandas handles column matching often,
        # BUT if the DB table lacks the column, this might fail.
        # Safe bet: If it fails, we drop and recreate (only for dev).
        # For now, let's try appending.
        df.to_sql('news_articles', engine, if_exists='append', index=False)
        logging.info(f"Successfully uploaded {len(df)} classified articles to DB.")
    except Exception as e:
        logging.error(f"Database Upload Failed: {e}")

if __name__ == "__main__":
    run_pipeline()