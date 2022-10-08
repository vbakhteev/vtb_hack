from typing import Literal
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    user_id: int
    full_name: str
    user_type: Literal["manager", "accountant"]


class RecommendResponse(BaseModel):
    publication_id: int
    title: str
    summary: str
    url: str


class SaveEventRequest(BaseModel):
    user_id: int
    publication_id: int
    event_type: Literal["like", "dislike", "click"]
