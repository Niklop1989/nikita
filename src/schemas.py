from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReceiptBase(BaseModel):
    id: int
    name: str
    time_to_cook: int
    description: str
    views: int


class ReceiptPostAdd(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)
