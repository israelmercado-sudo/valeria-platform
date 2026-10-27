import json

from app.api.routes import analizar, ConsultaRequest


def test_analizar_incluye_aviso_legal():
    resp = analizar(ConsultaRequest(consulta="prescripci\u00f3n de la potestad disciplinaria"))
    cuerpo = json.loads(resp.body)
    assert "aviso_legal" in cuerpo
    assert "no constituye asesor\u00eda jur\u00eddica" in cuerpo["aviso_legal"].lower()


def test_analizar_expone_estado_de_verificacion_de_normas():
    resp = analizar(ConsultaRequest(consulta="prescripci\u00f3n de la potestad disciplinaria"))
    citadas = json.loads(resp.body)["normas_citadas"]
    assert citadas
    for n in citadas:
        assert "verificado" in n
        if not n["verificado"]:
            assert n.get("advertencia")
