from pathlib import Path

ruta = Path(r".\app\core\typification_engine_v352_work.py")
texto = ruta.read_text(encoding="utf-8")

buscado = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue remitido\\b",
            r"\\bno fue remitida\\b",
            r"\\bno fueron remitidos\\b",
            r"\\bno fueron remitidas\\b",
            r"\\bno se remiti[oó]\\b"
        ]) and not falta_acreditacion_temporal["REMISIÓN"]:
'''

reemplazo = '''        ) and not any(contiene(p) for p in [
            r"\\bno fue remitido\\b",
            r"\\bno fue remitida\\b",
            r"\\bno fueron remitidos\\b",
            r"\\bno fueron remitidas\\b",
            r"\\bno se remiti[oó]\\b",
            r"\\bni\\s+se\\s+remiti[oó]\\b"
        ]) and not falta_acreditacion_temporal["REMISIÓN"]:
'''

if buscado not in texto:
    raise SystemExit("ERROR: no se encontró exactamente el bloque positivo de REMISIÓN. NO se modificó el archivo.")

texto = texto.replace(buscado, reemplazo, 1)

ruta.write_text(texto, encoding="utf-8")
print("PARCHE POSITIVO REMISIÓN APLICADO CORRECTAMENTE")
