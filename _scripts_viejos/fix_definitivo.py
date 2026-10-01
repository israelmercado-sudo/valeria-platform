# fix_definitivo.py
from pathlib import Path

RUTA = Path(r'.\app\core\typification_engine.py')

NUEVO_BLOQUE = '''    def _parsear_eventos(self, conducta: str) -> list:
        """
        Segmenta la conducta en eventos independientes (etapa + estado temporal).
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
            # ELABORACION
            if "elaborado" in f or "elaboro" in f:
                if ("no fue elaborado" in f or "no se elaboro" in f
                        or "no elaboro" in f):
                    eventos.append(("ELABORACION", "NO_EJECUTADO"))
                elif "fuera del plazo" in f or "fuera de plazo" in f:
                    eventos.append(("ELABORACION", "FUERA_DE_PLAZO"))
                elif "dentro del plazo" in f:
                    eventos.append(("ELABORACION", "DENTRO_DE_PLAZO"))

            # REMISION / PRESENTACION
            if ("remitido" in f or "remitida" in f
                    or "presentado" in f or "presentada" in f
                    or "presento" in f):
                if ("no fue remitido" in f or "no fue remitida" in f
                        or "no fue presentado" in f
                        or "no fue presentada" in f
                        or "no presento" in f):
                    eventos.append(("REMISION", "NO_EJECUTADO"))
                elif "fuera del plazo" in f or "fuera de plazo" in f:
                    eventos.append(("REMISION", "FUERA_DE_PLAZO"))
                elif "dentro del plazo" in f:
                    eventos.append(("REMISION", "DENTRO_DE_PLAZO"))

        return eventos

    def _determinar_tipo_conducta(self, conducta: str) -> str:
        """
        Clasificacion preliminar de la conducta.

        V3.5 - Segmentacion por eventos.
        """
        texto = (conducta or "").lower().strip()

        # 1. SEGMENTACION POR EVENTOS
        eventos = self._parsear_eventos(texto)

        # 2. SI HAY INCUMPLIMIENTOS, DEVOLVER TIPO COMPUESTO
        etapas_incumplidas = [
            (etapa, estado) for (etapa, estado) in eventos
            if estado in ("FUERA_DE_PLAZO", "NO_EJECUTADO")
        ]

        if etapas_incumplidas:
            partes = []
            for etapa, estado in etapas_incumplidas:
                if etapa == "ELABORACION" and estado == "FUERA_DE_PLAZO":
                    partes.append("INCUMPLIMIENTO DE PLAZO (ELABORACION)")
                elif etapa == "REMISION" and estado == "FUERA_DE_PLAZO":
                    partes.append("INCUMPLIMIENTO DE PLAZO (REMISION)")
                elif etapa == "REMISION" and estado == "NO_EJECUTADO":
                    partes.append("OMISION - NO REMISION")
                elif etapa == "ELABORACION" and estado == "NO_EJECUTADO":
                    partes.append("OMISION - NO ELABORACION")

            if partes:
                return " + ".join(partes)

        # 3. SI HAY EVENTOS SIN INCUMPLIMIENTO
        if eventos:
            return "CUMPLIMIENTO"

        # 4. FALLBACK: LOGICA ANTERIOR
        indicadores_cumplimiento = [
            "cumplio", "cumplio oportunamente",
            "cumplio dentro del plazo",
            "presento dentro del plazo",
            "remitio dentro del plazo",
            "elaboro dentro del plazo",
        ]
        if any(indicador in texto for indicador in indicadores_cumplimiento):
            return "CUMPLIMIENTO"

        indicadores_omision = [
            "no realizo", "no cumplio", "no efectuo",
            "no informo", "no comunico", "no atendio",
            "no verifico", "no aprobo", "no emitio",
            "dejo de", "incumplio", "omitio",
        ]
        if any(indicador in texto for indicador in indicadores_omision):
            return "OMISION"

        indicadores_accion = [
            "realizo", "efectuo", "presento", "autorizo",
            "emitio", "dispuso", "ordeno", "suscribio",
            "remitio", "comunico", "atendio", "verifico",
            "aprobo", "elaboro",
        ]
        if any(indicador in texto for indicador in indicadores_accion):
            return "ACCION"

        return "NO DETERMINADO"

'''

contenido = RUTA.read_text(encoding='utf-8-sig')

inicio = contenido.find('    def _parsear_eventos(')
fin = contenido.find('    def _extraer_modalidades_conducta(')

if inicio == -1 or fin == -1 or fin <= inicio:
    print('ERROR: no se encontraron los marcadores')
    exit(1)

contenido_nuevo = contenido[:inicio] + NUEVO_BLOQUE + contenido[fin:]
RUTA.write_text(contenido_nuevo, encoding='utf-8')
print('Fix aplicado')