# main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from contextlib import asynccontextmanager

from database.connection import Settings

from routes.sayings import saying_router
from routes.fourchars import fourchar_router


# lifesapn : 어플리케이션 시작과 종료 시 실행되는 프로세스 작성
@asynccontextmanager
async def lifesapn(app: FastAPI):
    # 앱 시작 시 작동되는 코드 작성
    Settings.conn()  # DB 연결 및 초기화

    yield
    # 앱 종료 시 작동되는 코드 작성


app = FastAPI(lifespan=lifesapn)  # FastAPI 인스턴스 생성


# 라우트 등록
app.include_router(saying_router, prefix="/saying")
app.include_router(fourchar_router, prefix="/fourchar")


# 첫 화면
@app.get("/")
async def main():
    return RedirectResponse(url="/saying/")


# uvicorn 앱 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)