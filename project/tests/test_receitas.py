import json


def test_create_receita(test_app_with_db):
    response = test_app_with_db.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "receita teste", "valor": 0, "data": "2022-08-02"}
        ),
    )

    assert response.status_code == 201
    assert response.json()["descricao"] == "receita teste"
    assert response.json()["valor"] == 0
    assert response.json()["data"] == "2022-08-02"


def test_create_receita_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/receitas/", data=json.dumps({}))

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
