from app.core.fact_extractor import fact_extractor
from app.core.prescription_engine import prescription_engine
from datetime import date


class LegalEngine:

    def analizar_materia(self, consulta: str):

        resultado = {
            "area": "Derecho Administrativo",
            "materia": "No determinada",
            "norma_base": [],
            "regla_juridica": "",
            "respuesta": "",
            "fechas_detectadas": [],
            "hechos_extraidos": {},
            "hechos_relevantes": [],
            "cuestiones_juridicas": [],
            "calculo_prescripcion": None,
            "analisis": "",
            "conclusion_preliminar": "",
            "informacion_faltante": [],
            "requiere_verificacion": True
        }

        # ---------------------------------------------------------
        # 1. Extracción de hechos y fechas
        # ---------------------------------------------------------

        hechos = fact_extractor.extraer(consulta)

        resultado["hechos_extraidos"] = hechos
        resultado["fechas_detectadas"] = hechos.get("fechas", [])

        # ---------------------------------------------------------
        # 2. Normalización del texto
        # ---------------------------------------------------------

        texto = consulta.lower()

        # ---------------------------------------------------------
        # 3. Identificación del área
        # ---------------------------------------------------------

        indicadores_pad = [
            "procedimiento administrativo disciplinario",
            "pad",
            "falta disciplinaria",
            "servidor",
            "recursos humanos",
            "prescripcion",
            "prescripción",
            "prescrita",
            "prescrito"
        ]

        if any(indicador in texto for indicador in indicadores_pad):
            resultado["area"] = "Procedimiento Administrativo Disciplinario"

        # ---------------------------------------------------------
        # 4. Identificación de prescripción
        # ---------------------------------------------------------

        es_prescripcion = any(
            palabra in texto
            for palabra in [
                "prescripcion",
                "prescripción",
                "prescribe",
                "prescrita",
                "prescrito",
                "prescripcion"
            ]
        )

        if not es_prescripcion:
            return resultado

        resultado["area"] = "Procedimiento Administrativo Disciplinario"
        resultado["materia"] = "Prescripción"

        # ---------------------------------------------------------
        # 5. Normativa base
        # ---------------------------------------------------------

        resultado["norma_base"] = [
            "Ley N.° 30057 - Ley del Servicio Civil",
            "Artículo 94 de la Ley N.° 30057",
            "Reglamento General de la Ley N.° 30057",
            "Artículo 97.1 del Reglamento General de la Ley N.° 30057"
        ]

        # ---------------------------------------------------------
        # 6. Regla jurídica
        # ---------------------------------------------------------

        resultado["regla_juridica"] = (
            "La potestad disciplinaria prescribe conforme a las reglas "
            "establecidas en el artículo 94 de la Ley N.° 30057 y el "
            "artículo 97.1 de su Reglamento General. Para determinar "
            "la prescripción deben identificarse la fecha de comisión "
            "de la falta, la fecha de conocimiento por la Oficina de "
            "Recursos Humanos y las demás circunstancias que puedan "
            "incidir en el cómputo del plazo."
        )

        # ---------------------------------------------------------
        # 7. Hechos relevantes
        # ---------------------------------------------------------

        resultado["hechos_relevantes"] = [
            "Fecha de comisión de la presunta falta",
            "Fecha de conocimiento de los hechos por la Oficina de Recursos Humanos",
            "Fecha de inicio del procedimiento administrativo disciplinario",
            "Fecha de notificación del acto de inicio, cuando corresponda",
            "Régimen jurídico aplicable al servidor"
        ]

        # ---------------------------------------------------------
        # 8. Cuestiones jurídicas
        # ---------------------------------------------------------

        resultado["cuestiones_juridicas"] = [
            "Determinar la regla de prescripción aplicable",
            "Determinar desde qué fecha corresponde efectuar el cómputo",
            "Verificar si existen circunstancias que afecten el cómputo",
            "Determinar si la potestad disciplinaria se encuentra prescrita"
        ]

        # ---------------------------------------------------------
        # 9. Cálculo automático de prescripción
        # ---------------------------------------------------------

        fechas = resultado["fechas_detectadas"]

        if len(fechas) >= 2:

            try:

                fecha_comision = date.fromisoformat(
                    fechas[0]["fecha"]
                )

                fecha_conocimiento = date.fromisoformat(
                    fechas[1]["fecha"]
                )

                calculo = prescription_engine.calcular(
                    fecha_comision,
                    fecha_conocimiento
                )

                resultado["calculo_prescripcion"] = {
                    "fecha_comision": calculo.fecha_comision.isoformat(),

                    "fecha_conocimiento_rrhh": (
                        calculo.fecha_conocimiento_rrhh.isoformat()
                        if calculo.fecha_conocimiento_rrhh
                        else None
                    ),

                    "limite_tres_anios": (
                        calculo.limite_tres_anios.isoformat()
                    ),

                    "limite_un_anio_conocimiento": (
                        calculo.limite_un_anio_conocimiento.isoformat()
                        if calculo.limite_un_anio_conocimiento
                        else None
                    ),

                    "fecha_limite_inicio_pad": (
                        calculo.fecha_limite_inicio_pad.isoformat()
                    ),

                    "estado": calculo.estado,

                    "fundamento": calculo.fundamento
                }

                resultado["respuesta"] = (
                    f"De acuerdo con las fechas identificadas, "
                    f"la fecha límite calculada para el inicio del PAD "
                    f"es {calculo.fecha_limite_inicio_pad.strftime('%d/%m/%Y')}. "
                    f"El motor determina preliminarmente que la potestad "
                    f"disciplinaria se encuentra: {calculo.estado}."
                )

                resultado["analisis"] = (
                    f"La fecha de comisión identificada es "
                    f"{fecha_comision.strftime('%d/%m/%Y')} y la fecha "
                    f"de conocimiento por la Oficina de Recursos Humanos "
                    f"es {fecha_conocimiento.strftime('%d/%m/%Y')}. "
                    f"Con base en dichas fechas, el motor calcula como "
                    f"fecha límite para el inicio del PAD el "
                    f"{calculo.fecha_limite_inicio_pad.strftime('%d/%m/%Y')}."
                )

                resultado["conclusion_preliminar"] = (
                    f"Con base exclusivamente en las fechas proporcionadas, "
                    f"el motor determina preliminarmente que la potestad "
                    f"disciplinaria se encuentra {calculo.estado}. "
                    f"Este resultado debe ser contrastado con el régimen "
                    f"jurídico aplicable, la documentación del expediente "
                    f"y cualquier circunstancia que pueda afectar el "
                    f"cómputo de la prescripción."
                )

                resultado["requiere_verificacion"] = True

            except Exception as error:

                resultado["informacion_faltante"].append(
                    f"No fue posible efectuar el cálculo automático: {error}"
                )

        else:

            resultado["respuesta"] = (
                "No existen suficientes fechas identificadas para "
                "efectuar el cálculo automático de la prescripción."
            )

            resultado["informacion_faltante"] = [
                "Fecha de comisión de la presunta falta",
                "Fecha de conocimiento por la Oficina de Recursos Humanos"
            ]

            resultado["conclusion_preliminar"] = (
                "Es necesario identificar las fechas relevantes del caso "
                "antes de efectuar el cálculo de prescripción."
            )

        return resultado


valeria_engine = LegalEngine()