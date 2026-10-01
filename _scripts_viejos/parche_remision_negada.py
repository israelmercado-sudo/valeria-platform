from pathlib import Path

archivo = Path(r".\app\core\typification_engine_v352_work.py")
texto = archivo.read_text(encoding="utf-8")

viejo = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue remitido\\b",
            r"\\bno fue remitida\\b",
            r"\\bno fueron remitidos\\b",
            r"\\bno fueron remitidas\\b"
        ]) and not falta_acreditacion_temporal["REMISIÓN"]:
            agregar("REMISIÓN")
'''

nuevo = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue remitido\\b",
            r"\\bno fue remitida\\b",
            r"\\bno fueron remitidos\\b",
            r"\\bno fueron remitidas\\b",
            r"\\bno se remiti[oó]\\b"
        ]) and not falta_acreditacion_temporal["REMISIÓN"]:
            agregar("REMISIÓN")
'''

if viejo not in texto:
    raise SystemExit("ERROR: no se encontró exactamente el bloque de REMISIÓN.")

texto = texto.replace(viejo, nuevo, 1)

archivo.write_text(texto, encoding="utf-8")

print("OK: corrección de REMISIÓN negada aplicada.")
