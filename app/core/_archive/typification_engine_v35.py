from typing import Any, Dict, List
import re

from app.core.typification_engine import TypificationEngine


class TypificationEngineV35(TypificationEngine):
    """
    V3.5 - Capa jurídica estructurada sobre V3.4.3.1.

    V3.5 agrega:
    - circunstancias separadas: tiempo, modo y lugar;
    - extracción estructurada de modalidades;
    - análisis del deber funcional;
    - análisis preliminar de intervención;
    - comparación CONDUCTA <-> DEBER;
    - identificación de brechas de información.

    No sustituye todavía al motor estable V3.4.3.1.
    """

    VERSION = "V3.5"

    # =============================================================
    # MÉTODO PRINCIPAL
    # =============================================================

    def analizar_dimensiones_juridicas(
        self,
        conducta: str,
        deber: str = "",
        posible_falta: str = "",
        normas: List[str] = None,
        hechos: List[str] = None,
        evidencia: List[str] = None,
    ) -> Dict[str, Any]:

        normas = normas or []
        hechos = hechos or []
        evidencia = evidencia or []

        # ---------------------------------------------------------
        # 1. MOTOR BASE V3.4.3.1
        # ---------------------------------------------------------
        base = self.analizar(
            conducta=conducta,
            deber=deber,
            posible_falta=posible_falta,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
        )

        # ---------------------------------------------------------
        # 2. CIRCUNSTANCIAS
        # ---------------------------------------------------------
        circunstancias = self._extraer_circunstancias_v35(
            conducta=conducta,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 3. CONDUCTA ESTRUCTURADA
        # ---------------------------------------------------------
        modalidades = self._obtener_modalidades_v35(
            conducta=conducta
        )

        temporalidad = self._obtener_temporalidad_v35(
            conducta=conducta
        )

        conducta_estructurada = {
            "conducta_identificada": base.conducta_identificada,
            "tipo_conducta": base.tipo_conducta,
            "modalidades": modalidades,
            "temporalidad": temporalidad,
        }

        # ---------------------------------------------------------
        # 4. DEBER
        # ---------------------------------------------------------
        deber_estructurado = self._analizar_deber_v35(
            deber=deber,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 5. INTERVENCIÓN
        # ---------------------------------------------------------
        intervencion = self._analizar_intervencion_v35(
            conducta=conducta,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 6. CONDUCTA <-> DEBER
        # ---------------------------------------------------------
        comparacion = self._comparar_conducta_deber_v35(
            conducta=conducta_estructurada,
            deber=deber_estructurado,
        )

        # ---------------------------------------------------------
        # 7. INFORMACIÓN FALTANTE
        # ---------------------------------------------------------
        informacion_faltante = self._informacion_faltante_v35(
            conducta=conducta,
            deber=deber,
            posible_falta=posible_falta,
            normas=normas,
            hechos=hechos,
            evidencia=evidencia,
            circunstancias=circunstancias,
            intervencion=intervencion,
            comparacion=comparacion,
        )

        # ---------------------------------------------------------
        # 8. RESULTADO
        # ---------------------------------------------------------
        return {
            "version": self.VERSION,

            "analisis_base": {
                "conducta_identificada": base.conducta_identificada,
                "tipo_conducta": base.tipo_conducta,
                "posible_falta": base.posible_falta,
                "subsuncion_preliminar": base.subsuncion_preliminar,
                "nivel_conclusion": base.nivel_conclusion,
                "requiere_verificacion": base.requiere_verificacion,
            },

            "conducta_estructurada": conducta_estructurada,

            "circunstancias": circunstancias,

            "deber_funcional": deber_estructurado,

            "intervencion": intervencion,

            "comparacion_conducta_deber": comparacion,

            "hechos_relevantes": hechos,

            "normas_proporcionadas": normas,

            "evidencia_proporcionada": evidencia,

            "informacion_faltante_v35": informacion_faltante,
        }

    # =============================================================
    # CIRCUNSTANCIAS
    # =============================================================

    def _extraer_circunstancias_v35(
        self,
        conducta: str,
        hechos: List[str],
    ) -> Dict[str, Any]:

        textos = [conducta] + hechos

        texto = " ".join(
            str(t).strip()
            for t in textos
            if t and str(t).strip()
        )

        tiempo_patrones = [
            r"\bdentro del plazo\b",
            r"\bfuera del plazo\b",
            r"\bplazo establecido\b",
            r"\bfecha\b",
            r"\bel día\b",
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            r"\b\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\b",
            r"\bantes de\b",
            r"\bdespués de\b",
            r"\bposteriormente\b",
            r"\bpreviamente\b",
            r"\boportunamente\b",
            r"\btardíamente\b",
        ]

        modo_patrones = [
            r"\bno elabor[óo]\b",
            r"\bno fue elaborado\b",
            r"\bno remit[ií][oó]\b",
            r"\bno fue remitido\b",
            r"\bno present[óo]\b",
            r"\bno fue presentado\b",
            r"\bno verific[óo]\b",
            r"\bsin verificar\b",
            r"\bsin presentar\b",
            r"\bsin elaborar\b",
            r"\bsin remitir\b",
            r"\bautoriz[óo]\b",
            r"\bsuscribi[óo]\b",
            r"\bfirm[óo]\b",
            r"\bremiti[óo]\b",
            r"\bpresent[óo]\b",
            r"\belabor[óo]\b",
            r"\bderiv[óo]\b",
            r"\bsolicit[óo]\b",
            r"\brequiri[óo]\b",
        ]

        lugar_patrones = [
            r"\ben la municipalidad\b",
            r"\ben la entidad\b",
            r"\ben la oficina\b",
            r"\ben la gerencia\b",
            r"\ben la subgerencia\b",
            r"\ben el área\b",
            r"\ben las instalaciones\b",
            r"\ben sede\b",
            r"\ben el domicilio\b",
            r"\ben el local\b",
        ]

        tiempo = self._detectar_dimension(
            texto,
            tiempo_patrones,
        )

        modo = self._detectar_dimension(
            texto,
            modo_patrones,
        )

        lugar = self._detectar_dimension(
            texto,
            lugar_patrones,
        )

        return {
            "tiempo": tiempo,
            "modo": modo,
            "lugar": lugar,
            "estado_general": self._estado_circunstancias(
                tiempo,
                modo,
                lugar,
            ),
        }

    def _detectar_dimension(
        self,
        texto: str,
        patrones: List[str],
    ) -> Dict[str, Any]:

        encontrados = []

        for patron in patrones:

            coincidencias = re.findall(
                patron,
                texto,
                flags=re.IGNORECASE,
            )

            if coincidencias:
                encontrados.extend(
                    coincidencias
                )

        encontrados = list(
            dict.fromkeys(encontrados)
        )

        if encontrados:
            return {
                "estado": "IDENTIFICADO",
                "indicadores": encontrados,
            }

        return {
            "estado": "NO DETERMINADO",
            "indicadores": [],
        }

    def _estado_circunstancias(
        self,
        tiempo: Dict[str, Any],
        modo: Dict[str, Any],
        lugar: Dict[str, Any],
    ) -> str:

        estados = [
            tiempo["estado"],
            modo["estado"],
            lugar["estado"],
        ]

        identificados = estados.count(
            "IDENTIFICADO"
        )

        if identificados == 3:
            return "COMPLETAMENTE IDENTIFICADAS"

        if identificados > 0:
            return "PARCIALMENTE IDENTIFICADAS"

        return "NO DETERMINADAS"

    # =============================================================
    # CONDUCTA
    # =============================================================

    def _obtener_modalidades_v35(
        self,
        conducta: str,
    ) -> List[str]:

        texto = conducta.lower()

        modalidades = []

        # =========================================================
        # NEGATIVAS
        # =========================================================

        # NO ELABORACIÓN
        if (
            "no fue elaborado" in texto
            or "no elabor?" in texto
            or "no elaboro" in texto
        ):
            modalidades.append(
                "NO ELABORACIÓN"
            )

        # NO REMISIÓN
        # Incluye formas directas y coordinaciones negativas:
        # "no fue elaborado ni remitido"
        # "no elabor? ni remiti?"
        if (
            "no fue remitido" in texto
            or "no remiti?" in texto
            or "no remitio" in texto
            or "ni remitido" in texto
            or "ni remitida" in texto
            or "ni remiti?" in texto
            or "ni remitio" in texto
        ):
            modalidades.append(
                "NO REMISIÓN"
            )

        # NO PRESENTACI?N
        if (
            "no fue presentado" in texto
            or "no present?" in texto
            or "no presento" in texto
            or "ni presentado" in texto
            or "ni present?" in texto
            or "ni presento" in texto
        ):
            modalidades.append(
                "NO PRESENTACI?N"
            )

        # NO VERIFICACI?N
        if (
            "no verific?" in texto
            or "no verifico" in texto
            or "sin verificar" in texto
            or "ni verific?" in texto
            or "ni verifico" in texto
        ):
            modalidades.append(
                "NO VERIFICACI?N"
            )

        # =========================================================
        # POSITIVAS
        # =========================================================

        # PRESENTACI?N
        if (
            "present?" in texto
            or "presento" in texto
            or "fue presentado" in texto
        ):
            if (
                "no present?" not in texto
                and "no presento" not in texto
                and "no fue presentado" not in texto
                and "ni present?" not in texto
                and "ni presento" not in texto
                and "ni presentado" not in texto
            ):
                modalidades.append(
                    "PRESENTACI?N"
                )

        # REMISIÓN
        if (
            "remiti?" in texto
            or "remitio" in texto
            or "fue remitido" in texto
        ):
            if (
                "no remiti?" not in texto
                and "no remitio" not in texto
                and "no fue remitido" not in texto
                and "ni remiti?" not in texto
                and "ni remitio" not in texto
                and "ni remitido" not in texto
                and "ni remitida" not in texto
            ):
                modalidades.append(
                    "REMISIÓN"
                )

        # ELABORACIÓN
        if (
            "elabor?" in texto
            or "elaboro" in texto
            or "fue elaborado" in texto
        ):
            if (
                "no elabor?" not in texto
                and "no elaboro" not in texto
                and "no fue elaborado" not in texto
                and "ni elabor?" not in texto
                and "ni elaboro" not in texto
                and "ni elaborado" not in texto
            ):
                modalidades.append(
                    "ELABORACIÓN"
                )

        # AUTORIZACI?N
        if (
            "autoriz?" in texto
            or "autorizo" in texto
        ):
            modalidades.append(
                "AUTORIZACI?N"
            )

        # SUSCRIPCI?N
        if (
            "suscribi?" in texto
            or "suscribio" in texto
        ):
            modalidades.append(
                "SUSCRIPCI?N"
            )

        # VERIFICACI?N
        if (
            "verific?" in texto
            or "verifico" in texto
        ):
            if (
                "no verific?" not in texto
                and "no verifico" not in texto
                and "sin verificar" not in texto
                and "ni verific?" not in texto
                and "ni verifico" not in texto
            ):
                modalidades.append(
                    "VERIFICACI?N"
                )

        return list(
            dict.fromkeys(modalidades)
        )

    # Negativas
        if (
            "no fue elaborado" in texto
            or "no elaboró" in texto
            or "no elaboro" in texto
        ):
            modalidades.append(
                "NO ELABORACIÓN"
            )

        if (
            "no fue remitido" in texto
            or "no remitió" in texto
            or "no remitio" in texto
        ):
            modalidades.append(
                "NO REMISIÓN"
            )

        if (
            "no fue presentado" in texto
            or "no presentó" in texto
            or "no presento" in texto
        ):
            modalidades.append(
                "NO PRESENTACIÓN"
            )

        if (
            "no verificó" in texto
            or "no verifico" in texto
            or "sin verificar" in texto
        ):
            modalidades.append(
                "NO VERIFICACIÓN"
            )

        # Positivas
        if (
            "presentó" in texto
            or "presento" in texto
            or "fue presentado" in texto
        ):
            if "no presentó" not in texto and \
               "no presento" not in texto and \
               "no fue presentado" not in texto:
                modalidades.append(
                    "PRESENTACIÓN"
                )

        if (
            "remitió" in texto
            or "remitio" in texto
            or "fue remitido" in texto
        ):
            if "no remitió" not in texto and \
               "no remitio" not in texto and \
               "no fue remitido" not in texto:
                modalidades.append(
                    "REMISIÓN"
                )

        if (
            "elaboró" in texto
            or "elaboro" in texto
            or "fue elaborado" in texto
        ):
            if "no elaboró" not in texto and \
               "no elaboro" not in texto and \
               "no fue elaborado" not in texto:
                modalidades.append(
                    "ELABORACIÓN"
                )

        if (
            "autorizó" in texto
            or "autorizo" in texto
        ):
            modalidades.append(
                "AUTORIZACIÓN"
            )

        if (
            "suscribió" in texto
            or "suscribio" in texto
        ):
            modalidades.append(
                "SUSCRIPCIÓN"
            )

        if (
            "verificó" in texto
            or "verifico" in texto
        ):
            if (
                "no verificó" not in texto
                and "no verifico" not in texto
            ):
                modalidades.append(
                    "VERIFICACIÓN"
                )

        return list(
            dict.fromkeys(modalidades)
        )

    def _obtener_temporalidad_v35(
        self,
        conducta: str,
    ) -> str:

        texto = conducta.lower()

        # Primero evaluar incumplimiento.
        # La expresión "no ... dentro del plazo"
        # NO constituye cumplimiento.
        patrones_incumplimiento = [
            "no fue elaborado dentro del plazo",
            "no fue remitido dentro del plazo",
            "no fue presentado dentro del plazo",
            "no elaboró dentro del plazo",
            "no elaboro dentro del plazo",
            "no remitió dentro del plazo",
            "no remitio dentro del plazo",
            "no presentó dentro del plazo",
            "no presento dentro del plazo",
            "fuera del plazo",
            "incumplió el plazo",
            "incumplio el plazo",
            "incumplimiento de plazo",
        ]

        if any(
            patron in texto
            for patron in patrones_incumplimiento
        ):
            return "INCUMPLIMIENTO DE PLAZO"

        # Casos negativos con referencia explícita
        # al plazo dentro de la misma conducta.
        if (
            ("no fue elaborado" in texto
             or "no elaboró" in texto
             or "no elaboro" in texto
             or "no fue remitido" in texto
             or "no remitió" in texto
             or "no remitio" in texto
             or "no fue presentado" in texto
             or "no presentó" in texto
             or "no presento" in texto)
            and "plazo" in texto
        ):
            return "INCUMPLIMIENTO DE PLAZO"

        # Cumplimiento explícito.
        if (
            "dentro del plazo" in texto
            and not (
                "no fue" in texto
                or "no " in texto
                or "fuera del plazo" in texto
            )
        ):
            return "CUMPLIMIENTO DE PLAZO"

        if "oportunamente" in texto:
            return "CUMPLIMIENTO DE PLAZO"

        return "SIN INFORMACIÓN TEMPORAL"

    # =============================================================
    # DEBER
    # =============================================================

    def _analizar_deber_v35(
        self,
        deber: str,
        hechos: List[str],
    ) -> Dict[str, Any]:

        if not deber or not deber.strip():
            return {
                "estado": "NO DETERMINADO",
                "texto": "",
                "componentes": [],
                "requiere_verificacion": True,
            }

        texto = deber.strip()

        componentes = []

        patrones = [
            (
                "ELABORACIÓN",
                r"\belaborar\b|\belaboración\b",
            ),
            (
                "REMISIÓN",
                r"\bremitir\b|\bremisión\b",
            ),
            (
                "PRESENTACIÓN",
                r"\bpresentar\b|\bpresentación\b",
            ),
            (
                "VERIFICACIÓN",
                r"\bverificar\b|\bverificación\b",
            ),
            (
                "SUSCRIPCIÓN",
                r"\bsuscribir\b|\bsuscripción\b",
            ),
            (
                "AUTORIZACIÓN",
                r"\bautorizar\b|\bautorización\b",
            ),
            (
                "PLAZO",
                r"\bdentro del plazo\b|\bplazo\b",
            ),
        ]

        for nombre, patron in patrones:

            if re.search(
                patron,
                texto,
                re.IGNORECASE,
            ):
                componentes.append(nombre)

        return {
            "estado": "IDENTIFICADO",
            "texto": texto,
            "componentes": list(
                dict.fromkeys(componentes)
            ),
            "requiere_verificacion": True,
        }

    # =============================================================
    # INTERVENCIÓN
    # =============================================================

    def _analizar_intervencion_v35(
        self,
        conducta: str,
        hechos: List[str],
    ) -> Dict[str, Any]:

        texto = " ".join(
            [conducta] + hechos
        ).lower()

        indicadores_fuertes = [
            "ordenó",
            "ordeno",
            "dispuso",
            "instruyó",
            "instruyo",
            "autorizó",
            "autorizo",
            "suscribió",
            "suscribio",
            "elaboró",
            "elaboro",
            "remitió",
            "remitio",
            "presentó",
            "presento",
            "emitió",
            "emitio",
            "derivó",
            "derivo",
            "solicitó",
            "solicito",
            "requirió",
            "requirio",
        ]

        encontrados = [
            indicador
            for indicador in indicadores_fuertes
            if indicador in texto
        ]

        encontrados = list(
            dict.fromkeys(encontrados)
        )

        if encontrados:
            return {
                "estado": "INDICIOS DE INTERVENCIÓN",
                "indicadores": encontrados,
                "requiere_verificacion": True,
            }

        return {
            "estado": "NO DETERMINADA",
            "indicadores": [],
            "requiere_verificacion": True,
        }

    # =============================================================
    # COMPARACIÓN CONDUCTA <-> DEBER
    # =============================================================

    def _comparar_conducta_deber_v35(
        self,
        conducta: Dict[str, Any],
        deber: Dict[str, Any],
    ) -> Dict[str, Any]:

        resultados = []

        modalidades = conducta.get(
            "modalidades",
            []
        )

        componentes = deber.get(
            "componentes",
            []
        )

        # ---------------------------------------------------------
        # NO ELABORACIÓN <-> ELABORACIÓN
        # ---------------------------------------------------------
        if (
            "NO ELABORACIÓN" in modalidades
            and "ELABORACIÓN" in componentes
        ):
            resultados.append({
                "dimension": "ELABORACIÓN",
                "conducta": "NO ELABORACIÓN",
                "deber": "ELABORAR",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "La conducta descrita como no elaboración "
                    "guarda correspondencia preliminar con "
                    "el deber de elaborar."
                ),
            })

        # ---------------------------------------------------------
        # NO REMISIÓN <-> REMISIÓN
        # ---------------------------------------------------------
        if (
            "NO REMISIÓN" in modalidades
            and "REMISIÓN" in componentes
        ):
            resultados.append({
                "dimension": "REMISIÓN",
                "conducta": "NO REMISIÓN",
                "deber": "REMITIR",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "La conducta descrita como no remisión "
                    "guarda correspondencia preliminar con "
                    "el deber de remitir."
                ),
            })

        # ---------------------------------------------------------
        # NO PRESENTACIÓN <-> PRESENTACIÓN
        # ---------------------------------------------------------
        if (
            "NO PRESENTACIÓN" in modalidades
            and "PRESENTACIÓN" in componentes
        ):
            resultados.append({
                "dimension": "PRESENTACIÓN",
                "conducta": "NO PRESENTACIÓN",
                "deber": "PRESENTAR",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "La conducta descrita como no presentación "
                    "guarda correspondencia preliminar con "
                    "el deber de presentar."
                ),
            })

        # ---------------------------------------------------------
        # NO VERIFICACIÓN <-> VERIFICACIÓN
        # ---------------------------------------------------------
        if (
            "NO VERIFICACIÓN" in modalidades
            and "VERIFICACIÓN" in componentes
        ):
            resultados.append({
                "dimension": "VERIFICACIÓN",
                "conducta": "NO VERIFICACIÓN",
                "deber": "VERIFICAR",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "La conducta descrita como no verificación "
                    "guarda correspondencia preliminar con "
                    "el deber de verificar."
                ),
            })

        # ---------------------------------------------------------
        # AUTORIZACIÓN <-> AUTORIZACIÓN
        # ---------------------------------------------------------
        if (
            "AUTORIZACIÓN" in modalidades
            and "AUTORIZACIÓN" in componentes
        ):
            resultados.append({
                "dimension": "AUTORIZACIÓN",
                "conducta": "AUTORIZACIÓN",
                "deber": "AUTORIZAR",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "Existe correspondencia textual preliminar "
                    "respecto de la función de autorizar."
                ),
            })

        # ---------------------------------------------------------
        # SUSCRIPCIÓN <-> SUSCRIPCIÓN
        # ---------------------------------------------------------
        if (
            "SUSCRIPCIÓN" in modalidades
            and "SUSCRIPCIÓN" in componentes
        ):
            resultados.append({
                "dimension": "SUSCRIPCIÓN",
                "conducta": "SUSCRIPCIÓN",
                "deber": "SUSCRIBIR",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "Existe correspondencia preliminar "
                    "respecto del deber de suscribir."
                ),
            })

        # ---------------------------------------------------------
        # PLAZO
        # ---------------------------------------------------------
        if (
            "PLAZO" in componentes
            and conducta.get("temporalidad")
            == "INCUMPLIMIENTO DE PLAZO"
        ):
            resultados.append({
                "dimension": "PLAZO",
                "conducta": "INCUMPLIMIENTO DE PLAZO",
                "deber": "CUMPLIR DENTRO DEL PLAZO",
                "correspondencia": "IDENTIFICADA",
                "fundamento": (
                    "La conducta contiene una referencia "
                    "al incumplimiento temporal y el deber "
                    "proporcionado contiene una exigencia "
                    "de plazo."
                ),
            })

        # ---------------------------------------------------------
        # Resultado global
        # ---------------------------------------------------------
        if resultados:
            estado = (
                "CORRESPONDENCIA PRELIMINAR IDENTIFICADA"
            )
        elif (
            not deber.get("texto")
        ):
            estado = (
                "NO EVALUABLE - DEBER NO DETERMINADO"
            )
        else:
            estado = (
                "NO SE IDENTIFICA CORRESPONDENCIA "
                "DIRECTA CON LOS COMPONENTES ANALIZADOS"
            )

        return {
            "estado": estado,
            "comparaciones": resultados,
            "requiere_verificacion": True,
            "advertencia": (
                "La correspondencia identificada es "
                "preliminar y no acredita por sí misma "
                "la comisión de una falta disciplinaria."
            ),
        }

    # =============================================================
    # INFORMACIÓN FALTANTE
    # =============================================================

    def _informacion_faltante_v35(
        self,
        conducta: str,
        deber: str,
        posible_falta: str,
        normas: List[str],
        hechos: List[str],
        evidencia: List[str],
        circunstancias: Dict[str, Any],
        intervencion: Dict[str, Any],
        comparacion: Dict[str, Any],
    ) -> List[str]:

        faltante = []

        if not deber.strip():
            faltante.append(
                "Precisar el deber, obligación o prohibición presuntamente incumplido."
            )

        if not normas:
            faltante.append(
                "Identificar la fuente normativa del deber y la norma tipificadora aplicable."
            )

        if not posible_falta.strip():
            faltante.append(
                "Precisar la posible falta disciplinaria objeto de contraste."
            )

        if not hechos:
            faltante.append(
                "Precisar los hechos relevantes que sustentan la imputación."
            )

        if not evidencia:
            faltante.append(
                "Identificar los medios probatorios que sustentan los hechos relevantes."
            )

        if circunstancias["tiempo"]["estado"] == "NO DETERMINADO":
            faltante.append(
                "Precisar las circunstancias de tiempo."
            )

        # El modo no se considera automáticamente
        # una brecha cuando la propia conducta ya describe
        # suficientemente la modalidad de actuación u omisión.
        if (
            circunstancias["modo"]["estado"]
            == "NO DETERMINADO"
            and not conducta.strip()
        ):
            faltante.append(
                "Precisar las circunstancias de modo."
            )

        # El lugar solamente se solicita cuando resulta
        # relevante para individualizar la conducta.
        if (
            circunstancias["lugar"]["estado"]
            == "NO DETERMINADO"
            and any(
                palabra in conducta.lower()
                for palabra in [
                    "en la oficina",
                    "en el local",
                    "en la sede",
                    "en las instalaciones",
                ]
            )
        ):
            faltante.append(
                "Precisar las circunstancias de lugar."
            )

        if intervencion["estado"] == "NO DETERMINADA":
            faltante.append(
                "Precisar y acreditar la intervención concreta del servidor en los hechos."
            )

        if (
            comparacion["estado"]
            == "NO SE IDENTIFICA CORRESPONDENCIA "
               "DIRECTA CON LOS COMPONENTES ANALIZADOS"
        ):
            faltante.append(
                "Verificar la correspondencia entre la conducta "
                "atribuida y el contenido concreto del deber funcional."
            )

        return list(
            dict.fromkeys(faltante)
        )


if __name__ == "__main__":
    engine = TypificationEngineV35()

    resultado = engine.analizar_dimensiones_juridicas(
        conducta=(
            "El informe no fue elaborado ni remitido "
            "dentro del plazo establecido."
        ),
        deber=(
            "El servidor tenía la obligación de elaborar "
            "y remitir el informe dentro del plazo establecido."
        ),
        posible_falta=(
            "Posible incumplimiento de obligaciones funcionales."
        ),
        normas=[
            "Norma que establece el deber funcional",
            "Norma que tipifica la falta disciplinaria",
        ],
        hechos=[
            (
                "El servidor tenía la obligación de elaborar "
                "y remitir el informe dentro del plazo."
            ),
            (
                "El informe no fue elaborado ni remitido "
                "dentro del plazo establecido."
            ),
        ],
        evidencia=[
            "Documento que establece la obligación funcional.",
            "Informe no elaborado ni remitido.",
            "Documentación que acredita el vencimiento del plazo.",
        ],
    )

    print("=== TYPIFICATION ENGINE V3.5 ===")
    print(resultado)
