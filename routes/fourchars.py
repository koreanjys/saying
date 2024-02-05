# routes/fourchars.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, delete
from typing import List

from models.fourchars import FourChar, FourCharUpdate

from database.connection import get_session


fourchar_router = APIRouter(tags=["FourChars"])


@fourchar_router.get("/", response_model=List[FourChar])
async def retrieve_all_fourchars(session=Depends(get_session)) -> List[FourChar]:
    statement = select(FourChar)
    fourchars = session.exec(statement).all()  # 사자성어 테이블의 모든 값을 fourchars에 리스트로 불러옴
    return fourchars


@fourchar_router.get("/{id}", response_model=FourChar)
async def retrieve_fourchar(id: int, session=Depends(get_session)) -> FourChar:
    fourchar = session.get(FourChar, id)
    if fourchar:
        return fourchar
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )


@fourchar_router.post("/new", response_model=FourChar)
async def create_new_fourchar(new_fourchar: FourChar, session=Depends(get_session)) -> FourChar:
    session.add(new_fourchar)
    session.commit()
    session.refresh(new_fourchar)  # 캐시 데이터 업데이트
    return new_fourchar


@fourchar_router.put("/edit/{id}", response_model=FourChar)
async def update_fourchar(id: int, new_data: FourCharUpdate, session=Depends(get_session)) -> FourChar:
    fourchar = session.get(FourChar, id)
    if fourchar:
        fourchar_data = new_data.model_dump(exclude_unset=True)  # 클라이언트가 작성한 데이터만 변경하는 dict 생성
        for key, value in fourchar_data.items():
            setattr(fourchar, key, value)  # setattr(object, name, value) >>> object에 존재하는 속성의 값을 바꾸거나, 새로운 속성을 생성하여 값을 부여한다.
        session.add(fourchar)
        session.commit()
        session.refresh(fourchar)
        return fourchar
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )

@fourchar_router.delete("/delete/{id}")
async def delete_fourchar(id: int, session=Depends(get_session)) -> dict:
    fourchar = session.get(FourChar, id)
    if fourchar:
        session.delete(fourchar)
        session.commit()
        return {
            "message": "사자성어를 삭제했습니다."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )