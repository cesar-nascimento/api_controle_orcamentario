# api_controle_orcamentario
Desenvolvimento de API para o desafio de back end da Alura.

Documentação: [https://api-controle-orcamentario.herokuapp.com/](https://api-controle-orcamentario.herokuapp.com/docs)

Atualmente estamos na [primeira semana](https://www.alura.com.br/challenges/back-end-4/semana-01-implementando-api-rest). Essa é a minha solução para o desafio com as [tecnologias](#tecnologias-utilizadas) que escolhi para criar a API.

## Índice
* [Sobre o desafio](#sobre-o-desafio)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Setup](#setup)
* [Documentação](#documentacao)

## Sobre o desafio
Após alguns testes com protótipos feitos pelo time de UX de uma empresa, foi requisitada a primeira versão de uma aplicação para controle de orçamento familiar. A aplicação deve permitir que uma pessoa cadastre suas receitas e despesas do mês, bem como gerar um relatório mensal.
	
## Tecnologias utilizadas
* Python 3.10
* Docker
* FastAPI
* PostgreSQL

## Setup
Para rodar a aplicação recomendo utilizar o Docker e instalar o Docker Composer. [Instalação do Docker.](https://docs.docker.com/get-docker/)

Depois de instalado, rode um dos seguintes comandos:

* Para rodar a aplicação e manter o terminal aberto com os outputs do log: `docker-compose up --build`
  * Para encerrar aperte `ctrl-c`

* Para rodar a aplicação no background: `docker-compose up -d --build`
  * Para encerrar use o comando: `docker-compose down`

* Em um navegador vá até a url `http://localhost:8000/healthcheck` ou `http://localhost:8000/docs` para verificar a aplicação funcionando.

## Documentação
A documentação pode ser encontrada em [https://api-controle-orcamentario.herokuapp.com/](https://api-controle-orcamentario.herokuapp.com/)
