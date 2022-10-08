# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
from enum import Enum, auto

from pydantic import BaseModel, Field
import typing as tp

from .utils import get_current_datetime


class AutoName(str, Enum):
    def _generate_next_value_(
        self: tp.Any, start: tp.Any, count: tp.Any, last_values: tp.Any
    ) -> str:
        return str(self)


class NewWebsiteEnum(AutoName):
    RIA = auto()
    RBC = auto()
    BUH = auto()
    CONSULTANT = auto()
    HH = auto()
    MY_BUSINESS = auto()


class NewsTopicEnum(AutoName):
    NOT_DEFINED = auto()

    POLITICS = auto()
    IN_THE_WORLD = auto()
    ECONOMICS = auto()
    SOCIETY = auto()
    EVENTS = auto()
    ARMY = auto()
    SCIENCE = auto()
    SPORT = auto()
    CULTURE = auto()
    RELIGION = auto()
    TOURISM = auto()

    RBC_SOCIAL = auto()
    RBC_EDUCATION = auto()
    RBC_INDUSTRY = auto()
    RBC_INNOVATION = auto()
    RBC_GREEN = auto()
    RBC_FUTUROLOGY = auto()
    RBC_SHARING = auto()


class ArticleInfo(BaseModel):
    title: str
    website: NewWebsiteEnum
    article_url: str
    img_url: str
    topic: NewsTopicEnum = Field(default_factory=lambda: NewsTopicEnum.NOT_DEFINED)
    release_time: datetime.datetime = Field(default_factory=get_current_datetime)
    tags: tp.List[str] = Field(default_factory=list)
    summary: str = Field(default_factory=str)
    text: str = Field(default_factory=str)
    meta: dict = Field(default_factory=dict)

    def __hash__(self):
        return hash(self.json())
