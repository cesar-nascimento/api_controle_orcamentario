import json
import uuid


def test_delete_receita(client):
    response = client.post(
        "/receitas/",
        data=json.dumps(
            {"descricao": "test_delete_receita", "valor": 10, "data": "2022-08-02"}
        ),
    )
    receita_id = response.json()["id"]
    response = client.delete(f"/receitas/{receita_id}")

    assert response.status_code == 200
    assert response.json() == {
        "descricao": "test_delete_receita",
        "valor": 10,
        "data": "2022-08-02",
        "id": receita_id,
    }
    receita_inexistente = client.get(f"/receitas/{receita_id}")
    assert receita_inexistente.status_code == 404
    assert receita_inexistente.json() == {"detail": "Receita não encontrada."}


def test_delete_receita_incorrect_id(client):
    response = client.delete(f"/receitas/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receita não encontrada."}
