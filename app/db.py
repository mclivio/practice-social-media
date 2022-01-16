from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DB"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# def create_all():    
#     Base.metadata.create_all(bind=engine)

# def drop_all():
#     Base.metadata.drop_all(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# while 1:
#     try:
#         conn = psycopg2.connect(host='localhost', database='social_media', user='postgres', password='password', cursor_factory=RealDictCursor )
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2) 
#RAW PSYCOPG2 CONNECTION INSTEAD OF USING SQLALCHEMY