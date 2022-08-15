import json
import uuid

import pytest


def test_read_resumo(client):
    receitas = [
        {"descricao": "test_read_resumo", "valor": 1, "data": "2022-08-02"},
        {"descricao": "test_read_resumo2", "valor": 10, "data": "2022-08-02"},
    ]
    despesas = [
        {"descricao": "test_read_resumo", "valor": 2, "data": "2022-08-02"},
        {"descricao": "test_read_resumo2", "valor": 11, "data": "2022-08-02"},
        {
            "descricao": "test_read_resumo3",
            "valor": 22,
            "data": "2022-08-02",
            "categoria": "Alimentação",
        },
        {
            "descricao": "test_read_resumo4",
            "valor": 44,
            "data": "2022-08-02",
            "categoria": "Saúde",
        },
    ]
    for receita in receitas:
        client.post("/receitas/", data=json.dumps(receita))
    for despesa in despesas:
        client.post("/despesas/", data=json.dumps(despesa))

    response = client.get("/resumo/2022/08")
    assert response.status_code == 200

    assert response.json() == {
        "total_receitas": 11,
        "total_despesas": 79,
        "saldo_final_mes": -68,
        "total_despesas_por_categoria": {
            "Alimentação": 22,
            "Saúde": 44,
            "Moradia": 0,
            "Transporte": 0,
            "Educação": 0,
            "Lazer": 0,
            "Imprevistos": 0,
            "Outras": 13,
        },
    }


def test_read_resumo_vazio(client):
    response = client.get("/resumo/2022/07")
    assert response.status_code == 200

    assert response.json() == {
        "total_receitas": 0,
        "total_despesas": 0,
        "saldo_final_mes": 0,
        "total_despesas_por_categoria": {
            "Alimentação": 0,
            "Saúde": 0,
            "Moradia": 0,
            "Transporte": 0,
            "Educação": 0,
            "Lazer": 0,
            "Imprevistos": 0,
            "Outras": 0,
        },
    }


def test_read_resumo_data_invalida(client):
    response = client.get("/resumo/2022/0")
    assert response.status_code == 422

    assert response.json() == {"detail": "Data informada inválida."}


def test_read_resumo_data_ridiculamente_longa(client):
    response = client.get("/resumo/999999999999/1")
    assert response.status_code == 422

    assert response.json() == {"detail": "Data informada inválida."}
