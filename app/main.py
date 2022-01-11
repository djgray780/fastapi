from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from starlette.status import HTTP_204_NO_CONTENT
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Prepare the base Pydantic model
class Post(BaseModel):
    # The annotation-only declaration tells pydantic that this field is required.
    title: str
    content: str
    published: bool = True  # Defaults to True
    rating: Optional[int] = None


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
def read_posts():
    cursor.execute(
        """ 
        SELECT * FROM posts 
        """
    )
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #
    cursor.execute(
        """ 
        INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")  # Path parameters are always returned as a string.
def get_posts(id: int):
    cursor.execute(
        """ 
        SELECT * FROM posts
        WHERE id = %s
        """,
        (str(id)),  # Convert id back to string to pass into SQL statement.
    )
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a single post"""
    cursor.execute(
        """
        DELETE FROM posts WHERE id = %s
        RETURNING *
     """,
        (str(id)),
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist.",
        )

    return Response(status_code=HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """Update posts"""
    cursor.execute(
        """
        UPDATE posts 
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist.",
        )
    return {"data": updated_post}
