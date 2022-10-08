from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


class PostgresClient:
    def __init__(self, conn_str):
        self.__session = None
        self.__conn_str = conn_str

    def connect(self):
        engine = create_engine(self.__conn_str)
        self.__session = sessionmaker(engine, expire_on_commit=False)

    @contextmanager
    def session(self):
        with self.__session() as session:
            try:
                yield session
                session.commit()
            except SQLAlchemyError as sql_ex:
                session.rollback()
                raise sql_ex
            finally:
                session.close()
