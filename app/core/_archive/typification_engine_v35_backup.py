from typing import Any, Dict, List
import re

from app.core.typification_engine import TypificationEngine


class TypificationEngineV35(TypificationEngine):
    """
    V3.5 - Capa jurídica estructurada sobre V3.4.3.1.

    Objetivo:
    - Mantener intacta la clasificación existente.
    - Extraer dimensiones jurídicas de los hechos.
    - Separar tiempo, modo y lugar.
    - Identificar deber, conducta e intervención.
    - No inventar normas ni conclusiones jurídicas.
    """

    VERSION = "V3.5"

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
        # 1. Análisis base V3.4.3.1
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
        # 2. Dimensiones de circunstancias
        # ---------------------------------------------------------
        circunstancias = self._extraer_circunstancias_v35(
            conducta=conducta,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 3. Conducta y modalidades
        # ---------------------------------------------------------
        conducta_estructurada = {
            "conducta_identificada": base.conducta_identificada,
            "tipo_conducta": base.tipo_conducta,
            "modalidades": self._obtener_modalidades_v35(conducta),
            "temporalidad": self._obtener_temporalidad_v35(conducta),
        }

        # ---------------------------------------------------------
        # 4. Deber funcional
        # ---------------------------------------------------------
        deber_estructurado = self._analizar_deber_v35(
            deber=deber,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 5. Intervención
        # ---------------------------------------------------------
        intervencion = self._analizar_intervencion_v35(
            conducta=conducta,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 6. Información faltante estructurada
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
        )

        # ---------------------------------------------------------
        # 7. Resultado
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
            r"\bel \d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
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
            r"\bno remit[ií][oó]\b",
            r"\bno present[óo]\b",
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
                encontrados.extend(coincidencias)

        encontrados = list(dict.fromkeys(encontrados))

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

        identificados = estados.count("IDENTIFICADO")

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

        try:
            resultado = self._extraer_modalidades_conducta(
                conducta
            )

            if isinstance(resultado, list):
                return resultado

        except Exception:
            pass

        return []

    def _obtener_temporalidad_v35(
        self,
        conducta: str,
    ) -> str:

        texto = conducta.lower()

        if "dentro del plazo" in texto:
            return "CUMPLIMIENTO DE PLAZO"

        if "oportunamente" in texto:
            return "CUMPLIMIENTO DE PLAZO"

        if "fuera del plazo" in texto:
            return "INCUMPLIMIENTO DE PLAZO"

        if "no fue elaborado" in texto and "plazo" in texto:
            return "INCUMPLIMIENTO DE PLAZO"

        if "no fue remitido" in texto and "plazo" in texto:
            return "INCUMPLIMIENTO DE PLAZO"

        if "no presentó" in texto and "plazo" in texto:
            return "INCUMPLIMIENTO DE PLAZO"

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

        componentes = []

        texto = deber.strip()

        if re.search(
            r"\belaborar\b|\belaboración\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("ELABORACIÓN")

        if re.search(
            r"\bremitir\b|\bremisión\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("REMISIÓN")

        if re.search(
            r"\bpresentar\b|\bpresentación\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("PRESENTACIÓN")

        if re.search(
            r"\bverificar\b|\bverificación\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("VERIFICACIÓN")

        if re.search(
            r"\bsuscribir\b|\bsuscripción\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("SUSCRIPCIÓN")

        if re.search(
            r"\bautorizar\b|\bautorización\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("AUTORIZACIÓN")

        if re.search(
            r"\bdentro del plazo\b|\bplazo\b",
            texto,
            re.IGNORECASE,
        ):
            componentes.append("PLAZO")

        return {
            "estado": "IDENTIFICADO",
            "texto": texto,
            "componentes": list(dict.fromkeys(componentes)),
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

        encontrados = list(dict.fromkeys(encontrados))

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

        if circunstancias["modo"]["estado"] == "NO DETERMINADO":
            faltante.append(
                "Precisar las circunstancias de modo."
            )

        if circunstancias["lugar"]["estado"] == "NO DETERMINADO":
            faltante.append(
                "Precisar las circunstancias de lugar, cuando resulten relevantes."
            )

        if intervencion["estado"] == "NO DETERMINADA":
            faltante.append(
                "Precisar y acreditar la intervención concreta del servidor en los hechos."
            )

        return list(dict.fromkeys(faltante))


if __name__ == "__main__":

    engine = TypificationEngineV35()

    resultado = engine.analizar_dimensiones_juridicas(
        conducta="El informe no fue elaborado ni remitido dentro del plazo establecido.",
        deber="El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo establecido.",
        posible_falta="Posible incumplimiento de obligaciones funcionales.",
        normas=[
            "Norma que establece el deber funcional",
            "Norma que tipifica la falta disciplinaria",
        ],
        hechos=[
            "El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo.",
            "El informe no fue elaborado ni remitido dentro del plazo establecido.",
        ],
        evidencia=[
            "Documento que establece la obligación funcional.",
            "Informe no elaborado ni remitido.",
            "Documentación que acredita el vencimiento del plazo.",
        ],
    )

    print("=== TYPIFICATION ENGINE V3.5 ===")
    print(resultado)
