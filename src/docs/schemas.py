from typing import Optional

from pydantic import BaseModel


class DocCreate(BaseModel):
    name: str
    description: str
    path: str
    user_id: int
