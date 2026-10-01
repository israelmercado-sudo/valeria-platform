from pathlib import Path

ruta = Path(r".\app\core\typification_engine_v352_work.py")
texto = ruta.read_text(encoding="utf-8")

original = texto

texto = texto.replace(
    'r"\\bno remiti[oó]\\b",\n            r"\\bno fue remitido\\b",',
    'r"\\bno remiti[oó]\\b",\n            r"\\bni\\s+se\\s+remiti[oó]\\b",\n            r"\\bno fue remitido\\b",',
    1
)

texto = texto.replace(
    'r"\\bno elabor[oó]\\b",\n            r"\\bno fue elaborado\\b",',
    'r"\\bno elabor[oó]\\b",\n            r"\\bni\\s+se\\s+elabor[oó]\\b",\n            r"\\bno fue elaborado\\b",',
    1
)

texto = texto.replace(
    'r"\\bno remiti[oó]\\b.{0,100}\\bdentro del plazo\\b",\n    r"\\bno elabor[oó]\\b.{0,100}\\bdentro del plazo\\b"',
    'r"\\bno remiti[oó]\\b.{0,100}\\bdentro del plazo\\b",\n    r"\\bni\\s+se\\s+remiti[oó]\\b.{0,100}\\bdentro del plazo\\b",\n    r"\\bno elabor[oó]\\b.{0,100}\\bdentro del plazo\\b",\n    r"\\bni\\s+se\\s+elabor[oó]\\b.{0,100}\\bdentro del plazo\\b"',
    1
)

if texto == original:
    raise SystemExit("ERROR: no se encontró alguno de los bloques esperados. NO se modificó el archivo.")

ruta.write_text(texto, encoding="utf-8")
print("PARCHE APLICADO CORRECTAMENTE")
