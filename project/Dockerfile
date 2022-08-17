# pull official base image
FROM python:3.10-alpine3.16 as base

# Evitar .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Envia stdout e stderr para o terminal
ENV PYTHONBUFFERED 1


FROM base as python-deps
# Build utilizada pra baixar as dependencias
# local de instalação do venv
WORKDIR /usr/src/app

# istala dependencias
RUN pip install --upgrade pip \
	&& pip install pipenv
COPY ./Pipfile ./
RUN  PIPENV_VENV_IN_PROJECT=1 pipenv install --skip-lock --dev

FROM base as runtime
# Build utilizada para o runtime
WORKDIR /home/app/web

# Copia virtual env do estágio python-deps
COPY --from=python-deps /usr/src/app/.venv /opt/venv
# Python utiliza a variável PATH para rodar dentro do venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN addgroup -S app \
	&& adduser -S app -G app \
	&& chown -R app:app /home/app/web

USER app

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/home/app/web/entrypoint.sh" ]