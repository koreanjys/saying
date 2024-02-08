# models/fourchars.py

from typing import Optional
from sqlmodel import Field, SQLModel

from datetime import datetime, timedelta

# datetime의 출력 형태를 설정
def current_time_kst():
    return (datetime.utcnow() + timedelta(hours=9)).replace(microsecond=0)  # UTC + 9시간 = 한국 시간


class FourChar(SQLModel, table=True):  # 사자성어 테이블 클래스

    # PK_ID
    id: Optional[int] = Field(default=None, primary_key=True)

    # 필수 필드
    contents_kr: str
    contents_detail: str

    type_id: int = Field(default=1, nullable=False)  # 자동생성
    use_yn: int = Field(default=1, nullable=False)  # 자동생성
    

    # 공백 가능 필드
    created_at: Optional[datetime] = Field(default_factory=current_time_kst, nullable=True)  # 자동생성
    category: Optional[str] = None
    url_name: Optional[str] = None
    contents_eng: Optional[str] = None
    contents_zh: Optional[str] = None
    contents_divided: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None

    updated_at: Optional[datetime] = None

    #모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "*사자성어 분류(예시: 인생)",
                "contents_kr": "*사자성어 원본을 한국어로 작성",
                "contents_detail": "*사자성어 원본을 해석",
                "contents_zh": "사자성어 원본을 한문으로 작성",
            }
        }
    }


class FourCharUpdate(SQLModel):
    url_name: Optional[str] = None
    contents_kr: Optional[str] = None
    contents_detail: Optional[str] = None
    type_id: Optional[int] = None
    category: Optional[str] = None
    contents_eng: Optional[str] = None
    contents_zh: Optional[str] = None
    contents_divided: Optional[str] = None
    author: Optional[str] = None
    continent: Optional[str] = None
    use_yn: Optional[int] = None
    # update_at: datetime = Field(default_factory=current_time_kst, nullable=False)  # 여기서 설정해도 적용이 안되므로 router의 update 함수에서 직접 값을 추가

    # 모델 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "url_name": "출처(URL 혹은 블로그명)",
                "contents_kr": "사자성어 원본을 한국어로 작성",
                "contents_detail": "사자성어 원본을 해석",
                "type_id": "0: 명언  1: 사자성어",
                "category": "사자성어 분류(예시: 인생)",
                "contents_eng": "사자성어 원본을 영어로 작성",
                "contents_zh": "사자성어 원본을 한자로 작성",
                "contents_divided": "사자성어 해석을 한글로만 작성(특수문자 외국어 제거)",
                "author": "저자",
                "continent": "출처(지역)",
                "use_yn": "운영에 반영 여부 1: Yes  0: No"
            }
        }
    }