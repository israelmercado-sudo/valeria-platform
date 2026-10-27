from app.core.typification_engine import TypificationEngine


def test_rectificacion_expresa_elaboracion_dentro_del_plazo():
    engine = TypificationEngine()
    texto = (
        "El informe no fue elaborado fuera del plazo, "
        "sino dentro del plazo."
    )

    eventos = engine._parsear_eventos(texto)

    assert eventos == [("ELABORACION", "DENTRO_DE_PLAZO")]


def test_rectificacion_expresa_remision_dentro_del_plazo():
    engine = TypificationEngine()
    texto = (
        "El informe no fue remitido fuera del plazo, "
        "sino dentro del plazo."
    )

    eventos = engine._parsear_eventos(texto)

    assert eventos == [("REMISION", "DENTRO_DE_PLAZO")]


def test_omision_sin_referencia_temporal_se_conserva():
    engine = TypificationEngine()

    eventos = engine._parsear_eventos("El informe no fue elaborado.")

    assert eventos == [("ELABORACION", "NO_EJECUTADO")]
