import sys
sys.path.insert(0, ".")
from app.core.typification_engine import TypificationEngine

OM = "OMISI\u00d3N"
AC = "ACCI\u00d3N"

CASOS = [
    ("El servidor no realiz\u00f3 la verificaci\u00f3n.", "OMISI\u00d3N - NO VERIFICACI\u00d3N"),
    ("El servidor no realizo la verificacion.", "OMISI\u00d3N - NO VERIFICACI\u00d3N"),
    ("El servidor no verific\u00f3 el expediente.", "OMISI\u00d3N - NO VERIFICACI\u00d3N"),
    ("El servidor autoriz\u00f3 el pago.", AC),
    ("El servidor autorizo el pago.", AC),
    ("EL SERVIDOR NO REALIZ\u00d3 LA VERIFICACI\u00d3N.", "OMISI\u00d3N - NO VERIFICACI\u00d3N"),
    ("El servidor omiti\u00f3 informar.", OM),
    ("El servidor no cumpli\u00f3 sus funciones.", OM),
    ("El servidor incumpli\u00f3 sus funciones.", OM),
    ("El servidor cumpli\u00f3 oportunamente.", "CUMPLIMIENTO"),
]

motor = TypificationEngine()
ok = 0
for i, (texto, esperado) in enumerate(CASOS, 1):
    obtenido = motor._determinar_tipo_conducta(texto)
    if obtenido == esperado:
        ok += 1
        print("CASO", str(i).zfill(2) + ": OK")
    else:
        print("CASO", str(i).zfill(2) + ": FALLO")
        print("  Texto:   ", texto)
        print("  Devuelto:", obtenido)
        print("  Esperado:", esperado)
print("RESULTADO:", str(ok) + "/" + str(len(CASOS)), "casos correctos")
