import datetime

import scrapy

from .baseline_spider import BaselineSpider
from ..items import ArticleInfo, NewWebsiteEnum, NewsTopicEnum


class RIASpider(BaselineSpider):
    name = "ria"
    start_urls = [
        "https://ria.ru/lenta/",
    ]

    TAG_TO_NEWS_TOPIC = {
        "политика": NewsTopicEnum.POLITICS,
        "в мире": NewsTopicEnum.IN_THE_WORLD,
        "экономика": NewsTopicEnum.ECONOMICS,
        "общество": NewsTopicEnum.SOCIETY,
        "происшествия": NewsTopicEnum.EVENTS,
        "армия": NewsTopicEnum.ARMY,
        "наука": NewsTopicEnum.SCIENCE,
        "спорт": NewsTopicEnum.SPORT,
        "культура": NewsTopicEnum.CULTURE,
        "религия": NewsTopicEnum.RELIGION,
        "туризм": NewsTopicEnum.TOURISM,
    }

    @classmethod
    def parse(cls, response, **kwargs):
        all_articles = response.css("div.list-item")
        for article_info in all_articles:
            article_link = article_info.css(".list-item__title::attr(href)").get()
            yield scrapy.Request(
                article_link,
                cls.parse_article_website
            )

    @classmethod
    def parse_article_website(cls, response):
        article_space = response.css(".layout-article__main")[0]
        article_title = article_space.css(".article__title::text").extract_first()
        article_url = response.url
        article_img_url = article_space.css(".photoview__open img::attr(src)").get()
        article_release_time_str = article_space.css(".article__info-date a::text").extract_first()
        article_release_time = datetime.datetime.strptime(article_release_time_str, "%H:%M %d.%m.%Y")
        article_tags_wrapper = article_space.css(".article__tags")[0]
        article_tags = article_tags_wrapper.css(".article__tags-item::text").extract()
        article_text_arr = article_space.css(".article__text::text").extract()
        article_website = NewWebsiteEnum.RIA

        yield from cls.yield_postprocess_article(
            article_title,
            article_website,
            article_url,
            article_img_url,
            article_release_time,
            article_tags,
            article_text_arr
        )
