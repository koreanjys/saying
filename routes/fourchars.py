# routes/fourchars.py

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import select, delete, func
from typing import List, Optional
from datetime import datetime, timedelta

from models.fourchars import FourChar, FourCharUpdate
from models.category import Category

from database.connection import get_session


fourchar_router = APIRouter(tags=["FourChars"])


## CRUD START ############################################################################################## 
@fourchar_router.get("", response_model=dict)
async def retrieve_all_fourchars(p: int=Query(default=1), session=Depends(get_session)) -> dict:
    """
    저장된 모든 사자성어들 조회
    """
    # 페이징 처리
    page = p
    unit_per_page = 15  # 페이지당 보여질 데이터 수
    offset = (page - 1) * unit_per_page
    statement = select(FourChar).offset(offset).limit(unit_per_page).order_by(FourChar.id.desc())
    fourchars = session.exec(statement).all()

    # 토탈페이지 확인
    total_record = session.exec(select(func.count(FourChar.id))).one()
    total_page = (total_record // unit_per_page) + bool(total_record % unit_per_page)

    return {
        "total_page": total_page,
        "content": fourchars
    }


@fourchar_router.get("/{id}", response_model=FourChar)
async def retrieve_fourchar(id: int, session=Depends(get_session)) -> FourChar:
    """
    사자성어 조회
    """
    fourchar = session.get(FourChar, id)
    if fourchar:
        return fourchar
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="선택한 ID를 가진 사자성어가 존재하지 않습니다."
    )


@fourchar_router.post("/new", response_model=FourChar)
async def create_new_fourchar(new_fourchar: FourChar, session=Depends(get_session)) -> FourChar:
    """
    사자성어 새로 생성
    """
    category_name = new_fourchar.category

    statement = select(Category).where(Category.name == category_name)
    category = session.exec(statement).first()

    if not category:
        category = Category(name=category_name)
        session.add(category)
        session.commit()
        session.refresh(category)

    session.add(new_fourchar)
    session.commit()
    session.refresh(new_fourchar)  # 캐시 데이터 업데이트
    return new_fourchar


@fourchar_router.put("/edit/{id}", response_model=FourChar)
async def update_fourchar(id: int, new_data: FourCharUpdate, session=Depends(get_session)) -> FourChar:
    """
    사자성어 수정
    """
    fourchar = session.get(FourChar, id)
    if fourchar:
        fourchar_data = new_data.model_dump(exclude_unset=True)  # 클라이언트가 작성한 데이터만 변경하는 dict 생성
        fourchar_data["updated_at"] = (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # updated_at 컬럼에 업데이트 시간 추가
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
    """
    사자성어 삭제
    """
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
## CRUD END ##############################################################################################

# 필터링
@fourchar_router.get("/filter")
async def filtering(categories: Optional[List[str]]=None, keyword: Optional[str]=None, chars: Optional[List[str]]=None , session=Depends(get_session)):
    queries = {}
    if categories:
        queries["categories"] = categories
    if keyword:
        queries["search"] = keyword
    if chars:
        queries["chars"] = chars

    with open("./logs/log.txt", "a", encoding="UTF-8") as f:
        f.write(str(queries)+"\n\n")
        
    return queries