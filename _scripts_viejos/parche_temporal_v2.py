from pathlib import Path

archivo = Path(r".\app\core\typification_engine_v352_work.py")

texto = archivo.read_text(encoding="utf-8")

viejo = '''        r"\\bno\\s+(?:fue\\s+|se\\s+)?(?:elaborad[oa]|remitid[oa]|presentad[oa]|realizad[oa]|cumpli[oó])\\b.{0,80}\\b(?:oportunamente|de manera oportuna)\\b",
'''

nuevo = '''        r"\\bno\\s+(?:fue\\s+|se\\s+)?(?:elaborad[oa]|elabor[oó]|remitid[oa]|remiti[oó]|presentad[oa]|present[oó]|realizad[oa]|realiz[oó]|cumpli[oó])\\b.{0,80}\\b(?:oportunamente|de manera oportuna)\\b",
'''

if viejo not in texto:
    raise SystemExit("ERROR: no se encontró exactamente el patrón esperado.")

texto = texto.replace(viejo, nuevo, 1)

archivo.write_text(texto, encoding="utf-8")

print("OK: corrección temporal para formas verbales simples aplicada.")
