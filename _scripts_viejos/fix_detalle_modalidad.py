from pathlib import Path

p = Path(r".\app\core\typification_engine.py")
texto = p.read_text(encoding="utf-8")

viejo = '''            detalle = {
                "componente_temporal": mapa_estado.get(
                    estado,
                    "SIN INFORMACIÓN TEMPORAL",
                ),
            }
'''

nuevo = '''            detalle = {
                "modalidad": modalidad,
                "componente_temporal": mapa_estado.get(
                    estado,
                    "SIN INFORMACIÓN TEMPORAL",
                ),
            }
'''

if viejo not in texto:
    raise SystemExit("ERROR: No se encontró exactamente el bloque defectuoso.")

p.write_text(texto.replace(viejo, nuevo, 1), encoding="utf-8")

print("Corrección aplicada: detalle incluye modalidad.")
