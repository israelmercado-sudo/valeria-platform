from app.core.negaciones import contexto_niega, omisiones, accion_positiva, accion_negada
import re
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any
from app.core.base_normativa import BaseNormativa
from app.core.plazos import CalculadorPlazos


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
    modalidades: List[str] = field(default_factory=list)
    componente_temporal: str = "SIN INFORMACIÓN TEMPORAL"
    modalidades_detalle: List[Dict[str, str]] = field(default_factory=list)
    normas_candidatas: List[Dict[str, Any]] = field(default_factory=list)
    preguntas_para_el_usuario: List[str] = field(default_factory=list)
    estado_tipificacion: str = "INFORMACION_INSUFICIENTE"
    calculo_plazo: Dict[str, Any] = field(default_factory=dict)

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

    def __init__(self):
        self.base = BaseNormativa()
        self.plazos = CalculadorPlazos()

    def analizar(
        self,
        conducta: str,
        deber: str = "",
        posible_falta: str = "",
        normas: List[str] = None,
        hechos: List[str] = None,
        evidencia: List[str] = None,
        regimen: str = None,
        funcion: str = None,
        fuente_funcion: str = None,
        norma_plazo: str = None,
        fecha_inicio_computo: str = None,
        plazo_dias_habiles: int = None,
        fecha_real: str = None,
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
        # 1-B. MODALIDADES Y RECONCILIACIÓN TEMPORAL V3.5.2
        # =========================================================

        reconciliacion_temporal = (
            self._reconciliar_modalidades_temporales(
                conducta_limpia
            )
        )

        modalidades = reconciliacion_temporal["modalidades"]
        componente_temporal = reconciliacion_temporal[
            "componente_temporal"
        ]
        modalidades_detalle = reconciliacion_temporal[
            "modalidades_detalle"
        ]

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

        # BASE NORMATIVA (candidatas, no altera la logica previa)
        _candidatas = self.base.candidatas(tipo_conducta, regimen)

        normas_candidatas = [
            {
                "id": n["id"],
                "cita": f'{n["norma"]}, art. {n["articulo"]}'
                + (f', inciso {n["inciso"]}' if n["inciso"] else ""),
                "verificado": n["verificado"],
                "advertencia": (
                    ""
                    if n["verificado"]
                    else "Norma pendiente de verificación por operador jurídico."
                ),
            }
            for n in _candidatas
        ]

        preguntas_para_el_usuario = sorted(
            {p for n in _candidatas for p in n["preguntas_pendientes"]}
        )

        resultado = TypificationResult(
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
            modalidades=modalidades,
            componente_temporal=componente_temporal,
            modalidades_detalle=modalidades_detalle,
            normas_candidatas=normas_candidatas,
            preguntas_para_el_usuario=preguntas_para_el_usuario,
        )

        resultado = self._aplicar_paso4(
            resultado,
            funcion or deber,
            fuente_funcion or "; ".join(normas or []),
            norma_plazo,
            fecha_inicio_computo,
            regimen,
        )
        resultado.calculo_plazo = self._calcular_plazo(
            resultado, fecha_inicio_computo, plazo_dias_habiles, fecha_real
        )
        return resultado

    # =============================================================
    # MÉTODOS AUXILIARES
    # =============================================================

    # =============================================================
    # V3.2 - MATRIZ DE SUBSUNCIÓN Y ACREDITACIÓN
    # =============================================================



    def _calcular_plazo(self, r, fecha_inicio, plazo_dias, fecha_real):
        """Calcula vencimiento y retraso. No modifica la clasificacion."""
        if not fecha_inicio or not plazo_dias:
            return {}

        from datetime import datetime

        advertencias = []
        try:
            venc = self.plazos.vencimiento(fecha_inicio, int(plazo_dias))
        except (ValueError, TypeError):
            return {
                "advertencias": [
                    "Fecha de inicio o plazo invalidos. Use AAAA-MM-DD y un numero entero."
                ]
            }

        calculo = {
            "fecha_inicio": str(fecha_inicio),
            "plazo_dias_habiles": int(plazo_dias),
            "vencimiento": str(venc),
            "dias_retraso": None,
            "advertencias": advertencias,
        }

        if not self.plazos.verificado:
            advertencias.append(
                "Calendario de feriados pendiente de verificacion: "
                "el vencimiento puede variar en uno o mas dias."
            )

        if fecha_real:
            try:
                real = datetime.strptime(str(fecha_real), "%Y-%m-%d").date()
                retraso = self.plazos.dias_de_retraso(venc, real)
                calculo["fecha_real"] = str(fecha_real)
                calculo["dias_retraso"] = retraso
                tipo = r.tipo_conducta or ""
                if retraso > 0 and tipo == "CUMPLIMIENTO":
                    advertencias.append(
                        "Inconsistencia: el texto indica cumplimiento pero la fecha real "
                        "es posterior al vencimiento calculado."
                    )
                if retraso == 0 and "PLAZO" in tipo:
                    advertencias.append(
                        "Inconsistencia: el texto indica incumplimiento de plazo pero la "
                        "fecha real esta dentro del vencimiento calculado."
                    )
            except ValueError:
                advertencias.append("Fecha real invalida. Use AAAA-MM-DD.")

        return calculo

    def _aplicar_paso4(self, r, funcion, fuente_funcion, norma_plazo,
                       fecha_inicio_computo, regimen):
        """Capa Paso 4: estado y preguntas segun funcion, fuente, plazo y regimen."""
        if r.tipo_conducta in ("CUMPLIMIENTO", "NO DETERMINADO"):
            r.normas_candidatas = []
            r.preguntas_para_el_usuario = []
            r.informacion_faltante = []
            r.observaciones = [
                o for o in r.observaciones if not o.startswith("RIESGO")
            ]
            if r.tipo_conducta == "CUMPLIMIENTO":
                r.estado_tipificacion = "SIN_FALTA_CANDIDATA"
                r.nivel_conclusion = (
                    "SIN INDICIOS DE INCUMPLIMIENTO EN LA CONDUCTA DESCRITA"
                )
            else:
                r.estado_tipificacion = "CONDUCTA_NO_CLASIFICADA"
                r.nivel_conclusion = (
                    "CONDUCTA NO CLASIFICADA: REQUIERE AN\u00c1LISIS ADICIONAL"
                )
            return r

        def hay(x):
            return bool((x or "").strip())

        es_plazo = "PLAZO" in r.tipo_conducta
        preguntas = []

        if not hay(regimen):
            preguntas.append(
                "¿Cuál es el régimen laboral del servidor (30057, 276, 728, CAS)?"
            )
        if not hay(funcion):
            preguntas.append(
                "¿Cuál es la función exacta del cargo que se habría incumplido?"
            )
        if not hay(fuente_funcion):
            preguntas.append(
                "¿En qué norma interna consta esa función (ROF, MOF o contrato)?"
            )
        if es_plazo and not hay(norma_plazo):
            preguntas.append("¿Qué norma establece el plazo y cuál es su duración?")
        if es_plazo and not hay(fecha_inicio_computo):
            preguntas.append("¿Desde qué fecha corre el plazo?")

        r.preguntas_para_el_usuario = preguntas

        if preguntas:
            r.estado_tipificacion = "INFORMACION_INSUFICIENTE"
        else:
            r.estado_tipificacion = "PRELIMINAR_COMPLETO_REQUIERE_REVISION"
        return r

    def _extraer_dimensiones_hecho(
        self,
        hecho: str,
        conducta: str = "",
        deber: str = "",
    ) -> List[Dict[str, Any]]:
        """
        V3.3.2
        Analiza multidimensionalmente un hecho sin confundir:

        - hecho objetivo
        - actuación del servidor
        - comunicación/conocimiento
        - deber funcional
        - conducta atribuida
        - participación/intervención

        Regla central:
        Una actuación administrativa ordinaria NO implica por sí sola
        participación disciplinaria.
        """

        dimensiones: List[Dict[str, Any]] = []

        hecho = (hecho or "").strip()
        conducta = (conducta or "").strip()
        deber = (deber or "").strip()

        if not hecho:
            return dimensiones

        hecho_lower = hecho.lower()

        def agregar(
            dimension: str,
            contenido: str,
            fundamento: str,
            prioridad: int,
        ) -> None:
            dimensiones.append(
                {
                    "dimension": dimension,
                    "contenido": contenido,
                    "fundamento": fundamento,
                    "prioridad": prioridad,
                }
            )

        # ============================================================
        # 1. HECHOS IMPUTADOS
        # ============================================================

        # No elaboración
        patrones_no_elaboracion = [
            r"\bno fue elaborado\b",
            r"\bno fue elaborada\b",
            r"\bno elaboró\b",
            r"\bno elaboro\b",
            r"\bno se elaboró\b",
            r"\bno se elaboro\b",
            r"\bomitió elaborar\b",
            r"\bomiti[oó] elaborar\b",
        ]

        if any(re.search(p, hecho_lower) for p in patrones_no_elaboracion):
            agregar(
                "HECHO IMPUTADO",
                "No elaboración del documento o informe",
                "Expresión objetiva identificada en el hecho proporcionado.",
                10,
            )

        # No remisión
        patrones_no_remision = [
            r"\bno fue remitido\b",
            r"\bno fue remitida\b",
            r"\bno remitió\b",
            r"\bno remitio\b",
            r"\bno se remitió\b",
            r"\bno se remitio\b",
            r"\bomitió remitir\b",
            r"\bomiti[oó] remitir\b",
        ]

        if any(re.search(p, hecho_lower) for p in patrones_no_remision):
            agregar(
                "HECHO IMPUTADO",
                "No remisión del documento o informe",
                "Expresión objetiva identificada en el hecho proporcionado.",
                10,
            )

        # ============================================================
        # COORDINACIÓN NEGATIVA
        # ============================================================
        #
        # Ejemplo:
        # "El informe no fue elaborado ni remitido."
        #
        # El "no" afecta a ambos verbos. El análisis debe separar
        # las dos conductas objetivas.
        #
        # Esta regla no realiza una valoración jurídica; únicamente
        # descompone la estructura factual.
        # ============================================================

        patrones_coordinacion_negativa = [
            (
                r"\bno fue elaborado\s+ni\s+remitido\b",
                "No remisión del documento o informe",
            ),
            (
                r"\bno fue elaborada\s+ni\s+remitida\b",
                "No remisión del documento o informe",
            ),
            (
                r"\bno fue elaborado\s+ni\s+enviado\b",
                "No envío del documento o informe",
            ),
            (
                r"\bno fue elaborada\s+ni\s+enviada\b",
                "No envío del documento o informe",
            ),
            (
                r"\bno fue elaborado\s+ni\s+presentado\b",
                "No presentación del documento o informe",
            ),
            (
                r"\bno fue elaborada\s+ni\s+presentada\b",
                "No presentación del documento o informe",
            ),
            (
                r"\bno fue comunicado\s+ni\s+notificado\b",
                "No notificación del documento o información",
            ),
            (
                r"\bno fue comunicada\s+ni\s+notificada\b",
                "No notificación del documento o información",
            ),
            (
                r"\bno fue presentado\s+ni\s+registrado\b",
                "No registro del documento o información",
            ),
            (
                r"\bno fue presentada\s+ni\s+registrada\b",
                "No registro del documento o información",
            ),
        ]

        for patron, contenido in patrones_coordinacion_negativa:
            if re.search(patron, hecho_lower):
                agregar(
                    "HECHO IMPUTADO",
                    contenido,
                    "La estructura coordinada del hecho contiene una segunda conducta objetiva asociada a la negación.",
                    10,
                )

        # No presentación
        patrones_no_presentacion = [
            r"\bno fue presentado\b",
            r"\bno fue presentada\b",
            r"\bno presentó\b",
            r"\bno presento\b",
            r"\bno se presentó\b",
            r"\bno se presento\b",
            r"\bomitió presentar\b",
            r"\bomiti[oó] presentar\b",
        ]

        if any(re.search(p, hecho_lower) for p in patrones_no_presentacion):
            agregar(
                "HECHO IMPUTADO",
                "No presentación del documento o informe",
                "Expresión objetiva identificada en el hecho proporcionado.",
                10,
            )

        # Incumplimiento expreso
        if re.search(
            r"\bno cumplió\b|\bno cumplio\b|\bincumplió\b|\bincumplio\b",
            hecho_lower,
        ):
            agregar(
                "HECHO IMPUTADO",
                "Incumplimiento de la actuación exigida",
                "Expresión objetiva de incumplimiento identificada en el hecho.",
                10,
            )

        # ============================================================
        # 2. CIRCUNSTANCIA TEMPORAL
        # ============================================================

        patrones_temporales = [
            r"\bdentro del plazo\b",
            r"\bfuera del plazo\b",
            r"\bplazo establecido\b",
            r"\bplazo señalado\b",
            r"\bvenció\b",
            r"\bvencio\b",
            r"\bvencimiento\b",
            r"\bfecha\b",
            r"\bel \d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        ]

        if any(re.search(p, hecho_lower) for p in patrones_temporales):
            agregar(
                "CIRCUNSTANCIA TEMPORAL",
                "El hecho contiene una referencia temporal relevante.",
                "Referencia temporal identificada en el hecho.",
                20,
            )

        # ============================================================
        # 3. CONOCIMIENTO / COMUNICACIÓN
        # ============================================================

        patrones_comunicacion = [
            r"\bcomunic[oó]\b",
            r"\bcomunicado\b",
            r"\bcomunicación\b",
            r"\bcomunicacion\b",
            r"\bnotific[oó]\b",
            r"\bnotificación\b",
            r"\bnotificacion\b",
            r"\binform[oó]\b",
            r"\bse le informó\b",
            r"\bse le informo\b",
            r"\btomó conocimiento\b",
            r"\btomo conocimiento\b",
            r"\btuvo conocimiento\b",
            r"\brecibió\b",
            r"\brecibio\b",
        ]

        hay_comunicacion = any(
            re.search(p, hecho_lower) for p in patrones_comunicacion
        )

        if hay_comunicacion:
            agregar(
                "CONOCIMIENTO / COMUNICACIÓN",
                "Comunicación dirigida a otro servidor.",
                "La comunicación puede ser relevante para determinar conocimiento del destinatario.",
                30,
            )

            agregar(
                "ACTUACIÓN DEL SERVIDOR",
                "Comunicación realizada por el servidor a otro servidor.",
                "El hecho describe una actuación concreta de comunicación.",
                40,
            )

        # ============================================================
        # 4. ACTUACIÓN DEL SERVIDOR
        # ============================================================

        actuaciones = [
            (r"\bsuscribió\b|\bsuscribio\b", "Suscripción de documento"),
            (r"\bfirmó\b|\bfirmo\b", "Firma de documento"),
            (r"\bderivó\b|\bderivo\b", "Derivación de expediente o documento"),
            (r"\bremitió\b|\bremitio\b", "Remisión de documento o expediente"),
            (r"\bpresentó\b|\bpresento\b", "Presentación de documento"),
            (r"\belaboró\b|\belaboro\b", "Elaboración de documento"),
            (r"\bemitió\b|\bemitio\b", "Emisión de documento o acto"),
            (r"\bsolicitó\b|\bsolicito\b", "Solicitud realizada"),
            (r"\brequirió\b|\brequirio\b", "Requerimiento realizado"),
            (r"\bregistró\b|\bregistro\b", "Registro de información o actuación"),
        ]

        for patron, contenido in actuaciones:
            if re.search(patron, hecho_lower):
                # La comunicación ya tiene una descripción específica.
                # No duplicamos otra actuación de comunicación.
                if contenido != "Comunicación realizada por el servidor a otro servidor.":
                    agregar(
                        "ACTUACIÓN DEL SERVIDOR",
                        contenido,
                        "Verbo de actuación identificado en el hecho.",
                        40,
                    )

        # ============================================================
        # 5. DEBER / FUNCIÓN
        # ============================================================
        #
        # V3.3.2:
        # No basta encontrar la palabra "obligación".
        #
        # "A comunicó a B la obligación de elaborar..." NO demuestra
        # que A tenga ese deber funcional.
        #
        # El deber se identifica cuando el propio hecho atribuye la
        # obligación al servidor analizado o cuando existe una fórmula
        # explícita de función/deber.
        # ============================================================

        patrones_deber_directo = [
            r"\btenía asignada la función\b",
            r"\btenía la función\b",
            r"\bsu función era\b",
            r"\bsu funcion era\b",
            r"\bsu obligación era\b",
            r"\bsu obligacion era\b",
            r"\btenía la obligación de\b",
            r"\btenia la obligacion de\b",
            r"\btenía el deber de\b",
            r"\btenia el deber de\b",
            r"\bdebía\b",
            r"\bdebia\b",
            r"\bdeber de\b",
            r"\bfunción de\b",
            r"\bfuncion de\b",
            r"\bconforme a sus funciones\b",
            r"\bconforme a las funciones asignadas\b",
        ]

        # Excluir expresamente construcciones donde el servidor solo
        # comunica/informa una obligación a otro servidor.
        comunicacion_de_obligacion = bool(
            re.search(
                r"\bcomunic[oó]\b.*\b(?:la|una)\s+obligación\s+de\b",
                hecho_lower,
            )
            or re.search(
                r"\binform[oó]\b.*\b(?:la|una)\s+obligación\s+de\b",
                hecho_lower,
            )
            or re.search(
                r"\bnotific[oó]\b.*\b(?:la|una)\s+obligación\s+de\b",
                hecho_lower,
            )
        )

        if (
            any(re.search(p, hecho_lower) for p in patrones_deber_directo)
            and not comunicacion_de_obligacion
        ):
            agregar(
                "DEBER / FUNCIÓN",
                "El hecho contiene una referencia a una función u obligación.",
                "Referencia expresa a función, deber u obligación atribuida al servidor.",
                50,
            )

        # ============================================================
        # 6. POSIBLE PARTICIPACIÓN / INTERVENCIÓN
        # ============================================================
        #
        # V3.3.2:
        # No se genera por derivar, remitir, firmar, suscribir o
        # comunicar.
        #
        # Solo se genera cuando aparecen verbos o expresiones que
        # requieren una valoración adicional de atribución.
        # ============================================================

        patrones_participacion = [
            r"\bordenó\b",
            r"\bordeno\b",
            r"\bdispuso\b",
            r"\binstruyó\b",
            r"\binstruyo\b",
            r"\bindujo\b",
            r"\bconcertó\b",
            r"\bconcerto\b",
            r"\bcoordinó\b",
            r"\bcoordino\b",
            r"\bacordó conjuntamente\b",
            r"\bacordo conjuntamente\b",
            r"\bparticipó conjuntamente\b",
            r"\bparticipo conjuntamente\b",
            r"\bintervino conjuntamente\b",
            r"\bintervino directamente\b",
        ]

        if any(re.search(p, hecho_lower) for p in patrones_participacion):
            agregar(
                "POSIBLE PARTICIPACIÓN / INTERVENCIÓN",
                "El hecho contiene un elemento adicional que podría ser relevante para determinar participación.",
                "La actuación identificada requiere valoración probatoria y análisis de atribución; no implica responsabilidad por sí misma.",
                60,
            )

        # ============================================================
        # 7. CONDUCTA ATRIBUIDA
        # ============================================================

        if conducta:
            conducta_lower = conducta.lower()

            indicadores_conducta = [
                r"\bomitió\b",
                r"\bomitio\b",
                r"\bincumplió\b",
                r"\bincumplio\b",
                r"\bno presentó\b",
                r"\bno presento\b",
                r"\bno remitió\b",
                r"\bno remitio\b",
                r"\bno elaboró\b",
                r"\bno elaboro\b",
                r"\bno cumplió\b",
                r"\bno cumplio\b",
            ]

            if any(re.search(p, conducta_lower) for p in indicadores_conducta):
                agregar(
                    "CONDUCTA ATRIBUIDA",
                    conducta,
                    "Conducta indicada en la imputación proporcionada.",
                    70,
                )

        # ============================================================
        # 8. ELIMINACIÓN DE DUPLICADOS
        # ============================================================

        unicas: List[Dict[str, Any]] = []
        vistos = set()

        for item in dimensiones:
            clave = (
                item["dimension"],
                item["contenido"],
            )

            if clave not in vistos:
                vistos.add(clave)
                unicas.append(item)

        unicas.sort(key=lambda x: x["prioridad"])

        return unicas

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
        V3.4 - Matriz multidimensional de subsunción preliminar.

        Objetivos:
        - Permitir que un mismo hecho tenga varias dimensiones jurídicas.
        - No reducir cada hecho a una sola categoría.
        - Relacionar hechos y evidencia por relevancia textual.
        - Evitar atribuir intervención o participación automáticamente.
        - Mantener carácter preliminar y sujeto a verificación.
        """

        matriz: List[Dict[str, Any]] = []

        def normalizar(texto: str) -> str:
            return " ".join((texto or "").lower().split())

        def contiene_alguno(texto: str, patrones: List[str]) -> bool:
            t = normalizar(texto)
            return any(p in t for p in patrones)

        def relevancia_evidencia(hecho: str, item: str) -> int:
            """
            Calcula una relevancia simple entre hecho y evidencia.
            No pretende sustituir análisis jurídico.
            """
            h = set(normalizar(hecho).replace(",", " ").replace(".", " ").split())
            e = set(normalizar(item).replace(",", " ").replace(".", " ").split())

            if not h or not e:
                return 0

            comunes = h.intersection(e)

            # Ignorar palabras excesivamente genéricas.
            comunes -= {
                "el", "la", "los", "las", "un", "una",
                "de", "del", "y", "o", "en", "por",
                "para", "con", "que", "se", "su"
            }

            return len(comunes)

        def agregar(
            dimension: str,
            contenido: str,
            fundamento: str = "",
            prioridad: str = "MEDIA",
            hecho_origen: str = "",
        ) -> None:
            if not contenido:
                return

            clave = (
                normalizar(dimension),
                normalizar(contenido),
                normalizar(hecho_origen),
            )

            for item in matriz:
                clave_existente = (
                    normalizar(item.get("dimension", "")),
                    normalizar(item.get("contenido", "")),
                    normalizar(item.get("hecho_origen", "")),
                )

                if clave == clave_existente:
                    return

            matriz.append(
                {
                    "dimension": dimension,
                    "contenido": contenido,
                    "fundamento": fundamento,
                    "prioridad": prioridad,
                    "hecho_origen": hecho_origen,
                }
            )

        # -------------------------------------------------
        # A. ANALISIS MULTIDIMENSIONAL DE CADA HECHO
        # -------------------------------------------------
        for hecho in hechos or []:

            hecho_l = normalizar(hecho)

            # ---------------------------------------------
            # HECHO IMPUTADO
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "no elaboró",
                    "no elaboro",
                    "no fue elaborado",
                    "no fue elaborada",
                    "omitió elaborar",
                    "omitir elaborar",
                    "no presentó",
                    "no presento",
                    "no fue presentado",
                    "no fue presentada",
                    "omitió presentar",
                    "no remitió",
                    "no remitio",
                    "no fue remitido",
                    "no fue remitida",
                    "omitió remitir",
                    "no envió",
                    "no envio",
                    "no fue enviado",
                    "no fue enviada",
                    "omitió enviar",
                    "incumplió",
                    "incumplio",
                    "incumplimiento",
                ],
            ):
                contenido = hecho

                agregar(
                    "HECHO IMPUTADO",
                    contenido,
                    "El hecho describe una conducta u omisión que requiere contraste con el deber y la norma tipificadora.",
                    "ALTA",
                    hecho,
                )

            # ---------------------------------------------
            # CIRCUNSTANCIA TEMPORAL
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "plazo",
                    "dentro del plazo",
                    "fuera del plazo",
                    "plazo establecido",
                    "plazo señalado",
                    "fecha",
                    "venció",
                    "vencio",
                    "vencimiento",
                    "días",
                    "dias",
                    "día",
                    "dia",
                ],
            ):
                agregar(
                    "CIRCUNSTANCIA TEMPORAL",
                    hecho,
                    "La dimensión temporal debe ser contrastada con las fechas y el plazo jurídicamente aplicable.",
                    "ALTA",
                    hecho,
                )

            # ---------------------------------------------
            # CONOCIMIENTO / COMUNICACION
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "comunicó",
                    "comunico",
                    "comunicación",
                    "comunicacion",
                    "notificó",
                    "notifico",
                    "notificación",
                    "notificacion",
                    "informó",
                    "informo",
                    "tomó conocimiento",
                    "tomo conocimiento",
                    "tuvo conocimiento",
                    "recibió",
                    "recibio",
                ],
            ):
                agregar(
                    "CONOCIMIENTO / COMUNICACIÓN",
                    hecho,
                    "Debe determinarse quién conoció, qué conoció, cuándo y mediante qué actuación o documento.",
                    "MEDIA",
                    hecho,
                )

            # ---------------------------------------------
            # ACTUACION DEL SERVIDOR
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "suscribió",
                    "suscribio",
                    "firmó",
                    "firmo",
                    "derivó",
                    "derivo",
                    "remitió",
                    "remitio",
                    "presentó",
                    "presento",
                    "elaboró",
                    "elaboro",
                    "emitió",
                    "emitio",
                    "solicitó",
                    "solicito",
                    "requirió",
                    "requirio",
                    "registró",
                    "registro",
                ],
            ):
                agregar(
                    "ACTUACIÓN DEL SERVIDOR",
                    hecho,
                    "La actuación debe contrastarse con las funciones, competencias y documentación que correspondan.",
                    "MEDIA",
                    hecho,
                )

            # ---------------------------------------------
            # DEBER / FUNCION
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "tenía asignada la función",
                    "tenia asignada la funcion",
                    "tenía la función",
                    "tenia la funcion",
                    "su función era",
                    "su funcion era",
                    "su obligación era",
                    "su obligacion era",
                    "tenía la obligación de",
                    "tenia la obligacion de",
                    "tenía el deber de",
                    "tenia el deber de",
                    "debía",
                    "debia",
                    "deber de",
                    "función de",
                    "funcion de",
                    "conforme a sus funciones",
                ],
            ):
                agregar(
                    "DEBER / FUNCIÓN",
                    hecho,
                    "Debe verificarse la fuente concreta del deber y su vigencia para el servidor investigado.",
                    "ALTA",
                    hecho,
                )

            # ---------------------------------------------
            # POSIBLE INTERVENCION
            # Solo indicadores fuertes.
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "ordenó",
                    "ordeno",
                    "dispuso",
                    "instruyó",
                    "instruyo",
                    "indujo",
                    "concertó",
                    "concerto",
                    "coordinó conjuntamente",
                    "coordino conjuntamente",
                    "acordó conjuntamente",
                    "acordo conjuntamente",
                    "participó conjuntamente",
                    "participo conjuntamente",
                    "intervino conjuntamente",
                    "intervino directamente",
                ],
            ):
                agregar(
                    "POSIBLE PARTICIPACIÓN / INTERVENCIÓN",
                    hecho,
                    "La posible intervención requiere acreditar concretamente la conducta de intervención y su relación con el hecho imputado.",
                    "ALTA",
                    hecho,
                )

        # -------------------------------------------------
        # B. CONDUCTA ATRIBUIDA
        # -------------------------------------------------
        if conducta and normalizar(conducta):
            agregar(
                "CONDUCTA ATRIBUIDA",
                conducta,
                "Hipótesis preliminar de conducta que debe ser contrastada con los hechos, funciones, evidencia y norma tipificadora.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # C. DEBER PROPORCIONADO POR EL ANALISIS
        # -------------------------------------------------
        if deber and normalizar(deber):
            agregar(
                "DEBER / FUNCIÓN",
                deber,
                "Deber invocado para efectuar la comparación preliminar con la conducta atribuida.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # D. POSIBLE FALTA
        # -------------------------------------------------
        if posible_falta and normalizar(posible_falta):
            agregar(
                "SUBSUNCIÓN",
                posible_falta,
                "La posible falta constituye una hipótesis de subsunción preliminar y no una declaración de responsabilidad.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # E. NORMAS
        # -------------------------------------------------
        for norma in normas or []:
            if norma and normalizar(norma):
                agregar(
                    "NORMA A CONTRASTAR",
                    norma,
                    "La norma debe ser verificada respecto de su vigencia, ámbito de aplicación y correspondencia con el hecho.",
                    "ALTA",
                    "",
                )

        # -------------------------------------------------
        # F. EVIDENCIA RELEVANTE
        # -------------------------------------------------
        for hecho in hechos or []:

            candidatos = []

            for item in evidencia or []:
                score = relevancia_evidencia(hecho, item)

                if score > 0:
                    candidatos.append((score, item))

            candidatos.sort(key=lambda x: x[0], reverse=True)

            for score, item in candidatos[:3]:
                agregar(
                    "EVIDENCIA RELACIONADA",
                    item,
                    f"Elemento de evidencia relacionado con el hecho; relevancia textual aproximada: {score}.",
                    "MEDIA" if score < 3 else "ALTA",
                    hecho,
                )

        # -------------------------------------------------
        # G. INFORMACION QUE AUN DEBE ACREDITARSE
        # -------------------------------------------------
        if deber:
            agregar(
                "VERIFICACIÓN DEL DEBER",
                "Acreditar documentalmente la asignación, contenido y vigencia del deber funcional.",
                "La sola invocación del deber no acredita por sí misma su asignación concreta al servidor.",
                "ALTA",
                "",
            )

        if conducta:
            agregar(
                "VERIFICACIÓN DE LA CONDUCTA",
                "Acreditar objetivamente la conducta u omisión atribuida mediante los medios probatorios pertinentes.",
                "La hipótesis de conducta requiere corroboración probatoria.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # H. ORDEN DE PRIORIDAD
        # -------------------------------------------------
        prioridades = {
            "ALTA": 0,
            "MEDIA": 1,
            "BAJA": 2,
        }

        matriz.sort(
            key=lambda x: (
                prioridades.get(x.get("prioridad", "MEDIA"), 1),
                x.get("dimension", ""),
                x.get("contenido", ""),
            )
        )

        return matriz

    def _parsear_eventos(self, conducta: str) -> list:
        """
        Segmenta la conducta en eventos independientes.

        Cada evento conserva:
        - ELABORACION
        - REMISION
        - PRESENTACION

        Estados:
        - DENTRO_DE_PLAZO
        - FUERA_DE_PLAZO
        - NO_EJECUTADO
        - SIN_INFORMACION_TEMPORAL
        """
        import re

        t = (conducta or "").lower().strip()

        if not t:
            return []

        eventos = []

        patrones = [
            (
                "ELABORACION",
                r"\b(?:elaborado|elaborada|elaboro|elaboró|"
                r"se elaboro|se elaboró|"
                r"emitido|emitida|emitio|emitió|"
                r"se emitio|se emitió|"
                r"suscrito|suscrita|suscribio|suscribió|"
                r"se suscribio|se suscribió)\b",
            ),
            (
                "REMISION",
                r"\b(?:remitido|remitida|remitio|remitió|"
                r"se remitio|se remitió|"
                r"notificado|notificada|notifico|notificó|"
                r"se notifico|se notificó)\b",
            ),
            (
                "PRESENTACION",
                r"\b(?:presentado|presentada|presento|presentó|"
                r"se presento|se presentó)\b",
            ),
        ]

        ocurrencias = []

        for etapa, patron in patrones:
            for m in re.finditer(patron, t):
                inicio_accion = m.start()
                fin_accion = m.end()

                contexto_previo = t[max(0, inicio_accion - 100):inicio_accion]

                negada = False

                # -------------------------------------------------
                # Negación directa.
                #
                # El contexto termina justo antes del verbo, por
                # lo que no debemos buscar la frase completa
                # "no fue remitido" dentro de contexto_previo.
                # Basta verificar que inmediatamente antes de la
                # acción aparezca una estructura negativa.
                # -------------------------------------------------
                if re.search(
                    r"\bno\s+(?:fue|se)?\s*$",
                    contexto_previo
                ):
                    negada = True

                # Formas activas: "no remitió", "no elaboró",
                # "no presentó", etc.
                if re.search(
                    r"\bno\s*$",
                    contexto_previo
                ):
                    negada = True

                # Coordinación negativa: "ni remitido".
                if re.search(
                    r"\bni\s*$",
                    contexto_previo
                ):
                    negada = True

                if contexto_niega(contexto_previo):
                    negada = True

                ocurrencias.append({
                    "inicio": inicio_accion,
                    "fin": fin_accion,
                    "etapa": etapa,
                    "negada": negada,
                })

        claves_por_etapa = {
            "ELABORACION": ["ELABORACION", "EMISION", "SUSCRIPCION"],
            "REMISION": ["REMISION", "NOTIFICACION"],
            "PRESENTACION": ["PRESENTACION"],
        }
        for etapa_om, claves_om in claves_por_etapa.items():
            for clave_om in claves_om:
                for ini_om, fin_om in omisiones(t, clave_om):
                    ocurrencias.append({
                        "inicio": ini_om,
                        "fin": fin_om,
                        "etapa": etapa_om,
                        "negada": True,
                    })

        ocurrencias.sort(key=lambda x: x["inicio"])

        # ---------------------------------------------------------
        # Eliminar duplicados y, sobre todo, evitar que una acción
        # negada genere además una ocurrencia positiva.
        # ---------------------------------------------------------
        limpias = []

        for o in ocurrencias:

            # Si ya existe la misma etapa y posición, ignorar.
            if any(
                x["inicio"] == o["inicio"]
                and x["fin"] == o["fin"]
                and x["etapa"] == o["etapa"]
                for x in limpias
            ):
                continue

            # Si una ocurrencia está negada, no debe existir otra
            # ocurrencia positiva equivalente en el mismo segmento.
            if o["negada"]:
                limpias = [
                    x for x in limpias
                    if not (
                        x["etapa"] == o["etapa"]
                        and abs(x["inicio"] - o["inicio"]) < 100
                    )
                ]

            limpias.append(o)

        ocurrencias = sorted(limpias, key=lambda x: x["inicio"])

        # ---------------------------------------------------------
        # Determinación temporal local
        # ---------------------------------------------------------
        for i, o in enumerate(ocurrencias):

            inicio_accion = o["inicio"]

            if i + 1 < len(ocurrencias):
                limite = ocurrencias[i + 1]["inicio"]
            else:
                limite = len(t)

            contexto = t[inicio_accion:limite]

            # Un adversativo introduce una nueva proposición.
            contexto = re.split(
                r"\b(?:pero|sin embargo|aunque)\b",
                contexto,
                maxsplit=1
            )[0]

             # --- 1. Estado de ejecución (independiente de la temporalidad) ---
            ejecutado = not o["negada"]

            # --- 2. Componente temporal (se detecta SIEMPRE) ---
            if (
                "fuera del plazo" in contexto
                or "fuera de plazo" in contexto
                or "fuera de término" in contexto
                or "fuera de termino" in contexto
            ):
                estado_temporal = "FUERA_DE_PLAZO"
            elif (
                "dentro del plazo" in contexto
                or "dentro de plazo" in contexto
                or "dentro del término" in contexto
                or "dentro del termino" in contexto
            ):
                estado_temporal = "DENTRO_DE_PLAZO"
            else:
                estado_temporal = "SIN_INFORMACION_TEMPORAL"

            # --- 3. Combinar ejecución + temporalidad ---
            if not ejecutado:
                if estado_temporal != "SIN_INFORMACION_TEMPORAL":
                    estado = f"NO_EJECUTADO_{estado_temporal}"
                else:
                    estado = "NO_EJECUTADO"
            else:
                estado = estado_temporal

            eventos.append((o["etapa"], estado))

        # ---------------------------------------------------------
        # Coordinación negativa explícita
        # ---------------------------------------------------------
        if re.search(
            r"\bno\s+(?:fue\s+)?elaborad[oa]\s+ni\s+remitid[oa]\b",
            t
        ):
            eventos = [
                e for e in eventos
                if e != ("ELABORACION", "SIN_INFORMACION_TEMPORAL")
            ]

            if ("ELABORACION", "NO_EJECUTADO") not in eventos:
                eventos.insert(0, ("ELABORACION", "NO_EJECUTADO"))

            if ("REMISION", "NO_EJECUTADO") not in eventos:
                eventos.append(("REMISION", "NO_EJECUTADO"))

        # ---------------------------------------------------------
        # "no fue elaborado pero posteriormente fue remitido"
        # ---------------------------------------------------------
        if re.search(
            r"\bno\s+(?:fue\s+)?elaborad[oa]\b.*?"
            r"\bpero\b.*?\bfue\s+remitid[oa]\b",
            t
        ):
            eventos = [
                e for e in eventos
                if e != ("ELABORACION", "SIN_INFORMACION_TEMPORAL")
            ]

            if ("ELABORACION", "NO_EJECUTADO") not in eventos:
                eventos.insert(0, ("ELABORACION", "NO_EJECUTADO"))

            if not any(
                etapa == "REMISION"
                for etapa, _ in eventos
            ):
                eventos.append(
                    ("REMISION", "SIN_INFORMACION_TEMPORAL")
                )

        return eventos

    def _determinar_tipo_conducta(self, conducta: str) -> str:
        """
        Clasificacion preliminar de la conducta.

        V3.5 - Segmentacion por eventos.
        """
        texto = (conducta or "").lower().strip()
        import unicodedata
        texto_plano = "".join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )

        eventos = self._parsear_eventos(texto)

        etapas_incumplidas = [
            (etapa, estado)
            for etapa, estado in eventos
            if estado in ("FUERA_DE_PLAZO", "NO_EJECUTADO")
            or estado.startswith("NO_EJECUTADO_")
        ]

        nombres = {
            "ELABORACION": "ELABORACIÓN",
            "EMISION": "EMISIÓN",
            "SUSCRIPCION": "SUSCRIPCIÓN",
            "PRESENTACION": "PRESENTACIÓN",
            "REMISION": "REMISIÓN",
            "NOTIFICACION": "NOTIFICACIÓN",
        }

        if etapas_incumplidas:
            partes = []

            for etapa, estado in etapas_incumplidas:
                nombre = nombres.get(etapa)
                if nombre is None:
                    continue

                if estado == "FUERA_DE_PLAZO":
                    partes.append(f"INCUMPLIMIENTO DE PLAZO ({nombre})")
                elif estado == "NO_EJECUTADO":
                    partes.append(f"OMISIÓN - NO {nombre}")
                elif estado == "NO_EJECUTADO_DENTRO_DE_PLAZO":
                    partes.append(f"OMISIÓN - NO {nombre}")
                elif estado == "NO_EJECUTADO_FUERA_DE_PLAZO":
                    partes.append(f"OMISIÓN - NO {nombre}")

            if partes:
                return " + ".join(dict.fromkeys(partes))

        if eventos and all(
            not e.startswith("NO_EJECUTADO")
            and e != "FUERA_DE_PLAZO"
            for _, e in eventos
        ):
            return "CUMPLIMIENTO"

        # Negaciones e incumplimientos explícitos: tienen prioridad
        # sobre cualquier indicador positivo de cumplimiento.
        indicadores_omision_generica = [
            "no cumplio",
            "no cumplió",
            "incumplio",
            "incumplió",
            "no realizo",
            "no realizó",
            "no efectuo",
            "no efectuó",
            "no atendio",
            "no atendió",
            "no verifico",
            "no verificó",
            "no aprobo",
            "no aprobó",
            "dejo de",
            "dejó de",
            "omitio",
            "omitió",
        ]

        if any(ind in texto_plano for ind in indicadores_omision_generica):
            return "OMISIÓN"

        indicadores_cumplimiento = [
            "cumplio",
            "cumplio oportunamente",
            "cumplio dentro del plazo",
            "presento dentro del plazo",
            "remitio dentro del plazo",
            "elaboro dentro del plazo",
        ]
        if any(
            indicador in texto_plano
            for indicador in indicadores_cumplimiento
        ):
            return "CUMPLIMIENTO"

        indicadores_omision = [
            "no realizo",
            "no cumplio",
            "no efectuo",
            "no informo",
            "no comunico",
            "no atendio",
            "no verifico",
            "no aprobo",
            "no emitio",
            "dejo de",
            "incumplio",
            "omitio",
        ]

        if any(
            indicador in texto_plano
            for indicador in indicadores_omision
        ):
            return "OMISIÓN"

        indicadores_accion = [
            "realizo",
            "efectuo",
            "presento",
            "autorizo",
            "emitio",
            "dispuso",
            "ordeno",
            "suscribio",
            "remitio",
            "comunico",
            "atendio",
            "verifico",
            "aprobo",
            "elaboro",
        ]

        if any(
            indicador in texto_plano
            for indicador in indicadores_accion
        ):
            return "ACCIÓN"

        return "NO DETERMINADO"

    def _reconciliar_modalidades_temporales(self, conducta: str) -> dict:
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
            "EMISION": "EMISIÓN",
            "SUSCRIPCION": "SUSCRIPCIÓN",
            "PRESENTACION": "PRESENTACIÓN",
            "REMISION": "REMISIÓN",
            "NOTIFICACION": "NOTIFICACIÓN",
        }

        mapa_modalidad_negativa = {
            "ELABORACION": "NO ELABORACIÓN",
            "EMISION": "NO EMISIÓN",
            "SUSCRIPCION": "NO SUSCRIPCIÓN",
            "PRESENTACION": "NO PRESENTACIÓN",
            "REMISION": "NO REMISIÓN",
            "NOTIFICACION": "NO NOTIFICACIÓN",
        }

        mapa_estado = {
            "DENTRO_DE_PLAZO": "CUMPLIMIENTO DE PLAZO",
            "FUERA_DE_PLAZO": "INCUMPLIMIENTO DE PLAZO",
            "NO_EJECUTADO": "SIN INFORMACIÓN TEMPORAL",
            "NO_EJECUTADO_DENTRO_DE_PLAZO": "INCUMPLIMIENTO DE PLAZO",
            "NO_EJECUTADO_FUERA_DE_PLAZO": "INCUMPLIMIENTO DE PLAZO",
            "SIN_INFORMACION_TEMPORAL": "SIN INFORMACIÓN TEMPORAL",
        }

        modalidades = []
        detalles = []
        _INCUMPLE = "INCUMPLIMIENTO DE PLAZO"

        for etapa, estado in eventos:

            if estado == "NO_EJECUTADO" or estado.startswith("NO_EJECUTADO_"):
                modalidad = mapa_modalidad_negativa.get(etapa)
            else:
                modalidad = mapa_modalidad.get(etapa)

            if modalidad is None:
                continue

            if modalidad not in modalidades:
                modalidades.append(modalidad)

            componente = mapa_estado.get(
                estado,
                "SIN INFORMACIÓN TEMPORAL",
            )

            existente = next(
                (d for d in detalles if d["modalidad"] == modalidad),
                None,
            )
            if existente is None:
                detalles.append({
                    "modalidad": modalidad,
                    "componente_temporal": componente,
                })
            elif componente == _INCUMPLE:
                # si la misma modalidad aparece dos veces,
                # el incumplimiento prevalece
                existente["componente_temporal"] = _INCUMPLE

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

        # 1. Incumplimiento explícito de plazo:
        #    - se hizo fuera del plazo (positivo tardío), o
        #    - no se hizo, con plazo explícito mencionado
        #      ("no se hizo dentro del plazo" = incumplimiento).
        if any(
            e == "FUERA_DE_PLAZO"
            or e in ("NO_EJECUTADO_DENTRO_DE_PLAZO",
                     "NO_EJECUTADO_FUERA_DE_PLAZO")
            for e in estados
        ):
            componente_temporal = "INCUMPLIMIENTO DE PLAZO"

        # 2. Cumplimiento explícito dentro del plazo (solo positivo).
        elif any(e == "DENTRO_DE_PLAZO" for e in estados):
            componente_temporal = "CUMPLIMIENTO DE PLAZO"

        # 3. Sin referencia temporal explícita.
        else:
            componente_temporal = "SIN INFORMACIÓN TEMPORAL"

        return {
            "modalidades": modalidades,
            "componente_temporal": componente_temporal,
            "modalidades_detalle": detalles,
        }

    def _extraer_modalidades_conducta(self, conducta: str) -> dict:
        """
        V3.4.3
        Extrae la conducta principal, modalidades negativas/asociadas
        y componente temporal.

        No determina responsabilidad disciplinaria ni realiza
        tipificación jurídica definitiva.
        """

        import re

        texto = (conducta or "").lower().strip()

        resultado = {
            "tipo_principal": "NO DETERMINADO",
            "modalidades": [],
            "componente_temporal": "SIN INFORMACIÓN TEMPORAL"
        }

        def contiene(patron):
            return re.search(patron, texto, flags=re.IGNORECASE) is not None

        def agregar(modalidad):
            if modalidad not in resultado["modalidades"]:
                resultado["modalidades"].append(modalidad)

        # ============================================================
        # 1. COMPONENTE TEMPORAL
        # ============================================================

        patrones_cumplimiento = [
            r"\bpresent[oó]\b.{0,100}\bdentro del plazo\b",
            r"\bremiti[oó]\b.{0,100}\bdentro del plazo\b",
            r"\belabor[oó]\b.{0,100}\bdentro del plazo\b",
            r"\bcumpli[oó]\b.{0,100}\bdentro del plazo\b",
            r"\bcumpli[oó]\b.{0,100}\boportunamente\b",
            r"\bde manera oportuna\b",
            r"\boportunamente\b"
        ]

        patrones_incumplimiento = [
            r"\bfuera del plazo\b",
            r"\bfuera de plazo\b",
            r"\bvencido el plazo\b",
            r"\bdespu[eé]s del plazo\b",
            r"\bposterior al plazo\b",
            r"\bextempor[aá]neamente\b",
            r"\bde manera extempor[aá]nea\b",
            r"\btard[ií]amente\b",
            r"\bfuera del t[eé]rmino\b",
            r"\bno cumpli[oó]\b.{0,100}\bdentro del plazo\b",
            r"\bno fue presentado\b.{0,100}\bdentro del plazo\b",
            r"\bno fue remitido\b.{0,100}\bdentro del plazo\b",
            r"\bno fue elaborado\b.{0,100}\bdentro del plazo\b",
            r"\bno present[oó]\b.{0,100}\bdentro del plazo\b",
            r"\bno remiti[oó]\b.{0,100}\bdentro del plazo\b",
            r"\bno elabor[oó]\b.{0,100}\bdentro del plazo\b"
        ]

        if any(contiene(p) for p in patrones_cumplimiento):
            resultado["componente_temporal"] = "CUMPLIMIENTO DE PLAZO"

        if any(contiene(p) for p in patrones_incumplimiento):
            resultado["componente_temporal"] = "INCUMPLIMIENTO DE PLAZO"

        # ============================================================
        # 2. MODALIDADES NEGATIVAS
        # ============================================================

        if any(contiene(p) for p in [
            r"\bno fue elaborado\b",
            r"\bno fue elaborada\b",
            r"\bno elabor[oó]\b",
            r"\bno se elabor[oó]\b",
            r"\bomiti[oó] elaborar\b",
            r"\bomiti[oó] la elaboraci[oó]n\b"
        ]):
            agregar("NO ELABORACIÓN")

        # Coordinación negativa: "no fue elaborado ni remitido"
        if any(contiene(p) for p in [
            r"\bno fue elaborado\s+ni\s+remitido\b",
            r"\bno fue elaborada\s+ni\s+remitida\b",
            r"\bno fue elaborado\s+ni\s+enviado\b",
            r"\bno fue elaborada\s+ni\s+enviada\b"
        ]):
            agregar("NO REMISIÓN")

        if any(contiene(p) for p in [
            r"\bno fue remitido\b",
            r"\bno fue remitida\b",
            r"\bno remiti[oó]\b",
            r"\bno se remiti[oó]\b",
            r"\bomiti[oó] remitir\b",
            r"\bomiti[oó] la remisi[oó]n\b"
        ]):
            agregar("NO REMISIÓN")

        if any(contiene(p) for p in [
            r"\bno fue presentado\b",
            r"\bno fue presentada\b",
            r"\bno fueron presentados\b",
            r"\bno fueron presentadas\b",
            r"\bno present[oó]\b",
            r"\bno se present[oó]\b",
            r"\bomiti[oó] presentar\b",
            r"\bomiti[oó] la presentaci[oó]n\b"
        ]):
            agregar("NO PRESENTACIÓN")

        if any(contiene(p) for p in [
            r"\bsin verificar\b",
            r"\bsin haber verificado\b",
            r"\bno verific[oó]\b",
            r"\bno se verific[oó]\b",
            r"\bomiti[oó] verificar\b",
            r"\bomiti[oó] realizar la verificaci[oó]n\b",
            r"\bomiti[oó] la verificaci[oó]n\b"
        ]):
            agregar("NO VERIFICACIÓN")

        # Revision general de negaciones (pronombres, coordinacion
        # activa, omitio/dejo de + infinitivo, notificar, etc.)
        for _clave, _modalidad in [
            ("ELABORACION", "NO ELABORACIÓN"),
            ("REMISION", "NO REMISIÓN"),
            ("PRESENTACION", "NO PRESENTACIÓN"),
            ("VERIFICACION", "NO VERIFICACIÓN"),
            ("NOTIFICACION", "NO NOTIFICACIÓN"),
            ("EMISION", "NO EMISIÓN"),
            ("SUSCRIPCION", "NO SUSCRIPCIÓN"),
            ("AUTORIZACION", "NO AUTORIZACIÓN"),
        ]:
            if accion_negada(texto, _clave):
                agregar(_modalidad)

        # ============================================================
        # 3. CONDUCTAS POSITIVAS
        # ============================================================

        # Límites de palabra para impedir falsos positivos.
        # Ejemplo: "emitió" NO debe detectarse dentro de "remitió".

        # PRESENTACIÓN: formas activas y pasivas.
        # Se excluyen expresamente las construcciones negativas.
        if (
            (
                contiene(r"\bpresent[oó]\b")
                and not contiene(r"\bno present[oó]\b")
            )
            or
            (
                contiene(r"\bfue presentado\b")
                or contiene(r"\bfue presentada\b")
                or contiene(r"\bfueron presentados\b")
                or contiene(r"\bfueron presentadas\b")
            )
        ) and not any(contiene(p) for p in [
            r"\bno fue presentado\b",
            r"\bno fue presentada\b",
            r"\bno fueron presentados\b",
            r"\bno fueron presentadas\b"
        ]):
            agregar("PRESENTACIÓN")

        if accion_positiva(texto, "REMISION"):
            agregar("REMISIÓN")

        if accion_positiva(texto, "ELABORACION"):
            agregar("ELABORACIÓN")

        if accion_positiva(texto, "AUTORIZACION"):
            agregar("AUTORIZACIÓN")

        if accion_positiva(texto, "SUSCRIPCION"):
            agregar("SUSCRIPCIÓN")

        if accion_positiva(texto, "EMISION"):
            agregar("EMISIÓN")

        if accion_positiva(texto, "VERIFICACION"):
            agregar("VERIFICACIÓN")

        # ============================================================
        # 4. CONDUCTA PRINCIPAL
        # ============================================================

        # Las conductas positivas son principales.
        # Una circunstancia como "sin verificar" no convierte
        # automáticamente una autorización en omisión.

        if "AUTORIZACIÓN" in resultado["modalidades"]:
            resultado["tipo_principal"] = "ACCIÓN"

        elif "SUSCRIPCIÓN" in resultado["modalidades"]:
            resultado["tipo_principal"] = "ACCIÓN"

        elif "EMISIÓN" in resultado["modalidades"]:
            resultado["tipo_principal"] = "ACCIÓN"

        elif "VERIFICACIÓN" in resultado["modalidades"]:
            resultado["tipo_principal"] = "ACCIÓN"

        elif "PRESENTACIÓN" in resultado["modalidades"]:
            if resultado["componente_temporal"] == "INCUMPLIMIENTO DE PLAZO":
                resultado["tipo_principal"] = "INCUMPLIMIENTO DE PLAZO"
            else:
                resultado["tipo_principal"] = "ACCIÓN"

        elif "REMISIÓN" in resultado["modalidades"]:
            if resultado["componente_temporal"] == "INCUMPLIMIENTO DE PLAZO":
                resultado["tipo_principal"] = "INCUMPLIMIENTO DE PLAZO"
            else:
                resultado["tipo_principal"] = "ACCIÓN"

        elif "ELABORACIÓN" in resultado["modalidades"]:
            if resultado["componente_temporal"] == "INCUMPLIMIENTO DE PLAZO":
                resultado["tipo_principal"] = "INCUMPLIMIENTO DE PLAZO"
            else:
                resultado["tipo_principal"] = "ACCIÓN"

        elif any(m.startswith("NO ") for m in resultado["modalidades"]):
            if resultado["componente_temporal"] == "INCUMPLIMIENTO DE PLAZO":
                resultado["tipo_principal"] = "INCUMPLIMIENTO DE PLAZO"
            else:
                resultado["tipo_principal"] = "OMISIÓN"

        # ============================================================
        # 5. CASO EXPLÍCITO DE CUMPLIMIENTO
        # ============================================================
        #
        # Si el hecho contiene una expresión inequívoca de cumplimiento
        # y además se identificó cumplimiento de plazo, se clasifica
        # expresamente como CUMPLIMIENTO.
        #
        # Esta regla no realiza valoración jurídica ni determina
        # responsabilidad disciplinaria.
        # ============================================================

        if (
            contiene(r"\bcumpli[oó]\b")
            and resultado["componente_temporal"] == "CUMPLIMIENTO DE PLAZO"
            and not any(m.startswith("NO ") for m in resultado["modalidades"])
        ):
            resultado["tipo_principal"] = "CUMPLIMIENTO"

        # ============================================================
        # 6. CASO EXPLÍCITO DE OMISIÓN DE VERIFICACIÓN
        # ============================================================

        if contiene(r"\bomiti[oó] realizar la verificaci[oó]n\b"):
            agregar("NO VERIFICACIÓN")
            resultado["tipo_principal"] = "OMISIÓN"

        elif contiene(r"\bomiti[oó] verificar\b"):
            agregar("NO VERIFICACIÓN")
            resultado["tipo_principal"] = "OMISIÓN"

        return resultado
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



