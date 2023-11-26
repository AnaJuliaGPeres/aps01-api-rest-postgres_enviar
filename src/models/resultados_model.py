from sqlmodel import Field, Relationship, SQLModel
from src.models.provas_model import Prova
from typing import Optional

class Resultados(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False)
    q1: str = Field(nullable=False)
    q2: str = Field(nullable=False)
    q3: str = Field(nullable=False)
    q4: str = Field(nullable=False)
    q5: str = Field(nullable=False)
    q6: str = Field(nullable=False)
    q7: str = Field(nullable=False)
    q8: str = Field(nullable=False)
    q9: str = Field(nullable=False)
    q10: str = Field(nullable=False)
    nota: float = Optional[float]
    prova_id: int = Field(nullable=False, foreign_key="prova.id")
    provas: Optional[Prova] = Relationship(back_populates="resultados")