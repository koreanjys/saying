# models/sayings.py

from typing import Optional
from sqlmodel import Field, SQLModel

from datetime import datetime, timedelta

# datetime의 출력 형태를 설정
def current_time_kst():
    return (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # UTC + 9시간 = 한국 시간


class Saying(SQLModel, table=True):  # 명언 테이블 클래스

    # 고유 필드
    id: Optional[int] = Field(default=None, primary_key=True)

    # 필수 필드
    url_name: str
    contents_kr: str
    contents_detail: str

    type_id: int = Field(default=0, nullable=False)  # 자동생성
    created_at: Optional[datetime] = Field(default_factory=current_time_kst, nullable=False)
    

    # 공백 가능 필드
    category: Optional[str] = None
    contents_eng: Optional[str] = None
    contents_zh: Optional[str] = None
    contents_divided: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None

    updated_at: Optional[datetime] = None

    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "url_name": "*출처(URL 혹은 블로그명)",
                "contents_kr": "*명언 원본을 한국어로 작성",
                "contents_detail": "*명언 원본을 해석",
                "category": "명언 분류(예시: 인생)",
                "contents_eng": "명언 원본을 영어로 작성",
                "contents_zh": "명언 원본을 한자로 작성",
                "contents_divided": "명언 해석을 한글로만 작성(특수문자 외국어 제거)",
                "author": "저자",
                "continent": "출처(지역)"
            }
        }
    }


class SayingUpdate(SQLModel):
    url_name: Optional[str] = None
    contents_kr: Optional[str] = None
    contents_detail: Optional[str] = None
    type_id: Optional[str] = None
    category: Optional[str] = None
    contents_eng: Optional[str] = None
    contents_zh: Optional[str] = None
    contents_divided: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None
    # updated_at: datetime = Field(default_factory=current_time_kst, nullable=False)  # 여기서 설정해도 적용이 안되므로 router에서 직접 값을 추가

    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "url_name": "출처(URL 혹은 블로그명)",
                "contents_kr": "명언 원본을 한국어로 작성",
                "contents_detail": "명언 원본을 해석",
                "type_id": "0: 명언  1: 사자성어",
                "category": "명언 분류(예시: 인생)",
                "contents_eng": "명언 원본을 영어로 작성",
                "contents_zh": "명언 원본을 한자로 작성",
                "contents_divided": "명언 해석을 한글로만 작성(특수문자 외국어 제거)",
                "author": "저자",
                "continent": "출처(지역)"
            }
        }
    }