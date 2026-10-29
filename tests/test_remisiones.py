from app.core.normas_verificadas import NORMAS, problemas_remision


def test_remisiones_apuntan_a_normas_existentes():
    for nid, n in NORMAS.items():
        for dest in n.get("remite_a", []):
            assert dest in NORMAS, f"{nid} remite a {dest} inexistente"
        for dest in n.get("sancionable_via", []):
            assert dest in NORMAS, f"{nid} sancionable_via -> {dest} inexistente"


def test_ley27815_sancionable_via_85q():
    for art in ("LEY27815_ART6", "LEY27815_ART7", "LEY27815_ART8"):
        assert "LEY30057_ART85_Q" in NORMAS[art]["sancionable_via"]


def test_85q_es_remision():
    n = NORMAS["LEY30057_ART85_Q"]
    assert n.get("es_norma_de_remision") is True
    assert "LEY27815_ART8" in n.get("remite_a", [])


def test_ley27815_sin_problemas_de_remision():
    for art in ("LEY27815_ART6", "LEY27815_ART7", "LEY27815_ART8"):
        assert problemas_remision(NORMAS[art]) == []


def test_ley27815_articulos_tienen_texto_literal_cargado():
    """Los artículos de la Ley 27815 deben tener texto y fuente declarada."""
    for numero in ("6", "7", "8"):
        nid = f"LEY27815_ART{numero}"
        assert nid in NORMAS, f"Falta el registro {nid}"

        norma = NORMAS[nid]
        texto = norma.get("texto_literal")
        fuente = norma.get("fuente_del_texto")

        assert isinstance(texto, str) and texto.strip(), (
            f"{nid} no tiene texto literal cargado"
        )
        assert f"Art\u00edculo {numero}" in texto, (
            f"El texto de {nid} no identifica su artículo"
        )
        assert isinstance(fuente, str) and fuente.strip(), (
            f"{nid} no tiene fuente declarada"
        )
