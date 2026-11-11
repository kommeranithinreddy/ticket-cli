from pydantic import BaseModel, Field
from typing import Literal


class Ticket(BaseModel):
    id : int = Field(gt = 0)
    title : str = Field(
        min_length = 5,
        max_length = 100
    )
    priority : Literal["High", "Medium", "Low"]
    status : Literal["Open", "In Progress", "Resolved"]
