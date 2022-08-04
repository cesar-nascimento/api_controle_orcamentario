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


def test_create_receita_duplicada(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_create_receita_duplicada",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {
                "descricao": "test_create_receita_duplicada",
                "valor": 0,
                "data": "2022-08-02",
            }
        ),
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Descrição duplicada para o mês informado"}


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
