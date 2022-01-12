from fastapi import FastAPI, Response, status, HTTPException, Depends
from starlette.status import HTTP_204_NO_CONTENT
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session


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


# Route definitions
@app.get("/")
def root():
    return {"message": "Hello World, how are you?"}


@app.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     SELECT * FROM posts
    #     """
    # )
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())  # Unpacking operator on a dictionary object.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())  # Unpacking operator on a dictionary object.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/posts/{id}")  # Path parameters are always returned as a string.
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #     SELECT * FROM posts
    #     WHERE id = %s
    #     """,
    #     (str(id)),  # Convert id back to string to pass into SQL statement.
    # )
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # """Delete a single post"""
    # cursor.execute(
    #     """
    #     DELETE FROM posts WHERE id = %s
    #     RETURNING *
    #  """,
    #     (str(id)),
    # )
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist.",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    # """Update posts"""
    # cursor.execute(
    #     """
    #     UPDATE posts
    #     SET title = %s, content = %s, published = %s
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist.",
        )
    post.query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
