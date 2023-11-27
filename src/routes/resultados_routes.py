# resultados_routes.py

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.config.database import get_session
from src.models.provas_model import Prova
from src.models.resultados_model import Resultados
import logging

resultados_router = APIRouter(prefix="/resultados")

logger = logging.getLogger(__name__)

@resultados_router.post("")
async def adicionar_resultado_prova(resultado: Resultados):
    with get_session() as session:

        prova_existente = session.query(Prova).filter_by(id=resultado.prova_id).first()

        if prova_existente is None:
            raise HTTPException(status_code=404, detail="Prova não cadastrada.")

        nota_final = 0
        for i in range(1, 11):
            resposta_correta = getattr(prova_existente, f"q{i}")
            resposta_aluno = getattr(resultado, f"q{i}")
            if resposta_correta == resposta_aluno:
                nota_final += 1

        resultado.nota = nota_final

        session.add(resultado)
        session.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=resultado.dict())


@resultados_router.get("/{prova_id}")
async def obter_resultados_prova(prova_id: int):
    with get_session() as session:
        prova = session.query(Prova).get(prova_id)
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não cadastrada.")

        resultados = session.query(Resultados).filter_by(prova_id=prova_id).all()

        resultados_finais = []
        for resultado in resultados:
            resultado_final = {
                "nome": resultado.aluno_nome,
                "nota": resultado.nota_final,
                "resultado_final": "aprovado" if resultado.nota_final >= 7 else "recuperação" if resultado.nota_final >= 5 else "reprovado"
            }
            resultados_finais.append(resultado_final)

        return {
            "descricao_prova": prova.descricao,
            "data_aplicacao": prova.data_realizacao,
            "resultados_alunos": resultados_finais
        }

@resultados_router.patch("/provas_aplicadas/{id}")
async def atualizar_respostas_prova(id: int, resultado_atualizado: Resultados):
    with get_session() as session:
        resultado_antigo = session.query(Resultados).get(id)
        if not resultado_antigo:
            raise HTTPException(status_code=404, detail="Resultado da prova não encontrado.")

        nota_final = 0
        for i in range(1, 11):
            resposta_correta = getattr(resultado_antigo, f"q{i}")
            resposta_aluno = getattr(resultado_atualizado, f"q{i}")
            if resposta_correta == resposta_aluno:
                nota_final += 1

        resultado_atualizado.nota_final = nota_final

        session.query(Resultados).filter_by(id=id).update(resultado_atualizado.dict())
        session.commit()

        return resultado_atualizado