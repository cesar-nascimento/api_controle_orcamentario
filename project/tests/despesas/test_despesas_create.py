import json
import pytest


def test_create_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_create_despesa", "valor": 1, "data": "2022-08-02"}
        ),
    )

    assert response.status_code == 201
    assert response.json()["descricao"] == "test_create_despesa"
    assert response.json()["valor"] == 1
    assert response.json()["data"] == "2022-08-02"


@pytest.mark.parametrize(
    "payload, server_response",
    [
        [
            {},
            {
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
            },
        ],
        [
            {"descricao": "string", "valor": 0, "data": "2022-08"},
            {
                "detail": [
                    {
                        "loc": ["body", "valor"],
                        "msg": "ensure this value is greater than 0",
                        "type": "value_error.number.not_gt",
                        "ctx": {"limit_value": 0},
                    },
                    {
                        "loc": ["body", "data"],
                        "msg": "invalid date format",
                        "type": "value_error.date",
                    },
                ]
            },
        ],
        [
            {"descricao": "string", "valor": 9999999999999, "data": "2022-08-12"},
            {
                "detail": [
                    {
                        "loc": ["body", "valor"],
                        "msg": "ensure that there are no more than 9 digits in total",
                        "type": "value_error.decimal.max_digits",
                        "ctx": {"max_digits": 9},
                    }
                ]
            },
        ],
        [
            {"descricao": "string", "valor": 99.2222, "data": "2022-08-12"},
            {
                "detail": [
                    {
                        "loc": ["body", "valor"],
                        "msg": "ensure that there are no more than 2 decimal places",
                        "type": "value_error.decimal.max_places",
                        "ctx": {"decimal_places": 2},
                    }
                ]
            },
        ],
    ],
)
def test_create_despesa_invalid_json(client, payload, server_response):
    response = client.post("/despesas/", data=json.dumps(payload))

    assert response.status_code == 422
    assert response.json() == server_response


def test_create_despesa_duplicated(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "test_create_despesa_duplicated",
                "valor": 1,
                "data": "2022-08-01",
            }
        ),
    )
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {
                "descricao": "TEST_CREATE_DESPESA_DUPLICATED",
                "valor": 1,
                "data": "2022-08-10",
            }
        ),
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Descrição duplicada para o mês informado."}
