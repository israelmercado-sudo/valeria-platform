from app.core.typification_engine import TypificationEngine

e = TypificationEngine()

casos = [
    "El informe fue elaborado dentro del plazo y posteriormente remitido fuera del plazo.",
    "El informe fue elaborado fuera del plazo y posteriormente remitido dentro del plazo.",
    "El informe fue elaborado fuera del plazo y posteriormente remitido fuera del plazo.",
    "El informe fue elaborado dentro del plazo y no fue remitido.",
    "El informe no fue elaborado y posteriormente fue remitido.",
    "El informe no fue elaborado ni remitido.",
    "El informe fue presentado dentro del plazo.",
    "El informe fue presentado fuera del plazo.",
    "El informe fue elaborado dentro del plazo, pero posteriormente remitido fuera del plazo.",
    "El informe fue elaborado fuera del plazo, pero posteriormente remitido dentro del plazo.",
    "El informe fue emitido dentro del plazo y posteriormente notificado fuera del plazo.",
    "El informe fue emitido fuera del plazo y posteriormente notificado dentro del plazo.",
]

for i, c in enumerate(casos, 1):
    r = e.analizar(conducta=c)
    print(f"\nCASO {i:02d}")
    print("TEXTO:", c)
    print("EVENTOS:", e._parsear_eventos(c))
    print("TIPO:", r.tipo_conducta)
