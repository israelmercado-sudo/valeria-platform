import pytest

from app.core.typification_engine import TypificationEngine

CONDUCTAS = [
    "El informe fue elaborado fuera del plazo.",
    "El informe no fue elaborado.",
    "No se ha acreditado que el informe fuera elaborado fuera del plazo.",
    "El informe fue elaborado oportunamente.",
]


@pytest.mark.parametrize("conducta", CONDUCTAS)
def test_to_dict_siempre_incluye_aviso_legal(conducta):
    d = TypificationEngine().analizar(conducta=conducta).to_dict()
    assert "no constituye asesoría jurídica" in d["aviso_legal"].lower()
