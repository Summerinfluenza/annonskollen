import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_db():
    if not firebase_admin._apps:
        BASE_DIR = Path(__file__).resolve().parent.parent
        DATA_DIR = BASE_DIR / "db"

        cred = credentials.Certificate(DATA_DIR/"firebase-adminsdk.json")
        database_url=os.getenv("DATABSE_URL")

        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
    return db
