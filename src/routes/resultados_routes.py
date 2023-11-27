# resultados_routes.py

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from src.config.database import get_session
from src.models.resultados_model import Resultados
from src.models.provas_model import Prova

resultados_router = APIRouter(prefix="/resultados")

logger = logging.getLogger(__name__)

@resultados_router.post("/resultados_provas")
async def adicionar_resultado_prova(resultado: Resultados):
    # Abrir uma sessão no banco de dados
    with get_session() as session:
        # Verificar se a prova associada ao resultado existe
        prova_existente = session.query(Prova).get(resultado.prova_id)
        if not prova_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prova não cadastrada."
            )

        # Calcular a nota final com base nas respostas do aluno
        resultado.nota_final = sum(
            getattr(prova_existente, f"q{i}") == getattr(resultado, f"q{i}")
            for i in range(1, 11)
        )

        # Adicionar o resultado ao banco de dados
        session.add(resultado)
        session.commit()

        # Retornar o resultado adicionado com status 201 Created
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=resultado.dict()
        )


@resultados_router.get("/{prova_id}")
async def obter_resultados_prova(prova_id: int):
    # Abrir uma sessão no banco de dados
    with get_session() as session:
        # Buscar a prova pelo ID
        prova = session.query(Prova).get(prova_id)
        if not prova:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prova não encontrada."
            )

        # Buscar os resultados da prova
        resultados = session.query(Resultados).filter_by(prova_id=prova_id).all()

        # Preparar os resultados finais em um formato mais estruturado
        resultados_finais = [
            {
                "nome_aluno": resultado.aluno_nome,
                "nota_final": resultado.nota_final,
                "status": obter_status(resultado.nota_final)
            }
            for resultado in resultados
        ]

        # Retornar os resultados da prova e informações relacionadas
        return {
            "descricao_prova": prova.descricao,
            "data_aplicacao": prova.data_realizacao,
            "resultados_alunos": resultados_finais
        }

def obter_status(nota_final):
    if nota_final >= 7:
        return "aprovado"
    elif nota_final >= 5:
        return "recuperação"
    else:
        return "reprovado"


@resultados_router.patch("/provas_aplicadas/{id}")
async def atualizar_respostas_prova(id: int, resultado_atualizado: Resultados):
    # Abrir uma sessão no banco de dados
    with get_session() as session:
        # Buscar o resultado da prova pelo ID
        resultado_antigo = session.query(Resultados).get(id)
        if not resultado_antigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resultado da prova não encontrado."
            )

        # Calcular a nova nota final com base nas respostas atualizadas
        nota_final = calcular_nota_final(resultado_antigo, resultado_atualizado)
        resultado_atualizado.nota_final = nota_final

        # Atualizar as respostas e a nota final no banco de dados
        session.query(Resultados).filter_by(id=id).update(resultado_atualizado.dict())
        session.commit()

        # Retornar o resultado atualizado
        return resultado_atualizado

def calcular_nota_final(resultado_antigo, resultado_atualizado):
    nota_final = 0
    for i in range(1, 11):
        resposta_correta = getattr(resultado_antigo, f"q{i}")
        resposta_aluno = getattr(resultado_atualizado, f"q{i}")
        if resposta_correta == resposta_aluno:
            nota_final += 1
    return nota_final





