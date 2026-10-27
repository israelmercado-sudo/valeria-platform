import pytest

from app.core.base_normativa import BaseNormativa

# SNAPSHOT del comportamiento actual. No es validación jurídica:
# los resultados esperados definitivos los fija un abogado.


def ids(tipo, regimen=None):
    return {n["id"] for n in BaseNormativa().candidatas(tipo, regimen)}


def test_omision_elaboracion_regimen_30057():
    assert ids("OMISIÓN - NO ELABORACIÓN", "30057") == {"LEY30057_ART85_A", "LEY30057_ART85_D"}


def test_plazo_elaboracion_regimen_30057():
    assert ids("INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)", "30057") == {
        "LEY30057_ART85_A", "LEY30057_ART85_D", "TUO27444_DEBERES_AUTORIDADES",
    }


def test_plazo_elaboracion_regimen_276_solo_tuo():
    assert ids("INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)", "276") == {"TUO27444_DEBERES_AUTORIDADES"}


@pytest.mark.parametrize("tipo", ["CUMPLIMIENTO", "NO DETERMINADO", "CONDUCTA INVENTADA"])
def test_sin_gatillo_no_devuelve_nada(tipo):
    assert ids(tipo, "30057") == set()


def test_regimen_desconocido_no_devuelve_nada():
    assert ids("OMISIÓN - NO ELABORACIÓN", "NO_EXISTE") == set()
