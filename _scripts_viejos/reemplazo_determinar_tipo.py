def _determinar_tipo_conducta(self, conducta: str) -> str:
        """
        Clasificación preliminar de la conducta.

        V3.5 - Segmentación por eventos:
        - Divide la conducta en eventos independientes (etapa + estado).
        - Distingue elaboración y remisión/presentación.
        - Detecta incumplimientos múltiples.
        - Detecta omisiones específicas (no remisión, no elaboración).
        - Mantiene compatibilidad con clasificación de ACCIÓN / OMISIÓN.
        - No constituye calificación jurídica definitiva.
        """
        texto = (conducta or "").lower().strip()

        # ---------------------------------------------------------
        # 1. SEGMENTACIÓN POR EVENTOS
        # ---------------------------------------------------------
        eventos = self._parsear_eventos(texto)

        # ---------------------------------------------------------
        # 2. SI HAY EVENTOS CON INCUMPLIMIENTO, DEVOLVER TIPO COMPUESTO
        # ---------------------------------------------------------
        etapas_incumplidas = [
            (etapa, estado) for (etapa, estado) in eventos
            if estado in ("FUERA_DE_PLAZO", "NO_EJECUTADO")
        ]

        if etapas_incumplidas:
            partes = []
            for etapa, estado in etapas_incumplidas:
                if etapa == "ELABORACION" and estado == "FUERA_DE_PLAZO":
                    partes.append("INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)")
                elif etapa == "REMISION" and estado == "FUERA_DE_PLAZO":
                    partes.append("INCUMPLIMIENTO DE PLAZO (REMISIÓN)")
                elif etapa == "REMISION" and estado == "NO_EJECUTADO":
                    partes.append("OMISIÓN - NO REMISIÓN")
                elif etapa == "ELABORACION" and estado == "NO_EJECUTADO":
                    partes.append("OMISIÓN - NO ELABORACIÓN")

            if partes:
                return " + ".join(partes)

        # ---------------------------------------------------------
        # 3. SI HAY EVENTOS CON CUMPLIMIENTO Y NO HAY INCUMPLIMIENTOS
        # ---------------------------------------------------------
        if eventos:
            return "CUMPLIMIENTO"

        # ---------------------------------------------------------
        # 4. FALLBACK A LA LÓGICA ANTERIOR
        # ---------------------------------------------------------

        indicadores_cumplimiento = [
            "cumplió", "cumplio",
            "cumplió oportunamente", "cumplio oportunamente",
            "cumplió dentro del plazo", "cumplio dentro del plazo",
            "presentó dentro del plazo", "presento dentro del plazo",
            "remitió dentro del plazo", "remitio dentro del plazo",
            "elaboró dentro del plazo", "elaboro dentro del plazo",
        ]
        if any(indicador in texto for indicador in indicadores_cumplimiento):
            return "CUMPLIMIENTO"

        indicadores_omision = [
            "no realizó", "no realizo", "no cumplió", "no cumplio",
            "no efectuó", "no efectuo", "no informó", "no informo",
            "no comunicó", "no comunico", "no atendió", "no atendio",
            "no verificó", "no verifico", "no aprobó", "no aprobo",
            "no emitió", "no emitio", "dejó de", "dejo de",
            "incumplió", "incumplio", "omitió", "omitio",
        ]
        if any(indicador in texto for indicador in indicadores_omision):
            return "OMISIÓN"

        indicadores_accion = [
            "realizó", "realizo", "efectuó", "efectuo",
            "presentó", "presento", "autorizó", "autorizo",
            "emitió", "emitio", "dispuso", "ordenó", "ordeno",
            "suscribió", "suscribio", "remitió", "remitio",
            "comunicó", "comunico", "atendió", "atendio",
            "verificó", "verifico", "aprobó", "aprobo",
            "elaboró", "elaboro",
        ]
        if any(indicador in texto for indicador in indicadores_accion):
            return "ACCIÓN"

        return "NO DETERMINADO"