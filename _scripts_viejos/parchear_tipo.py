RUTA = r"app\core\typification_engine.py"

with open(RUTA, "rb") as f:
    crudo = f.read().decode("utf-8")

eol = "\r\n" if "\r\n" in crudo else "\n"
src = crudo.replace("\r\n", "\n")

i_def = src.index("def _determinar_tipo_conducta")
i_ini = src.index("        if etapas_incumplidas:\n", i_def)
fin_txt = 'return " + ".join(dict.fromkeys(partes))\n'
i_fin = src.index(fin_txt, i_ini) + len(fin_txt)

nuevo = '''        nombres = {
            "ELABORACION": "ELABORACI\u00d3N",
            "REMISION": "REMISI\u00d3N",
            "PRESENTACION": "PRESENTACI\u00d3N",
        }

        if etapas_incumplidas:
            partes = []

            for etapa, estado in etapas_incumplidas:
                nombre = nombres.get(etapa)
                if nombre is None:
                    continue

                if estado == "FUERA_DE_PLAZO":
                    partes.append(f"INCUMPLIMIENTO DE PLAZO ({nombre})")
                elif estado == "NO_EJECUTADO":
                    partes.append(f"OMISI\u00d3N - NO {nombre}")

            if partes:
                return " + ".join(dict.fromkeys(partes))
'''

src = src[:i_ini] + nuevo + src[i_fin:]

with open(RUTA, "wb") as f:
    f.write(src.replace("\n", eol).encode("utf-8"))

print("OK: bloque reemplazado")
