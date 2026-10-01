p='app/core/typification_engine_v352_work.py'
lines=open(p,encoding='utf-8').readlines()
nuevo=['            if modalidad in [
','                "NO ELABORACIÓN",
','                "NO REMISIÓN",
','                "NO PRESENTACIÓN",
','                "NO VERIFICACIÓN",
','            ]:
','                # La temporalidad de una modalidad negativa
','                # solo se atribuye cuando el indicador temporal
','                # pertenece a la misma proposición negativa.
','
','                if modalidad == "NO ELABORACIÓN":
','                    patrones_negativos = [
','                        r"\\bno fue elaborad[oa]\\b",
','                        r"\\bno elabor[oó]\\b",
','                    ]
','                elif modalidad == "NO REMISIÓN":
','                    patrones_negativos = [
','                        r"\\bno fue remitid[oa]\\b",
','                        r"\\bno remiti[oó]\\b",
','                        r"\\bni remitid[oa]\\b",
','                    ]
','                elif modalidad == "NO PRESENTACIÓN":
','                    patrones_negativos = [
','                        r"\\bno fue presentad[oa]\\b",
','                        r"\\bno fueron presentad[oa]s\\b",
','                        r"\\bno present[oó]\\b",
','                        r"\\bno se present[oó]\\b",
','                        r"\\bomiti[oó] presentar\\b",
','                    ]
','                elif modalidad == "NO VERIFICACIÓN":
','                    patrones_negativos = [
','                        r"\\bsin verificar\\b",
','                        r"\\bno verific[oó]\\b",
','                        r"\\bno se verific[oó]\\b",
','                        r"\\bomiti[oó] verificar\\b",
','                    ]
',]
lines[1939:1955]=nuevo
open(p,'w',encoding='utf-8').writelines(lines)
print('OK', len(nuevo))

