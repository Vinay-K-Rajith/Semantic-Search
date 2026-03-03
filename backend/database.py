import os
import urllib
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

server = os.getenv('DB_SERVER')
username = urllib.parse.quote_plus(os.getenv('DB_USER'))
password = urllib.parse.quote_plus(os.getenv('DB_PASSWORD'))
database = os.getenv('DB_NAME')

# SQL Server Connection
# Driver: pymssql (Pure Python)
# Encryption: Yes (with TrustServerCertificate)
SQLALCHEMY_DATABASE_URL = f"mssql+pymssql://{username}:{password}@{server}/{database}"

# fast_executemany=True improves insert performance for SQL Server
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

