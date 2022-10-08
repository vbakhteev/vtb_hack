import datetime
from abc import ABC, abstractmethod

import scrapy
import typing as tp

from ..items import ArticleInfo, NewsTopicEnum, NewWebsiteEnum


class BaselineSpider(scrapy.Spider, ABC):
    TAG_TO_NEWS_TOPIC = {}

    @classmethod
    @abstractmethod
    def parse(cls, response, **kwargs):
        pass

    @classmethod
    def extract_topic_form_tags(cls, tags: tp.List[str]) -> NewsTopicEnum:
        for tag in tags:
            if tag.lower() in cls.TAG_TO_NEWS_TOPIC:
                return cls.TAG_TO_NEWS_TOPIC[tag.lower()]
        return NewsTopicEnum.NOT_DEFINED

    @staticmethod
    def strip_list(data: tp.List[str]) -> tp.List[str]:
        return list(map(lambda x: x.strip(), data))

    @classmethod
    def yield_postprocess_article(
            cls, title: str, website: NewWebsiteEnum, article_url: str, img_url: str, release_time: datetime.datetime,
            tags: tp.List[str], text: tp.List[str], topic: tp.Optional[NewsTopicEnum] = None
    ):
        article_tags = cls.strip_list(tags)
        article_text_arr = cls.strip_list(text)
        if len(article_text_arr) > 0:
            article_summary = article_text_arr[0]
        else:
            article_summary = ""
        article_text = "\n\n".join(article_text_arr)
        if topic is None:
            article_topic = cls.extract_topic_form_tags(article_tags)
        else:
            article_topic = topic
        yield ArticleInfo(
            title=title.strip(),
            website=website,
            article_url=article_url.strip(),
            img_url=img_url.strip(),
            topic=article_topic,
            release_time=release_time,
            tags=article_tags,
            summary=article_summary,
            text=article_text,
        )
