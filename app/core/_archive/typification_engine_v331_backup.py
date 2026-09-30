import re
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
    matriz_subsuncion: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TypificationEngine:
    """
    Motor preliminar de análisis de tipificación disciplinaria.

    V3.2:
    - No confunde información proporcionada con hechos acreditados.
    - Incorpora matriz preliminar de subsunción y acreditación.
    - Relaciona hechos, elementos jurídicos, deber y evidencia.
    - Mantiene pendiente la acreditación jurídica de los hechos.
    - No considera acreditada una falta por su sola descripción.
    - Diferencia deber funcional, fuente normativa y norma tipificadora.
    - Verifica preliminarmente intervención y nexo con la conducta.
    - Identifica circunstancias de tiempo, modo y lugar.
    - Identifica riesgos jurídicos de tipificación.
    - Mantiene carácter preliminar y no determina responsabilidad.
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

        # =========================================================
        # 1. TIPO DE CONDUCTA
        # =========================================================

        tipo_conducta = self._determinar_tipo_conducta(
            conducta_limpia
        )

        # =========================================================
        # 2. HECHOS RELEVANTES
        # =========================================================

        hechos_relevantes = list(hechos)

        if not hechos_relevantes:
            hechos_relevantes.append(
                "Debe identificarse y describirse el hecho concreto atribuido al servidor."
            )

        # =========================================================
        # 3. ELEMENTOS DEL ANÁLISIS
        # =========================================================

        elementos_tipo = [
            "Identificación concreta de la conducta atribuida.",
            "Existencia del hecho materia de imputación.",
            "Intervención o participación del servidor investigado.",
            "Nexo entre la conducta atribuida y la actuación u omisión del servidor.",
            "Circunstancias de tiempo, modo y lugar.",
            "Identificación concreta del deber funcional presuntamente incumplido.",
            "Identificación de la fuente normativa del deber.",
            "Vigencia y aplicabilidad de la norma al momento de los hechos.",
            "Identificación de la norma que contiene la tipificación aplicable.",
            "Correspondencia entre la conducta y el deber funcional.",
            "Correspondencia entre los hechos acreditados y los elementos de la falta imputada.",
            "Existencia de medios probatorios pertinentes y suficientes para sustentar los hechos relevantes.",
        ]

        # =========================================================
        # 4. ELEMENTOS ACREDITADOS
        # =========================================================
        #
        # Regla V3.1:
        # Los datos proporcionados por el usuario NO se consideran
        # jurídicamente acreditados por el solo hecho de haber sido
        # ingresados al motor.
        #
        # Por ello, inicialmente esta lista permanece vacía.
        # Una futura integración con el Fact Extractor y un módulo
        # probatorio podrá incorporar estados de acreditación.
        # =========================================================

        elementos_acreditados = []

        # =========================================================
        # 5. ELEMENTOS NO ACREDITADOS
        # =========================================================

        elementos_no_acreditados = [
            "La existencia del hecho atribuido requiere acreditación mediante medios probatorios pertinentes.",
            "La intervención o participación del servidor requiere acreditación individualizada.",
            "El nexo entre la conducta atribuida y la actuación u omisión del servidor requiere verificación.",
            "Las circunstancias de tiempo, modo y lugar requieren verificación.",
            "El deber funcional presuntamente incumplido requiere verificación de su existencia, contenido y exigibilidad.",
            "La fuente normativa del deber requiere individualización y verificación.",
            "La vigencia y aplicabilidad de las normas al momento de los hechos requiere verificación.",
            "La norma tipificadora aplicable requiere individualización y verificación.",
            "La correspondencia entre los hechos acreditados y los elementos de la falta requiere análisis de subsunción.",
            "La suficiencia y pertinencia de los medios probatorios requiere evaluación respecto de cada hecho relevante.",
        ]

        # Información que falta de manera específica
        if not hechos:
            elementos_no_acreditados.append(
                "No se han proporcionado hechos concretos y circunstanciados para efectuar una evaluación probatoria."
            )

        if not evidencia:
            elementos_no_acreditados.append(
                "No se han identificado medios probatorios concretos vinculados individualmente con los hechos."
            )

        if not deber_limpio:
            elementos_no_acreditados.append(
                "No se ha identificado un deber funcional concreto."
            )

        if not normas:
            elementos_no_acreditados.append(
                "No se han proporcionado referencias normativas para identificar la fuente del deber y la tipificación."
            )

        # =========================================================
        # 6. ELEMENTOS A ACREDITAR
        # =========================================================

        elementos_a_acreditar = [
            "Existencia del hecho atribuido.",
            "Intervención o participación del servidor investigado.",
            "Nexo causal o relación concreta entre la conducta y la actuación u omisión atribuida al servidor, según corresponda al caso.",
            "Circunstancias de tiempo, modo y lugar.",
            "Existencia y contenido del deber funcional presuntamente incumplido.",
            "Fuente normativa que establece el deber funcional.",
            "Vigencia y aplicabilidad de la norma al momento de los hechos.",
            "Norma que contiene la tipificación disciplinaria aplicable.",
            "Correspondencia entre la conducta acreditada y el deber funcional.",
            "Correspondencia entre los hechos acreditados y cada elemento relevante de la falta imputada.",
            "Pertinencia, suficiencia y vinculación de los medios probatorios con los hechos imputados.",
        ]

        # =========================================================
        # 7. EVIDENCIA NECESARIA
        # =========================================================

        evidencia_necesaria = list(evidencia)

        if not evidencia_necesaria:
            evidencia_necesaria = [
                "Documento o registro que sustente la ocurrencia del hecho.",
                "Documento o registro que permita determinar la intervención del servidor.",
                "Documento que permita establecer el vínculo entre el servidor y la conducta atribuida.",
                "Documento que acredite la función, obligación, deber o prohibición aplicable.",
                "Norma vigente y aplicable al momento de los hechos.",
                "Documento que establezca el plazo, condición o exigencia presuntamente incumplida, cuando corresponda.",
                "Documento que permita identificar la tipificación disciplinaria aplicable.",
                "Informes, memorandos, registros, comunicaciones u otros medios probatorios relacionados con la conducta.",
            ]

        # =========================================================
        # 8. INFORMACIÓN FALTANTE
        # =========================================================

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

        if not self._contiene_circunstancias(hechos):
            informacion_faltante.append(
                "Verificar y precisar las circunstancias de tiempo, modo y lugar."
            )

        if not self._contiene_intervencion(hechos, conducta_limpia):
            informacion_faltante.append(
                "Verificar la intervención o participación concreta del servidor en la conducta atribuida."
            )

        if deber_limpio and not normas:
            informacion_faltante.append(
                "Verificar que el deber invocado tenga una fuente normativa concreta, vigente y aplicable."
            )

        if falta_limpia and not normas:
            informacion_faltante.append(
                "Verificar la norma que contiene la tipificación disciplinaria propuesta."
            )

        # =========================================================
        # 9. SUBSUNCIÓN PRELIMINAR
        # =========================================================

        subsuncion_preliminar = self._generar_subsuncion(
            conducta=conducta_limpia,
            deber=deber_limpio,
            posible_falta=falta_limpia,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
        )

        # =========================================================
        # 10. RIESGOS JURÍDICOS
        # =========================================================

        riesgos = self._detectar_riesgos(
            conducta=conducta_limpia,
            deber=deber_limpio,
            posible_falta=falta_limpia,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
        )

        # =========================================================
        # 11. OBSERVACIONES
        # =========================================================

        observaciones = [
            "La información proporcionada constituye insumo para análisis y no equivale por sí misma a hechos jurídicamente acreditados.",
            "La posible falta disciplinaria constituye una hipótesis de trabajo y no una conclusión de responsabilidad.",
            "La sola descripción de una conducta no acredita por sí misma la comisión de una falta disciplinaria.",
            "Debe verificarse la existencia, contenido, vigencia y exigibilidad del deber funcional.",
            "Debe individualizarse y verificarse la norma tipificadora aplicable.",
            "Debe verificarse la intervención concreta del servidor y su relación con la conducta atribuida.",
            "Cada hecho relevante debe vincularse con el medio probatorio correspondiente.",
            "La subsunción realizada por este motor tiene carácter preliminar.",
            "La conclusión requiere revisión integral del expediente y de los medios probatorios.",
        ]

        for indice, riesgo in enumerate(riesgos, start=1):
            observaciones.append(
                f"RIESGO {indice}: {riesgo}"
            )

        # =========================================================
        # 12. NIVEL DE CONCLUSIÓN
        # =========================================================

        if (
            falta_limpia
            and normas
            and hechos
            and deber_limpio
            and evidencia
        ):
            nivel_conclusion = (
                "PRELIMINAR - INFORMACIÓN SUFICIENTE PARA ANÁLISIS, "
                "PENDIENTE DE ACREDITACIÓN Y VERIFICACIÓN"
            )

            requiere_verificacion = True

            conclusion_falta = (
                "Hipótesis de falta disciplinaria pendiente de contraste: "
                + falta_limpia
            )

        elif falta_limpia and (
            normas or deber_limpio or hechos
        ):
            nivel_conclusion = (
                "PRELIMINAR - INFORMACIÓN PARCIAL, "
                "PENDIENTE DE VERIFICACIÓN"
            )

            requiere_verificacion = True

            conclusion_falta = (
                "Hipótesis de falta disciplinaria pendiente de verificación: "
                + falta_limpia
            )

        else:
            nivel_conclusion = (
                "INFORMACIÓN INSUFICIENTE PARA REALIZAR "
                "UNA TIPIFICACIÓN PRELIMINAR COMPLETA"
            )

            requiere_verificacion = True

            conclusion_falta = (
                "No corresponde establecer una tipificación definitiva "
                "con la información actualmente proporcionada."
            )

        # =========================================================
        # 13. FUENTE DEL DEBER
        # =========================================================

        if normas:
            fuente_del_deber = (
                "Las normas proporcionadas constituyen referencias para "
                "identificar y verificar la fuente concreta del deber funcional. "
                "Debe individualizarse la disposición aplicable y diferenciarla "
                "de la norma que contiene la tipificación."
            )
        else:
            fuente_del_deber = (
                "No determinada. Debe identificarse la disposición normativa "
                "que establece concretamente el deber funcional."
            )

        # =========================================================
        # 14. MATRIZ DE SUBSUNCIÓN Y ACREDITACIÓN V3.2
        # =========================================================

        matriz_subsuncion = self._generar_matriz_subsuncion(
            conducta=conducta_limpia,
            deber=deber_limpio,
            posible_falta=falta_limpia,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
            tipo_conducta=tipo_conducta,
        )

        # =========================================================
        # 15. RETORNO
        # =========================================================

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
            matriz_subsuncion=matriz_subsuncion,
        )

    # =============================================================
    # MÉTODOS AUXILIARES
    # =============================================================

    # =============================================================
    # V3.2 - MATRIZ DE SUBSUNCIÓN Y ACREDITACIÓN
    # =============================================================



    def _extraer_dimensiones_hecho(
        self,
        hecho: str,
        conducta: str = "",
        deber: str = "",
    ) -> List[Dict[str, Any]]:
        """
        V3.3.1 - Descomposición multidimensional de hechos.

        Un mismo hecho puede generar varias dimensiones jurídicas.

        Esta capa:
        1. identifica hechos imputados diferenciables;
        2. identifica circunstancias temporales;
        3. identifica conocimiento/comunicación;
        4. identifica actuaciones;
        5. identifica funciones/deberes;
        6. identifica posibles elementos de participación.

        No determina responsabilidad disciplinaria.
        """

        dimensiones: List[Dict[str, Any]] = []

        texto_hecho = (hecho or "").strip()
        texto_lower = texto_hecho.lower()

        if not texto_hecho:
            return dimensiones

        def agregar(
            dimension: str,
            contenido: str,
            fundamento: str,
            prioridad: int,
        ) -> None:
            dimensiones.append({
                "dimension": dimension,
                "contenido": contenido,
                "fundamento": fundamento,
                "prioridad": prioridad,
            })

        # ==========================================================
        # 1. HECHOS IMPUTADOS — DESCOMPOSICIÓN MULTIPLE
        # ==========================================================

        reglas_hechos = [
            (
                r"\bno fue elaborado\b",
                "No elaboración del documento o informe",
            ),
            (
                r"\bno fue remitido\b",
                "No remisión del documento o informe",
            ),
            (
                r"\bno fue presentado\b",
                "No presentación del documento o informe",
            ),
            (
                r"\bno elaboró\b",
                "No elaboración del documento o informe",
            ),
            (
                r"\bno remitió\b",
                "No remisión del documento o informe",
            ),
            (
                r"\bno presentó\b",
                "No presentación del documento o informe",
            ),
            (
                r"\bno cumplió\b",
                "Incumplimiento de la obligación descrita",
            ),
            (
                r"\bincumplió\b",
                "Incumplimiento de la obligación descrita",
            ),
        ]

        hechos_detectados = set()

        for patron, contenido in reglas_hechos:
            if re.search(patron, texto_lower):
                if contenido not in hechos_detectados:
                    hechos_detectados.add(contenido)

                    agregar(
                        "HECHO IMPUTADO",
                        contenido,
                        "Expresión objetiva identificada en el hecho proporcionado.",
                        10,
                    )

        # ==========================================================
        # 2. OMISIÓN + VERBOS COORDINADOS
        # ==========================================================
        #
        # Ejemplo:
        # "omitió elaborar y remitir el informe"
        #
        # Debe poder producir dos posibles acciones:
        # - omisión de elaborar
        # - omisión de remitir
        #
        # No se declara responsabilidad; solo se descompone
        # la conducta descrita.
        # ==========================================================

        if re.search(r"\bomit[ií]ó\b", texto_lower):

            if re.search(r"\bomit[ií]ó .*elaborar\b", texto_lower):
                if "No elaboración del documento o informe" not in hechos_detectados:
                    hechos_detectados.add(
                        "No elaboración del documento o informe"
                    )

                    agregar(
                        "HECHO IMPUTADO",
                        "Omisión de elaborar el documento o informe",
                        "La conducta contiene el verbo 'omitió' asociado a 'elaborar'.",
                        10,
                    )

            if re.search(r"\bomit[ií]ó .*remitir\b", texto_lower):
                if "No remisión del documento o informe" not in hechos_detectados:
                    hechos_detectados.add(
                        "No remisión del documento o informe"
                    )

                    agregar(
                        "HECHO IMPUTADO",
                        "Omisión de remitir el documento o informe",
                        "La conducta contiene el verbo 'omitió' asociado a 'remitir'.",
                        10,
                    )

            if re.search(r"\bomit[ií]ó .*presentar\b", texto_lower):
                if "No presentación del documento o informe" not in hechos_detectados:
                    hechos_detectados.add(
                        "No presentación del documento o informe"
                    )

                    agregar(
                        "HECHO IMPUTADO",
                        "Omisión de presentar el documento o informe",
                        "La conducta contiene el verbo 'omitió' asociado a 'presentar'.",
                        10,
                    )

        # ==========================================================
        # 3. CIRCUNSTANCIA TEMPORAL
        # ==========================================================

        patrones_temporales = [
            r"\bdentro del plazo\b",
            r"\bfuera del plazo\b",
            r"\bplazo establecido\b",
            r"\bplazo señalado\b",
            r"\bplazo .* venció\b",
            r"\bvenció\b",
            r"\bvencimiento\b",
            r"\bfecha\b",
            r"\b\d{1,2}/\d{1,2}/\d{4}\b",
            r"\bel \d{1,2} de [a-záéíóú]+ de \d{4}\b",
        ]

        for patron in patrones_temporales:
            if re.search(patron, texto_lower):
                agregar(
                    "CIRCUNSTANCIA TEMPORAL",
                    "El hecho contiene una referencia temporal relevante.",
                    "Referencia temporal identificada en el hecho.",
                    20,
                )
                break

        # ==========================================================
        # 4. CONOCIMIENTO / RECEPCIÓN / COMUNICACIÓN
        # ==========================================================

        reglas_conocimiento = [
            (r"\bnotificad[oa]\b", "Notificación al servidor"),
            (r"\bnotificación\b", "Notificación relacionada con el hecho"),
            (r"\brecibió\b", "Recepción de documento, expediente o comunicación"),
            (r"\brecibido\b", "Recepción de documento, expediente o comunicación"),
            (r"\btuvo conocimiento\b", "Conocimiento del hecho o de la obligación"),
            (r"\btomó conocimiento\b", "Conocimiento del hecho o de la obligación"),
            (r"\bse le informó\b", "Información comunicada al servidor"),
            (r"\binformó\b", "Comunicación de información"),
        ]

        conocimiento_detectado = False

        for patron, contenido in reglas_conocimiento:
            if re.search(patron, texto_lower):
                agregar(
                    "CONOCIMIENTO / COMUNICACIÓN",
                    contenido,
                    "Referencia a conocimiento, recepción o comunicación.",
                    30,
                )
                conocimiento_detectado = True
                break

        # Comunicación activa de un servidor a otro
        if re.search(
            r"\bcomunic[oó]\b.*\bal servidor\b",
            texto_lower,
        ):
            agregar(
                "ACTUACIÓN DEL SERVIDOR",
                "Comunicación realizada por el servidor a otro servidor.",
                "El hecho describe una actuación concreta de comunicación.",
                40,
            )

            if not conocimiento_detectado:
                agregar(
                    "CONOCIMIENTO / COMUNICACIÓN",
                    "Comunicación dirigida a otro servidor.",
                    "La comunicación puede ser relevante para determinar conocimiento del destinatario.",
                    30,
                )

        # ==========================================================
        # 5. ACTUACIÓN DEL SERVIDOR
        # ==========================================================

        reglas_actuacion = [
            (r"\bsuscribió\b", "Suscripción de documento"),
            (r"\bfirmó\b", "Firma de documento"),
            (r"\bderivó\b", "Derivación de expediente o documento"),
            (r"\bremitió\b", "Remisión de documento o expediente"),
            (r"\bpresentó\b", "Presentación de documento"),
            (r"\belaboró\b", "Elaboración de documento"),
            (r"\bemitió\b", "Emisión de documento o acto"),
            (r"\bsolicitó\b", "Solicitud realizada"),
            (r"\brequirió\b", "Requerimiento realizado"),
            (r"\bregistró\b", "Registro de actuación"),
        ]

        for patron, contenido in reglas_actuacion:
            if re.search(patron, texto_lower):
                agregar(
                    "ACTUACIÓN DEL SERVIDOR",
                    contenido,
                    "Verbo de actuación identificado en el hecho.",
                    40,
                )

        # ==========================================================
        # 6. DEBER / FUNCIÓN
        # ==========================================================

        reglas_deber = [
            r"\btenía asignada la función\b",
            r"\btenía la función\b",
            r"\bfunción de\b",
            r"\bobligación de\b",
            r"\bdebía\b",
            r"\bdeber de\b",
            r"\bconforme a las funciones\b",
            r"\bfunciones asignadas\b",
        ]

        for patron in reglas_deber:
            if re.search(patron, texto_lower):
                agregar(
                    "DEBER / FUNCIÓN",
                    "El hecho contiene una referencia a una función u obligación.",
                    "Referencia expresa a función, deber u obligación.",
                    50,
                )
                break

        # ==========================================================
        # 7. POSIBLE PARTICIPACIÓN / INTERVENCIÓN
        # ==========================================================

        reglas_participacion = [
            r"\bderivó .* al servidor\b",
            r"\bremitió .* al servidor\b",
            r"\bparticipó\b",
            r"\bintervino\b",
            r"\bintervino en\b",
            r"\bencargó\b",
            r"\bentregó .* al servidor\b",
        ]

        for patron in reglas_participacion:
            if re.search(patron, texto_lower):
                agregar(
                    "POSIBLE PARTICIPACIÓN / INTERVENCIÓN",
                    "El hecho contiene una actuación potencialmente relevante para determinar participación.",
                    "La actuación requiere valoración probatoria y análisis de atribución.",
                    60,
                )
                break

        # ==========================================================
        # 8. CONDUCTA ATRIBUIDA
        # ==========================================================

        if conducta:
            conducta_l = conducta.lower().strip()

            indicadores_conducta = [
                "omitió",
                "incumplió",
                "no presentó",
                "no remitió",
                "no elaboró",
                "no cumplió",
            ]

            if any(x in conducta_l for x in indicadores_conducta):
                agregar(
                    "CONDUCTA ATRIBUIDA",
                    conducta.strip(),
                    "Conducta indicada en la imputación proporcionada.",
                    70,
                )

        # ==========================================================
        # 9. DEPURACIÓN
        # ==========================================================

        resultado = []
        vistos = set()

        for item in sorted(
            dimensiones,
            key=lambda x: (x["prioridad"], x["dimension"], x["contenido"])
        ):
            clave = (
                item["dimension"],
                item["contenido"],
            )

            if clave not in vistos:
                vistos.add(clave)
                resultado.append(item)

        return resultado


    def _generar_matriz_subsuncion(
        self,
        conducta: str,
        deber: str,
        posible_falta: str,
        normas: List[str],
        hechos: List[str],
        evidencia: List[str],
        tipo_conducta: str,
    ) -> List[Dict[str, Any]]:
        """
        V3.2.1 - Matriz de subsunción preliminar.

        Mejora respecto de V3.2:
        - diferencia deber, vigencia, conocimiento/notificación,
          circunstancias temporales, hecho imputado e intervención;
        - no equipara notificación con intervención;
        - no declara hechos como acreditados por la sola existencia
          de una referencia probatoria;
        - mantiene la naturaleza preliminar de la matriz;
        - incorpora elementos transversales de conducta, intervención
          y subsunción.
        """

        matriz: List[Dict[str, Any]] = []

        if not hechos:
            matriz.append({
                "hecho": "No se han proporcionado hechos concretos.",
                "categoria_hecho": "INFORMACIÓN FALTANTE",
                "elemento_tipo": "Identificación concreta de los hechos materia de imputación.",
                "deber_relacionado": deber or "No identificado.",
                "evidencia_relacionada": "No proporcionada.",
                "estado_acreditacion": "PENDIENTE DE ACREDITACIÓN",
                "justificacion": (
                    "La ausencia de hechos concretos impide realizar una "
                    "subsunción preliminar adecuada. Deben identificarse "
                    "hechos verificables, concretos y relevantes."
                ),
            })

        def clasificar_hecho(hecho: str) -> Dict[str, str]:
            h = hecho.lower().strip()

            # 1. Vigencia y aplicabilidad
            if any(p in h for p in [
                "estaba vigente",
                "vigente",
                "vigencia",
                "era aplicable",
                "aplicable",
                "se encontraba vigente",
                "norma vigente",
            ]):
                return {
                    "categoria": "VIGENCIA / APLICABILIDAD",
                    "elemento": (
                        "Vigencia y aplicabilidad de la norma "
                        "o deber al momento de los hechos."
                    ),
                }

            # 2. Conocimiento / notificación
            if any(p in h for p in [
                "fue notificado",
                "fue notificada",
                "se le notificó",
                "se notificó",
                "notificado formalmente",
                "notificación",
                "comunicado",
                "comunicación",
                "tomó conocimiento",
                "tuvo conocimiento",
                "conocía",
            ]):
                return {
                    "categoria": "CONOCIMIENTO / NOTIFICACIÓN",
                    "elemento": (
                        "Conocimiento o comunicación de la obligación, "
                        "exigencia o circunstancia relevante."
                    ),
                }

            # 3. Circunstancia temporal
            if any(p in h for p in [
                "plazo",
                "venció",
                "vencimiento",
                "fecha",
                "día",
                "periodo",
                "período",
                "dentro del plazo",
                "fuera del plazo",
                "antes de",
                "después de",
            ]):
                return {
                    "categoria": "CIRCUNSTANCIA TEMPORAL",
                    "elemento": (
                        "Circunstancias de tiempo, modo y lugar "
                        "relevantes para la imputación."
                    ),
                }

            # 4. Hecho imputado / conducta omisiva o incumplimiento
            if any(p in h for p in [
                "no presentó",
                "no presento",
                "no fue presentado",
                "no se presentó",
                "no fue entregado",
                "no se entregó",
                "no fue remitido",
                "no se remitió",
                "no fue realizado",
                "no se realizó",
                "no fue cumplido",
                "no se cumplió",
                "omitió",
                "omitiò",
                "no realizó",
                "no realizo",
                "no cumplió",
                "no cumplio",
                "incumplió",
                "incumplio",
                "dejó de",
                "dejo de",
                "no efectuó",
                "no efectuo",
                "no remitió",
                "no remitio",
                "no entregó",
                "no entrego",
            ]):
                return {
                    "categoria": "HECHO IMPUTADO",
                    "elemento": (
                        "Existencia del hecho materia de imputación."
                    ),
                }

            # 5. Deber / obligación
            if any(p in h for p in [
                "obligación",
                "obligacion",
                "deber",
                "función",
                "funcion",
                "prohibición",
                "prohibicion",
                "responsabilidad funcional",
                "correspondía",
                "correspondia",
                "tenía la obligación",
                "tenia la obligacion",
            ]):
                return {
                    "categoria": "DEBER / OBLIGACIÓN",
                    "elemento": (
                        "Identificación concreta del deber funcional "
                        "presuntamente incumplido."
                    ),
                }

            # 6. Intervención: solamente ante expresiones que indiquen
            # participación o ejecución directa.
            if any(p in h for p in [
                "participó",
                "participo",
                "intervino",
                "intervino directamente",
                "ejecutó",
                "ejecuto",
                "realizó personalmente",
                "realizo personalmente",
                "suscribió",
                "suscribio",
                "emitió",
                "emitio",
                "elaboró",
                "elaboro",
                "aprobó",
                "aprobo",
                "dispuso",
                "autorizó",
                "autorizo",
            ]):
                return {
                    "categoria": "INTERVENCIÓN",
                    "elemento": (
                        "Intervención o participación del servidor "
                        "investigado en el hecho atribuido."
                    ),
                }

            # 7. Hecho relevante no categorizado específicamente
            return {
                "categoria": "HECHO RELEVANTE",
                "elemento": (
                    "Existencia y relevancia del hecho para el análisis "
                    "de la imputación."
                ),
            }

        # Construcción de la matriz por cada hecho proporcionado.
        for indice, hecho in enumerate(hechos):

            clasificacion = clasificar_hecho(hecho)

            evidencia_relacionada = ""

            if evidencia:
                if indice < len(evidencia):
                    evidencia_relacionada = evidencia[indice]
                elif len(evidencia) == 1:
                    evidencia_relacionada = evidencia[0]

            if evidencia_relacionada:
                estado = "REFERENCIA PROBATORIA PROPORCIONADA"
                justificacion = (
                    "Se ha proporcionado una referencia probatoria relacionada "
                    "con el hecho. Esta referencia no permite, por sí sola, "
                    "considerar el hecho acreditado; corresponde verificar "
                    "su contenido, autenticidad, pertinencia y suficiencia."
                )
            else:
                estado = "SIN EVIDENCIA IDENTIFICADA"
                justificacion = (
                    "No se ha identificado una referencia probatoria específica "
                    "para este hecho dentro de la información proporcionada."
                )

            if clasificacion["categoria"] == "CONOCIMIENTO / NOTIFICACIÓN":
                justificacion += (
                    " La notificación o comunicación puede sustentar el "
                    "conocimiento de una obligación o circunstancia, pero no "
                    "demuestra por sí misma la intervención material del servidor."
                )

            matriz.append({
                "hecho": hecho,
                "categoria_hecho": clasificacion["categoria"],
                "elemento_tipo": clasificacion["elemento"],
                "deber_relacionado": deber or "No identificado.",
                "evidencia_relacionada": (
                    evidencia_relacionada
                    if evidencia_relacionada
                    else "No identificada."
                ),
                "estado_acreditacion": estado,
                "justificacion": justificacion,
            })

        # Elemento transversal 1: conducta atribuida.
        matriz.append({
            "hecho": conducta or "No se ha identificado conducta concreta.",
            "categoria_hecho": "CONDUCTA ATRIBUIDA",
            "elemento_tipo": (
                "Identificación concreta de la conducta atribuida "
                "al servidor investigado."
            ),
            "deber_relacionado": deber or "No identificado.",
            "evidencia_relacionada": (
                "Debe verificarse con los medios probatorios pertinentes."
            ),
            "estado_acreditacion": "PENDIENTE DE ACREDITACIÓN",
            "justificacion": (
                "La conducta constituye una hipótesis de imputación "
                "y requiere ser contrastada con los hechos y medios "
                "probatorios incorporados al expediente."
            ),
        })

        # Elemento transversal 2: intervención.
        matriz.append({
            "hecho": conducta or "Conducta atribuida no especificada.",
            "categoria_hecho": "INTERVENCIÓN",
            "elemento_tipo": (
                "Intervención o participación del servidor investigado "
                "en el hecho atribuido."
            ),
            "deber_relacionado": deber or "No identificado.",
            "evidencia_relacionada": (
                "Debe identificarse el medio probatorio que permita "
                "establecer la intervención del servidor."
            ),
            "estado_acreditacion": "PENDIENTE DE ACREDITACIÓN",
            "justificacion": (
                "La atribución de responsabilidad requiere establecer "
                "la relación del servidor con el hecho investigado. "
                "La sola notificación o conocimiento de una obligación "
                "no equivale automáticamente a intervención."
            ),
        })

        # Elemento transversal 3: subsunción.
        matriz.append({
            "hecho": (
                posible_falta
                if posible_falta
                else "Posible falta disciplinaria no especificada."
            ),
            "categoria_hecho": "SUBSUNCIÓN",
            "elemento_tipo": (
                "Correspondencia entre los hechos acreditados y los "
                "elementos de la falta disciplinaria imputada."
            ),
            "deber_relacionado": deber or "No identificado.",
            "evidencia_relacionada": (
                "Debe verificarse la totalidad de los elementos "
                "relevantes antes de concluir la subsunción."
            ),
            "estado_acreditacion": "PENDIENTE DE SUBSUNCIÓN",
            "justificacion": (
                "La posible falta constituye una hipótesis preliminar. "
                "La subsunción definitiva requiere identificar la norma "
                "tipificadora aplicable y contrastar sus elementos con "
                "los hechos efectivamente acreditados."
            ),
        })

        return matriz

    def _determinar_tipo_conducta(self, conducta: str) -> str:
        """
        Clasificación preliminar de la conducta.
        No constituye calificación jurídica definitiva.
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
            "no verificó",
            "no verifico",
            "no aprobó",
            "no aprobo",
            "no emitió",
            "no emitio",
            "no elaboró",
            "no elaboro",
            "omitió",
            "omitio",
            "dejó de",
            "dejo de",
            "incumplió",
            "incumplio",
            "omitió realizar",
            "omitio realizar",
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
            "verificó",
            "verifico",
            "aprobó",
            "aprobo",
            "elaboró",
            "elaboro",
        ]

        if any(
            indicador in texto
            for indicador in indicadores_omision
        ):
            return "OMISIÓN"

        if any(
            indicador in texto
            for indicador in indicadores_accion
        ):
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
                "identificado medios probatorios que permitan evaluar "
                "la acreditación de los hechos y la intervención del servidor."
            )

        return (
            "Preliminarmente, los hechos proporcionados describen una conducta "
            "que podría guardar correspondencia con el deber funcional indicado "
            "y con la posible falta propuesta. Esta correspondencia constituye "
            "una hipótesis de subsunción y no una conclusión definitiva. "
            "Debe verificarse la norma aplicable, la vigencia y exigibilidad "
            "del deber, la correspondencia de cada elemento relevante de la "
            "falta con los hechos acreditados, la intervención del servidor, "
            "el nexo con la conducta y la suficiencia de los medios probatorios."
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
                "ausencia de referencia normativa para verificar el deber y la tipificación"
            )

        if not evidencia:
            riesgos.append(
                "insuficiencia probatoria inicial"
            )

        if not self._contiene_circunstancias(hechos):
            riesgos.append(
                "circunstancias de tiempo, modo y lugar pendientes de individualización o verificación"
            )

        if not self._contiene_intervencion(
            hechos,
            conducta
        ):
            riesgos.append(
                "intervención del servidor y nexo con la conducta pendientes de acreditación"
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
                "incumplimiento de deberes",
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
                "cumplir con la normativa",
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
            texto_deber = deber.lower()

            if (
                "no presentó" in texto_conducta
                or "no presento" in texto_conducta
            ) and (
                "presentar" not in texto_deber
                and "presentación" not in texto_deber
                and "presentacion" not in texto_deber
            ):
                riesgos.append(
                    "la conducta descrita y el deber proporcionado podrían no estar suficientemente conectados"
                )

        if normas and len(normas) == 1:
            riesgos.append(
                "se proporcionó una sola referencia normativa; debe verificarse si corresponde al deber, a la tipificación o a otra regla aplicable"
            )

        return riesgos

    def _contiene_circunstancias(
        self,
        hechos: List[str],
    ) -> bool:

        if not hechos:
            return False

        texto = " ".join(hechos).lower()

        indicadores_tiempo = [
            "fecha",
            "día",
            "dia",
            "plazo",
            "mes",
            "año",
            "ano",
            "el ",
            "durante",
            "antes",
            "después",
            "despues",
        ]

        indicadores_lugar = [
            "en la",
            "en el",
            "oficina",
            "gerencia",
            "subgerencia",
            "municipalidad",
            "sede",
            "área",
            "area",
        ]

        indicadores_modo = [
            "mediante",
            "por medio",
            "a través",
            "a traves",
            "sin",
            "con",
            "utilizando",
            "remitió",
            "remitio",
            "presentó",
            "presento",
            "omitió",
            "omitio",
        ]

        tiene_tiempo = any(
            indicador in texto
            for indicador in indicadores_tiempo
        )

        tiene_lugar = any(
            indicador in texto
            for indicador in indicadores_lugar
        )

        tiene_modo = any(
            indicador in texto
            for indicador in indicadores_modo
        )

        return (
            tiene_tiempo
            and tiene_lugar
            and tiene_modo
        )

    def _contiene_intervencion(
        self,
        hechos: List[str],
        conducta: str,
    ) -> bool:

        texto = (
            " ".join(hechos) + " " + conducta
        ).lower()

        indicadores = [
            "servidor",
            "servidora",
            "funcionario",
            "funcionaria",
            "trabajador",
            "trabajadora",
            "investigado",
            "investigada",
            "responsable",
            "tenía asignada",
            "tenia asignada",
            "estaba a cargo",
            "a su cargo",
            "participó",
            "participo",
            "realizó",
            "realizo",
            "omitió",
            "omitio",
        ]

        return any(
            indicador in texto
            for indicador in indicadores
        )


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

    print("=== PRUEBA TYPOFICATION ENGINE V3.1 ===")
    print(resultado.to_dict())
    print("=== PRUEBA COMPLETADA ===")