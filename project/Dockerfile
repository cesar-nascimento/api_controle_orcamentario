FROM python:3.10-alpine3.16

WORKDIR /usr/src/app

# Evitar .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Envia stdout e stderr para o terminal
ENV PYTHONBUFFERED 1

# copia app e instala dependencias do python
COPY ./Pipfile ./
RUN pip install --upgrade pip \
	&& pip install pipenv \
	&& pipenv install --system --skip-lock

COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]