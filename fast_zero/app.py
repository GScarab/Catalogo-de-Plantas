from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, PlantaBase, PlantaPublic

app = FastAPI()

plantas_db: list[PlantaPublic] = []
proximo_id = 1


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/plantas',
    status_code=HTTPStatus.CREATED,
    response_model=PlantaPublic,
)
def criar_planta(planta: PlantaBase):
    global proximo_id

    nova_planta = PlantaPublic(
        id=proximo_id,
        **planta.model_dump(),
    )

    plantas_db.append(nova_planta)
    proximo_id += 1

    return nova_planta


@app.get(
    '/plantas',
    status_code=HTTPStatus.OK,
    response_model=list[PlantaPublic],
)
def listar_plantas():
    return plantas_db


@app.get(
    '/plantas/{planta_id}',
    status_code=HTTPStatus.OK,
    response_model=PlantaPublic,
)
def buscar_planta(planta_id: int):
    for planta in plantas_db:
        if planta.id == planta_id:
            return planta

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Planta não encontrada',
    )


@app.put(
    '/plantas/{planta_id}',
    status_code=HTTPStatus.OK,
    response_model=PlantaPublic,
)
def atualizar_planta(planta_id: int, dados: PlantaBase):
    for indice, planta in enumerate(plantas_db):
        if planta.id == planta_id:
            planta_atualizada = PlantaPublic(
                id=planta_id,
                **dados.model_dump(),
            )
            plantas_db[indice] = planta_atualizada
            return planta_atualizada

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Planta não encontrada',
    )


@app.delete(
    '/plantas/{planta_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def remover_planta(planta_id: int):
    for indice, planta in enumerate(plantas_db):
        if planta.id == planta_id:
            plantas_db.pop(indice)
            return

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Planta não encontrada',
    )
