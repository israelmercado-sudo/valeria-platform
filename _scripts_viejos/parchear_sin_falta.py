RUTA = r"app\core\typification_engine.py"

with open(RUTA, "rb") as f:
    crudo = f.read().decode("utf-8")

eol = "\r\n" if "\r\n" in crudo else "\n"
src = crudo.replace("\r\n", "\n")

viejo = '''        if r.tipo_conducta in ("CUMPLIMIENTO", "NO DETERMINADO"):
            r.normas_candidatas = []
            r.preguntas_para_el_usuario = []
            r.estado_tipificacion = "SIN_FALTA_CANDIDATA"
            return r
'''

nuevo = '''        if r.tipo_conducta in ("CUMPLIMIENTO", "NO DETERMINADO"):
            r.normas_candidatas = []
            r.preguntas_para_el_usuario = []
            r.informacion_faltante = []
            r.observaciones = [
                o for o in r.observaciones if not o.startswith("RIESGO")
            ]
            if r.tipo_conducta == "CUMPLIMIENTO":
                r.estado_tipificacion = "SIN_FALTA_CANDIDATA"
                r.nivel_conclusion = (
                    "SIN INDICIOS DE INCUMPLIMIENTO EN LA CONDUCTA DESCRITA"
                )
            else:
                r.estado_tipificacion = "CONDUCTA_NO_CLASIFICADA"
                r.nivel_conclusion = (
                    "CONDUCTA NO CLASIFICADA: REQUIERE AN\\u00c1LISIS ADICIONAL"
                )
            return r
'''

if src.count(viejo) != 1:
    raise SystemExit(f"No se encontro el bloque exacto ({src.count(viejo)} coincidencias). Sin cambios.")

src = src.replace(viejo, nuevo)

with open(RUTA, "wb") as f:
    f.write(src.replace("\n", eol).encode("utf-8"))

print("OK: bloque reemplazado")
