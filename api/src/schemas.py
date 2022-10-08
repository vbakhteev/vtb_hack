import datetime
import typing as tp
from pydantic import BaseModel


class TopicsResponse(BaseModel):
    topic_id: int
    name: str


class PublicationsResponse(BaseModel):
    title: str
    url: str
    text: str
    publication_datetime: datetime.datetime


class TrendsResponseCountInfo(BaseModel):
    month: str
    count: int


class TrendsResponse(BaseModel):
    frequency: tp.List[TrendsResponseCountInfo]
