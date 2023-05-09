from pydantic import BaseModel
from typing import Any


class ResponseBaseModel(BaseModel):
    message: str
    code: int

    class Config:
        orm_mode = True


class ResponseListModel(BaseModel):
    total: int
    page_size: int
    page_current: int
    list: Any
