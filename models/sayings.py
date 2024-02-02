# models/sayings.py

from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field

class Saying(BaseModel):

    # 고유 필드
    id: Optional[int] = Field(default=None, primary_key=True)

    # 필수 필드
    type_id: int
    contents_kr: str
    url_name: str

    # 공백 가능 필드
    category: Optional[str] = None


    model_config = {
        "json_schema_extra": {
            "contents_kr": "꿈을 꾸지 않으면 다른 사람이 당신을 고용하여 꿈을 꾸도록 도와 줄 것입니다.",

        }
    }