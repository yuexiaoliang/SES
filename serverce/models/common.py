from pydantic import BaseModel
from typing import Any


class ResponseBaseModel(BaseModel):
    class Config:
        orm_mode = True

    message: str
    code: int


class ResponseListModel(BaseModel):
    total: int
    page_size: int
    page_current: int
    list: Any
