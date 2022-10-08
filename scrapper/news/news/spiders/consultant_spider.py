import datetime
import os

import scrapy

from .baseline_spider import BaselineSpider
from ..items import NewWebsiteEnum


class ConsultantSpider(BaselineSpider):
    name = "consultant"

    TEMPLATE_URL = "http://www.consultant.ru/legalnews/?page={}"

    TAG_TO_NEWS_TOPIC = {}

    MONTH_TO_NUMBER = {
        "янв": 1,
        "февр": 2,
        "мар": 3,
        "апр": 4,
        "мая": 5,
        "май": 5,
        "июн": 6,
        "июл": 7,
        "авг": 8,
        "сент": 9,
        "окт": 10,
        "ноя": 11,
        "дек": 12,
    }

    ACCOUNTANT_FILTER_COOKIE = "rlWyozSvoTIxH2AipTImVwc7VwNvBvWuL2AiqJ50LJ50VvjvZFV6VzW1MTqyqPW9YPWwo2kfLKOmMJEGL29jMKZvBag9sD"

    def start_requests(self):
        yield scrapy.Request(
            self.TEMPLATE_URL.format(1),
            self.parse,
            cookies={
                "_settings": self.ACCOUNTANT_FILTER_COOKIE
            }
        )

    @classmethod
    def parse(cls, response, i=1):
        all_articles = response.css(".listing-news__item-title::attr(href)").extract()
        for article_sublink in all_articles:
            article_link = "http://www.consultant.ru" + article_sublink
            yield scrapy.Request(
                article_link,
                cls.parse_article_website
            )
        i += 1
        if os.getenv("SCRAP_ALL_DATA", None) is not None:
            yield scrapy.Request(
                cls.TEMPLATE_URL.format(i),
                cls.parse,
                cookies={
                    "_settings": cls.ACCOUNTANT_FILTER_COOKIE
                },
                cb_kwargs={"i": i},
            )

    @classmethod
    def parse_article_website(cls, response):
        article_title = response.css(".news-page__title::text").get()
        article_url = response.url

        article_body = response.css(".news-page")
        article_img_url = article_body.css("img::attr(src)").get()
        if article_img_url is None:
            article_img_url = ""
        article_release_time_str = article_body.css(".news-page__date::text").get()
        article_release_time = cls.extract_date(article_release_time_str)

        article_tags = article_body.css(".tags-news__text::text").extract()

        article_text_arr = article_body.css(".news-page__text p::text").extract()
        article_website = NewWebsiteEnum.CONSULTANT

        yield from cls.yield_postprocess_article(
            article_title,
            article_website,
            article_url,
            article_img_url,
            article_release_time,
            article_tags,
            article_text_arr,
        )

    @classmethod
    def extract_date(cls, date_str: str) -> datetime.datetime:
        day, month, year = date_str.split()
        month_num = 1
        for month_name, cur_month_num in cls.MONTH_TO_NUMBER.items():
            if month.lower().startswith(month_name):
                month_num = cur_month_num
                break
        return datetime.datetime(int(year), month_num, int(day))
