import os

import uvicorn
from fastapi import FastAPI, HTTPException

from src.postgres_client import PostgresClient
from src.use_cases import UseCases
from src.schemas import (
    RegisterRequest,
    SaveEventRequest,
    RecommendResponse,
)


app = FastAPI()
postgres_client = PostgresClient(os.getenv("DB_URL"))
use_cases = UseCases(postgres_client)


@app.on_event("startup")
async def startup_event():
    postgres_client.connect()


@app.get("/recommend", response_model=RecommendResponse)
def recommend(user_id: int):
    publication_id, title, summary, url = use_cases.recommend(
        user_id=user_id,
    )
    return RecommendResponse(
        publication_id=publication_id,
        title=title,
        summary=summary,
        url=url,
    )


@app.get("/publication_url")
def publication_url(publication_id: int):
    url = use_cases.publication_url(
        publication_id=publication_id,
    )
    return url


@app.post("/register")
def register(request: RegisterRequest):
    use_cases.register_or_update_role(
        user_id=request.user_id,
        full_name=request.full_name,
        user_type=request.user_type,
    )
    return "OK"


@app.post("/save_event")
def save_event(request: SaveEventRequest):
    use_cases.save_event(
        user_id=request.user_id,
        publication_id=request.publication_id,
        event_type=request.event_type,
    )
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
