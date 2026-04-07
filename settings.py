from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_path = os.getenv("DB_PATH")
mode = os.getenv("MODE")
test_db_path = os.getenv("TEST_DB_PATH")

