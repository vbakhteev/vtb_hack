import os

import typing as tp

from src.postgres_client import PostgresClient
from src.models import Publication, TopicInfo

POSTGRES_CLIENT = None


def dump_topic_to_db(info: tp.List[int, int, str]) -> None:
    for doc_id, topic_id, topic_name in info:
        dump_topic_to_db_one_row(doc_id, topic_id, topic_name)


def dump_topic_to_db_one_row(doc_id: int, topic_id: int, topic_name: str) -> None:
    global POSTGRES_CLIENT
    if POSTGRES_CLIENT is None:
        POSTGRES_CLIENT = PostgresClient(os.getenv("DB_URL"))
        POSTGRES_CLIENT.connect()
    with POSTGRES_CLIENT.session() as session:
        topic_row = session.query(TopicInfo).get(topic_id)
        if topic_row is None:
            session.add(TopicInfo(id=topic_id, topic_name=topic_name))
        elif topic_row.topic_name != topic_name:
            session.query(TopicInfo).filter(TopicInfo.id == topic_id).update({"topic_name": "no relevant"})
        session.query(Publication).filter(Publication.id == doc_id).update({"topic_id": topic_id})
