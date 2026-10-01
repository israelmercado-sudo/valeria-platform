from app.core.typification_engine import TypificationEngine

motor = TypificationEngine()

casos = [
    "El servidor no elaboró ni remitió el informe",
    "El servidor emitió la resolución",
    "El servidor remitió el informe dentro del plazo",
    "El servidor autorizó el pago sin haber verificado los documentos",
    "El servidor omitió verificar los documentos",
    "El servidor omitió notificar la decisión",
    "El informe no fue elaborado ni remitido",
    "El servidor elaboró el informe pero no lo remitió",
]

for c in casos:
    r = motor._extraer_modalidades_conducta(c)
    print(c)
    print("   tipo:", r["tipo_principal"])
    print("   modalidades:", r["modalidades"])
    print("   temporal:", r["componente_temporal"])
    print()