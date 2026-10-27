from app.core.normas_verificadas import NORMAS
from app.core.typification_engine import _verif


def test_id_desconocido_nunca_es_verificado():
    assert _verif({"id": "NO_EXISTE", "verificado": True}) is False


def test_base_dice_verificado_pero_registro_incompleto():
    for nid in NORMAS:
        assert _verif({"id": nid, "verificado": True}) is False


def test_base_dice_no_verificado():
    for nid in NORMAS:
        assert _verif({"id": nid, "verificado": False}) is False
