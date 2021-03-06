from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Establish the connection to the Postgres database.
# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         dbname="fastapi",
#         user="postgres",
#         password="postgres",
#         cursor_factory=RealDictCursor,
#     )
#     cursor = conn.cursor()
#     print("Connected to Database ... ")
# except Exception as error:
#     print("Connecting to database failed ...")
#     print("Error", error)
