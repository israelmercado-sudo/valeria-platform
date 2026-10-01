import sys
sys.path.insert(0, ".")

from app.core.typification_engine_v352_work import TypificationEngine

e = TypificationEngine()

r = e.analizar(
    conducta="El informe no fue elaborado ni remitido dentro del plazo establecido.",
    deber="El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo establecido.",
    posible_falta="Posible incumplimiento de obligaciones funcionales.",
    normas=[
        "Norma que establece el deber",
        "Norma tipificadora"
    ],
    hechos=[
        "El servidor tenía la obligación de elaborar y remitir el informe.",
        "El informe no fue elaborado ni remitido dentro del plazo."
    ]
)

print("=== MATRIZ COMPLETA V3.5.2 ===")

for i, x in enumerate(r.matriz_subsuncion, 1):
    print(
        f"{i}. [{x.get('dimension')}] "
        f"{x.get('contenido')} | "
        f"PRIORIDAD={x.get('prioridad')} | "
        f"ORIGEN={x.get('hecho_origen')}"
    )

print("=== FIN MATRIZ ===")
