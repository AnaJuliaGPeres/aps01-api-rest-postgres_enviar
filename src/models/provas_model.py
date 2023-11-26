from typing import List
from sqlmodel import Field, Relationship, SQLModel
from src.models.resultados_model import Resultados
from src.models.provas_model import Prova

class Prova(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    descricao: str = Field(nullable=False)
    data_prova: str = Field(nullable=False)
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
    resultados: List["Resultados"] = Relationship(back_populates="provas")