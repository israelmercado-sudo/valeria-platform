from pathlib import Path

path = Path("app/core/typification_engine.py")
texto = path.read_text(encoding="utf-8")

viejo = '''                "no presentó",
                "no presento",
                "no presentó",
                "omitió",
'''

nuevo = '''                "no presentó",
                "no presento",
                "no fue presentado",
                "no se presentó",
                "no fue entregado",
                "no se entregó",
                "no fue remitido",
                "no se remitió",
                "no fue realizado",
                "no se realizó",
                "no fue cumplido",
                "no se cumplió",
                "omitió",
'''

if viejo not in texto:
    raise SystemExit("ERROR: No se encontró el bloque esperado.")

texto = texto.replace(viejo, nuevo, 1)

path.write_text(texto, encoding="utf-8")

print("CORRECCIÓN V3.2.1 APLICADA")
