from pathlib import Path

ruta = Path("./app/core/typification_engine.py")
texto = ruta.read_text(encoding="utf-8")

bloque_antiguo = '''        if contiene(r"\\bpresent[oó]\\b") and not contiene(r"\\bno present[oó]\\b"):
            agregar("PRESENTACIÓN")
'''

bloque_nuevo = '''        # PRESENTACIÓN: formas activas y pasivas.
        # Se excluyen expresamente las construcciones negativas.
        if (
            (
                contiene(r"\\bpresent[oó]\\b")
                and not contiene(r"\\bno present[oó]\\b")
            )
            or
            (
                contiene(r"\\bfue presentado\\b")
                or contiene(r"\\bfue presentada\\b")
                or contiene(r"\\bfueron presentados\\b")
                or contiene(r"\\bfueron presentadas\\b")
            )
        ) and not any(contiene(p) for p in [
            r"\\bno fue presentado\\b",
            r"\\bno fue presentada\\b",
            r"\\bno fueron presentados\\b",
            r"\\bno fueron presentadas\\b"
        ]):
            agregar("PRESENTACIÓN")
'''

if bloque_antiguo not in texto:
    raise SystemExit("ERROR: No se encontró exactamente el bloque de PRESENTACIÓN. NO SE MODIFICÓ EL ARCHIVO.")

texto = texto.replace(bloque_antiguo, bloque_nuevo, 1)
ruta.write_text(texto, encoding="utf-8")

print("CORRECCIÓN V3.4.3.1 APLICADA")
print("Se amplió la detección de PRESENTACIÓN a formas activas y pasivas.")
