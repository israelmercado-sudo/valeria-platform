from datetime import date
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta


# ============================================================
# RESULTADO DEL MOTOR DE PRESCRIPCIÓN
# ============================================================

@dataclass
class PrescriptionResult:
    fecha_comision: date
    fecha_conocimiento_rrhh: date | None

    limite_tres_anios: date
    limite_un_anio_conocimiento: date | None

    fecha_limite_inicio_pad: date

    estado: str
    dias_restantes: int

    fundamento: str
    regla_aplicada: str

    requiere_verificacion: bool
    observaciones: str


# ============================================================
# MOTOR DE PRESCRIPCIÓN
# ============================================================

class PrescriptionEngine:

    def calcular(
        self,
        fecha_comision: date,
        fecha_conocimiento_rrhh: date | None = None,
        fecha_referencia: date | None = None
    ) -> PrescriptionResult:

        # =====================================================
        # 1. VALIDACIÓN DE DATOS
        # =====================================================

        self._validar_fecha(
            fecha_comision,
            "fecha_comision"
        )

        if fecha_conocimiento_rrhh is not None:
            self._validar_fecha(
                fecha_conocimiento_rrhh,
                "fecha_conocimiento_rrhh"
            )

        if fecha_referencia is not None:
            self._validar_fecha(
                fecha_referencia,
                "fecha_referencia"
            )

        # La fecha de conocimiento no puede ser anterior
        # a la fecha de comisión.
        if (
            fecha_conocimiento_rrhh is not None
            and fecha_conocimiento_rrhh < fecha_comision
        ):
            raise ValueError(
                "La fecha de conocimiento de Recursos Humanos "
                "no puede ser anterior a la fecha de comisión "
                "de la falta."
            )

        # =====================================================
        # 2. FECHA DE REFERENCIA
        # =====================================================

        # Permite realizar pruebas históricas.
        # Si no se proporciona, utiliza la fecha actual.
        hoy = fecha_referencia or date.today()

        # =====================================================
        # 3. PLAZO GENERAL DE TRES AÑOS
        # =====================================================

        limite_tres_anios = (
            fecha_comision + relativedelta(years=3)
        )

        # =====================================================
        # 4. PLAZO DE UN AÑO DESDE CONOCIMIENTO DE RR. HH.
        # =====================================================

        limite_un_anio_conocimiento = None

        if fecha_conocimiento_rrhh is not None:

            limite_un_anio_conocimiento = (
                fecha_conocimiento_rrhh
                + relativedelta(years=1)
            )

        # =====================================================
        # 5. DETERMINACIÓN DE LA FECHA LÍMITE
        # =====================================================

        if fecha_conocimiento_rrhh is None:

            # No existe fecha de conocimiento proporcionada.
            fecha_limite_inicio_pad = limite_tres_anios

            regla_aplicada = (
                "Se aplica preliminarmente el plazo general de "
                "tres años calendario desde la comisión de la falta, "
                "al no haberse proporcionado una fecha de conocimiento "
                "de Recursos Humanos."
            )

        elif fecha_conocimiento_rrhh <= limite_tres_anios:

            # El conocimiento ocurrió dentro del período de tres años.
            #
            # El plazo de un año desde conocimiento no puede superar
            # el límite máximo de tres años desde la comisión.

            fecha_limite_inicio_pad = min(
                limite_tres_anios,
                limite_un_anio_conocimiento
            )

            regla_aplicada = (
                "Se considera el plazo de un año calendario desde "
                "la toma de conocimiento de Recursos Humanos, "
                "sujeto al límite máximo de tres años desde la "
                "comisión de la falta."
            )

        else:

            # El conocimiento ocurrió después de vencido el plazo
            # general de tres años.

            fecha_limite_inicio_pad = limite_tres_anios

            regla_aplicada = (
                "El conocimiento de Recursos Humanos se produjo "
                "después del vencimiento del plazo general de tres "
                "años; por ello, preliminarmente se mantiene como "
                "fecha límite la correspondiente al plazo de tres "
                "años desde la comisión de la falta."
            )

        # =====================================================
        # 6. CÁLCULO DE DÍAS RESTANTES
        # =====================================================

        dias_restantes = (
            fecha_limite_inicio_pad - hoy
        ).days

        # =====================================================
        # 7. DETERMINACIÓN DEL ESTADO
        # =====================================================

        if hoy > fecha_limite_inicio_pad:

            estado = "PRESCRITO"

        elif hoy == fecha_limite_inicio_pad:

            estado = "VENCE HOY"

        elif dias_restantes <= 30:

            estado = "POR VENCER"

        else:

            estado = "NO PRESCRITO"

        # =====================================================
        # 8. FUNDAMENTO JURÍDICO
        # =====================================================

        fundamento = (
            "Artículo 94 de la Ley N.° 30057 y artículo 97.1 "
            "de su Reglamento General, aprobado por Decreto "
            "Supremo N.° 040-2014-PCM. El cómputo de la prescripción "
            "para el inicio del procedimiento administrativo "
            "disciplinario debe determinarse considerando el plazo "
            "general previsto legalmente y, cuando corresponda, "
            "la toma de conocimiento de la falta por la Oficina "
            "de Recursos Humanos o quien haga sus veces."
        )

        # =====================================================
        # 9. VERIFICACIÓN JURÍDICA Y DOCUMENTAL
        # =====================================================

        requiere_verificacion = True

        observaciones = self._generar_observaciones(
            fecha_comision=fecha_comision,
            fecha_conocimiento_rrhh=fecha_conocimiento_rrhh,
            limite_tres_anios=limite_tres_anios,
            limite_un_anio_conocimiento=limite_un_anio_conocimiento,
            fecha_limite_inicio_pad=fecha_limite_inicio_pad,
            hoy=hoy,
            estado=estado
        )

        # =====================================================
        # 10. DEVOLVER RESULTADO
        # =====================================================

        return PrescriptionResult(
            fecha_comision=fecha_comision,
            fecha_conocimiento_rrhh=fecha_conocimiento_rrhh,

            limite_tres_anios=limite_tres_anios,
            limite_un_anio_conocimiento=limite_un_anio_conocimiento,

            fecha_limite_inicio_pad=fecha_limite_inicio_pad,

            estado=estado,
            dias_restantes=dias_restantes,

            fundamento=fundamento,
            regla_aplicada=regla_aplicada,

            requiere_verificacion=requiere_verificacion,
            observaciones=observaciones
        )

    # =========================================================
    # VALIDACIÓN DE FECHAS
    # =========================================================

    @staticmethod
    def _validar_fecha(
        valor: date,
        nombre: str
    ) -> None:

        if not isinstance(valor, date):

            raise TypeError(
                f"{nombre} debe ser una fecha válida."
            )

    # =========================================================
    # GENERACIÓN DE OBSERVACIONES
    # =========================================================

    @staticmethod
    def _generar_observaciones(
        fecha_comision: date,
        fecha_conocimiento_rrhh: date | None,
        limite_tres_anios: date,
        limite_un_anio_conocimiento: date | None,
        fecha_limite_inicio_pad: date,
        hoy: date,
        estado: str
    ) -> str:

        observaciones = []

        # -----------------------------------------------------
        # Fecha de conocimiento
        # -----------------------------------------------------

        if fecha_conocimiento_rrhh is None:

            observaciones.append(
                "No se proporcionó la fecha de conocimiento de "
                "Recursos Humanos. El resultado se calcula "
                "preliminarmente sobre la base del plazo general "
                "de tres años desde la comisión de la falta."
            )

        else:

            observaciones.append(
                "La fecha de conocimiento de Recursos Humanos "
                "debe encontrarse respaldada por documentación "
                "que permita establecer una fecha cierta."
            )

        # -----------------------------------------------------
        # Estado
        # -----------------------------------------------------

        if estado == "PRESCRITO":

            observaciones.append(
                "El cálculo efectuado indica que la fecha límite "
                "para el inicio del PAD ya habría vencido. "
                "Debe efectuarse la verificación jurídica y "
                "documental correspondiente antes de emitir una "
                "conclusión definitiva."
            )

        elif estado == "VENCE HOY":

            observaciones.append(
                "La fecha de referencia coincide con la fecha "
                "límite calculada. El expediente requiere atención "
                "inmediata y verificación documental."
            )

        elif estado == "POR VENCER":

            observaciones.append(
                "La fecha límite calculada se encuentra próxima. "
                "Se recomienda verificar inmediatamente la "
                "documentación del expediente y las actuaciones "
                "realizadas."
            )

        else:

            observaciones.append(
                "De acuerdo con las fechas proporcionadas, "
                "el plazo calculado aún no habría vencido."
            )

        # -----------------------------------------------------
        # Verificación del inicio del PAD
        # -----------------------------------------------------

        observaciones.append(
            "El cálculo corresponde únicamente al plazo para "
            "determinar preliminarmente la prescripción de la "
            "potestad para iniciar el procedimiento. Debe "
            "verificarse el acto de inicio del PAD, su fecha de "
            "emisión, la fecha de notificación y demás actuaciones "
            "que resulten jurídicamente relevantes."
        )

        # -----------------------------------------------------
        # Supuestos especiales
        # -----------------------------------------------------

        observaciones.append(
            "El resultado debe ser revisado cuando existan hechos "
            "continuados o permanentes, pluralidad de conductas, "
            "regímenes jurídicos especiales, actuaciones que "
            "incidan en el cómputo del plazo u otras circunstancias "
            "que requieran un análisis jurídico específico."
        )

        return " ".join(observaciones)


