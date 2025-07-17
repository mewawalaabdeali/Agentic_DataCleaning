import os
import sys
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
#from scripts.test_mysql_connection import engine
from test_mysql_connection import engine


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")

class DataIngestion:
    def __init__(self):
        """Initialize the ingestion class with a database engine."""
        self.engine = engine

    def load_csv(self, file_name):
        """Load a CSV file from the data folder"""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_csv(file_path)
            print(f"CSV Loaded succesfully: {file_path}")
            return df
        except Exception as e:
            print(f"Error Loading CSV: {e}")
            return None
        
    def load_excel(self, file_name, sheet_name=0):
        """Load an Excel file from the data folder."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Excel loaded succesfully: {file_path}")
            return df
        except Exception as e:
            print(f"Error loading Excel: {e}")
            return None
        
    def connect_database(self, db_url):
        """Optional: Establish connection using a custom db_url"""
        try:
            self.engine = create_engine(db_url)
            print("Database connection established")
        except Exception as e:
            print(f"Error creating engine: {e}")

    def load_query(self, query):
        """Run a custom SQL query and return results as DataFrame"""
        if not self.engine:
            print("No active database connection.")
            return None
        try:
            df = pd.read_sql(query, self.engine)
            print("Query Executed Succesfully")
            return df
        except SQLAlchemyError as e:
            print(f"SQL Execution error: {e}")
            return None
        
    def load_table(self, table_name):
        """Load a full table from the connect database."""
        if not self.engine:
            print("No Active Database connection")
            return None
        try:
            query = f"SELECT * FROM {table_name};"
            df= pd.read_sql(query, self.engine)
            print(f"Table '{table_name}' loaded successfully")
            return df
        except SQLAlchemyError as e:
            print(f"Error loading table '{table_name}': {e}")
            return None
        
    def fetch_from_api(self, api_url, params = None):
        """Call an external API and return results as DataFrame"""
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                print("API Data Fetched Succesfully")
                return df
            else:
                print(f"API Request Failed with Status: {response.status_code}")
                return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
        
if __name__=="__main__":
    ingest = DataIngestion()
    #df = ingest.load_table("raw_data_uploads")
    #if df is not None:
    #    print(df.head())

    df = ingest.load_csv("SampleData.csv")
    if df is not None:
        print(df.head())