import os

from fastapi import FastAPI
import uvicorn

from src_api.postgres_client import PostgresClient
from src_api.schemas import (
    PublicationsResponse,
    SearchRequest,
    SearchResponse,
)


app = FastAPI()
postgres_client = PostgresClient(os.getenv("DB_URL"))
use_cases = UseCases(postgres_client)


@app.get("/search", response_model=SearchResponse)
def search(search_info: SearchRequest):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
