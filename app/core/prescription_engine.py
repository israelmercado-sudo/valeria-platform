from datetime import date
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta


@dataclass
class PrescriptionResult:
    fecha_comision: date
    fecha_conocimiento_rrhh: date | None
    limite_tres_anios: date
    limite_un_anio_conocimiento: date | None
    fecha_limite_inicio_pad: date
    estado: str
    fundamento: str
    regla_aplicada: str
    requiere_verificacion: bool
    observaciones: str


class PrescriptionEngine:

    def calcular(
        self,
        fecha_comision: date,
        fecha_conocimiento_rrhh: date | None = None
    ) -> PrescriptionResult:

        # =========================================================
        # 1. VALIDACION DE DATOS
        # =========================================================

        if not isinstance(fecha_comision, date):
            raise TypeError(
                "fecha_comision debe ser una fecha valida."
            )

        if (
            fecha_conocimiento_rrhh is not None
            and not isinstance(fecha_conocimiento_rrhh, date)
        ):
            raise TypeError(
                "fecha_conocimiento_rrhh debe ser una fecha valida o None."
            )

        if (
            fecha_conocimiento_rrhh is not None
            and fecha_conocimiento_rrhh < fecha_comision
        ):
            raise ValueError(
                "La fecha de conocimiento de RR. HH. no puede ser "
                "anterior a la fecha de comision de la falta."
            )

        # =========================================================
        # 2. PLAZO GENERAL DE TRES ANOS
        # =========================================================

        limite_tres_anios = (
            fecha_comision + relativedelta(years=3)
        )

        # =========================================================
        # 3. PLAZO DE UN ANO DESDE CONOCIMIENTO DE RR. HH.
        # =========================================================

        limite_un_anio_conocimiento = None

        if fecha_conocimiento_rrhh is not None:
            limite_un_anio_conocimiento = (
                fecha_conocimiento_rrhh + relativedelta(years=1)
            )

        # =========================================================
        # 4. DETERMINACION DE LA FECHA LIMITE
        # =========================================================

        if (
            fecha_conocimiento_rrhh is not None
            and fecha_conocimiento_rrhh <= limite_tres_anios
        ):

            fecha_limite_inicio_pad = min(
                limite_tres_anios,
                limite_un_anio_conocimiento
            )

            regla_aplicada = (
                "Plazo de un ano calendario desde la toma de "
                "conocimiento de la Oficina de Recursos Humanos, "
                "sujeto al limite maximo de tres anos desde la "
                "comision de la falta."
            )

        else:

            fecha_limite_inicio_pad = limite_tres_anios

            regla_aplicada = (
                "Plazo general de tres anos calendario desde la "
                "comision de la falta."
            )

        # =========================================================
        # 5. DETERMINACION DEL ESTADO
        # =========================================================

        hoy = date.today()

        if hoy > fecha_limite_inicio_pad:
            estado = "PRESCRITO"
        else:
            estado = "NO PRESCRITO"

        # =========================================================
        # 6. FUNDAMENTO JURIDICO
        # =========================================================

        fundamento = (
            "Articulo 94 de la Ley N.° 30057 y articulo 97.1 de su "
            "Reglamento General. La potestad para iniciar el "
            "procedimiento administrativo disciplinario prescribe "
            "a los tres anos calendario de cometida la falta. "
            "Si durante ese periodo la Oficina de Recursos Humanos, "
            "o quien haga sus veces, toma conocimiento de la falta, "
            "opera el plazo de un ano calendario desde dicha toma "
            "de conocimiento, siempre que no hubiera transcurrido "
            "el plazo de tres anos."
        )

        # =========================================================
        # 7. VERIFICACION DOCUMENTAL
        # =========================================================

        requiere_verificacion = True

        if fecha_conocimiento_rrhh is None:

            observaciones = (
                "No se proporciono la fecha de conocimiento de la "
                "Oficina de Recursos Humanos. El calculo se efectua "
                "sobre la base del plazo general de tres anos desde "
                "la comision de la falta. Corresponde verificar "
                "documentalmente si existe una fecha de conocimiento "
                "de RR. HH. que resulte juridicamente relevante."
            )

        else:

            observaciones = (
                "El resultado constituye un calculo preliminar. "
                "Debe verificarse documentalmente la fecha de "
                "conocimiento de Recursos Humanos, el acto de inicio "
                "del PAD, la fecha de su notificacion y cualquier "
                "circunstancia juridica que pueda afectar el computo "
                "del plazo."
            )

        # =========================================================
        # 8. RESULTADO
        # =========================================================

        return PrescriptionResult(
            fecha_comision=fecha_comision,
            fecha_conocimiento_rrhh=fecha_conocimiento_rrhh,
            limite_tres_anios=limite_tres_anios,
            limite_un_anio_conocimiento=limite_un_anio_conocimiento,
            fecha_limite_inicio_pad=fecha_limite_inicio_pad,
            estado=estado,
            fundamento=fundamento,
            regla_aplicada=regla_aplicada,
            requiere_verificacion=requiere_verificacion,
            observaciones=observaciones
        )


prescription_engine = PrescriptionEngine()