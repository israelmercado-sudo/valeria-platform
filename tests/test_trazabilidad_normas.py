import pytest

from app.core.typification_engine import TypificationEngine

CONDUCTAS = [
    "El informe fue elaborado fuera del plazo.",
    "El informe no fue elaborado.",
]


@pytest.mark.parametrize("conducta", CONDUCTAS)
def test_toda_candidata_explica_su_gatillo(conducta):
    r = TypificationEngine().analizar(conducta=conducta)
    assert r.normas_candidatas
    for n in r.normas_candidatas:
        assert n["gatillo_activado"], n["id"]
        for g in n["gatillo_activado"]:
            assert g in r.tipo_conducta
            assert g in n["razon_seleccion"]


def test_trazabilidad_sobrevive_en_to_dict():
    d = TypificationEngine().analizar(
        conducta="El informe fue elaborado fuera del plazo."
    ).to_dict()
    for n in d["normas_candidatas"]:
        assert "gatillo_activado" in n
        assert "razon_seleccion" in n
