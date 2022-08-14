import json
import uuid


def test_update_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_update_despesa", "valor": 1, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]
    response = client.put(
        f"/despesas/{despesa_id}",
        data=json.dumps(
            {
                "descricao": "test_update_despesa2",
                "valor": 100,
                "data": "2021-08-10",
                "categoria": "Alimentação",
            }
        ),
    )

    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_update_despesa2",
        "valor": 100,
        "data": "2021-08-10",
        "id": despesa_id,
        "categoria": "Alimentação",
    }
    response = client.get(f"/despesas/{despesa_id}")
    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_update_despesa2",
        "valor": 100,
        "data": "2021-08-10",
        "id": despesa_id,
        "categoria": "Alimentação",
    }


def test_update_despesa_duplicada(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_duplicada",
                "valor": 100,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_duplicada2",
                "valor": 100,
                "data": "2022-08-02",
            }
        ),
    )
    despesa_id = response.json()["id"]
    response = client.put(
        f"/despesas/{despesa_id}",
        data=json.dumps(
            {
                "descricao": "TEST_UPDATE_DESPESA_DUPLICADA",
                "valor": 10,
                "data": "2022-08-10",
            }
        ),
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Update vai gerar descrição duplicada para o mês informado."
    }


def test_update_despesa_incorrect_id(client):
    response = client.put(
        f"/despesas/{str(uuid.uuid4())}",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_incorrect_id",
                "valor": 10,
                "data": "2022-08-02",
            }
        ),
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Despesa não encontrada."}


def test_update_despesa_invalid_json(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_invalid_json",
                "valor": 10,
                "data": "2022-08-02",
            }
        ),
    )
    despesa_id = response.json()["id"]
    response = client.put(
        f"/despesas/{despesa_id}",
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
