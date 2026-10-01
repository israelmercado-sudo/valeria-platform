from app.core.typification_engine import TypificationEngine

e = TypificationEngine()

print("--- A: incumplimiento de plazo sin datos ---")
r = e.analizar(conducta="El informe fue remitido fuera del plazo.")
print(r.estado_tipificacion)
for p in r.preguntas_para_el_usuario:
    print("  ?", p)

print("--- B: con todos los datos ---")
r = e.analizar(
    conducta="El informe fue remitido fuera del plazo.",
    funcion="Cumplir con las disposiciones legales que regulan las contrataciones.",
    fuente_funcion="TUO del ROF, art. 85 k)",
    norma_plazo="Reglamento de la Ley de Contrataciones, art. 205.6 (12 días hábiles)",
    fecha_inicio_computo="2023-08-17",
    regimen="30057",
)
print(r.estado_tipificacion)
print([n["id"] for n in r.normas_candidatas])
print(r.preguntas_para_el_usuario)

print("--- C: omisión (no pide plazo) ---")
r = e.analizar(conducta="El informe no fue remitido.")
print(r.estado_tipificacion)
for p in r.preguntas_para_el_usuario:
    print("  ?", p)

print("--- D: cumplimiento ---")
r = e.analizar(conducta="El informe fue remitido dentro del plazo.")
print(r.estado_tipificacion, r.normas_candidatas, r.preguntas_para_el_usuario)