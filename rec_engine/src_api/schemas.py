import datetime
import typing as tp
from pydantic import BaseModel


class PublicationsResponse(BaseModel):
    title: str
    url: str
    text: str
    publication_datetime: datetime.datetime


class SearchRequest(BaseModel):
    query: str
    num: int


class SearchResponse(BaseModel):
    similar_names: tp.List[str]
    publications: tp.List[PublicationsResponse]
