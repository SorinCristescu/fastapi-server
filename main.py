from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

mock_posts = [
    {"id": 1, "title": "Post 1", "content": "This is post 1", "published": True, "rating": 5},
    {"id": 2, "title": "Post 2", "content": "This is post 2", "published": False, "rating": 4},
    {"id": 3, "title": "Post 3", "content": "This is post 3", "published": True, "rating": 3},
    {"id": 4, "title": "Post 4", "content": "This is post 4", "published": False, "rating": 2},
    {"id": 5, "title": "Post 5", "content": "This is post 5", "published": True, "rating": 1}
]

def find_post_by_id(id):
    for p in mock_posts:
        if p["id"] == id:
            return p

@app.get("/")
def read_root():
    return {"message": "Welcome to my apis"}

@app.get("/posts")
def get_posts():
    return {"message": "These are your posts.", "data": mock_posts}

@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response): # always path params are strings so we enforce to be integer with validation
    post = find_post_by_id(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, message=f"Post with id: {id} not found.")
    
    return {"message": "This is your post.", "data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000000)
    mock_posts.append(post_dict)
    return {"message": "Post created successfully.", "data": post_dict}

@app.put("/posts/{id}")
def update_post(post: Post):
    return {"message": "Post updated successfully.", "data": post}

@app.delete("/posts/{id}")
def delete_post():
    return {"message": "Post deleted successfully."}

