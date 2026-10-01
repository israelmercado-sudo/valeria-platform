from app.core.typification_engine_v352_work import TypificationEngine

e = TypificationEngine()

casos = [
    "El informe fue presentado dentro del plazo establecido.",
    "El informe fue presentado fuera del plazo establecido.",
    "El informe fue presentado oportunamente.",
    "El informe no fue presentado dentro del plazo establecido.",
]

for c in casos:
    print("\nCASO:", c)
    print("RESULTADO:", e._extraer_modalidades_conducta(c))
