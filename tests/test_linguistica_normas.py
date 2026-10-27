import pytest

from app.core.typification_engine import TypificationEngine


def analizar(frase):
    return TypificationEngine().analizar(conducta=frase)


@pytest.mark.parametrize("frase", [
    "El servidor no elaboró el informe.",
    "Nunca elaboró el informe.",
    "No se elaboró el informe.",
    "No elaboro el informe.",
])
def test_negaciones_y_sin_tildes_son_omision(frase):
    assert analizar(frase).tipo_conducta == "OMISIÓN - NO ELABORACIÓN"


@pytest.mark.parametrize("frase", [
    "Intentó elaborar el informe pero no logró terminarlo.",
    "Si hubiera elaborado el informe, no habría retraso.",
])
def test_intento_y_condicional_no_se_tipifican(frase):
    r = analizar(frase)
    assert r.tipo_conducta == "NO DETERMINADO"
    assert r.normas_candidatas == []


@pytest.mark.parametrize("frase", [
    "El informe fue elaborado fuera del plaso.",
    "El informe fue elavorado fuera del plazo.",
    "El colega no hizo el informe.",
    "Se le pasó el plazo para el informe.",
])
def test_errores_y_coloquial_nunca_se_toman_como_cumplimiento(frase):
    r = analizar(frase)
    assert r.tipo_conducta != "CUMPLIMIENTO"
    assert r.estado_tipificacion != "SIN_FALTA_CANDIDATA"


def test_snapshot_emision_fuera_de_plazo_sin_norma_en_base():
    """SNAPSHOT de un hueco conocido: la base no tiene gatillos de emision.
    Si se agregan, este test debe actualizarse a proposito."""
    r = analizar("El informe se emitio fuera del plazo.")
    assert r.tipo_conducta == "INCUMPLIMIENTO DE PLAZO (EMISIÓN)"
    assert r.normas_candidatas == []
