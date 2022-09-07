import json
import pytest

from app.controller import usuario


@pytest.mark.parametrize(
    "usuario, senha",
    [
        ["usuario_errado", "admin"],
        ["garibaldo", "senha_errada"],
        ["usuario_errado", "senha_errada"],
    ],
)
def test_dados_errados(client_without_login, usuario, senha):
    response = client_without_login.post(
        "/token/",
        data={"grant_type": "password", "username": usuario, "password": senha},
    )
    print(response.text)
    assert response.status_code == 401

    assert response.json() == {"detail": "Usuário ou Senha incorreta."}


def test_login_correto_usuario_ativo(client_without_login):
    response = client_without_login.post(
        "/token/", data={"username": "garibaldo", "password": "admin"}
    )

    assert response.status_code == 200


def test_login_correto_usuario_inativo(client_without_login):
    response = client_without_login.post(
        "/token/", data={"username": "elmo", "password": "admin"}
    )

    assert response.status_code == 200


def test_read_all_receitas_usuario_inativo(client_without_login):
    access_token = usuario.create_access_token(data={"sub": "elmo"})
    client_without_login.headers.update({"Authorization": f"Bearer {access_token}"})
    response = client_without_login.get("/receitas/")
    assert response.status_code == 400

    assert response.json() == {"detail": "Inactive user"}
