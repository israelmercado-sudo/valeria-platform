from app.core.typification_engine import TypificationEngine


def test_hecho_no_acreditado_no_se_clasifica_como_incumplimiento():
    motor = TypificationEngine()
    conducta = (
        "No se ha acreditado que el informe fuera elaborado "
        "fuera del plazo."
    )

    resultado = motor.analizar(conducta=conducta)

    assert resultado.tipo_conducta != (
        "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)"
    )


def test_incumplimiento_temporal_afirmado_se_conserva():
    motor = TypificationEngine()
    conducta = "El informe fue elaborado fuera del plazo."

    resultado = motor.analizar(conducta=conducta)

    assert resultado.tipo_conducta == (
        "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)"
    )


def test_omision_explicita_se_conserva():
    motor = TypificationEngine()
    conducta = "El informe no fue elaborado."

    resultado = motor.analizar(conducta=conducta)

    assert resultado.tipo_conducta == (
        "OMISIÓN - NO ELABORACIÓN"
    )
