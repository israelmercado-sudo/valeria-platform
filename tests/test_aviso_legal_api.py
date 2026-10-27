import json

from app.api.routes import analizar, ConsultaRequest


def test_analizar_incluye_aviso_legal():
    resp = analizar(ConsultaRequest(consulta="prescripci\u00f3n de la potestad disciplinaria"))
    cuerpo = json.loads(resp.body)
    assert "aviso_legal" in cuerpo
    assert "no constituye asesor\u00eda jur\u00eddica" in cuerpo["aviso_legal"].lower()
