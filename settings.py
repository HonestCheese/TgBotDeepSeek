from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()


db_path = os.getenv("DB_PATH")

engine = create_engine(f"sqlite:///{db_path}")

def get_session_connection():
    return sessionmaker(bind=engine)