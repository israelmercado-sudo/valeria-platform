from app.core.typification_engine_v35 import TypificationEngineV35

engine = TypificationEngineV35()

resultado = engine.analizar_dimensiones_juridicas(
    conducta="El informe no fue elaborado ni remitido dentro del plazo establecido.",
    deber="El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo establecido.",
    posible_falta="Posible incumplimiento de obligaciones funcionales.",
    normas=[
        "Norma que establece el deber funcional",
        "Norma que tipifica la falta disciplinaria"
    ],
    hechos=[
        "El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo.",
        "El informe no fue elaborado ni remitido dentro del plazo establecido."
    ],
    evidencia=[
        "Documento que establece la obligación funcional.",
        "Informe no elaborado ni remitido.",
        "Documentación que acredita el vencimiento del plazo."
    ]
)

print("==============================================")
print(" PRUEBA V3.5 - CONDUCTA Y DEBER")
print("==============================================")

print("\n=== CONDUCTA ===")
print(resultado["conducta_estructurada"])

print("\n=== CIRCUNSTANCIAS ===")
print(resultado["circunstancias"])

print("\n=== DEBER FUNCIONAL ===")
print(resultado["deber_funcional"])

print("\n=== COMPARACIÓN CONDUCTA <-> DEBER ===")
print("ESTADO:")
print(resultado["comparacion_conducta_deber"]["estado"])

for item in resultado["comparacion_conducta_deber"]["comparaciones"]:
    print("\nDIMENSIÓN:", item["dimension"])
    print("CONDUCTA:", item["conducta"])
    print("DEBER:", item["deber"])
    print("CORRESPONDENCIA:", item["correspondencia"])
    print("FUNDAMENTO:", item["fundamento"])

print("\nADVERTENCIA:")
print(resultado["comparacion_conducta_deber"]["advertencia"])

print("\n=== INFORMACIÓN FALTANTE ===")
for item in resultado["informacion_faltante_v35"]:
    print("-", item)

print("\n==============================================")
print(" PRUEBA V3.5 COMPLETADA")
print("==============================================")
