from pathlib import Path

p = Path(r".\app\core\typification_engine.py")
texto = p.read_text(encoding="utf-8")

inicio = texto.index("    def _reconciliar_modalidades_temporales(")
fin = texto.index("    def _extraer_modalidades_conducta(", inicio)

nuevo = '''    def _reconciliar_modalidades_temporales(self, conducta: str) -> dict:
        """
        V3.5.2 - Reconciliación temporal por modalidad.

        Utiliza _parsear_eventos() como fuente única de eventos.

        Distingue:
            - modalidad positiva ejecutada;
            - modalidad negativa por NO_EJECUTADO;
            - componente temporal de cada modalidad.

        La temporalidad global se mantiene separada de la
        temporalidad específica de cada modalidad.
        """

        eventos = self._parsear_eventos(conducta)

        mapa_modalidad = {
            "ELABORACION": "ELABORACIÓN",
            "REMISION": "REMISIÓN",
            "PRESENTACION": "PRESENTACIÓN",
        }

        mapa_modalidad_negativa = {
            "ELABORACION": "NO ELABORACIÓN",
            "REMISION": "NO REMISIÓN",
            "PRESENTACION": "NO PRESENTACIÓN",
        }

        mapa_estado = {
            "DENTRO_DE_PLAZO": "CUMPLIMIENTO DE PLAZO",
            "FUERA_DE_PLAZO": "INCUMPLIMIENTO DE PLAZO",
            "NO_EJECUTADO": "SIN INFORMACIÓN TEMPORAL",
            "SIN_INFORMACION_TEMPORAL": "SIN INFORMACIÓN TEMPORAL",
        }

        modalidades = []
        detalles = []

        for etapa, estado in eventos:

            if estado == "NO_EJECUTADO":
                modalidad = mapa_modalidad_negativa.get(etapa)
            else:
                modalidad = mapa_modalidad.get(etapa)

            if modalidad is None:
                continue

            if modalidad not in modalidades:
                modalidades.append(modalidad)

            detalle = {
                "modalidad": modalidad,
                "componente_temporal": mapa_estado.get(
                    estado,
                    "SIN INFORMACIÓN TEMPORAL",
                ),
            }

            if not any(
                d["modalidad"] == modalidad
                for d in detalles
            ):
                detalles.append(detalle)

        # =========================================================
        # TEMPORALIDAD GLOBAL
        #
        # Prioridad:
        # 1. cualquier incumplimiento explícito;
        # 2. cualquier cumplimiento explícito;
        # 3. sin información temporal.
        #
        # NO_EJECUTADO no constituye por sí mismo una
        # clasificación temporal de cumplimiento/incumplimiento.
        # =========================================================

        estados = [estado for _, estado in eventos]

        if "FUERA_DE_PLAZO" in estados:
            componente_temporal = "INCUMPLIMIENTO DE PLAZO"
        elif "DENTRO_DE_PLAZO" in estados:
            componente_temporal = "CUMPLIMIENTO DE PLAZO"
        else:
            componente_temporal = "SIN INFORMACIÓN TEMPORAL"

        return {
            "modalidades": modalidades,
            "componente_temporal": componente_temporal,
            "modalidades_detalle": detalles,
        }

'''

p.write_text(texto[:inicio] + nuevo + texto[fin:], encoding="utf-8")

print("Reconciliador temporal reemplazado correctamente.")
