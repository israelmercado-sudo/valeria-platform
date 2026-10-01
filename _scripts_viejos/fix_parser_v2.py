# fix_parser_v2.py
from pathlib import Path

RUTA = Path(r'.\app\core\typification_engine.py')

# Reemplazar _parsear_eventos completo por una version ampliada
NUEVO_PARSER = '''    def _parsear_eventos(self, conducta: str) -> list:
        """
        Segmenta la conducta en eventos independientes (etapa + estado temporal).

        Detecta:
        - Formas pasivas: "fue elaborado", "fue remitido", "fue presentado"
        - Formas reflexivas/activas: "se elaboro", "se remitio", "se presento"
        - Formas sin acento: "elaboro", "remitio", "presento"
        """
        t = (conducta or "").lower()

        separadores = [
            " y posteriormente ",
            " posteriormente ",
            " pero ",
            " y luego ",
            " y ",
        ]
        fragmentos = [t]
        for sep in separadores:
            nuevos = []
            for f in fragmentos:
                nuevos.extend(f.split(sep))
            fragmentos = nuevos

        fragmentos = [
            f.strip().strip(",").strip(".") for f in fragmentos if f.strip()
        ]

        eventos = []

        for f in fragmentos:
            # ---- ELABORACION ----
            # Disparadores: elaborado, elaboro, elaboró, se elaboro, se elaboró
            tiene_elab = any(x in f for x in [
                "elaborado", "elaboro", "elaboró", "se elaboro", "se elaboró"
            ])

            if tiene_elab:
                if any(x in f for x in [
                    "no fue elaborado", "no se elaboro", "no se elaboró",
                    "no elaboro", "no elaboró"
                ]):
                    eventos.append(("ELABORACION", "NO_EJECUTADO"))
                elif "fuera del plazo" in f or "fuera de plazo" in f:
                    eventos.append(("ELABORACION", "FUERA_DE_PLAZO"))
                elif "dentro del plazo" in f:
                    eventos.append(("ELABORACION", "DENTRO_DE_PLAZO"))

            # ---- REMISION / PRESENTACION ----
            # Disparadores: remitido, remitio, remitió, se remitio, se remitió,
            #               presentado, presento, presentó, se presento, se presentó
            tiene_rem = any(x in f for x in [
                "remitido", "remitida", "remitio", "remitió",
                "se remitio", "se remitió",
                "presentado", "presentada", "presento", "presentó",
                "se presento", "se presentó"
            ])

            if tiene_rem:
                if any(x in f for x in [
                    "no fue remitido", "no fue remitida",
                    "no se remitio", "no se remitió",
                    "no remitio", "no remitió",
                    "no fue presentado", "no fue presentada",
                    "no se presento", "no se presentó",
                    "no presento", "no presentó"
                ]):
                    eventos.append(("REMISION", "NO_EJECUTADO"))
                elif "fuera del plazo" in f or "fuera de plazo" in f:
                    eventos.append(("REMISION", "FUERA_DE_PLAZO"))
                elif "dentro del plazo" in f:
                    eventos.append(("REMISION", "DENTRO_DE_PLAZO"))

        return eventos
'''

contenido = RUTA.read_text(encoding='utf-8-sig')

inicio = contenido.find('    def _parsear_eventos(')
fin = contenido.find('    def _determinar_tipo_conducta(')

if inicio == -1 or fin == -1 or fin <= inicio:
    print('ERROR: no se encontraron los marcadores')
    exit(1)

contenido_nuevo = contenido[:inicio] + NUEVO_PARSER + '\n' + contenido[fin:]
RUTA.write_text(contenido_nuevo, encoding='utf-8')
print('Parser v2 aplicado')
