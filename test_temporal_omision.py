from app.core.typification_engine import TypificationEngine

e = TypificationEngine()

casos = [
    "El informe no fue elaborado dentro del plazo establecido.",
    "El informe no fue elaborado fuera del plazo establecido.",
    "El informe no fue remitido dentro del plazo establecido.",
    "El informe fue elaborado fuera del plazo establecido.",
    "El informe no fue elaborado.",
]

for c in casos:
    r = e.analizar(c)
    print(c)
    print("  tipo:", r.tipo_conducta)
    print("  temporal:", r.componente_temporal)
    print("  detalle:", r.modalidades_detalle)
    print()