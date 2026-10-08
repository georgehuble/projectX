from pydantic import BaseModel
from typing import Annotated
from pydantic.types import StringConstraints

Username = Annotated[
    str, StringConstraints(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
]


class User(BaseModel):
    username: Username


user = User(username="John")
user2 = User(username="ab1")
