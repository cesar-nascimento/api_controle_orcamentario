import json


def test_create_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_create_despesa", "valor": 0, "data": "2022-08-02"}
        ),
    )

    assert response.status_code == 201
    assert response.json()["descricao"] == "test_create_despesa"
    assert response.json()["valor"] == 0
    assert response.json()["data"] == "2022-08-02"


def test_create_despesa_invalid_json(client):
    response = client.post("/despesas/", data=json.dumps({}))

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


def test_create_despesa_duplicated(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_create_despesa_duplicated",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "TEST_CREATE_DESPESA_DUPLICATED",
                "valor": 0,
                "data": "2022-08-10",
            }
        ),
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Descrição duplicada para o mês informado."}


def test_read_all_despesas(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_read_all_despesas", "valor": 0, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]

    response = client.get("/despesas/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == despesa_id, response_list))) == 1


def test_read_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_read_despesa", "valor": 0, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]

    response = client.get(f"/despesas/{despesa_id}")
    assert response.status_code == 200
    assert response.json()["descricao"] == "test_read_despesa"
    assert response.json()["valor"] == 0
    assert response.json()["data"] == "2022-08-02"


def test_read_despesa_incorrect_id(client):

    response = client.get("/despesas/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Despesa não encontrada."}


def test_update_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_update_despesa", "valor": 0, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]
    response = client.put(
        f"/despesas/{despesa_id}",
        data=json.dumps(
            {"descricao": "test_update_despesa2", "valor": 100, "data": "2021-08-02"}
        ),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert despesa_id == response_dict["id"]
    assert response_dict["descricao"] == "test_update_despesa2"
    assert response_dict["valor"] == 100
    assert response_dict["data"] == "2021-08-02"


def test_update_despesa_duplicada(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_duplicada",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_duplicada2",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    despesa_id = response.json()["id"]
    response = client.put(
        f"/despesas/{despesa_id}",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_duplicada",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Update vai gerar descrição duplicada para o mês informado."
    }


def test_update_despesa_incorrect_id(client):
    response = client.put(
        "/despesas/999",
        data=json.dumps(
            {
                "descricao": "test_update_despesa_incorrect_id",
                "valor": 0,
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
                "valor": 0,
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


def test_delete_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_delete_despesa", "valor": 0, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]
    response = client.delete(f"/despesas/{despesa_id}")

    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_delete_despesa",
        "valor": 0,
        "data": "2022-08-02",
        "id": despesa_id,
    }


def test_delete_despesa_incorrect_id(client):
    response = client.delete("/despesas/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Despesa não encontrada."}
