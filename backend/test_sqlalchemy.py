from database import get_db, engine
from sqlalchemy import text

def test_connection():
    print("Testing SQLAlchemy connection...")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection successful: {result.fetchone()}")
            
            # Additional check if we can query tables
            # result = connection.execute(text("SELECT TOP 5 * FROM LMSVideoContents"))
            # print("Query successful")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
