from pydantic import BaseModel


class Message(BaseModel):
    message: str


class PlantaBase(BaseModel):
    nome: str
    especie: str
    frequencia_rega: str
    local: str


class PlantaPublic(PlantaBase):
    id: int
