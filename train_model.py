import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def train():
    print("1. Loading data...")
    try:
        # Load the dataset we created yesterday
        df = pd.read_csv('training_data.csv')
        # Drop rows where data might be missing/corrupt
        df = df.dropna()
        print(f"   Loaded {len(df)} rows of data.")
    except FileNotFoundError:
        print("   Error: 'training_data.csv' not found. Please run create_dataset.py first.")
        return

    # 2. Split into Training (80%) and Testing (20%)
    # We hide 20% of the data to quiz the model later
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['category'], test_size=0.2, random_state=42
    )

    print("2. Converting text to numbers (TF-IDF)...")
    # TfidfVectorizer turns words into a matrix of numbers
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    
    # Learn the vocabulary from training data
    X_train_vec = vectorizer.fit_transform(X_train)
    # Transform the test data (using the same vocabulary)
    X_test_vec = vectorizer.transform(X_test)

    print("3. Training the model (Logistic Regression)...")
    # Logistic Regression is simple, fast, and great for text classification
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    print("4. Evaluating...")
    # Ask the model to predict the hidden test set
    predictions = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, predictions)
    print(f"   Model Accuracy: {accuracy * 100:.2f}%")
    print("\nDetailed Report:\n")
    print(classification_report(y_test, predictions))

    print("5. Saving the brain...")
    # We save BOTH the model and the vectorizer (the dictionary)
    joblib.dump(model, 'market_intel_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("   Saved to 'market_intel_model.pkl' and 'vectorizer.pkl'")

if __name__ == "__main__":
    train()