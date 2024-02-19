# tools/pagination.py
"""
페이지 처리
"""
from sqlmodel import select, delete, func, or_, and_


def paging(page, size, Table, statement):  # 페이징 처리 함수
    offset = (page - 1) * size
    statement = statement.offset(offset).limit(size).order_by(Table.id.desc())
    return statement