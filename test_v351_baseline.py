from app.core.typification_engine import TypificationEngine

engine = TypificationEngine()

hechos = (
    "El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo establecido. "
    "El informe no fue elaborado ni remitido dentro del plazo establecido."
)

deber = "Cumplir las funciones asignadas y elaborar los informes dentro de los plazos establecidos."

falta = "Posible incumplimiento de obligaciones funcionales."

normas = [
    "Norma que establece el deber",
    "Norma tipificadora"
]

evidencias = [
    "El servidor tenía la obligación de elaborar y remitir el informe.",
    "El informe no fue elaborado ni remitido dentro del plazo."
]

resultado = engine.analizar(
    hechos,
    deber,
    falta,
    normas,
    evidencias
)

print("=== VALERIA V3.5.1 - LINEA BASE ===")
print("TIPO:", resultado.tipo_conducta)
print("CONDUCTA:", resultado.conducta_identificada)
print("DEBER:", resultado.deber_presuntamente_incumplido)
print("FALTA:", resultado.posible_falta)
print("SUBSUNCIÓN:", resultado.subsuncion_preliminar)
print("NIVEL:", resultado.nivel_conclusion)
print("REQUIERE VERIFICACIÓN:", resultado.requiere_verificacion)

print("\n=== ELEMENTOS ===")
for elemento in resultado.elementos_tipo:
    print("-", elemento)

print("\n=== HECHOS RELEVANTES ===")
for hecho in resultado.hechos_relevantes:
    print("-", hecho)

print("\n=== MATRIZ DE SUBSUNCIÓN ===")
for item in resultado.matriz_subsuncion:
    print(item)

print("\n=== FIN LINEA BASE ===")
