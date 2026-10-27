import pytest

from app.core.typification_engine import TypificationEngine

CONDUCTAS = [
    "El informe fue elaborado fuera del plazo.",
    "El informe no fue elaborado.",
    "No se ha acreditado que el informe fuera elaborado fuera del plazo.",
    "El informe fue elaborado oportunamente.",
]


@pytest.mark.parametrize("conducta", CONDUCTAS)
def test_ninguna_norma_sale_verificada_en_el_resultado_final(conducta):
    resultado = TypificationEngine().analizar(conducta=conducta)
    for n in resultado.normas_candidatas:
        assert n["verificado"] is False, n["id"]
        assert n["advertencia"], n["id"]


@pytest.mark.parametrize("conducta", CONDUCTAS)
def test_to_dict_tampoco_expone_normas_verificadas(conducta):
    d = TypificationEngine().analizar(conducta=conducta).to_dict()
    for n in d["normas_candidatas"]:
        assert n["verificado"] is False, n["id"]


def test_hay_candidatas_para_incumplimiento_afirmado():
    r = TypificationEngine().analizar(conducta="El informe fue elaborado fuera del plazo.")
    assert r.normas_candidatas, "se esperaba al menos una norma candidata"
