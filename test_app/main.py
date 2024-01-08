from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg.connect(dbname= 'fastapi', user= 'postgres',
                                password= 'jch0618', row_factory= dict_row)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i, post
    return None, None

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts_test""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts_test (title, content, published) 
                        VALUES (%s, %s, %s)
                        RETURNING *""", 
                        (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * 
                        FROM posts_test 
                        WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts_test 
                        WHERE id = %s
                        RETURNING *""", (str(id),))
    post = cursor.fetchone()

    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    conn.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts_test
                        SET title= %s, content= %s, published= %s
                        WHERE id = %s
                        RETURNING *""",
                        (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    conn.commit()

    return {"data": updated_post}