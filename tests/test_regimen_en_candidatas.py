from app.core.typification_engine import TypificationEngine

CONDUCTA = "El informe fue elaborado fuera del plazo."


def test_sin_regimen_se_advierte_en_cada_candidata():
    r = TypificationEngine().analizar(conducta=CONDUCTA)
    assert r.normas_candidatas
    for n in r.normas_candidatas:
        assert n["regimen_especificado"] is False
        assert "Régimen no especificado" in n["advertencia"]
        assert n["regimenes_aplicables"]


def test_con_regimen_276_solo_aparecen_normas_de_ese_regimen():
    r = TypificationEngine().analizar(conducta=CONDUCTA, regimen="276")
    for n in r.normas_candidatas:
        assert "276" in n["regimenes_aplicables"]
        assert n["regimen_especificado"] is True
        assert "Régimen no especificado" not in n["advertencia"]


def test_con_regimen_30057_no_aparece_norma_de_otro_regimen():
    r = TypificationEngine().analizar(conducta=CONDUCTA, regimen="30057")
    ids = {n["id"] for n in r.normas_candidatas}
    assert ids <= {"LEY30057_ART85_A", "LEY30057_ART85_D", "TUO27444_DEBERES_AUTORIDADES"}
    for n in r.normas_candidatas:
        assert "30057" in n["regimenes_aplicables"]
