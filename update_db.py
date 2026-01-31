import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

# Setup DB Connection
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
engine = sqlalchemy.create_engine(db_url)

def migrate():
    print("Connecting to database...")
    with engine.connect() as conn:
        # We wrap the SQL in text() to make SQLAlchemy happy
        try:
            conn.execute(sqlalchemy.text("ALTER TABLE news_articles ADD COLUMN category TEXT;"))
            conn.commit()
            print("Success! Added 'category' column to news_articles table.")
        except Exception as e:
            print(f"Note: {e}")
            print("(This usually means the column already exists, which is fine.)")

if __name__ == "__main__":
    migrate()