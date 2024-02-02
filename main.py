# main.py

from fastapi import FastAPI

from routes.sayings import saying_router

app = FastAPI()  # FastAPI 인스턴스 생성

# 첫 화면
@app.get("/")
async def main() -> dict:
    return {
        "message": "게시판"
    }


# 라우트 등록
app.include_router(saying_router, prefix="/saying")