import json
import uuid


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
    }


def test_read_despesa_incorrect_id(client):

    response = client.get(f"/despesas/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Despesa não encontrada."}
