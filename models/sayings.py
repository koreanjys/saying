# models/sayings.py

from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field

class Saying(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    saying: str = Field(max_length=256)
    author: str = Field(max_length=128)
    