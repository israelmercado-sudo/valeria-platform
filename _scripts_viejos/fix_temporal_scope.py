from pathlib import Path

ruta = Path(r".\app\core\typification_engine_v352_work.py")

texto = ruta.read_text(encoding="utf-8")

bloque_anterior = '''            if len(ocurrencias) >= 2:
                for indice in range(len(ocurrencias) - 1):
                    primera = ocurrencias[indice]
                    segunda = ocurrencias[indice + 1]

                    if primera["tipo"] == segunda["tipo"]:
                        continue

                    texto_entre = texto_local[primera["fin"]:segunda["inicio"]]

                    if re.search(r"\\b(?:pero|sin embargo|aunque)\\b", texto_entre, flags=re.IGNORECASE):
                        continue

                    if not re.search(r"\\b(?:y|luego|posteriormente)\\b", texto_entre, flags=re.IGNORECASE):
                        continue

                    segmento_segunda = texto_local[segunda["fin"]:]
                    segmento_segunda = re.split(r"[.!?;]", segmento_segunda, maxsplit=1)[0]

                    estado_segunda = clasificar_segmento(segmento_segunda)

                    if estado_segunda is None:
                        continue

                    if (
                        primera["tipo"] == modalidad
                        or segunda["tipo"] == modalidad
                    ):
                        return estado_segunda
'''

bloque_nuevo = '''            if len(ocurrencias) >= 2:
                for indice in range(len(ocurrencias) - 1):
                    primera = ocurrencias[indice]
                    segunda = ocurrencias[indice + 1]

                    if primera["tipo"] == segunda["tipo"]:
                        continue

                    texto_entre = texto_local[primera["fin"]:segunda["inicio"]]

                    if re.search(
                        r"\\b(?:pero|sin embargo|aunque)\\b",
                        texto_entre,
                        flags=re.IGNORECASE,
                    ):
                        continue

                    if not re.search(
                        r"\\b(?:y|luego|posteriormente)\\b",
                        texto_entre,
                        flags=re.IGNORECASE,
                    ):
                        continue

                    segmento_segunda = texto_local[segunda["fin"]:]
                    segmento_segunda = re.split(
                        r"[.!?;]",
                        segmento_segunda,
                        maxsplit=1,
                    )[0]

                    estado_segunda = clasificar_segmento(segmento_segunda)

                    if estado_segunda is None:
                        continue

                    # ALCANCE TEMPORAL:
                    #
                    # 1. "A y B fuera/dentro del plazo"
                    #    -> la condición temporal se considera compartida.
                    #
                    # 2. "A y posteriormente B fuera/dentro del plazo"
                    #    -> la condición temporal pertenece a B.
                    #
                    # 3. "A y luego B fuera/dentro del plazo"
                    #    -> la condición temporal pertenece a B.
                    #
                    # Por ello, NO se propaga el estado de B hacia A
                    # cuando el conector expresa secuencia explícita.

                    if re.search(
                        r"\\b(?:luego|posteriormente)\\b",
                        texto_entre,
                        flags=re.IGNORECASE,
                    ):
                        if segunda["tipo"] == modalidad:
                            return estado_segunda
                        continue

                    if (
                        primera["tipo"] == modalidad
                        or segunda["tipo"] == modalidad
                    ):
                        return estado_segunda
'''

cantidad = texto.count(bloque_anterior)

if cantidad != 1:
    raise SystemExit(
        f"ERROR: se esperaba encontrar exactamente 1 bloque. "
        f"Encontrados: {cantidad}"
    )

texto_nuevo = texto.replace(bloque_anterior, bloque_nuevo, 1)

ruta.write_text(texto_nuevo, encoding="utf-8")

print("OK: bloque de alcance temporal reemplazado.")
print(f"Archivo: {ruta}")
