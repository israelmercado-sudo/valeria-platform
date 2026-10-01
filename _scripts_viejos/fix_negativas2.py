# -*- coding: utf-8 -*-
p = "app/core/typification_engine_v352_work.py"

with open(p, encoding="utf-8") as f:
    lines = f.readlines()

nuevo_bloque = []
nuevo_bloque.append("            if modalidad in [\n")
nuevo_bloque.append("                \"NO ELABORACIÓN\",\n")
nuevo_bloque.append("                \"NO REMISIÓN\",\n")
nuevo_bloque.append("                \"NO PRESENTACIÓN\",\n")
nuevo_bloque.append("                \"NO VERIFICACIÓN\",\n")
nuevo_bloque.append("            ]:\n")
nuevo_bloque.append("                # La temporalidad de una modalidad negativa\n")
nuevo_bloque.append("                # solo se atribuye si el indicador temporal\n")
nuevo_bloque.append("                # pertenece a la misma proposición negativa.\n")
nuevo_bloque.append("\n")
nuevo_bloque.append("                if modalidad == \"NO ELABORACIÓN\":\n")
nuevo_bloque.append("                    patrones_negativos = [\n")
nuevo_bloque.append("                        r\"\\bno fue elaborad[oa]\\b\",\n")
nuevo_bloque.append("                        r\"\\bno elabor[oó]\\b\",\n")
nuevo_bloque.append("                    ]\n")
nuevo_bloque.append("                elif modalidad == \"NO REMISIÓN\":\n")
nuevo_bloque.append("                    patrones_negativos = [\n")
nuevo_bloque.append("                        r\"\\bno fue remitid[oa]\\b\",\n")
nuevo_bloque.append("                        r\"\\bno remiti[oó]\\b\",\n")
nuevo_bloque.append("                        r\"\\bni remitid[oa]\\b\",\n")
nuevo_bloque.append("                    ]\n")
nuevo_bloque.append("                elif modalidad == \"NO PRESENTACIÓN\":\n")
nuevo_bloque.append("                    patrones_negativos = [\n")
nuevo_bloque.append("                        r\"\\bno fue presentad[oa]\\b\",\n")
nuevo_bloque.append("                        r\"\\bno fueron presentad[oa]s\\b\",\n")
nuevo_bloque.append("                        r\"\\bno present[oó]\\b\",\n")
nuevo_bloque.append("                        r\"\\bno se present[oó]\\b\",\n")
nuevo_bloque.append("                        r\"\\bomiti[oó] presentar\\b\",\n")
nuevo_bloque.append("                    ]\n")
nuevo_bloque.append("                elif modalidad == \"NO VERIFICACIÓN\":\n")
nuevo_bloque.append("                    patrones_negativos = [\n")
nuevo_bloque.append("                        r\"\\bsin verificar\\b\",\n")
nuevo_bloque.append("                        r\"\\bno verific[oó]\\b\",\n")
nuevo_bloque.append("                        r\"\\bno se verific[oó]\\b\",\n")
nuevo_bloque.append("                        r\"\\bomiti[oó] verificar\\b\",\n")
nuevo_bloque.append("                    ]\n")

lines[1939:1955] = nuevo_bloque

with open(p, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("OK reemplazadas", len(nuevo_bloque), "lineas")
