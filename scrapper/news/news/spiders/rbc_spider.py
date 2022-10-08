import datetime
import os

import scrapy

from .baseline_spider import BaselineSpider
from ..items import NewWebsiteEnum, NewsTopicEnum


class RBCSpider(BaselineSpider):
    name = "rbc"
    start_urls = [
        "https://trends.rbc.ru/trends/short_news?from=newsfeed_bar",
    ]

    TAG_TO_NEWS_TOPIC = {}

    def start_requests(self):
        if os.getenv("SCRAP_FROM_TXT", None) is not None:
            with open("../rbc_data/rbc_links.txt", "r") as f:
                links = f.readlines()
            for link in links:
                link = link.strip()
                yield scrapy.Request(
                    link,
                    self.parse_article_website
                )
        else:
            for start_url in self.start_urls:
                yield scrapy.Request(
                    start_url,
                    self.parse
                )

    @classmethod
    def parse(cls, response, **kwargs):
        for article_link in response.css(".js-item-link::attr(href)").extract()[::2]:
            yield scrapy.Request(
                article_link,
                cls.parse_article_website
            )

    @classmethod
    def parse_article_website(cls, response):
        article_header = response.css(".article__header")[0]
        article_body = response.css(".article__text")[0]

        article_title = article_header.css(".article__header__title-in::text").extract_first()
        article_url = response.url

        article_img_url = article_body.css(".article__main-image img::attr(src)").get()

        article_release_time_str = article_header.css(".article__header__date::attr(datetime)").extract_first()
        if article_release_time_str is None:
            article_release_time_str = response.css(".atricle__date-update::text").extract_first().split()[1]
            article_release_time = datetime.datetime.strptime(article_release_time_str, "%d.%m.%Y")
        else:
            article_release_time = datetime.datetime.fromisoformat(article_release_time_str)

        article_tags_wrapper = response.css(".article__tags__container")
        if len(article_tags_wrapper) > 0:
            article_tags_wrapper = article_tags_wrapper[0]
            article_tags = article_tags_wrapper.css(".article__tags__item::text").extract()
        else:
            article_tags = []

        article_text_arr = article_body.css("p::text").extract()
        article_website = NewWebsiteEnum.RBC

        request_domain = article_url.split("/")[-2].upper()
        if request_domain == "CMRM":
            request_domain = "SOCIAL"
        article_topic = NewsTopicEnum("RBC_" + request_domain)

        yield from cls.yield_postprocess_article(
            article_title,
            article_website,
            article_url,
            article_img_url,
            article_release_time,
            article_tags,
            article_text_arr,
            topic=article_topic
        )
