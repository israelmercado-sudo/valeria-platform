from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class TypificationResult:
    conducta_identificada: str
    tipo_conducta: str
    deber_presuntamente_incumplido: str
    fuente_del_deber: str
    posible_falta: str
    norma_tipificacion: List[str]
    subsuncion_preliminar: str
    elementos_tipo: List[str]
    elementos_acreditados: List[str]
    elementos_no_acreditados: List[str]
    elementos_a_acreditar: List[str]
    hechos_relevantes: List[str]
    evidencia_necesaria: List[str]
    informacion_faltante: List[str]
    nivel_conclusion: str
    requiere_verificacion: bool
    observaciones: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TypificationEngine:
    """
    Motor preliminar de análisis de tipificación disciplinaria.

    V3:
    - Diferencia información proporcionada de hechos acreditados.
    - Trata la posible falta como hipótesis de trabajo.
    - Analiza la relación entre conducta, deber y falta.
    - Identifica riesgos de tipificación genérica o insuficiente.
    - Identifica información y evidencia pendientes.
    - No determina responsabilidad administrativa.
    """

    def analizar(
        self,
        conducta: str,
        deber: str = "",
        posible_falta: str = "",
        normas: List[str] = None,
        hechos: List[str] = None,
        evidencia: List[str] = None,
    ) -> TypificationResult:

        if not conducta or not conducta.strip():
            raise ValueError(
                "Debe proporcionarse la descripción de la conducta."
            )

        normas = normas or []
        hechos = hechos or []
        evidencia = evidencia or []

        conducta_limpia = conducta.strip()
        deber_limpio = deber.strip()
        falta_limpia = posible_falta.strip()

        # ---------------------------------------------------------
        # 1. TIPO DE CONDUCTA
        # ---------------------------------------------------------

        tipo_conducta = self._determinar_tipo_conducta(
            conducta_limpia
        )

        # ---------------------------------------------------------
        # 2. HECHOS RELEVANTES
        # ---------------------------------------------------------

        hechos_relevantes = list(hechos)

        if not hechos_relevantes:
            hechos_relevantes.append(
                "Debe identificarse y describirse el hecho concreto atribuido al servidor."
            )

        # ---------------------------------------------------------
        # 3. ELEMENTOS DEL ANÁLISIS DE TIPIFICACIÓN
        # ---------------------------------------------------------

        elementos_tipo = [
            "Identificación concreta de la conducta atribuida.",
            "Existencia del hecho materia de imputación.",
            "Intervención o participación del servidor investigado.",
            "Circunstancias de tiempo, modo y lugar.",
            "Identificación concreta del deber funcional presuntamente incumplido.",
            "Identificación de la fuente normativa del deber.",
            "Vigencia y aplicabilidad de la norma al momento de los hechos.",
            "Identificación de la norma que contiene la tipificación aplicable.",
            "Correspondencia entre la conducta y el deber funcional.",
            "Correspondencia entre los hechos acreditados y los elementos de la falta imputada.",
            "Existencia de medios probatorios suficientes para sustentar los hechos relevantes.",
        ]

        # ---------------------------------------------------------
        # 4. INFORMACIÓN PROPORCIONADA
        # ---------------------------------------------------------

        informacion_proporcionada = []

        if conducta_limpia:
            informacion_proporcionada.append(
                "Se ha proporcionado una descripción de la conducta."
            )

        if hechos:
            informacion_proporcionada.append(
                "Se han proporcionado hechos para evaluación preliminar."
            )

        if deber_limpio:
            informacion_proporcionada.append(
                "Se ha proporcionado un deber u obligación que se plantea como presuntamente incumplido."
            )

        if falta_limpia:
            informacion_proporcionada.append(
                "Se ha proporcionado una posible falta como hipótesis de análisis."
            )

        if normas:
            informacion_proporcionada.append(
                "Se han proporcionado referencias normativas que requieren verificación."
            )

        if evidencia:
            informacion_proporcionada.append(
                "Se han proporcionado referencias a medios probatorios."
            )

        # ---------------------------------------------------------
        # 5. ELEMENTOS ACREDITADOS PRELIMINARMENTE
        # ---------------------------------------------------------

        elementos_acreditados = []

        if hechos:
            elementos_acreditados.append(
                "Existen hechos proporcionados que pueden ser objeto de evaluación y contraste probatorio."
            )

        if evidencia:
            elementos_acreditados.append(
                "Existen medios probatorios identificados que deben ser vinculados individualmente con los hechos correspondientes."
            )

        # Importante:
        # La existencia de un texto ingresado por el usuario NO convierte
        # automáticamente el deber, la falta o la norma en elementos acreditados.

        if deber_limpio:
            elementos_acreditados.append(
                "Existe un deber funcional propuesto para análisis; su existencia, contenido y exigibilidad deben ser verificados."
            )

        if normas:
            elementos_acreditados.append(
                "Existen referencias normativas propuestas; corresponde verificar cuál contiene el deber y cuál contiene la tipificación."
            )

        if falta_limpia:
            elementos_acreditados.append(
                "Existe una falta propuesta como hipótesis de tipificación; no se considera jurídicamente acreditada por su sola consignación."
            )

        # ---------------------------------------------------------
        # 6. ELEMENTOS NO ACREDITADOS / RIESGOS
        # ---------------------------------------------------------

        elementos_no_acreditados = []

        if not hechos:
            elementos_no_acreditados.append(
                "No se han proporcionado hechos concretos y verificables."
            )

        if not deber_limpio:
            elementos_no_acreditados.append(
                "No se ha identificado un deber funcional concreto."
            )

        if not normas:
            elementos_no_acreditados.append(
                "No se han proporcionado normas para verificar la fuente del deber y la tipificación."
            )

        if not evidencia:
            elementos_no_acreditados.append(
                "No se han identificado medios probatorios concretos."
            )

        if not hechos or not evidencia:
            elementos_no_acreditados.append(
                "No puede tenerse por acreditada la ocurrencia del hecho únicamente con la descripción de la conducta."
            )

        if not deber_limpio or not normas:
            elementos_no_acreditados.append(
                "No puede establecerse todavía una relación normativa suficiente entre el hecho y el deber funcional."
            )

        if falta_limpia and not normas:
            elementos_no_acreditados.append(
                "La posible falta permanece como hipótesis porque no se ha identificado y verificado la norma tipificadora aplicable."
            )

        # ---------------------------------------------------------
        # 7. ELEMENTOS QUE DEBEN ACREDITARSE
        # ---------------------------------------------------------

        elementos_a_acreditar = [
            "Existencia del hecho atribuido.",
            "Participación o intervención del servidor investigado.",
            "Circunstancias de tiempo, modo y lugar.",
            "Existencia y contenido del deber funcional presuntamente incumplido.",
            "Fuente normativa que establece el deber funcional.",
            "Vigencia y aplicabilidad de la norma al momento de los hechos.",
            "Norma que contiene la tipificación disciplinaria aplicable.",
            "Correspondencia entre la conducta acreditada y el deber funcional.",
            "Correspondencia entre los hechos acreditados y cada elemento relevante de la falta imputada.",
            "Suficiencia y pertinencia de los medios probatorios respecto de los hechos imputados.",
        ]

        # ---------------------------------------------------------
        # 8. EVIDENCIA
        # ---------------------------------------------------------

        evidencia_necesaria = list(evidencia)

        if not evidencia_necesaria:
            evidencia_necesaria = [
                "Documento que sustente la ocurrencia del hecho.",
                "Documento o registro que permita determinar la intervención del servidor.",
                "Documento que acredite la función, obligación o deber asignado.",
                "Norma vigente y aplicable al momento de los hechos.",
                "Documento o disposición que permita identificar el plazo, condición o exigencia presuntamente incumplida.",
                "Documento que contenga o permita verificar la tipificación disciplinaria aplicable.",
                "Informes, memorandos, registros u otros medios probatorios relacionados con la conducta.",
            ]

        # ---------------------------------------------------------
        # 9. INFORMACIÓN FALTANTE
        # ---------------------------------------------------------

        informacion_faltante = []

        if not hechos:
            informacion_faltante.append(
                "Precisar los hechos concretos, verificables y circunstanciados."
            )

        if not deber_limpio:
            informacion_faltante.append(
                "Precisar el deber, obligación o prohibición presuntamente incumplido."
            )

        if not normas:
            informacion_faltante.append(
                "Identificar la fuente normativa del deber y la norma tipificadora aplicable."
            )

        if not evidencia:
            informacion_faltante.append(
                "Identificar los medios probatorios que sustentan cada hecho relevante."
            )

        if hechos and not evidencia:
            informacion_faltante.append(
                "Vincular cada hecho relevante con el medio probatorio que permita acreditarlo."
            )

        if deber_limpio and not normas:
            informacion_faltante.append(
                "Verificar que el deber invocado tenga una fuente normativa concreta y aplicable."
            )

        if falta_limpia and not normas:
            informacion_faltante.append(
                "Verificar la norma que contiene la falta disciplinaria propuesta."
            )

        # ---------------------------------------------------------
        # 10. SUBSUNCIÓN PRELIMINAR
        # ---------------------------------------------------------

        subsuncion_preliminar = self._generar_subsuncion(
            conducta=conducta_limpia,
            deber=deber_limpio,
            posible_falta=falta_limpia,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
        )

        # ---------------------------------------------------------
        # 11. RIESGOS JURÍDICOS DE TIPIFICACIÓN
        # ---------------------------------------------------------

        riesgos = self._detectar_riesgos(
            conducta=conducta_limpia,
            deber=deber_limpio,
            posible_falta=falta_limpia,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
        )

        # Los riesgos se incorporan a las observaciones para mantener
        # compatibilidad con la estructura V2.
        observaciones = [
            "La posible falta proporcionada constituye una hipótesis de análisis y no una conclusión de responsabilidad.",
            "La sola descripción de una conducta no acredita por sí misma la comisión de una falta disciplinaria.",
            "La tipificación debe guardar correspondencia con los hechos efectivamente acreditados.",
            "Debe verificarse la existencia, contenido, vigencia y aplicabilidad del deber funcional.",
            "Debe verificarse la norma que contiene la tipificación disciplinaria aplicable.",
            "Debe verificarse la intervención del servidor y su relación con la conducta atribuida.",
            "Cada hecho relevante debe contar con respaldo probatorio pertinente.",
            "La subsunción realizada por este motor tiene carácter preliminar.",
            "La conclusión requiere revisión integral del expediente administrativo.",
        ]

        if riesgos:
            observaciones.append(
                "Riesgos preliminares identificados: "
                + " ".join(riesgos)
            )

        # ---------------------------------------------------------
        # 12. NIVEL DE CONCLUSIÓN
        # ---------------------------------------------------------

        if (
            falta_limpia
            and normas
            and hechos
            and deber_limpio
            and evidencia
        ):
            nivel_conclusion = "PRELIMINAR CON INFORMACIÓN SUFICIENTE PARA VERIFICACIÓN"
            requiere_verificacion = True
            conclusion_falta = (
                "Hipótesis de falta disciplinaria: "
                + falta_limpia
            )

        elif falta_limpia and (normas or deber_limpio or hechos):
            nivel_conclusion = "PRELIMINAR CON INFORMACIÓN PARCIAL"
            requiere_verificacion = True
            conclusion_falta = (
                "Hipótesis de falta disciplinaria pendiente de verificación: "
                + falta_limpia
            )

        else:
            nivel_conclusion = "INFORMACIÓN INSUFICIENTE"
            requiere_verificacion = True
            conclusion_falta = (
                "No corresponde establecer una tipificación definitiva "
                "con la información actualmente proporcionada."
            )

        # ---------------------------------------------------------
        # 13. FUENTE DEL DEBER
        # ---------------------------------------------------------

        if normas:
            fuente_del_deber = (
                "Las normas proporcionadas constituyen referencias para "
                "identificar y verificar la fuente concreta del deber funcional. "
                "No se considera determinada hasta individualizar la disposición aplicable."
            )
        else:
            fuente_del_deber = (
                "No determinada. Debe identificarse la disposición normativa "
                "que establece concretamente el deber funcional."
            )

        # ---------------------------------------------------------
        # 14. RETORNO
        # ---------------------------------------------------------

        return TypificationResult(
            conducta_identificada=conducta_limpia,
            tipo_conducta=tipo_conducta,
            deber_presuntamente_incumplido=(
                deber_limpio
                if deber_limpio
                else "No determinado con la información proporcionada."
            ),
            fuente_del_deber=fuente_del_deber,
            posible_falta=conclusion_falta,
            norma_tipificacion=list(normas),
            subsuncion_preliminar=subsuncion_preliminar,
            elementos_tipo=elementos_tipo,
            elementos_acreditados=elementos_acreditados,
            elementos_no_acreditados=elementos_no_acreditados,
            elementos_a_acreditar=elementos_a_acreditar,
            hechos_relevantes=hechos_relevantes,
            evidencia_necesaria=evidencia_necesaria,
            informacion_faltante=informacion_faltante,
            nivel_conclusion=nivel_conclusion,
            requiere_verificacion=requiere_verificacion,
            observaciones=observaciones,
        )

    # =============================================================
    # MÉTODOS AUXILIARES
    # =============================================================

    def _determinar_tipo_conducta(self, conducta: str) -> str:
        """
        Clasificación preliminar de la conducta.

        No constituye una calificación jurídica definitiva.
        """

        texto = conducta.lower()

        indicadores_omision = [
            "no realizó",
            "no realizo",
            "no cumplió",
            "no cumplio",
            "no efectuó",
            "no efectuo",
            "no presentó",
            "no presento",
            "no informó",
            "no informo",
            "no remitió",
            "no remitio",
            "no comunicó",
            "no comunico",
            "no atendió",
            "no atendio",
            "omitió",
            "omitio",
            "dejó de",
            "dejo de",
            "incumplió",
            "incumplio",
        ]

        indicadores_accion = [
            "realizó",
            "realizo",
            "efectuó",
            "efectuo",
            "presentó",
            "presento",
            "autorizó",
            "autorizo",
            "emitió",
            "emitio",
            "dispuso",
            "ordenó",
            "ordeno",
            "suscribió",
            "suscribio",
            "remitió",
            "remitio",
            "comunicó",
            "comunico",
            "atendió",
            "atendio",
        ]

        if any(indicador in texto for indicador in indicadores_omision):
            return "OMISIÓN"

        if any(indicador in texto for indicador in indicadores_accion):
            return "ACCIÓN"

        return "NO DETERMINADO"

    def _generar_subsuncion(
        self,
        conducta: str,
        deber: str,
        posible_falta: str,
        normas: List[str],
        hechos: List[str],
        evidencia: List[str],
    ) -> str:

        if not hechos:
            return (
                "No es posible realizar una subsunción preliminar adecuada "
                "porque no se han proporcionado hechos concretos."
            )

        if not deber:
            return (
                "Se identifican hechos para evaluación, pero no puede "
                "establecerse una relación suficiente con un deber funcional "
                "mientras este no sea precisado."
            )

        if not posible_falta:
            return (
                "Se identifican hechos y un posible deber funcional, pero "
                "no se ha proporcionado una hipótesis de falta disciplinaria "
                "para realizar la comparación correspondiente."
            )

        if not normas:
            return (
                "Existe una hipótesis de correspondencia entre los hechos, "
                "el deber y la posible falta; sin embargo, no puede "
                "verificarse la subsunción normativa porque no se ha "
                "identificado la fuente normativa aplicable."
            )

        if not evidencia:
            return (
                "Existe una hipótesis preliminar de correspondencia entre "
                "conducta, deber y posible falta; sin embargo, no se han "
                "identificado medios probatorios que permitan sostener "
                "la acreditación de los hechos y la intervención del servidor."
            )

        return (
            "Preliminarmente, los hechos proporcionados describen una conducta "
            "que podría guardar correspondencia con el deber funcional indicado "
            "y con la posible falta propuesta. Esta correspondencia constituye "
            "una hipótesis de subsunción y no una conclusión definitiva. Debe "
            "verificarse la norma aplicable, la vigencia y exigibilidad del deber, "
            "la correspondencia de cada elemento relevante de la falta con los "
            "hechos acreditados, la intervención del servidor y la suficiencia "
            "de los medios probatorios."
        )

    def _detectar_riesgos(
        self,
        conducta: str,
        deber: str,
        posible_falta: str,
        normas: List[str],
        hechos: List[str],
        evidencia: List[str],
    ) -> List[str]:

        riesgos = []

        if not hechos:
            riesgos.append(
                "hechos insuficientemente individualizados"
            )

        if not deber:
            riesgos.append(
                "deber funcional no individualizado"
            )

        if not normas:
            riesgos.append(
                "ausencia de referencia normativa para verificar la tipificación"
            )

        if not evidencia:
            riesgos.append(
                "insuficiencia probatoria inicial"
            )

        if posible_falta:
            texto_falta = posible_falta.lower()

            expresiones_genericas = [
                "incumplimiento de obligaciones",
                "incumplimiento de funciones",
                "incumplimiento funcional",
                "obligaciones funcionales",
                "falta administrativa",
                "conducta irregular",
            ]

            if any(
                expresion in texto_falta
                for expresion in expresiones_genericas
            ):
                riesgos.append(
                    "posible formulación genérica de la falta que requiere individualización y contraste con la norma tipificadora"
                )

        if deber:
            texto_deber = deber.lower()

            deberes_genericos = [
                "cumplir las funciones",
                "cumplir sus funciones",
                "cumplir con sus funciones",
                "cumplir las obligaciones",
                "cumplir sus obligaciones",
                "actuar conforme a la normativa",
            ]

            if any(
                expresion in texto_deber
                for expresion in deberes_genericos
            ):
                riesgos.append(
                    "deber funcional formulado de manera genérica; requiere identificar la obligación concreta exigible"
                )

        if conducta and deber:
            texto_conducta = conducta.lower()

            if (
                "no presentó" in texto_conducta
                or "no presento" in texto_conducta
            ) and (
                "presentar" not in deber.lower()
                and "presentación" not in deber.lower()
                and "presentacion" not in deber.lower()
            ):
                riesgos.append(
                    "la conducta descrita y el deber proporcionado podrían no estar suficientemente conectados"
                )

        return riesgos


typification_engine = TypificationEngine()


if __name__ == "__main__":

    resultado = typification_engine.analizar(
        conducta=(
            "El servidor no presentó dentro del plazo establecido "
            "la documentación que tenía a su cargo."
        ),
        deber=(
            "Cumplir las funciones y obligaciones asignadas "
            "conforme a la normativa aplicable."
        ),
        posible_falta=(
            "Posible incumplimiento de obligaciones funcionales."
        ),
        normas=[
            "Norma que establece el deber funcional.",
            "Norma que contiene la tipificación aplicable."
        ],
        hechos=[
            "El servidor tenía asignada la responsabilidad de presentar la documentación.",
            "La documentación no fue presentada dentro del plazo establecido."
        ],
        evidencia=[
            "Documento que acredita la función asignada.",
            "Documento que establece el plazo.",
            "Registro que acredita la falta de presentación."
        ],
    )

    print("=== PRUEBA TYPOFICATION ENGINE V3 ===")
    print(resultado.to_dict())
    print("=== PRUEBA COMPLETADA ===")
