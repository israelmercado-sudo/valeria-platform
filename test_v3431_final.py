from app.core.typification_engine import TypificationEngine

engine = TypificationEngine()

casos = [
    "El informe no fue elaborado ni remitido dentro del plazo establecido.",
    "El informe fue presentado dentro del plazo establecido.",
    "El informe fue presentado fuera del plazo establecido.",
    "El servidor no presentó la documentación dentro del plazo establecido.",
    "El servidor no remitió la documentación.",
    "El funcionario autorizó el pago sin verificar la documentación.",
    "El servidor suscribió el documento.",
    "El servidor omitió realizar la verificación correspondiente.",
    "El servidor cumplió oportunamente con la obligación."
]

print("=== PRUEBA FUNCIONAL V3.4.3.1 ===")

for i, conducta in enumerate(casos, 1):
    resultado = engine._extraer_modalidades_conducta(conducta)

    print(f"\nCASO {i}")
    print("Conducta:", conducta)
    print("Tipo principal:", resultado["tipo_principal"])
    print("Modalidades:", resultado["modalidades"])
    print("Componente temporal:", resultado["componente_temporal"])

print("\n=== FIN DE PRUEBA ===")
