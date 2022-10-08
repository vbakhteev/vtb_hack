from sqlalchemy import create_engine
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()


class DataLoader:

    def __init__(self):
        connection_string = os.getenv('DB_URL')
        alchemyEngine = create_engine(connection_string, pool_recycle=3600)
        self.dbConnection = alchemyEngine.connect()

    def get_publications_over_period_by(self, sources: tuple, date_start, date_end):
        if len(sources) > 1:
            data = pd.read_sql(f"""
            select id, title, summary, text, publication_datetime, url  
            from publications
            where source in {sources}
                  and publication_datetime >= '{date_start}' and publication_datetime < '{date_end}'
            """, self.dbConnection)
        else:
            data = pd.read_sql(f"""
                        select id, title, summary, text, publication_datetime, url  
                        from publications
                        where source='{sources[0]}'
                              and publication_datetime >= '{date_start}' and publication_datetime < '{date_end}'
                        """, self.dbConnection)
        return data


if __name__ == '__main__':
    data_loader = DataLoader()
    print(data_loader.get_publications_over_period_by(sources=('RBC',),
                                                      date_start='2019-01-01',
                                                      date_end='2022-10-10'
                                                      ))
