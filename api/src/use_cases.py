from collections import Counter
import datetime
import typing as tp

from sqlalchemy.future import select

from src.postgres_client import PostgresClient
from src.models import (
    User,
    UserType,
    Publication,
    TopicInfo,
    EventType,
    Event,
)


class UseCases:
    def __init__(self, postgres_client: PostgresClient):
        self.db: PostgresClient = postgres_client

    def register_or_update_role(self, user_id: int, full_name: str, user_type: str):
        with self.db.session() as session:
            user_type = UserType(user_type)

            q = select(User).where(User.id == user_id).limit(1)
            user: User = (list(session.execute(q)) or [None])[0]
            is_registered = user is not None

            if is_registered:
                print(user)
                user[0].user_type = user_type        
            else:
                item = User(
                    id=user_id,
                    fullname=full_name,
                )
                session.add(item)


    def recommend(self, user_id: int):

        publication_id=1337
        title="Заголовок интересной новости"
        summary="Описание интересной новости"
        url="https://aussiedlerbote.de/2022/09/oktoberfest-2022-festival-oficialno-nachalsya/"

        return publication_id, title, summary, url

    def publication_url(self, publication_id: int) -> str:
        return "https://github.com/"

    def save_event(self, user_id: int, publication_id: int, event_type: str):
        with self.db.session() as session:
            event = Event(
                user_id=user_id,
                publication_id=publication_id,
                event_type=EventType(event_type),
            )
            session.add(event)

    def get_topics_for_role(self, role: tp.Literal["manager", "accountant"]) -> tp.List[tp.Tuple[int, str]]:
        with self.db.session() as session:
            ans = []
            if role == "manager":
                for row in session.query(TopicInfo).filter(TopicInfo.for_businessman):
                    ans.append((row.id, row.topic_name))
            elif role == "accountant":
                for row in session.query(TopicInfo).filter(TopicInfo.for_accountant):
                    ans.append((row.id, row.topic_name))
            else:
                raise RuntimeError("Incorrect role porvided")
        return ans

    def get_publications_by_topic(self, topic_id: int, num: int) -> tp.List[tp.Tuple[str, str, str, datetime.datetime]]:
        ans = []
        with self.db.session() as session:
            for row in session.query(Publication).filter(
                    Publication.topic_id == topic_id
            ).order_by(Publication.publication_datetime.desc()).limit(num):
                ans.append((row.title, row.url, row.text, row.publication_datetime))
        return ans

    def get_topic_occurrence_info(self, topic_id: int) -> tp.Dict[str, int]:
        with self.db.session() as session:
            data = []
            for row in session.query(Publication).filter(Publication.topic_id == topic_id):
                data.append("{:04d}-{:02d}".format(row.publication_datetime.year, row.publication_datetime.month))
        return Counter(data)

    def get_topic_by_name(self, topic_name: str) -> tp.Optional[int]:
        with self.db.session() as session:
            cur_rows = session.query(TopicInfo).filter(TopicInfo.topic_name == topic_name).all()
            if len(cur_rows) == 0:
                return None
            return cur_rows[0].id
