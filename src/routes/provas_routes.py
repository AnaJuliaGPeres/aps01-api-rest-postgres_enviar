from fastapi import APIRouter, HTTPException, status, Response 
from fastapi.responses import JSONResponse
from src.config.database import get_session
from src.models.resultados_model import Resultados
from src.models.provas_model import Prova

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


@provas_router.delete("/{id}")
async def excluir_prova(id: int):
    # Abrir uma sessão no banco de dados
    with get_session() as session:
        # Verificar se existem resultados de provas cadastrados para a prova a ser excluída
        resultados_prova = session.query(Resultados).filter_by(prova_id=id).all()
        if resultados_prova:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Existem resultados de provas cadastrados para esta prova. Não é possível excluí-la."
            )

        # Buscar a prova pelo ID
        prova = session.query(Prova).get(id)
        if not prova:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prova não encontrada."
            )

        # Excluir a prova
        session.delete(prova)
        session.commit()

        # Retornar uma mensagem de sucesso
        return {"mensagem": "Prova excluída com sucesso."}    