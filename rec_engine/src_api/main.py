import os

from fastapi import FastAPI
import typing as tp
import uvicorn

from src.postgres_client import PostgresClient
from src.schemas import (
    PublicationsResponse,
    SearchRequest,
    SearchResponse,
)
from src.use_cases import UseCases
from model import NewsTMModel


app = FastAPI()
postgres_client = PostgresClient(os.getenv("DB_URL"))
use_cases = UseCases(postgres_client)
businessman_model: tp.Optional[NewsTMModel] = None
accounter_model: tp.Optional[NewsTMModel] = None


@app.on_event("startup")
async def startup_event():
    postgres_client.connect()
    global businessman_model
    global accounter_model
    businessman_model = NewsTMModel()
    businessman_model.load("weights/rbc_tm")
    accounter_model = NewsTMModel()
    accounter_model.load("weights/buh_tm")


@app.get("/search", response_model=SearchResponse)
def search(query: str, num: int, role_name: tp.Literal["manager", "accountant"]):
    if role_name == "manager":
        news_model = businessman_model
    elif role_name == "accountant":
        news_model = accounter_model
    else:
        raise RuntimeError()
    assert news_model is not None
    assert num > 0
    _, topic_names = news_model.find_topics(query)
    topic_id = use_cases.get_topic_by_name(topic_names[0])
    relevant_publications = use_cases.get_publications_by_topic(topic_id, num)
    return SearchResponse(
        similar_names=topic_names,
        publications=[
            PublicationsResponse(title=title, url=url, text=text, publication_datetime=publication_datetime)
            for title, url, text, publication_datetime in relevant_publications
        ],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
