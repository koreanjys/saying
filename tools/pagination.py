# tools/pagination.py
"""
페이징 처리를 여러번 사용한다면 여기에 함수를 만들어서 재사용
현재는 미구현
"""
# 페이징 처리
async def paging(Table, page, unit_per_page=15):
    offset = (page - 1) * unit_per_page
    pass


# page = p
# unit_per_page = 15  # 페이지당 보여질 데이터 수
# offset = (page - 1) * unit_per_page
# statement = select(FourChar).offset(offset).limit(unit_per_page).order_by(FourChar.id.desc())
# fourchars = session.exec(statement).all()
# return {"content": fourchars}