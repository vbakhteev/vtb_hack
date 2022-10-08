import datetime
import sys
import os
import typing as tp

from sqlalchemy import func

from news.items import ArticleInfo

sys.path.insert(1, "../../api/")

from src.postgres_client import PostgresClient
from src.models import Publication, PublicationSource, TopicInfo


def read_jsonlines_file(filename: str) -> tp.List[ArticleInfo]:
    data = []
    with open(filename) as f:
        for line in f:
            data.append(ArticleInfo.parse_raw(line))
    data = sorted(list(set(data)), key=lambda x: x.release_time)
    return data


def insert_deafult_topic_info_if_not_present(db: PostgresClient) -> None:
    with db.session() as session:
        is_present = session.query(TopicInfo).get(-2)
        if is_present is None:
            session.add(TopicInfo(id=-2, topic_name="not labeled"))


def get_first_datetime_for_source(db: PostgresClient) -> tp.Dict[PublicationSource, datetime.datetime]:
    source_to_first_datetime = {}
    with db.session() as session:
        for cur_source in PublicationSource:
            first_datetime = session.query(func.min(Publication.publication_datetime)).filter(Publication.source == cur_source).first()[0]
            if first_datetime is None:
                first_datetime = datetime.datetime.max
            source_to_first_datetime[cur_source] = first_datetime
    return source_to_first_datetime


def get_last_datetime_for_source(db: PostgresClient) -> tp.Dict[PublicationSource, datetime.datetime]:
    source_to_last_datetime = {}
    with db.session() as session:
        for cur_source in PublicationSource:
            last_datetime = session.query(func.max(Publication.publication_datetime)).filter(Publication.source == cur_source).first()[0]
            if last_datetime is None:
                last_datetime = datetime.datetime.min
            source_to_last_datetime[cur_source] = last_datetime
    return source_to_last_datetime


def dump_data_to_db(db: PostgresClient, data: tp.List[ArticleInfo]) -> None:
    for cur_sample in data:
        publication = Publication(
            title=cur_sample.title,
            summary=cur_sample.summary,
            text=cur_sample.text,
            publication_datetime=cur_sample.release_time,
            url=cur_sample.article_url,
            image_url=cur_sample.img_url,
            source=PublicationSource(cur_sample.website),
            tags=cur_sample.tags
        )
        with db.session() as session:
            session.add(publication)


if __name__ == "__main__":
    postgres_client = PostgresClient(os.getenv("DB_URL"))
    postgres_client.connect()
    insert_deafult_topic_info_if_not_present(postgres_client)
    source_to_first_datetime = get_first_datetime_for_source(postgres_client)
    source_to_last_datetime = get_last_datetime_for_source(postgres_client)
    for cur_source in PublicationSource:
        assert isinstance(cur_source, PublicationSource)
        filename = f"../../data/{cur_source.value.lower()}_items.jsonl"
        cur_first_datetime = source_to_first_datetime[cur_source]
        cur_last_datetime = source_to_last_datetime[cur_source]
        if os.path.exists(filename):
            samples = read_jsonlines_file(filename)
            samples = [
                sample for sample in samples
                if sample.release_time > cur_last_datetime or cur_first_datetime > sample.release_time
            ]
            dump_data_to_db(postgres_client, samples)