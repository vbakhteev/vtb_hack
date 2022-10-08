import os

from fastapi import FastAPI
import typing as tp
import uvicorn

from src.postgres_client import PostgresClient
from src.use_cases import UseCases
from src.schemas import (
    TopicsResponse,
    PublicationsResponse,
    TrendsResponse,
    TrendsResponseCountInfo,
)


app = FastAPI()
postgres_client = PostgresClient(os.getenv("DB_URL"))
use_cases = UseCases(postgres_client)


@app.on_event("startup")
async def startup_event():
    postgres_client.connect()


@app.get("/topics", response_model=tp.List[TopicsResponse])
def topics(role_name: tp.Literal["manager", "accountant"]):
    relevant_topics = use_cases.get_topics_for_role(role_name)
    return [TopicsResponse(topic_id=topic_id, topic_name=topic_name) for topic_id, topic_name in relevant_topics]


@app.get("/publications", response_model=tp.List[PublicationsResponse])
def publications(topic_id: int, num: int):
    relevant_publications = use_cases.get_publications_by_topic(topic_id, num)
    return [
        PublicationsResponse(title=title, url=url, text=text, publication_datetime=publication_datetime)
        for title, url, text, publication_datetime in relevant_publications
    ]


@app.get("/trend", response_model=TrendsResponse)
def trend(topic_id: int):
    frequencies = use_cases.get_topic_occurrence_info(topic_id)
    return TrendsResponse(
        frequency=[TrendsResponseCountInfo(month=date, count=cnt) for date, cnt in frequencies.items()]
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
