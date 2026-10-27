from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.legal_engine import valeria_engine


router = APIRouter()

AVISO_LEGAL = (
    "Resultado preliminar de orientaci\u00f3n generado autom\u00e1ticamente. "
    "No constituye asesor\u00eda jur\u00eddica, dictamen ni conclusi\u00f3n de responsabilidad. "
    "Las normas y plazos citados no han sido verificados contra fuente oficial "
    "(SPIJ / El Peruano); un operador jur\u00eddico competente debe contrastarlos "
    "antes de usarlos en un procedimiento administrativo."
)


class ConsultaRequest(BaseModel):
    consulta: str


@router.post("/analizar")
def analizar(request: ConsultaRequest):
    resultado = valeria_engine.analizar_materia(request.consulta)

    return JSONResponse(
        content={
            "consulta": request.consulta,
            "aviso_legal": AVISO_LEGAL,
            "analisis": resultado
        },
        media_type="application/json"
    )
