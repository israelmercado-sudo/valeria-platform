from app.core.normas_verificadas import NORMAS
from app.core.typification_engine import _verif


def test_id_desconocido_nunca_es_verificado():
    assert _verif({"id": "NO_EXISTE", "verificado": True}) is False


def test_base_dice_verificado_pero_registro_incompleto():
    # Buscamos una norma que aún NO esté verificada en el sistema
    # (porque ahora ya tenemos 4 normas verificadas y antes asumíamos que todas estaban vacías)
    norma_no_verificada = None
    for nid in NORMAS:
        if not _verif({"id": nid, "verificado": False}):
            norma_no_verificada = nid
            break
    
    assert norma_no_verificada is not None, "Todas las normas están verificadas, no se puede probar este caso"
    assert _verif({"id": norma_no_verificada, "verificado": True}) is False


def test_base_dice_no_verificado():
    for nid in NORMAS:
        assert _verif({"id": nid, "verificado": False}) is False
