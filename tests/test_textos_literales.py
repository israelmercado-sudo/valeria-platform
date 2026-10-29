import json
from pathlib import Path

from app.core.normas_verificadas import NORMAS, MARCADORES_PLACEHOLDER, esta_verificada

RUTA = Path(__file__).resolve().parent.parent / "app" / "data" / "normas_textos_literales.json"


def test_textos_literales_cargados_en_el_registro():
    datos = json.loads(RUTA.read_text(encoding="utf-8"))
    assert datos
    for nid, d in datos.items():
        assert nid in NORMAS, nid
        assert NORMAS[nid]["texto_literal"] == d["texto_literal"], nid
        assert not any(m in d["texto_literal"] for m in MARCADORES_PLACEHOLDER), nid


def test_texto_literal_solo_no_verifica_la_norma():
    for nid, n in NORMAS.items():
        if not (n.get("url_fuente") and n.get("fecha_consulta") and n.get("verificado_por") and n.get("vigencia")):
            assert not esta_verificada(n), nid
