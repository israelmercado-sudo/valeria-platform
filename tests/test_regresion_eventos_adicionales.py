import pytest
from app.core.typification_engine import TypificationEngine


@pytest.mark.parametrize(
    "texto,eventos_esperados,tipo_esperado",
    [
        (
            "El informe fue elaborado dentro del plazo y posteriormente remitido fuera del plazo.",
            [
                ("ELABORACION", "DENTRO_DE_PLAZO"),
                ("REMISION", "FUERA_DE_PLAZO"),
            ],
            "INCUMPLIMIENTO DE PLAZO (REMISIÓN)",
        ),
        (
            "El informe fue elaborado fuera del plazo y posteriormente remitido dentro del plazo.",
            [
                ("ELABORACION", "FUERA_DE_PLAZO"),
                ("REMISION", "DENTRO_DE_PLAZO"),
            ],
            "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)",
        ),
        (
            "El informe no fue elaborado ni remitido.",
            [
                ("ELABORACION", "NO_EJECUTADO"),
                ("REMISION", "NO_EJECUTADO"),
            ],
            "OMISIÓN - NO ELABORACIÓN + OMISIÓN - NO REMISIÓN",
        ),
        (
            "El informe fue emitido dentro del plazo y posteriormente notificado fuera del plazo.",
            [
                ("EMISION", "DENTRO_DE_PLAZO"),
                ("NOTIFICACION", "FUERA_DE_PLAZO"),
            ],
            "INCUMPLIMIENTO DE PLAZO (NOTIFICACIÓN)",
        ),
        (
            "El informe fue emitido fuera del plazo y posteriormente notificado dentro del plazo.",
            [
                ("EMISION", "FUERA_DE_PLAZO"),
                ("NOTIFICACION", "DENTRO_DE_PLAZO"),
            ],
            "INCUMPLIMIENTO DE PLAZO (EMISIÓN)",
        ),
        (
            "El informe no fue elaborado.",
            [
                ("ELABORACION", "NO_EJECUTADO"),
            ],
            "OMISIÓN - NO ELABORACIÓN",
        ),
    ],
)
def test_eventos_y_clasificacion_independiente(
    texto, eventos_esperados, tipo_esperado
):
    engine = TypificationEngine()

    eventos = engine._parsear_eventos(texto)
    resultado = engine.analizar(conducta=texto)

    assert eventos == eventos_esperados, (
        f"Eventos inesperados para: {texto}\n"
        f"Obtenidos: {eventos}"
    )
    assert resultado.tipo_conducta == tipo_esperado, (
        f"Clasificación inesperada para: {texto}\n"
        f"Obtenida: {resultado.tipo_conducta}"
    )
