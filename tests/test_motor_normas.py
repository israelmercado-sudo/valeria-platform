from app.core.normas_verificadas import NORMAS
from app.core.typification_engine import _verif


def test_id_desconocido_nunca_es_verificado():
    assert _verif({"id": "NO_EXISTE", "verificado": True}) is False


def test_base_dice_verificado_pero_registro_incompleto():
    # Usamos una norma ficticia que NO exista en NORMAS.
    # El diccionario externo dice "verificado: True", pero como el ID no está en
    # el registro real, el motor debe devolver False y no dejarse engañar.
    registro_falso = {
        "id": "LEY_FICTICIA_999",
        "verificado": True,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
    }
    assert _verif(registro_falso) is False


def test_base_dice_no_verificado():
    for nid in NORMAS:
        assert _verif({"id": nid, "verificado": False}) is False
