import datetime
import typing as tp
from pydantic import BaseModel


class TopicsRequest(BaseModel):
    role_name: tp.Literal["manager", "accountant"]


class TopicsResponse(BaseModel):
    topic_id: int
    topic_name: str


class PublicationsRequest(BaseModel):
    topic_id: int
    num: int = 5


class PublicationsResponse(BaseModel):
    title: str
    url: str
    text: str
    publication_datetime: datetime.datetime


class TrendsRequest(BaseModel):
    topic_id: int


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
