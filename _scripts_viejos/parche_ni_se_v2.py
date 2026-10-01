from pathlib import Path

ruta = Path(r".\app\core\typification_engine_v352_work.py")
texto = ruta.read_text(encoding="utf-8")

original = texto

# 1. El "ni se..." debe prevalecer como incumplimiento temporal.
texto = texto.replace(
    r'            r"\bno fue remitido\b.{0,100}\bdentro del plazo\b",',
    r'            r"\bno fue remitido\b.{0,100}\bdentro del plazo\b",' + "\n"
    + r'            r"\bni\s+se\s+remiti[oó]\b.{0,100}\bdentro del plazo\b",',
    1
)

texto = texto.replace(
    r'            r"\bno fue elaborado\b.{0,100}\bdentro del plazo\b",',
    r'            r"\bno fue elaborado\b.{0,100}\bdentro del plazo\b",' + "\n"
    + r'            r"\bni\s+se\s+elabor[oó]\b.{0,100}\bdentro del plazo\b",',
    1
)

# 2. "ni se remitió" es negación de REMISIÓN, no REMISIÓN positiva.
texto = texto.replace(
    r'            r"\bno se remiti[oó]\b"',
    r'            r"\bno se remiti[oó]\b",' + "\n"
    + r'            r"\bni\s+se\s+remiti[oó]\b"',
    1
)

if texto == original:
    raise SystemExit("ERROR: no se encontró ningún bloque esperado. NO se modificó el archivo.")

ruta.write_text(texto, encoding="utf-8")
print("PARCHE APLICADO CORRECTAMENTE")
