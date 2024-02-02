# routes/sayings.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, delete
from typing import List

from models.sayings import Saying

from database.connection import get_session

saying_router = APIRouter(tags=["Sayings"])

@saying_router.get("/", response_model=List[Saying])
async def retrieve_all_saying(session=Depends(get_session)) -> List[Saying]:
    statement = select(Saying)
    sayings = session.exec(statement).all()  # 명언 테이블의 모든 값을 sayings에 리스트로 불러옴