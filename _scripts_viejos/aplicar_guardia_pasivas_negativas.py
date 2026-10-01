from pathlib import Path

p = Path.cwd() / "app" / "core" / "typification_engine_v352_work.py"
s = p.read_text(encoding="utf-8")

viejo = '''        for patron, contenido in actuaciones:
            if re.search(patron, hecho_lower):
                # La comunicación ya tiene una descripción específica.
                # No duplicamos otra actuación de comunicación.
                if contenido != "Comunicación realizada por el servidor a otro servidor.":'''

nuevo = '''        for patron, contenido in actuaciones:
            if re.search(patron, hecho_lower):

                # Las formas pasivas positivas no deben activarse
                # cuando forman parte de una construcción negativa.
                # Ej.: "no fue presentado", "no fue remitido",
                # "no fue elaborado".
                if contenido == "Presentación de documento" and re.search(
                    r"\\bno fue presentado\\b|\\bno fue presentada\\b|\\bno fueron presentados\\b|\\bno fueron presentadas\\b",
                    hecho_lower,
                ):
                    continue

                if contenido == "Remisión de documento o expediente" and re.search(
                    r"\\bno fue remitido\\b|\\bno fue remitida\\b|\\bno fueron remitidos\\b|\\bno fueron remitidas\\b",
                    hecho_lower,
                ):
                    continue

                if contenido == "Elaboración de documento" and re.search(
                    r"\\bno fue elaborado\\b|\\bno fue elaborada\\b|\\bno fueron elaborados\\b|\\bno fueron elaboradas\\b",
                    hecho_lower,
                ):
                    continue

                # La comunicación ya tiene una descripción específica.
                # No duplicamos otra actuación de comunicación.
                if contenido != "Comunicación realizada por el servidor a otro servidor.":'''

if viejo not in s:
    raise SystemExit("BLOQUE OBJETIVO NO ENCONTRADO. NO SE MODIFICO EL ARCHIVO.")

p.write_text(s.replace(viejo, nuevo, 1), encoding="utf-8")
print("BARRERA NEGATIVA APLICADA")
