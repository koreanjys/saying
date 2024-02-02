# models/fourchars.py

from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, DateTime

from datetime import datetime, timedelta

class FourChar(BaseModel):  # 사자성어 테이블 클래스

    # 고유 필드
    id: Optional[int] = Field(default=None, primary_key=True)

    # 필수 필드
    url_name: str
    category: str
    contents_zh: str
    contents_kr: str
    contents_detail: str

    type_id: int = Field(default=1, nullable=False)  # 자동생성
    created_at: Optional[DateTime] = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=9), nullable=False)  # UTC + 9시(한국 시간)
    

    # 공백 가능 필드
    contents_eng: Optional[str] = None
    contents_divided: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None

    updated_at: Optional[DateTime] = None



    model_config = {
        "json_schema_extra": {
            "example": {
                "url_name": "출처(URL 혹은 블로그명)",
                "contents_kr": "사자성어 원본을 한국어로 작성",
                "contents_detail": "사자성어 원본을 해석",
                "category": "사자성어 분류(예시: 인생)",
                "contents_eng": "사자성어 원본을 영어로 작성",
                "contents_zh": "사자성어 원본을 한자로 작성",
                "contents_divided": "사자성어 해석을 한글로만 작성(특수문자 외국어 제거)",
                "author": "저자",
                "continent": "출처(지역)"
            }
        }
    }