# database/connection.py

from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# # 데이터베이스 환경설정 및 엔진 생성

# database_file = "saying.db"  # DB 파일명
# database_connection_string = f"sqlite:///{database_file}"  # DB 연결주소
# connect_args = {"check_same_thread": False}  # False: 여러 쓰레드에서 동일한 연결을 공유

# engine_url = create_engine(database_connection_string, connect_args=connect_args, echo=True)  # DB 엔진 생성


# # 데이터베이스 연결 및 세션 함수들

# def conn():
#     SQLModel.metadata.create_all(engine_url)  # 프로그램 실행 시 작성된 모든 테이블을 데이터베이스에 생성

####################################################################################################
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
# 환경변수 불러오기 작업 다시 하기
####################################################################################################


# 세션을 관리하는 함수. FastAPI의 Depends()와 함께 사용하면 관리가 용이
def get_session():
    with Session(Settings.engine_url) as session:  # 세션을 종료하면 세션이 닫히도록 with문으로 작성
        yield session  # 각 작업마다 독립된 세션을 연결하기 위해 제너레이터 형태로 반환