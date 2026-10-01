from app.core.typification_engine_v351 import TypificationEngineV351

engine = TypificationEngineV351()

resultado = engine.analizar_elementos_evidencia(
    conducta="El informe no fue elaborado ni remitido dentro del plazo establecido.",
    deber="El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo establecido.",
    posible_falta="Posible incumplimiento de obligaciones funcionales.",
    normas=[
        "Norma que establece el deber funcional",
        "Norma tipificadora"
    ],
    hechos=[
        "El servidor tenía la obligación de elaborar y remitir el informe.",
        "El informe no fue elaborado ni remitido dentro del plazo."
    ],
    evidencia=[]
)

print()
print("==============================================")
print(" PRUEBA FUNCIONAL V3.5.1")
print("==============================================")

print()
print("=== ELEMENTOS A VERIFICAR ===")

for elemento in resultado["elementos_a_verificar"]:
    print()
    print("CODIGO:", elemento["codigo"])
    print("ELEMENTO:", elemento["elemento"])
    print("ESTADO:", elemento["estado_acreditacion"])
    print("EVIDENCIA SUGERIDA:")

    for evidencia in elemento["evidencia_sugerida"]:
        print(" -", evidencia)

print()
print("=== BRECHAS PROBATORIAS ===")

for brecha in resultado["brechas_probatorias"]:
    print()
    print("ELEMENTO:", brecha["codigo_elemento"])
    print("ESTADO:", brecha["estado"])
    print("BRECHA:", brecha["brecha"])

print()
print("=== CONCLUSIÓN ===")
print(resultado["conclusion_preliminar"])

print()
print("=== ADVERTENCIA ===")
print(resultado["advertencia_juridica"])

print()
print("==============================================")
print(" PRUEBA V3.5.1 COMPLETADA")
print("==============================================")
