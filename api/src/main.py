import os

from fastapi import FastAPI
import typing as tp
import uvicorn

from src.postgres_client import PostgresClient
from src.use_cases import UseCases
from src.schemas import (
    TopicsRequest,
    TopicsResponse,
    PublicationsRequest,
    PublicationsResponse,
    TrendsResponse,
    TrendsResponseCountInfo,
    TrendsRequest
)


app = FastAPI()
postgres_client = PostgresClient(os.getenv("DB_URL"))
use_cases = UseCases(postgres_client)


@app.on_event("startup")
async def startup_event():
    postgres_client.connect()


@app.get("/topics", response_model=tp.List[TopicsResponse])
def topics(topic_info: TopicsRequest):
    relevant_topics = use_cases.get_topics_for_role(topic_info.role_name)
    return [TopicsResponse(topic_id=topic_id, topic_name=topic_name) for topic_id, topic_name in relevant_topics]


@app.get("/publications", response_model=tp.List[PublicationsResponse])
def publications(publication_info: PublicationsRequest):
    relevant_publications = use_cases.get_publications_by_topic(publication_info.topic_id, publication_info.num)
    return [
        PublicationsResponse(title=title, url=url, text=text, publication_datetime=publication_datetime)
        for title, url, text, publication_datetime in relevant_publications
    ]


@app.get("/trend", response_model=TrendsResponse)
def trend(trend_info: TrendsRequest):
    frequencies = use_cases.get_topic_occurrence_info(trend_info.topic_id)
    return TrendsResponse(
        frequency=[TrendsResponseCountInfo(month=date, count=cnt) for date, cnt in frequencies.items()]
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
