import joblib
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 1. Define Paths to your specific files
BASE_PATH = "/app/models/"
MODEL_FILE = os.path.join(BASE_PATH, "market_intel_model.pkl")
VECT_FILE = os.path.join(BASE_PATH, "vectorizer.pkl")

# Global variables
model = None
vectorizer = None

@app.on_event("startup")
def load_artifacts():
    global model, vectorizer
    try:
        # Load Vectorizer
        if os.path.exists(VECT_FILE):
            vectorizer = joblib.load(VECT_FILE)
            print(f"✅ Vectorizer loaded from {VECT_FILE}")
        else:
            print(f"❌ Vectorizer not found at {VECT_FILE}")

        # Load Model
        if os.path.exists(MODEL_FILE):
            model = joblib.load(MODEL_FILE)
            print(f"✅ Model loaded from {MODEL_FILE}")
        else:
            print(f"❌ Model not found at {MODEL_FILE}")

    except Exception as e:
        print(f"❌ Critical Error loading artifacts: {e}")

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: TextRequest):
    # 1. Fail fast if model/vectorizer are missing
    if not model or not vectorizer:
        return {"category": "Error: Model/Vectorizer missing", "confidence": 0.0}
    
    try:
        # 2. Transform Text -> Numbers (Vectorization)
        # Note: transform expects a list/iterable, hence [request.text]
        text_vector = vectorizer.transform([request.text])
        
        # 3. Predict Category
        prediction = model.predict(text_vector)[0]
        
        return {"category": str(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))