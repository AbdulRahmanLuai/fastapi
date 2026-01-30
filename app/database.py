from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings





SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='2021905157',
#                                 cursor_factory=RealDictCursor)
        
#         print("Database connection was succesful!")
#         break
#     except Exception as error:
#         print (f"failed to connect to database, error: {error}")
        


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
