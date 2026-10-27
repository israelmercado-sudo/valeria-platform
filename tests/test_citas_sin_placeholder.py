import pytest

from app.core.normas_verificadas import MARCADORES_PLACEHOLDER
from app.core.typification_engine import TypificationEngine

CONDUCTAS = [
    "El informe fue elaborado fuera del plazo.",
    "El informe no fue elaborado.",
    "No se ha acreditado que el informe fuera elaborado fuera del plazo.",
    "El informe fue elaborado oportunamente.",
]


@pytest.mark.parametrize("conducta", CONDUCTAS)
def test_ninguna_cita_expuesta_contiene_placeholder(conducta):
    r = TypificationEngine().analizar(conducta=conducta)
    for n in r.normas_candidatas:
        for m in MARCADORES_PLACEHOLDER:
            assert m not in n["cita"], (n["id"], n["cita"])
