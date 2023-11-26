from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from src.models.provas_model import Prova
from src.models.resultados_model import Resultados
from src.config.database import get_session

provas_router = APIRouter(prefix="/provas")

@provas_router.post("")
def cria_prova(prova: Prova):
    with get_session() as session:

        # verifica se a prova com a mesma descrição e data, já existe
        query = session.query(Prova).filter(
            Prova.descricao == prova.descricao,
            Prova.data_prova == prova.data_prova
        )
        if query.count() > 0:
            raise HTTPException(status_code=400, detail="Prova já cadastrada.")

        session.add(prova)
        session.commit()
        session.refresh(prova)

        prova_for_Return = prova.dict()

        return JSONResponse(status_code=201, content=prova_for_Return)
    