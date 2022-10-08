from sqlalchemy.future import select

from src.postgres_client import PostgresClient
from src.models import (
    User,
    UserType,
    Publication,
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
