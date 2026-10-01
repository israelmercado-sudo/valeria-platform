from pathlib import Path

archivo = Path(r".\app\core\typification_engine_v352_work.py")
texto = archivo.read_text(encoding="utf-8")

marcador = '''        # 3. CONDUCTAS POSITIVAS
'''

bloque_nuevo = '''        # =========================================================
        # CONTROL DE ACREDITACIÓN TEMPORAL
        # =========================================================
        # "No se acredita cuándo fue elaborado/remitido..." no
        # acredita por sí mismo la realización del acto.
        #
        # La regla solo opera cuando "no se acredita" aparece
        # ANTES de la referencia al acto. Esto permite conservar
        # casos como:
        # "El informe fue elaborado, pero no se acredita cuándo."
        #
        falta_acreditacion_temporal = {
            "ELABORACIÓN": False,
            "REMISIÓN": False,
        }

        for coincidencia in re.finditer(
            r"\\bno\\s+se\\s+acredita\\b",
            texto,
            flags=re.IGNORECASE,
        ):
            resto = texto[coincidencia.end():coincidencia.end() + 160]

            if re.search(
                r"\\b(?:cu[aá]ndo|fecha(?:\\s+en\\s+que)?|fecha\\s+de)\\b"
                r".{0,100}\\b(?:fue\\s+elaborad[oa]|se\\s+elabor[oó]|"
                r"elaboraci[oó]n)\\b",
                resto,
                flags=re.IGNORECASE,
            ):
                falta_acreditacion_temporal["ELABORACIÓN"] = True

            if re.search(
                r"\\b(?:cu[aá]ndo|fecha(?:\\s+en\\s+que)?|fecha\\s+de)\\b"
                r".{0,100}\\b(?:fue\\s+remitid[oa]|se\\s+remiti[oó]|"
                r"remisi[oó]n)\\b",
                resto,
                flags=re.IGNORECASE,
            ):
                falta_acreditacion_temporal["REMISIÓN"] = True

        # 3. CONDUCTAS POSITIVAS
'''

if marcador not in texto:
    raise SystemExit("ERROR: no se encontró el marcador de CONDUCTAS POSITIVAS.")

texto = texto.replace(marcador, bloque_nuevo, 1)

viejo_elaboracion = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue elaborado\\b",
            r"\\bno fue elaborada\\b",
            r"\\bno fueron elaborados\\b",
            r"\\bno fueron elaboradas\\b",
            r"\\bno se elabor[oó]\\b"
        ]):
            agregar("ELABORACIÓN")
'''

nuevo_elaboracion = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue elaborado\\b",
            r"\\bno fue elaborada\\b",
            r"\\bno fueron elaborados\\b",
            r"\\bno fueron elaboradas\\b",
            r"\\bno se elabor[oó]\\b"
        ]) and not falta_acreditacion_temporal["ELABORACIÓN"]:
            agregar("ELABORACIÓN")
'''

if viejo_elaboracion not in texto:
    raise SystemExit("ERROR: no se encontró exactamente el bloque de ELABORACIÓN.")

texto = texto.replace(viejo_elaboracion, nuevo_elaboracion, 1)

viejo_remision = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue remitido\\b",
            r"\\bno fue remitida\\b",
            r"\\bno fueron remitidos\\b",
            r"\\bno fueron remitidas\\b"
        ]):
            agregar("REMISIÓN")
'''

nuevo_remision = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue remitido\\b",
            r"\\bno fue remitida\\b",
            r"\\bno fueron remitidos\\b",
            r"\\bno fueron remitidas\\b"
        ]) and not falta_acreditacion_temporal["REMISIÓN"]:
            agregar("REMISIÓN")
'''

if viejo_remision not in texto:
    raise SystemExit("ERROR: no se encontró exactamente el bloque de REMISIÓN.")

texto = texto.replace(viejo_remision, nuevo_remision, 1)

archivo.write_text(texto, encoding="utf-8")

print("OK: control de acreditación temporal aplicado.")
