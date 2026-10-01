from app.core.typification_engine import TypificationEngine

engine = TypificationEngine()

casos = [
    "El informe fue presentado dentro del plazo establecido.",
    "El informe fue presentado fuera del plazo establecido.",
    "El informe fue presentado.",
    "Los informes fueron presentados oportunamente.",
    "El servidor presentó la documentación.",
    "El servidor presentó la documentación dentro del plazo.",
    "El servidor no presentó la documentación.",
    "El informe no fue presentado.",
    "Los informes no fueron presentados."
]

print("=== PRUEBA PRESENTACIÓN V3.4.3.1 ===")

for i, conducta in enumerate(casos, 1):
    resultado = engine._extraer_modalidades_conducta(conducta)

    print(f"\nCASO {i}")
    print("Conducta:", conducta)
    print("Tipo principal:", resultado["tipo_principal"])
    print("Modalidades:", resultado["modalidades"])
    print("Componente temporal:", resultado["componente_temporal"])

print("\n=== FIN DE PRUEBA ===")
