from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    id: int
    text: str


db = []


async def get_post_or_404(id: int):
    try:
        return db[id]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/message/{id}")
async def get_message(post: Annotated[Post, Depends(get_post_or_404)]):
    return post


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(post: Post) -> str:
    post.id = len(db)
    db.append(post)
    return "Message creates!"


@app.put("/message/{id}", status_code=status.HTTP_201_CREATED)
async def update_message(post: Annotated[Post, Depends(get_post_or_404)]):
    pass


@app.delete("/message/{id}", status_code=status.HTTP_200_OK)
async def remove_message(post: Annotated[Post, Depends(get_post_or_404)]):
    pass


class Paginator:
    def __init__(self, limit: int = 10, page: int = 1):
        self.limit = limit
        self.page = page

    def __call__(self, limit: int):
        if limit < self.limit:
            return [{"limit": self.limit, "page": self.page}]
        else:
            return [{"limit": limit, "page": self.page}]


my_paginator = Paginator()


@app.get("/users")
async def all_users(pagination: Annotated[list, Depends(my_paginator)]):
    return {"user": pagination}


from starlette.requests import Request


async def sub_dependency(request: Request) -> str:
    return request.method


async def main_dependency(sub_dependency_value: str = Depends(sub_dependency)) -> str:
    return sub_dependency_value


@app.get("/test")
async def test_endpoint(test: str = Depends(main_dependency)):
    return test
