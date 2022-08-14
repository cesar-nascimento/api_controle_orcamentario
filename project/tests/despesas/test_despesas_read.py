import json
import uuid

import pytest


def test_read_all_despesas(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_read_all_despesas", "valor": 1, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]

    response = client.get("/despesas/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == despesa_id, response_list))) == 1


def test_read_all_despesas_com_descricao(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_read_all_despesas_com_descricao",
                "valor": 1,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_read_all_despesas_com_descricao_diferente",
                "valor": 1,
                "data": "2022-08-02",
            }
        ),
    )
    despesa_id = response.json()["id"]

    response = client.get("/despesas/?descricao=diferente")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == despesa_id, response_list))) == 1


def test_read_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_read_despesa", "valor": 1, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]

    response = client.get(f"/despesas/{despesa_id}")
    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_read_despesa",
        "valor": 1,
        "data": "2022-08-02",
        "id": despesa_id,
        "categoria": "Outras",
    }


def test_read_despesa_incorrect_id(client):

    response = client.get(f"/despesas/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Despesa não encontrada."}


def test_read_all_despesas_mes(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_read_all_despesas_mes",
                "valor": 1,
                "data": "2022-07-02",
            }
        ),
    )
    despesa_id = response.json()["id"]

    response = client.get("/despesas/2022/07")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == despesa_id, response_list))) == 1


@pytest.mark.parametrize(
    "ano, mes", [[0, 0], [2022, 0], [2022, 13], [9999999999999999, 1]]
)
def test_read_all_despesas_ano_mes_invalido(client, ano, mes):

    response = client.get(f"/despesas/{ano}/{mes}")
    assert response.status_code == 422

    assert response.json() == {"detail": "Data informada inválida."}
