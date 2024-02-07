# models/sayings.py

from typing import Optional
from sqlmodel import Field, SQLModel

from datetime import datetime, timedelta

# datetime의 출력 형태를 설정
def current_time_kst():
    return (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # UTC + 9시간 = 한국 시간


class Saying(SQLModel, table=True):  # 명언 테이블 클래스

    # PK_ID
    id: Optional[int] = Field(default=None, primary_key=True)

    # 필수 필드
    category: str = Field(max_length=20, nullable=False)
    type_id: int = Field(nullable=False)
    content_desc_kr: str = Field(max_length=500, nullable=False)
    useyn: int = Field(nullable=False)

    # 공백 가능 필드
    type_kr: Optional[str] = Field(default=None, max_length=50)
    url_name: Optional[str] = Field(default=None, max_length=50)
    type_chn: Optional[str] = Field(default=None, max_length=50)
    content_desc_en: Optional[str] = Field(default=None, max_length=500)
    author: Optional[str] = Field(default=None, max_length=50)
    continent: Optional[str] = Field(default=None, max_length=20)
    created_at: Optional[datetime] = Field(default_factory=current_time_kst)
    updated_at: Optional[datetime] = None


    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "예시: 인생",
                "type_id": "0: 명언  1: 사자성어",
                "type_chn": "사자성어(한자)",
                "author": "저자",
                "continent": "출처(지역)",
                "url_name": "출처(웹)",
                "content_desc_kr": "내용(한글)",
                "content_desc_en": "내용(영문)",
                "useyn": "반영 여부 0: 반영  1: 미반영"
            }
        }
    }


class SayingUpdate(SQLModel):
    category: Optional[str] = None
    type_id: Optional[int] = None
    content_desc_kr: Optional[str] = None
    useyn: Optional[int] = None
    type_kr: Optional[str] = None
    url_name: Optional[str] = None
    type_chn: Optional[str] = None
    content_desc_en: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None

    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "예시: 인생",
                "type_id": "0: 명언  1: 사자성어",
                "type_chn": "사자성어(한자)",
                "author": "저자",
                "continent": "출처(지역)",
                "url_name": "출처(웹)",
                "content_desc_kr": "내용(한글)",
                "content_desc_en": "내용(영문)",
                "useyn": "반영 여부 0: 반영  1: 미반영"
            }
        }
    }