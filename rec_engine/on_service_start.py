import os
import sys

import typing as tp

from model import NewsTMModel
from utils import DataLoader

sys.path.insert(1, "../api/")

from src.postgres_client import PostgresClient
from src.models import TopicInfo, Publication


class NewsTopicAssessor:
    def __init__(self, businessman_model_path, accounter_model_path):
        self.businessman_model = NewsTMModel()
        self.businessman_model.load(businessman_model_path)
        self.accounter_model = NewsTMModel()
        self.accounter_model.load(accounter_model_path)
        data = DataLoader().get_data_with_unnassigned_topics()
        self.business_news = data[data["source"].isin(["RBC"])]
        self.accounter_news = data[data["source"].isin(["BUH", "CONSULTANT"])]

    def get_topic_labels_for_businessman(self):
        return self.businessman_model.topic_model.generate_topic_labels()

    def get_topic_labels_for_accounter(self):
        return self.accounter_model.topic_model.generate_topic_labels()

    def label_business_news(self):
        if len(self.business_news) == 0:
            return None
        topics, probs = self.businessman_model.predict(self.business_news)
        self.business_news['topic_id'] = topics
        return self.business_news

    def label_accounter_news(self):
        if len(self.accounter_news) == 0:
            return None
        topics, probs = self.accounter_model.predict(self.accounter_news)
        self.accounter_news['topic_id'] = topics
        return self.accounter_news


def build_topic_info(news_topic_assessor: NewsTopicAssessor):
    topic_info = []
    for i, topics_by_person_type in enumerate(
            [
                news_topic_assessor.get_topic_labels_for_businessman(),
                news_topic_assessor.get_topic_labels_for_accounter()
            ],
    ):
        for topic in topics_by_person_type:
            offset = i * 50
            num = int(topic.split("_")[0])
            if num != -1:
                num += offset
            topic_info.append((num, topic, i))
    return topic_info


def insert_topic_info_to_db(db: PostgresClient, topic_info: tp.List[tp.Tuple[int, str, int]]) -> None:
    with db.session() as session:
        for topic_id, topic_name, person_type in topic_info:
            for_businessman = False
            for_accountant = False

            if topic_id == -1:
                topic_name = "not relevant"
            else:
                if person_type == 0:
                    for_businessman = True
                elif person_type == 1:
                    for_accountant = True
                else:
                    raise RuntimeError()
            topic_row = session.query(TopicInfo).get(topic_id)
            if topic_row is None:
                session.add(TopicInfo(
                    id=topic_id,
                    topic_name=topic_name,
                    for_businessman=for_businessman,
                    for_accountant=for_accountant)
                )


def set_topic_id_to_document(db: PostgresClient, doc_id: int, topic_id: int) -> None:
    with db.session() as session:
        session.query(Publication).filter(Publication.id == doc_id).update({"topic_id": topic_id})


if __name__ == '__main__':
    news_topic_assessor = NewsTopicAssessor("weights/rbc_tm", "weights/buh_tm")

    postgres_client = PostgresClient(os.getenv("DB_URL"))
    postgres_client.connect()
    topic_info = build_topic_info(news_topic_assessor)
    insert_topic_info_to_db(postgres_client, topic_info)

    business_news = news_topic_assessor.label_business_news()
    accountant_news = news_topic_assessor.label_accounter_news()
    if accountant_news is not None:
        accountant_news["topic_id"] = accountant_news["topic_id"].apply(lambda x: x + 50 if x > -1 else -1)
    for df in [business_news, accountant_news]:
        if df is None:
            continue
        for _, row in df.iterrows():
            doc_id = row["id"]
            topic_id = row["topic_id"]
            set_topic_id_to_document(postgres_client, doc_id, topic_id)
