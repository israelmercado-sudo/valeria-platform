from pathlib import Path

archivo = Path(r".\app\core\typification_engine_v352_work.py")
texto = archivo.read_text(encoding="utf-8")

viejo = '''        if (
            (
                contiene(r"\\belabor[oó]\\b")
                and not contiene(r"\\bno elabor[oó]\\b")
            )
            or
            contiene(r"\\bfue elaborado\\b")
            or
            contiene(r"\\bfue elaborada\\b")
            or
            contiene(r"\\bfueron elaborados\\b")
            or
            contiene(r"\\bfueron elaboradas\\b")
        ) and not any(contiene(p) for p in [
            r"\\bno fue elaborado\\b",
            r"\\bno fue elaborada\\b",
            r"\\bno fueron elaborados\\b",
            r"\\bno fueron elaboradas\\b"
        ]):
            agregar("ELABORACIÓN")
'''

nuevo = '''        if (
            (
                contiene(r"\\belabor[oó]\\b")
                and not contiene(r"\\bno elabor[oó]\\b")
                and not contiene(r"\\bno se elabor[oó]\\b")
            )
            or
            contiene(r"\\bfue elaborado\\b")
            or
            contiene(r"\\bfue elaborada\\b")
            or
            contiene(r"\\bfueron elaborados\\b")
            or
            contiene(r"\\bfueron elaboradas\\b")
        ) and not any(contiene(p) for p in [
            r"\\bno fue elaborado\\b",
            r"\\bno fue elaborada\\b",
            r"\\bno fueron elaborados\\b",
            r"\\bno fueron elaboradas\\b",
            r"\\bno se elabor[oó]\\b"
        ]):
            agregar("ELABORACIÓN")
'''

if texto.count(viejo) != 1:
    print(f"ERROR: bloque de ELABORACIÓN encontrado {texto.count(viejo)} veces. NO se modificó el archivo.")
    raise SystemExit(1)

archivo.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
print("OK: corrección de ELABORACIÓN aplicada.")
