from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Establish the connection to the Postgres database.
try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="fastapi",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Connected to Database ... ")
except Exception as error:
    print("Connecting to database failed ...")
    print("Error", error)


app.include_router(post.router)
app.include_router(user.router)

# Route definitions
@app.get("/")
def root():
    return {"message": "Hello World, how are you?"}
