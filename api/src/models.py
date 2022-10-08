import enum

import sqlalchemy as sqla
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from src.utils import todict


class Enum(str, enum.Enum):
    pass


class Base:
    def __repr__(self):
        params = ', '.join(f'{k}={v}' for k, v in todict(self).items())
        return f"{self.__class__.__name__}({params})"


Base = declarative_base(cls=Base)


class UserType(Enum):
    manager = "manager"
    accountant = "accountant"


class User(Base):
    __tablename__ = 'users'

    id = sqla.Column(sqla.BigInteger, primary_key=True, index=True)  # from Telegram
    fullname = sqla.Column(sqla.String)
    registration_datetime = sqla.Column(sqla.DateTime, server_default=func.now())
    user_type = sqla.Column(sqla.Enum(UserType))

    features = sqla.Column(sqla.JSON)


class PublicationSource(Enum):
    times = "times"
    RIA = "RIA"
    RBC = "RBC"
    BUH = "BUH"
    CONSULTANT = "CONSULTANT"


def default_as_topic_name(context):
    return context.current_parameters.get('topic_name')


class TopicInfo(Base):
    __tablename__ = "topic_info"

    id = sqla.Column(sqla.Integer, primary_key=True, index=True)

    topic_name = sqla.Column(sqla.String)
    for_accountant = sqla.Column(sqla.Boolean, default=False)
    for_businessman = sqla.Column(sqla.Boolean, default=False)

    topic_name_display = sqla.Column(sqla.String, default=default_as_topic_name)


class Publication(Base):
    __tablename__ = 'publications'

    id = sqla.Column(sqla.BigInteger, primary_key=True, index=True)

    title = sqla.Column(sqla.String)
    summary = sqla.Column(sqla.String)
    text = sqla.Column(sqla.String)

    publication_datetime = sqla.Column(sqla.DateTime)
    scrape_datetime = sqla.Column(sqla.DateTime, server_default=func.now())
    url = sqla.Column(sqla.String)
    image_url = sqla.Column(sqla.String, default=None)
    source = sqla.Column(sqla.Enum(PublicationSource))

    topic_id = sqla.Column(sqla.Integer, sqla.ForeignKey("topic_info.id"), default=-2)
    is_duplicate = sqla.Column(sqla.Boolean, default=None)
    tags = sqla.Column(sqla.ARRAY(sqla.String))
    features = sqla.Column(sqla.JSON)


class History(Base):
    __tablename__ = 'history'

    id = sqla.Column(sqla.BigInteger, primary_key=True)
    user_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey(User.id))
    publication_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey(Publication.id))

    show_datetime = sqla.Column(sqla.DateTime, server_default=func.now())


class EventType(Enum):
    like = "like"
    dislike = "dislike"
    click = "click"


class Event(Base):
    __tablename__ = 'events'

    id = sqla.Column(sqla.BigInteger, primary_key=True)
    user_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey(User.id))
    publication_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey(Publication.id))

    event_type = sqla.Column(sqla.Enum(EventType))
    event_datetime = sqla.Column(sqla.DateTime, server_default=func.now())
