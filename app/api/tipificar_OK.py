from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.typification_engine import TypificationEngine

router_tipificar = APIRouter(tags=["Tipificación"])

_motor = TypificationEngine()


class SolicitudTipificacion(BaseModel):
    conducta: str
    deber: str = ""
    regimen: Optional[str] = None
    funcion: Optional[str] = None
    fuente_funcion: Optional[str] = None
    norma_plazo: Optional[str] = None
    fecha_inicio_computo: Optional[str] = None
    plazo_dias_habiles: Optional[int] = None
    fecha_real: Optional[str] = None


@router_tipificar.post("/tipificar")
def tipificar(s: SolicitudTipificacion):
    r = _motor.analizar(
        conducta=s.conducta,
        deber=s.deber,
        regimen=s.regimen,
        funcion=s.funcion,
        fuente_funcion=s.fuente_funcion,
        norma_plazo=s.norma_plazo,
        fecha_inicio_computo=s.fecha_inicio_computo,
        plazo_dias_habiles=s.plazo_dias_habiles,
        fecha_real=s.fecha_real,
    )
    return {
        "aviso": "Apoyo para el operador. Resultado preliminar que requiere revisión humana.",
        "resultado": r.to_dict(),
    }