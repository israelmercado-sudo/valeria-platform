from pathlib import Path

ruta = Path(r".\app\core\typification_engine_v352_work.py")
texto = ruta.read_text(encoding="utf-8")

buscado = r'            r"\bno se remiti[oó]\b"'
reemplazo = (
    r'            r"\bno se remiti[oó]\b",' + "\n"
    + r'            r"\bni\s+se\s+remiti[oó]\b"'
)

if buscado not in texto:
    raise SystemExit("ERROR: no se encontró el bloque esperado. NO se modificó el archivo.")

texto = texto.replace(buscado, reemplazo, 1)

ruta.write_text(texto, encoding="utf-8")
print("PARCHE REMISIÓN NEGADA APLICADO CORRECTAMENTE")
