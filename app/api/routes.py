from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.legal_engine import valeria_engine


router = APIRouter()


class ConsultaRequest(BaseModel):
    consulta: str


@router.post("/analizar")
def analizar(request: ConsultaRequest):
    resultado = valeria_engine.analizar_materia(request.consulta)

    return JSONResponse(
        content={
            "consulta": request.consulta,
            "analisis": resultado
        },
        media_type="application/json"
    )