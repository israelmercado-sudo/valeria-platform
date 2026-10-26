import pytest
from app.core.typification_engine import TypificationEngine

engine = TypificationEngine()

CASOS = [
    ("El informe fue presentado dentro del plazo establecido.", ["PRESENTACIÓN"], "CUMPLIMIENTO DE PLAZO"),
    ("El informe fue presentado oportunamente.",                ["PRESENTACIÓN"], "CUMPLIMIENTO DE PLAZO"),
    ("Los informes fueron presentados oportunamente.",          ["PRESENTACIÓN"], "CUMPLIMIENTO DE PLAZO"),
    ("Los informes fueron presentados dentro del plazo.",       ["PRESENTACIÓN"], "CUMPLIMIENTO DE PLAZO"),
    ("Los informes fueron presentados fuera del plazo.",        ["PRESENTACIÓN"], "INCUMPLIMIENTO DE PLAZO"),
    ("Los informes no fueron presentados dentro del plazo.",    ["NO PRESENTACIÓN"], "INCUMPLIMIENTO DE PLAZO"),
    ("Las resoluciones fueron notificadas fuera del plazo.",    ["NOTIFICACIÓN"], "INCUMPLIMIENTO DE PLAZO"),
    ("Las resoluciones no fueron notificadas.",                 ["NO NOTIFICACIÓN"], "SIN INFORMACIÓN TEMPORAL"),
]

@pytest.mark.parametrize("texto,modalidades_esp,comp_esp", CASOS)
def test_casos(texto, modalidades_esp, comp_esp):
    r = engine.analizar(conducta=texto).to_dict()
    assert r["modalidades"] == modalidades_esp, f"{texto} -> {r['modalidades']}"
    assert r["componente_temporal"] == comp_esp, f"{texto} -> {r['componente_temporal']}"


CASOS_EMISION = [
    ("El informe fue emitido dentro del plazo y posteriormente notificado fuera del plazo.",
     [("EMISION", "DENTRO_DE_PLAZO"), ("NOTIFICACION", "FUERA_DE_PLAZO")]),
    ("El informe fue emitido fuera del plazo y posteriormente notificado dentro del plazo.",
     [("EMISION", "FUERA_DE_PLAZO"), ("NOTIFICACION", "DENTRO_DE_PLAZO")]),
]

@pytest.mark.parametrize("texto,eventos_esp", CASOS_EMISION)
def test_eventos_emision(texto, eventos_esp):
    assert engine._parsear_eventos(texto) == eventos_esp
