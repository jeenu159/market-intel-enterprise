import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the connection string from Environment Variable
# This is injected by Docker Compose
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create the Engine
# This represents the core interface to the database
engine = create_engine(DATABASE_URL)

# 3. Create a Session Factory
# We use this to create a temporary "session" for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Define the Base Class for models
Base = declarative_base()

# 5. Define the Table Schema
class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category = Column(String)  # This will be filled by the AI
    source = Column(String)
    published_at = Column(DateTime)

# Helper to create tables on startup
def init_db():
    Base.metadata.create_all(bind=engine)