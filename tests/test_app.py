from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_deve_criar_uma_planta():
    response = client.post(
        '/plantas',
        json={
            'nome': 'Samambaia',
            'especie': 'Nephrolepis exaltata',
            'frequencia_rega': '3 vezes por semana',
            'local': 'Sala',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['nome'] == 'Samambaia'
    assert response.json()['id'] >= 1


def test_deve_listar_as_plantas():
    response = client.get('/plantas')

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


def test_deve_buscar_uma_planta():
    response = client.get('/plantas/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['nome'] == 'Samambaia'


def test_deve_atualizar_uma_planta():
    response = client.put(
        '/plantas/1',
        json={
            'nome': 'Samambaia Atualizada',
            'especie': 'Nephrolepis exaltata',
            'frequencia_rega': '2 vezes por semana',
            'local': 'Varanda',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['nome'] == 'Samambaia Atualizada'
    assert response.json()['local'] == 'Varanda'


def test_deve_remover_uma_planta():
    response = client.delete('/plantas/1')

    assert response.status_code == HTTPStatus.NO_CONTENT
