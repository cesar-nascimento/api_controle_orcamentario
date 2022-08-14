import json
import uuid

import pytest


def test_read_all_receitas(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_read_all_receitas", "valor": 1, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]

    response = client.get("/receitas/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == receita_id, response_list))) == 1


def test_read_all_receitas_com_descricao(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_read_all_receitas_com_descricao",
                "valor": 1,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_read_all_receitas_com_descricao_diferente",
                "valor": 1,
                "data": "2022-08-02",
            }
        ),
    )
    receita_id = response.json()["id"]

    response = client.get("/receitas/?descricao=diferente")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == receita_id, response_list))) == 1


def test_read_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_read_receita", "valor": 1, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]

    response = client.get(f"/receitas/{receita_id}")
    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_read_receita",
        "valor": 1,
        "data": "2022-08-02",
        "id": receita_id,
    }


def test_read_receita_incorrect_id(client):

    response = client.get(f"/receitas/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receita não encontrada."}


def test_read_all_receitas_mes(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_read_all_receitas_mes",
                "valor": 1,
                "data": "2022-07-02",
            }
        ),
    )
    receita_id = response.json()["id"]

    response = client.get("/receitas/2022/07")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == receita_id, response_list))) == 1


@pytest.mark.parametrize(
    "ano, mes", [[0, 0], [2022, 0], [2022, 13], [9999999999999999, 1]]
)
def test_read_all_receitas_ano_mes_invalido(client, ano, mes):

    response = client.get(f"/receitas/{ano}/{mes}")
    assert response.status_code == 422

    assert response.json() == {"detail": "Data informada inválida."}
