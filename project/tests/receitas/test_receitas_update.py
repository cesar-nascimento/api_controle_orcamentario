import json
import uuid


def test_update_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_update_receita", "valor": 1, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]
    response = client.put(
        f"/receitas/{receita_id}",
        data=json.dumps(
            {"descricao": "test_update_receita2", "valor": 100, "data": "2021-08-10"}
        ),
    )
    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_update_receita2",
        "valor": 100,
        "data": "2021-08-10",
        "id": receita_id,
    }
    response = client.get(f"/receitas/{receita_id}")
    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_update_receita2",
        "valor": 100,
        "data": "2021-08-10",
        "id": receita_id,
    }


def test_update_receita_duplicada(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_update_receita_duplicada",
                "valor": 100,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_update_receita_duplicada2",
                "valor": 100,
                "data": "2022-08-02",
            }
        ),
    )
    receita_id = response.json()["id"]
    response = client.put(
        f"/receitas/{receita_id}",
        data=json.dumps(
            {
                "descricao": "TEST_UPDATE_RECEITA_DUPLICADA",
                "valor": 10,
                "data": "2022-08-10",
            }
        ),
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Update vai gerar descrição duplicada para o mês informado."
    }


def test_update_receita_incorrect_id(client):
    response = client.put(
        f"/receitas/{str(uuid.uuid4())}",
        data=json.dumps(
            {
                "descricao": "test_update_receita_incorrect_id",
                "valor": 10,
                "data": "2022-08-02",
            }
        ),
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Receita não encontrada."}


def test_update_receita_invalid_json(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_update_receita_invalid_json",
                "valor": 10,
                "data": "2022-08-02",
            }
        ),
    )
    receita_id = response.json()["id"]
    response = client.put(
        f"/receitas/{receita_id}",
        data=json.dumps({}),
    )
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "descricao"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "valor"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "data"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }
