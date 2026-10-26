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

CASOS_EMISION = [
    ("El informe fue emitido dentro del plazo y posteriormente notificado fuera del plazo.",
     [("EMISION", "DENTRO_DE_PLAZO"), ("NOTIFICACION", "FUERA_DE_PLAZO")]),
    ("El informe fue emitido fuera del plazo y posteriormente notificado dentro del plazo.",
     [("EMISION", "FUERA_DE_PLAZO"), ("NOTIFICACION", "DENTRO_DE_PLAZO")]),
]

ok = fail = 0
for texto, mod_esp, comp_esp in CASOS:
    r = engine.analizar(conducta=texto).to_dict()
    if r["modalidades"] == mod_esp and r["componente_temporal"] == comp_esp:
        ok += 1; print(f"[OK]    {texto}")
    else:
        fail += 1; print(f"[FALLA] {texto} -> {r['modalidades']} / {r['componente_temporal']}")

for texto, ev_esp in CASOS_EMISION:
    ev = engine._parsear_eventos(texto)
    if ev == ev_esp:
        ok += 1; print(f"[OK]    {texto}")
    else:
        fail += 1; print(f"[FALLA] {texto} -> {ev}")

print(f"\n=== {ok} OK / {fail} FALLA ===")
