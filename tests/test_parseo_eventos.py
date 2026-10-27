# -*- coding: utf-8 -*-

from app.core.typification_engine import TypificationEngine

motor = TypificationEngine()

CASOS = [
    (
        "El informe se emitió fuera del plazo.",
        [("EMISION", "FUERA_DE_PLAZO")],
    ),
    (
        "El informe fue emitido fuera del plazo establecido.",
        [("EMISION", "FUERA_DE_PLAZO")],
    ),
    (
        "El informe fue elaborado fuera del plazo establecido.",
        [("ELABORACION", "FUERA_DE_PLAZO")],
    ),
    (
        "La resolución se notificó fuera del plazo establecido.",
        [("NOTIFICACION", "FUERA_DE_PLAZO")],
    ),
    (
        "La resolución fue notificada dentro del plazo establecido.",
        [("NOTIFICACION", "DENTRO_DE_PLAZO")],
    ),
    (
        "Se notificó la resolución fuera del plazo.",
        [("NOTIFICACION", "FUERA_DE_PLAZO")],
    ),
    (
        "El informe se emitió dentro del plazo.",
        [("EMISION", "DENTRO_DE_PLAZO")],
    ),
]


def test_parseo_eventos():
    errores = []

    for texto, esperado in CASOS:
        obtenido = motor._parsear_eventos(texto)

        if obtenido != esperado:
            errores.append(
                f"\nTexto: {texto}"
                f"\nEsperado: {esperado}"
                f"\nObtenido: {obtenido}"
            )

    assert not errores, "\n".join(errores)
