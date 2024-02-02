# routes/sayings.py

from fastapi import APIRouter
from typing import List

from models.sayings import Saying

saying_router = APIRouter(tags=["Sayings"])

@saying_router.get("/", response_model=List[Saying])
async def retrieve_all_saying() -> List[Saying]:
    pass