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
    Motor preliminar de tipificación disciplinaria.

    Objetivo:
    - Identificar la conducta descrita.
    - Separar hechos de conclusiones jurídicas.
    - Determinar preliminarmente si la conducta constituye
      una acción, omisión o situación no determinada.
    - Identificar el deber funcional presuntamente incumplido.
    - Identificar la posible falta disciplinaria.
    - Realizar una subsunción preliminar de los hechos
      respecto del deber y la posible falta.
    - Identificar elementos acreditados y pendientes.
    - Vincular la evidencia disponible con los hechos.
    - Señalar expresamente la información que debe verificarse.

    Este motor NO determina responsabilidad administrativa.
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
        # 1. DETERMINACIÓN PRELIMINAR DEL TIPO DE CONDUCTA
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
        # 3. ELEMENTOS DEL TIPO / DEBER QUE DEBEN SER VERIFICADOS
        # ---------------------------------------------------------

        elementos_tipo = [
            "Identificación concreta de la conducta atribuida.",
            "Existencia del hecho materia de imputación.",
            "Intervención o participación del servidor investigado.",
            "Circunstancias de tiempo, modo y lugar.",
            "Existencia del deber, obligación o prohibición aplicable.",
            "Vigencia y aplicabilidad de la norma al momento de los hechos.",
            "Correspondencia entre la conducta y el deber funcional.",
            "Correspondencia entre los hechos acreditados y la falta disciplinaria imputada.",
        ]

        # ---------------------------------------------------------
        # 4. ELEMENTOS ACREDITADOS
        # ---------------------------------------------------------

        elementos_acreditados = []

        if hechos:
            elementos_acreditados.append(
                "Existen hechos proporcionados para su evaluación preliminar."
            )

        if deber_limpio:
            elementos_acreditados.append(
                "Se ha proporcionado un deber u obligación presuntamente incumplido."
            )

        if falta_limpia:
            elementos_acreditados.append(
                "Se ha proporcionado una posible falta disciplinaria."
            )

        if normas:
            elementos_acreditados.append(
                "Se han proporcionado referencias normativas para verificación."
            )

        if evidencia:
            elementos_acreditados.append(
                "Se han identificado medios probatorios relacionados con el caso."
            )

        # ---------------------------------------------------------
        # 5. ELEMENTOS NO ACREDITADOS / PENDIENTES
        # ---------------------------------------------------------

        elementos_no_acreditados = []

        if not hechos:
            elementos_no_acreditados.append(
                "No se han proporcionado hechos concretos y verificables."
            )

        if not deber_limpio:
            elementos_no_acreditados.append(
                "No se ha determinado el deber funcional presuntamente incumplido."
            )

        if not falta_limpia:
            elementos_no_acreditados.append(
                "No se ha determinado la posible falta disciplinaria."
            )

        if not normas:
            elementos_no_acreditados.append(
                "No se ha identificado la norma que sustenta el deber y/o la tipificación."
            )

        if not evidencia:
            elementos_no_acreditados.append(
                "No se han identificado medios probatorios concretos."
            )

        # ---------------------------------------------------------
        # 6. ELEMENTOS GENERALES A ACREDITAR
        # ---------------------------------------------------------

        elementos_a_acreditar = [
            "Existencia del hecho atribuido.",
            "Participación o intervención del servidor investigado.",
            "Circunstancias de tiempo, modo y lugar.",
            "Existencia del deber, obligación o prohibición presuntamente incumplida.",
            "Vigencia de la norma aplicable al momento de los hechos.",
            "Correspondencia entre la conducta acreditada y la falta disciplinaria imputada.",
        ]

        # ---------------------------------------------------------
        # 7. EVIDENCIA
        # ---------------------------------------------------------

        evidencia_necesaria = list(evidencia)

        if not evidencia_necesaria:
            evidencia_necesaria = [
                "Documentación que sustente la ocurrencia de los hechos.",
                "Documentos que permitan determinar la intervención del servidor.",
                "Documento que acredite el deber o función asignada.",
                "Normativa vigente y aplicable al momento de los hechos.",
                "Informes, memorandos, registros u otros documentos relacionados con la conducta.",
                "Demás medios probatorios pertinentes según la naturaleza del caso.",
            ]

        # ---------------------------------------------------------
        # 8. INFORMACIÓN FALTANTE
        # ---------------------------------------------------------

        informacion_faltante = []

        if not deber_limpio:
            informacion_faltante.append(
                "Precisar el deber, obligación o prohibición presuntamente incumplido."
            )

        if not falta_limpia:
            informacion_faltante.append(
                "Precisar la falta disciplinaria que podría corresponder."
            )

        if not normas:
            informacion_faltante.append(
                "Identificar y verificar la norma que contiene la obligación y/o tipificación aplicable."
            )

        if not hechos:
            informacion_faltante.append(
                "Incorporar los hechos concretos y verificables que sustentan la imputación."
            )

        if not evidencia:
            informacion_faltante.append(
                "Identificar los medios probatorios concretos que sustentan cada hecho imputado."
            )

        # ---------------------------------------------------------
        # 9. SUBSUNCIÓN PRELIMINAR
        # ---------------------------------------------------------

        subsuncion_preliminar = self._generar_subsuncion(
            conducta=conducta_limpia,
            deber=deber_limpio,
            posible_falta=falta_limpia,
            normas=normas,
            hechos=hechos,
        )

        # ---------------------------------------------------------
        # 10. NIVEL DE CONCLUSIÓN
        # ---------------------------------------------------------

        if falta_limpia and normas and hechos and deber_limpio:
            nivel_conclusion = "PRELIMINAR CON INFORMACIÓN SUFICIENTE"
            requiere_verificacion = True
            conclusion_falta = falta_limpia

        elif falta_limpia and normas:
            nivel_conclusion = "PRELIMINAR"
            requiere_verificacion = True
            conclusion_falta = falta_limpia

        else:
            nivel_conclusion = "INFORMACIÓN INSUFICIENTE"
            requiere_verificacion = True
            conclusion_falta = (
                "No corresponde establecer una tipificación definitiva "
                "con la información actualmente proporcionada."
            )

        # ---------------------------------------------------------
        # 11. FUENTE DEL DEBER
        # ---------------------------------------------------------

        if normas:
            fuente_del_deber = (
                "Debe verificarse en las normas proporcionadas "
                "cuál contiene específicamente el deber funcional."
            )
        else:
            fuente_del_deber = (
                "No determinada. Debe identificarse la fuente normativa "
                "del deber funcional."
            )

        # ---------------------------------------------------------
        # 12. OBSERVACIONES JURÍDICAS
        # ---------------------------------------------------------

        observaciones = [
            "La identificación de una posible falta no implica por sí misma responsabilidad administrativa.",
            "La tipificación debe guardar correspondencia con los hechos efectivamente acreditados.",
            "Debe verificarse la norma vigente y aplicable al momento de los hechos.",
            "Debe verificarse que la norma invocada sea aplicable al servidor y a la conducta atribuida.",
            "Debe evitarse atribuir hechos que no se encuentren sustentados documentalmente.",
            "La subsunción realizada por este motor tiene carácter preliminar.",
            "La conclusión requiere revisión integral del expediente administrativo.",
        ]

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


    def _determinar_tipo_conducta(self, conducta: str) -> str:
        """
        Clasificación preliminar simple de la conducta.

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
                "Se identifica un posible incumplimiento del deber descrito, "
                "pero no se ha proporcionado una posible falta disciplinaria "
                "que permita efectuar la subsunción correspondiente."
            )

        if not normas:
            return (
                "Existe una posible correspondencia entre los hechos, el deber "
                "y la falta propuesta; sin embargo, falta identificar y verificar "
                "la norma jurídica aplicable."
            )

        return (
            "Preliminarmente, los hechos proporcionados describen una conducta "
            "que podría guardar correspondencia con el deber funcional indicado "
            "y con la posible falta señalada. Esta correspondencia debe ser "
            "verificada mediante la revisión de la norma aplicable, la acreditación "
            "de los hechos, la intervención del servidor y los medios probatorios "
            "incorporados al expediente."
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

    print("=== PRUEBA TYPOFICATION ENGINE V2 ===")
    print(resultado.to_dict())
    print("=== PRUEBA COMPLETADA ===")