# ============================================================
# INSTANCIA DEL MOTOR
# ============================================================

prescription_engine_v2 = PrescriptionEngine()


# ============================================================
# FUNCIONES AUXILIARES PARA VALERIA
# ============================================================

def calcular_prescripcion(
    fecha_comision: date,
    fecha_conocimiento_rrhh: date | None = None,
    fecha_referencia: date | None = None
) -> PrescriptionResult:

    """
    Función sencilla para que otros módulos de Valeria
    puedan utilizar el motor.

    Ejemplo:

        resultado = calcular_prescripcion(
            date(2024, 1, 15),
            date(2024, 3, 20)
        )
    """

    return prescription_engine_v2.calcular(
        fecha_comision=fecha_comision,
        fecha_conocimiento_rrhh=fecha_conocimiento_rrhh,
        fecha_referencia=fecha_referencia
    )


# ============================================================
# PRUEBAS DEL MOTOR
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("VALERIA PLATFORM - PRESCRIPTION ENGINE V2")
    print("=" * 70)

    # --------------------------------------------------------
    # CASO 1
    # Sin fecha de conocimiento de RR. HH.
    # --------------------------------------------------------

    caso1 = prescription_engine_v2.calcular(
        fecha_comision=date(2024, 1, 15)
    )

    print("\n=== CASO 1: SIN FECHA DE CONOCIMIENTO RR. HH. ===")
    print(
        f"Fecha comisión: "
        f"{caso1.fecha_comision}"
    )

    print(
        f"Límite tres años: "
        f"{caso1.limite_tres_anios}"
    )

    print(
        f"Fecha límite inicio PAD: "
        f"{caso1.fecha_limite_inicio_pad}"
    )

    print(
        f"Estado: "
        f"{caso1.estado}"
    )

    print(
        f"Días restantes: "
        f"{caso1.dias_restantes}"
    )

    print(
        f"Regla aplicada: "
        f"{caso1.regla_aplicada}"
    )

    # --------------------------------------------------------
    # CASO 2
    # Con fecha de conocimiento de RR. HH.
    # --------------------------------------------------------

    caso2 = prescription_engine_v2.calcular(
        fecha_comision=date(2023, 6, 1),
        fecha_conocimiento_rrhh=date(2025, 3, 15)
    )

    print("\n=== CASO 2: CON FECHA DE CONOCIMIENTO RR. HH. ===")

    print(
        f"Fecha comisión: "
        f"{caso2.fecha_comision}"
    )

    print(
        f"Fecha conocimiento RR. HH.: "
        f"{caso2.fecha_conocimiento_rrhh}"
    )

    print(
        f"Límite tres años: "
        f"{caso2.limite_tres_anios}"
    )

    print(
        f"Límite un año conocimiento: "
        f"{caso2.limite_un_anio_conocimiento}"
    )

    print(
        f"Fecha límite inicio PAD: "
        f"{caso2.fecha_limite_inicio_pad}"
    )

    print(
        f"Estado: "
        f"{caso2.estado}"
    )

    print(
        f"Días restantes: "
        f"{caso2.dias_restantes}"
    )

    print(
        f"Regla aplicada: "
        f"{caso2.regla_aplicada}"
    )

    print(
        f"Observaciones: "
        f"{caso2.observaciones}"
    )

    # --------------------------------------------------------
    # CASO 3
    # Prueba con fecha de referencia controlada
    # --------------------------------------------------------

    caso3 = prescription_engine_v2.calcular(
        fecha_comision=date(2022, 1, 15),
        fecha_conocimiento_rrhh=date(2022, 3, 20),
        fecha_referencia=date(2025, 3, 20)
    )

    print("\n=== CASO 3: FECHA DE REFERENCIA CONTROLADA ===")

    print(
        f"Fecha comisión: "
        f"{caso3.fecha_comision}"
    )

    print(
        f"Fecha conocimiento RR. HH.: "
        f"{caso3.fecha_conocimiento_rrhh}"
    )

    print(
        f"Fecha límite inicio PAD: "
        f"{caso3.fecha_limite_inicio_pad}"
    )

    print(
        f"Fecha referencia: "
        f"{date(2025, 3, 20)}"
    )

    print(
        f"Estado: "
        f"{caso3.estado}"
    )

    print(
        f"Días restantes: "
        f"{caso3.dias_restantes}"
    )

    print("\n" + "=" * 70)
    print("PRUEBAS FINALIZADAS")
    print("=" * 70)