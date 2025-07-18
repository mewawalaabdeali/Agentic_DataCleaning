import sys
import os
import pandas as pd
import io
import aiohttp
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from sqlalchemy import create_engine
from pydantic import BaseModel
import requests

#Ensure the scripts folder is in Python's path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scripts.aiagent import AIAgent
from scripts.dataCleaning import DataCleaner

app = FastAPI()

aiagent = AIAgent()
cleaner = DataCleaner()

@app.post("/clean-data")
async def clean_data(file:UploadFile = File(...)):
    """Receives file from UI, cleans it using rule-based & AI methods, returns cleaned JSON."""