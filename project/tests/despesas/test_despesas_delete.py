import json
import uuid


def test_delete_despesa(client):
    response = client.post(
        "/despesas/",
        data=json.dumps(
            {"descricao": "test_delete_despesa", "valor": 10, "data": "2022-08-02"}
        ),
    )
    despesa_id = response.json()["id"]
    response = client.delete(f"/despesas/{despesa_id}")

    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_delete_despesa",
        "valor": 10,
        "data": "2022-08-02",
        "id": despesa_id,
        "categoria": "Outras",
    }
    despesa_inexistente = client.get(f"/despesas/{despesa_id}")
    assert despesa_inexistente.status_code == 404
    assert despesa_inexistente.json() == {"detail": "Despesa não encontrada."}


def test_delete_despesa_incorrect_id(client):
    response = client.delete(f"/despesas/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Despesa não encontrada."}
