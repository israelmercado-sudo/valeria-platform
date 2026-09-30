from app.core.fact_extractor import fact_extractor


class LegalEngine:
    """
    Motor jurídico base de Valeria Platform.
    Especializado en Derecho Administrativo Peruano.
    """

    def analizar_materia(self, consulta: str):
        consulta_normalizada = consulta.lower().strip()

        if self._es_prescripcion(consulta_normalizada):
            return self._analizar_prescripcion(consulta)

        if self._es_pad(consulta_normalizada):
            return self._analizar_pad(consulta)

        return {
            "area": "Derecho Administrativo",
            "materia": "No determinada",
            "norma_base": [],
            "respuesta": (
                "La consulta requiere mayor información para determinar "
                "la materia jurídica aplicable."
            ),
            "hechos_relevantes": [],
            "cuestiones_juridicas": [],
            "requiere_verificacion": True
        }

    def _es_prescripcion(self, consulta: str) -> bool:
        terminos = [
            "prescripcion",
            "prescripción",
            "plazo prescriptorio",
            "plazo de prescripcion",
            "plazo de prescripción"
        ]

        return any(termino in consulta for termino in terminos)

    def _es_pad(self, consulta: str) -> bool:
        terminos = [
            "pad",
            "procedimiento administrativo disciplinario",
            "disciplinario"
        ]

        return any(termino in consulta for termino in terminos)

    def _analizar_prescripcion(self, consulta: str):
        extraccion = fact_extractor.extraer(consulta)

        return {
            "area": "Procedimiento Administrativo Disciplinario",
            "materia": "Prescripción",
            "norma_base": [
                "Ley N° 30057 - Ley del Servicio Civil",
                "Reglamento General de la Ley N° 30057"
            ],
            "respuesta": (
                "La consulta se refiere a la prescripción dentro de un "
                "procedimiento administrativo disciplinario."
            ),
            "fechas_detectadas": extraccion.get("fechas", []),
            "hechos_extraidos": extraccion.get("hechos_relevantes", []),
            "hechos_relevantes": [
                "Fecha de comisión de la presunta falta",
                "Fecha en que la Oficina de Recursos Humanos tomó conocimiento",
                "Fecha de inicio del procedimiento administrativo disciplinario",
                "Fecha de notificación del acto de inicio, cuando corresponda",
                "Régimen jurídico aplicable al servidor"
            ],
            "cuestiones_juridicas": [
                "Determinar qué regla de prescripción resulta aplicable",
                "Determinar desde qué momento debe efectuarse el cómputo",
                "Verificar si existen circunstancias que afecten el cómputo del plazo",
                "Determinar si el procedimiento fue iniciado dentro del plazo legal"
            ],
            "conclusion_preliminar": (
                "No es posible determinar si una falta se encuentra prescrita "
                "sin verificar las fechas extraídas y las circunstancias "
                "relevantes del caso."
            ),
            "requiere_verificacion": True
        }

    def _analizar_pad(self, consulta: str):
        extraccion = fact_extractor.extraer(consulta)

        return {
            "area": "Procedimiento Administrativo Disciplinario",
            "materia": "PAD",
            "norma_base": [
                "Ley N° 30057 - Ley del Servicio Civil",
                "Reglamento General de la Ley N° 30057"
            ],
            "respuesta": (
                "La consulta corresponde al análisis de un procedimiento "
                "administrativo disciplinario."
            ),
            "fechas_detectadas": extraccion.get("fechas", []),
            "hechos_extraidos": extraccion.get("hechos_relevantes", []),
            "hechos_relevantes": [
                "Conducta atribuida",
                "Fecha de los hechos",
                "Servidor presuntamente responsable",
                "Régimen jurídico aplicable"
            ],
            "cuestiones_juridicas": [
                "Determinar la conducta imputada",
                "Identificar la norma presuntamente infringida",
                "Determinar la responsabilidad administrativa correspondiente"
            ],
            "requiere_verificacion": True
        }


valeria_engine = LegalEngine()

