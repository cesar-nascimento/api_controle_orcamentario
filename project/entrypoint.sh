#!/bin/sh

echo "Aguardando Postgres..."

while ! nc -z web-db 5432; do
	sleep 0.1
done

echo "PostgreSQL Iniciado"

aerich init -t app.db.TORTOISE_ORM
aerich init-db

exec "$@"