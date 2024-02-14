# routes/category.py

from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from models.category import Category
from models.sayings import Saying
from models.fourchars import FourChar

from database.connection import get_session


category_router = APIRouter(tags=["Category"])


@category_router.get("/")
async def retrieve_all_category(session=Depends(get_session)):
    statement = select(Category.name)
    categories = session.exec(statement).all()
    return categories


# 카테고리 테이블 업데이트 URL
@category_router.get("/new_all")
async def new_all_categories(session=Depends(get_session)) -> dict:
    """
    카테고리 테이블의 데이터를 업데이트 합니다.
    """
    categrory_set = set()  # 카테고리명 중복제거를 위한 집합형태

    # 명언 데이터의 카테고리 불러오기 & category_set에 데이터 넣기
    statement = select(Saying.category).distinct()
    categories = session.exec(statement).all()
    for cat in categories:
        categrory_set.add(cat)
    
    # 사자성어 데이터의 카테고리 불러오기 & category_set에 데이터 넣기
    statement = select(FourChar.category).distinct()
    categories = session.exec(statement).all()
    for cat in categories:
        categrory_set.add(cat)
    
    # 카테고리 테이블 업데이트
    statement = select(Category.name)
    categories = session.exec(statement).all()
    cat_list = []
    for cat in categories:
        cat_list.append(cat)
    for cat in categrory_set:
        if cat not in cat_list:
            category = Category(name=cat)
            session.add(category)
    session.commit()
    return {
        "message": "카테고리 테이블 업데이트 완료"
    }