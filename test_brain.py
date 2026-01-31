import joblib

# 1. Load the Brain and the Dictionary
print("Loading model...")
model = joblib.load('market_intel_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

print("\n--- AI News Classifier (Type 'exit' to quit) ---")

while True:
    # 2. Get user input
    headline = input("\nEnter a news headline: ")
    if headline.lower() == 'exit':
        break
    
    # 3. Transform input (Text -> Numbers)
    # We must use 'transform', NOT 'fit_transform' (because the dictionary is already fixed)
    headline_vec = vectorizer.transform([headline])
    
    # 4. Predict
    prediction = model.predict(headline_vec)[0]
    probability = model.predict_proba(headline_vec).max() * 100
    
    print(f"Prediction: {prediction} (Confidence: {probability:.2f}%)")