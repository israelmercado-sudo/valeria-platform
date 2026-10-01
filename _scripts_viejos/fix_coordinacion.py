from pathlib import Path

ruta = Path("./app/core/typification_engine.py")
texto = ruta.read_text(encoding="utf-8")

bloque_antiguo = '''        if any(contiene(p) for p in [
            r"\\bno fue elaborado\\b",
            r"\\bno fue elaborada\\b",
            r"\\bno elabor[oó]\\b",
            r"\\bno se elabor[oó]\\b",
            r"\\bomiti[oó] elaborar\\b",
            r"\\bomiti[oó] la elaboraci[oó]n\\b"
        ]):
            agregar("NO ELABORACIÓN")
'''

bloque_nuevo = '''        if any(contiene(p) for p in [
            r"\\bno fue elaborado\\b",
            r"\\bno fue elaborada\\b",
            r"\\bno elabor[oó]\\b",
            r"\\bno se elabor[oó]\\b",
            r"\\bomiti[oó] elaborar\\b",
            r"\\bomiti[oó] la elaboraci[oó]n\\b"
        ]):
            agregar("NO ELABORACIÓN")

        # Coordinación negativa: "no fue elaborado ni remitido"
        if any(contiene(p) for p in [
            r"\\bno fue elaborado\\s+ni\\s+remitido\\b",
            r"\\bno fue elaborada\\s+ni\\s+remitida\\b",
            r"\\bno fue elaborado\\s+ni\\s+enviado\\b",
            r"\\bno fue elaborada\\s+ni\\s+enviada\\b"
        ]):
            agregar("NO REMISIÓN")
'''

if bloque_antiguo not in texto:
    raise SystemExit("ERROR: No se encontró exactamente el bloque esperado. NO SE MODIFICÓ EL ARCHIVO.")

texto = texto.replace(bloque_antiguo, bloque_nuevo, 1)
ruta.write_text(texto, encoding="utf-8")

print("CORRECCIÓN V3.4.3.1 APLICADA")
print("Se agregó detección de NO REMISIÓN en coordinación negativa.")
