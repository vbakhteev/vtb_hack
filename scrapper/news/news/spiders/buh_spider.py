import datetime
import os

import scrapy

from .baseline_spider import BaselineSpider
from ..items import NewWebsiteEnum


class BUHSpider(BaselineSpider):
    name = "buh"
    start_urls = [
        "https://buh.ru/news/uchet_nalogi/",
    ]

    TEMPLATE_URL = "https://buh.ru/news/uchet_nalogi/?PAGEN_1={}"

    TAG_TO_NEWS_TOPIC = {}

    @classmethod
    def parse(cls, response, i=1):
        all_articles = response.css(".article")
        for article_info in all_articles:
            article_link = "https://buh.ru" + article_info.css("a::attr(href)").get()
            yield scrapy.Request(
                article_link,
                cls.parse_article_website
            )
        i += 1
        if os.getenv("SCRAP_ALL_DATA", None) is not None:
            yield scrapy.Request(
                cls.TEMPLATE_URL.format(i),
                cls.parse,
                cb_kwargs={"i": i}
            )

    @classmethod
    def parse_article_website(cls, response):
        meta_types = response.css(".content_page meta::attr(itemprop)").extract()
        meta_contents = response.css(".content_page meta::attr(content)").extract()
        meta_info = {meta_type: meta_content for meta_type, meta_content in zip(meta_types, meta_contents)}

        article_title = response.css(".margin_line-height::text").get()
        article_url = response.url
        article_img_url = meta_info.get("image", "")
        article_release_time_str = meta_info["datePublished"]
        article_release_time = datetime.datetime.strptime(article_release_time_str, "%Y-%m-%dT%H:%M:%S%z")
        rubrics = response.css(".rubric")

        article_tags = []
        article_tags.extend(rubrics[0].css("a::text").extract())
        article_tags.extend(rubrics[1].css("a::attr(title)").extract())

        article_text_arr = response.css(".tip-news p::text").extract()[:-1]
        article_website = NewWebsiteEnum.BUH

        yield from cls.yield_postprocess_article(
            article_title,
            article_website,
            article_url,
            article_img_url,
            article_release_time,
            article_tags,
            article_text_arr,
        )
