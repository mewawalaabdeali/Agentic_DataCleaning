import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

#Database credentials
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE();"))
            print(f"Connected to the Database: {result.scalar()}")
    except Exception as e:
        print(f"Connection failed: {e}")

def list_tables():
    try:
        with engine.connect() as conn:
            query = text("SHOW TABLES;")
            result = conn.execute(query)
            tables = [row[0] for row in result.fetchall()]
            print("Tables in database: ")
            for table in tables:
                print(f"{table}")
    except Exception as e:
        print(f"Failed to fetch tables: {e}")

if __name__=="__main__":
    test_connection()
    list_tables()