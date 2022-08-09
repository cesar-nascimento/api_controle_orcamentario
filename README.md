# api_controle_orcamentario
Desenvolvimento de API para o desafio de back end da Alura.

Documentação: [https://api-controle-orcamentario.herokuapp.com/redoc](https://api-controle-orcamentario.herokuapp.com/redoc)

Atualmente estamos na [primeira semana](https://www.alura.com.br/challenges/back-end-4/semana-01-implementando-api-rest). Essa é a minha solução para o desafio com as [tecnologias](#tecnologias-utilizadas) que escolhi para criar a API.

## Índice
* [Sobre o desafio](#sobre-o-desafio)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Setup](#setup)
* [Documentação](#documentação)

## Sobre o desafio
Após alguns testes com protótipos feitos pelo time de UX de uma empresa, foi requisitada a primeira versão de uma aplicação para controle de orçamento familiar. A aplicação deve permitir que uma pessoa cadastre suas receitas e despesas do mês, bem como gerar um relatório mensal.
	
## Tecnologias utilizadas
* Python 3.10
* Docker
* FastAPI
* PostgreSQL

## Setup
1. Para rodar a aplicação recomendo utilizar o Docker e instalar o Docker Composer. [Instalação do Docker.](https://docs.docker.com/get-docker/)

2. Depois de instalado, siga um dos seguintes passos:

	2.1. Rodando através da imagem disponível no Docker Hub:

		2.1.1. `docker pull cesar0nascimento/api-controle-orcamentario:latest`
	
		2.1.2. `docker run --name api_controle_orcamentario -e PORT=8000 -e DATABASE_URL=sqlite://sqlite.db -p 8000:8000 cesar0nascimento/api-controle-orcamentario:latest`

	2.2. Rodando a aplicação através de imagem local:
		
		2.2.1. `git clone https://github.com/cesar-nascimento/api_controle_orcamentario.git`
		
		2.2.2. `docker-compose up --build`

3. Navegue até a url `http://localhost:8000/healthcheck` ou `http://localhost:8000/docs` para verificar a aplicação funcionando e testar requisições.

4. Informações sobre as rotas disponíveis e o formato das requisições podem ser verificados na [Documentação](#documentação)

## Documentação
A documentação pode ser encontrada em [https://api-controle-orcamentario.herokuapp.com/redoc](https://api-controle-orcamentario.herokuapp.com/redoc)
