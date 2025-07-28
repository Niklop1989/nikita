from typing import Optional

from pydantic import BaseModel


class ReceiptBase(BaseModel):
    id: int
    name: str
    time_to_cook: int
    description: str
    views: int


class ReceiptPostAdd(ReceiptBase):

    class Config:
        orm_mode = True

