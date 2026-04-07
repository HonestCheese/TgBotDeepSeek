from sqlalchemy.orm import scoped_session

from settings import *
if mode == "PROD":
    engine = create_engine(f"sqlite:///{db_path}")
if mod == "TEST":
    engine = create_engine(f"sqlite:///{test_db_path}")

session = sessionmaker(bind=engine)
def get_session_connection():
    return session()