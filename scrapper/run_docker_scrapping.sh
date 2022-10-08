docker run --mount type=bind,source="$(pwd)"/../data,target=/data --net=host --env DB_URL=postgresql://user:password123@localhost:5432/postgresdb scrapers
