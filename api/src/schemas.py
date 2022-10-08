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


class SearchRequest(BaseModel):
    query: str
    num: int = 5
    role_name: tp.Literal["manager", "accountant"] = "manager"


class SearchResponse(BaseModel):
    similar_names: tp.List[str]
    publications: tp.List[PublicationsResponse]
