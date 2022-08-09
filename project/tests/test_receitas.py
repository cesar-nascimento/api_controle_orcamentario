import json


def test_create_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_create_receita", "valor": 0, "data": "2022-08-02"}
        ),
    )

    assert response.status_code == 201
    assert response.json()["descricao"] == "test_create_receita"
    assert response.json()["valor"] == 0
    assert response.json()["data"] == "2022-08-02"


def test_create_receita_invalid_json(client):
    response = client.post("/receitas/", data=json.dumps({}))

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


def test_create_receita_duplicated(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_create_receita_duplicated",
                "valor": 0,
                "data": "2022-08-01",
            }
        ),
    )
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "TEST_CREATE_RECEITA_DUPLICATED",
                "valor": 0,
                "data": "2022-08-10",
            }
        ),
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Descrição duplicada para o mês informado."}


def test_read_all_receitas(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_read_all_receitas", "valor": 0, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]

    response = client.get("/receitas/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == receita_id, response_list))) == 1


def test_read_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_read_receita", "valor": 0, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]

    response = client.get(f"/receitas/{receita_id}")
    assert response.status_code == 200
    assert response.json()["descricao"] == "test_read_receita"
    assert response.json()["valor"] == 0
    assert response.json()["data"] == "2022-08-02"


def test_read_receita_incorrect_id(client):

    response = client.get("/receitas/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receita não encontrada."}


def test_update_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_update_receita", "valor": 0, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]
    response = client.put(
        f"/receitas/{receita_id}",
        data=json.dumps(
            {"descricao": "test_update_receita2", "valor": 100, "data": "2021-08-02"}
        ),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert receita_id == response_dict["id"]
    assert response_dict["descricao"] == "test_update_receita2"
    assert response_dict["valor"] == 100
    assert response_dict["data"] == "2021-08-02"


def test_update_receita_duplicada(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_update_receita_duplicada",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_update_receita_duplicada2",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    receita_id = response.json()["id"]
    response = client.put(
        f"/receitas/{receita_id}",
        data=json.dumps(
            {
                "descricao": "test_update_receita_duplicada",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Update vai gerar descrição duplicada para o mês informado."
    }


def test_update_receita_incorrect_id(client):
    response = client.put(
        "/receitas/999",
        data=json.dumps(
            {
                "descricao": "test_update_receita_incorrect_id",
                "valor": 0,
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
                "valor": 0,
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


def test_delete_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_delete_receita", "valor": 0, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]
    response = client.delete(f"/receitas/{receita_id}")

    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_delete_receita",
        "valor": 0,
        "data": "2022-08-02",
        "id": receita_id,
    }


def test_delete_receita_incorrect_id(client):
    response = client.delete("/receitas/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receita não encontrada."}
