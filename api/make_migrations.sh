#!/bin/bash

if [ "$GENERATE_MIGRATIONS" = "true" ]
then
  echo "Generating migrations files..."
  alembic upgrade head
  alembic revision --autogenerate
fi

echo "Applying migrations..."
alembic upgrade head

echo "Migrations done!"
