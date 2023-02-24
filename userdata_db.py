from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user_db_url = 'sqlite:///./user_data.db'  #defining database url
engine = create_engine(user_db_url, connect_args={"check_same_thread": False}) #creating engine 

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close