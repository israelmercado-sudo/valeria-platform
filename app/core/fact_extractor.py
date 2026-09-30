import re
from datetime import datetime


class FactExtractor:

    MESES = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "setiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12,
    }

    def extraer(self, texto: str):

        fechas = []
        hechos = []

        # =========================================================
        # 1. FECHAS NUMERICAS
        # =========================================================
        #
        # Reconoce:
        # 15/01/2022
        # 15-01-2022
        # 15.01.2022
        #
        # =========================================================

        patron_fecha_numerica = re.compile(
            r"\b(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{4})\b"
        )

        for coincidencia in patron_fecha_numerica.finditer(texto):

            dia = int(coincidencia.group(1))
            mes = int(coincidencia.group(2))
            anio = int(coincidencia.group(3))

            try:

                fecha = datetime(
                    anio,
                    mes,
                    dia
                ).strftime("%Y-%m-%d")

                fechas.append({
                    "texto": coincidencia.group(0),
                    "fecha": fecha
                })

            except ValueError:
                continue

        # =========================================================
        # 2. FECHAS CON NOMBRE DEL MES
        # =========================================================
        #
        # Reconoce:
        # 15 de enero de 2022
        # 15 de enero del 2022
        # 15 de Enero de 2022
        #
        # =========================================================

        patron_fecha_texto = re.compile(
            r"\b(\d{1,2})\s+de\s+"
            r"(enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
            r"septiembre|setiembre|octubre|noviembre|diciembre)"
            r"\s+(?:de|del)\s+(\d{4})\b",
            re.IGNORECASE
        )

        for coincidencia in patron_fecha_texto.finditer(texto):

            dia = int(coincidencia.group(1))
            nombre_mes = coincidencia.group(2).lower()
            anio = int(coincidencia.group(3))

            mes = self.MESES[nombre_mes]

            try:

                fecha = datetime(
                    anio,
                    mes,
                    dia
                ).strftime("%Y-%m-%d")

                fechas.append({
                    "texto": coincidencia.group(0),
                    "fecha": fecha
                })

            except ValueError:
                continue

        # =========================================================
        # 3. ELIMINAR FECHAS DUPLICADAS
        # =========================================================

        fechas_unicas = []
        fechas_vistas = set()

        for item in fechas:

            clave = (
                item["fecha"],
                item["texto"]
            )

            if clave not in fechas_vistas:

                fechas_vistas.add(clave)
                fechas_unicas.append(item)

        fechas = fechas_unicas

        # =========================================================
        # 4. ORDENAR LAS FECHAS SEGUN SU POSICION EN EL TEXTO
        # =========================================================
        #
        # Esto evita que las fechas se reordenen simplemente
        # por año o por fecha cronologica.
        #
        # =========================================================

        def posicion_fecha(item):

            posicion = texto.find(item["texto"])

            if posicion == -1:
                return 999999

            return posicion

        fechas.sort(key=posicion_fecha)

        # =========================================================
        # 5. IDENTIFICAR HECHOS RELEVANTES
        # =========================================================

        texto_lower = texto.lower()

        if "falta" in texto_lower or "conducta" in texto_lower:
            hechos.append(
                "Posible fecha de comisión de la conducta"
            )

        if (
            "recursos humanos" in texto_lower
            or "rr. hh." in texto_lower
            or "rr.hh." in texto_lower
            or "rrhh" in texto_lower
        ):
            hechos.append(
                "Fecha de conocimiento de los hechos por la Oficina de Recursos Humanos"
            )

        if "inicio" in texto_lower and "pad" in texto_lower:
            hechos.append(
                "Fecha de inicio del procedimiento administrativo disciplinario"
            )

        if "notific" in texto_lower:
            hechos.append(
                "Fecha de notificación del acto correspondiente"
            )

        # =========================================================
        # 6. RETORNO
        # =========================================================

        return {
            "texto_original": texto,
            "fechas": fechas,
            "hechos_relevantes": hechos
        }


fact_extractor = FactExtractor()