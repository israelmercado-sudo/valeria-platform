from pathlib import Path

ruta = Path("./app/core/typification_engine.py")
texto = ruta.read_text(encoding="utf-8")

bloque_antiguo = '''        if any(contiene(p) for p in [
            r"\\bno fue presentado\\b",
            r"\\bno fue presentada\\b",
            r"\\bno present[oó]\\b",
            r"\\bno se present[oó]\\b",
            r"\\bomiti[oó] presentar\\b",
            r"\\bomiti[oó] la presentaci[oó]n\\b"
        ]):
            agregar("NO PRESENTACIÓN")
'''

bloque_nuevo = '''        if any(contiene(p) for p in [
            r"\\bno fue presentado\\b",
            r"\\bno fue presentada\\b",
            r"\\bno fueron presentados\\b",
            r"\\bno fueron presentadas\\b",
            r"\\bno present[oó]\\b",
            r"\\bno se present[oó]\\b",
            r"\\bomiti[oó] presentar\\b",
            r"\\bomiti[oó] la presentaci[oó]n\\b"
        ]):
            agregar("NO PRESENTACIÓN")
'''

if bloque_antiguo not in texto:
    raise SystemExit("ERROR: No se encontró exactamente el bloque de NO PRESENTACIÓN. NO SE MODIFICÓ EL ARCHIVO.")

texto = texto.replace(bloque_antiguo, bloque_nuevo, 1)
ruta.write_text(texto, encoding="utf-8")

print("CORRECCIÓN APLICADA")
print("Se agregaron las formas plurales de NO PRESENTACIÓN.")
