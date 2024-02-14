# routes/category.py

from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from models.category import Category, CategoryName
from models.sayings import Saying
from models.fourchars import FourChar

from database.connection import get_session


category_router = APIRouter(tags=["Category"])


@category_router.get("/")
async def retrieve_all_category(session=Depends(get_session)):
    statement = select(Category.name)
    categories = session.exec(statement).all()
    return categories


@category_router.post("/new_all")
async def new_all_categories(session=Depends(get_session)):
    statement = select(Saying.category).distinct()
    categories = session.exec(statement).all()
    for cat in categories:
        category = Category(name=cat.category)
        session.add(category)
    