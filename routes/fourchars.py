# routes/fourchars.py

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import select, delete, func, or_
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

    statement = select(Category).where(Category.fourchar_categories == category_name)
    category = session.exec(statement).first()

    if not category:
        category = Category(fourchar_categories=category_name)
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

# 프론트엔드에서 쿼리가 잘 날아오는지 확인하기 위한 코드
"""
@fourchar_router.get("/filter/")
async def fourchar_filtering(keyword: Optional[str]=Query(default=None), session=Depends(get_session)):

    with open("./logs/log.txt", "a", encoding="UTF-8") as f:
        f.write("키워드"+str(keyword)+"\n\n")
        
    return keyword
"""


# 필터링 라우터 함수
@fourchar_router.get("/filter/", response_model=dict)
async def fourchar_filtering(
        categories: Optional[List[str]]=Query(default=None),
        keyword: Optional[str]=Query(default=None),
        chars: Optional[List[str]]=Query(default=None),
        p: int=Query(default=1),
        session=Depends(get_session)
        ) -> dict:

    statement = select(FourChar)
    if categories:
        conditions = [FourChar.category==cat for cat in categories]
        statement = statement.where(or_(*conditions))
    if keyword:
        statement = statement.where(FourChar.contents_divided.like(f"%{keyword}%"))
    if chars:
        ranges = {
                "ㄱ": ("가", "깋"),
                "ㄴ": ("나", "닣"),
                "ㄷ": ("다", "딯"),
                "ㄹ": ("라", "맇"),
                "ㅁ": ("마", "밓"),
                "ㅂ": ("바", "빟"),
                "ㅅ": ("사", "싷"),
                "ㅇ": ("아", "잏"),
                "ㅈ": ("자", "짛"),
                "ㅊ": ("차", "칳"),
                "ㅋ": ("카", "킿"),
                "ㅌ": ("타", "팋"),
                "ㅍ": ("파", "핗"),
                "ㅎ": ("하", "힣"),
                }

        conditions = [FourChar.contents_kr.like(f"{char}%") for char in chars]
        statement = statement.where(or_(*conditions))

    # 페이징 처리
    page = p
    unit_per_page = 15  # 페이지당 보여질 데이터 수
    offset = (page - 1) * unit_per_page
    statement = statement.offset(offset).limit(unit_per_page).order_by(FourChar.id.desc())

    filtered_fourchars = session.exec(statement).all()

    # 토탈 페이지 확인
    total_record = session.exec(select(func.count()).where(statement._whereclause)).one()
    total_page = (total_record // unit_per_page) + bool(total_record % unit_per_page)

    return {"total_page": total_page, "content": filtered_fourchars}