from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None

class Book(BookCreate):
    id: int

    class Config:
        from_attributes = True
