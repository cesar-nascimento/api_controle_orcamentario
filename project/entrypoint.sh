#!/bin/sh

echo "Aguardando Postgres..."

while ! nc -z web-db 5432; do
	sleep 0.1
done

echo "PostgreSQL Iniciado"

exec "$@"