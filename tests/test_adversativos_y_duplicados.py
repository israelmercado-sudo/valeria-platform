# -*- coding: utf-8 -*-
from app.core.typification_engine import TypificationEngine

engine = TypificationEngine()


def test_aunque_no_propaga_temporalidad():
    """El conector concesivo 'aunque' introduce una proposicion nueva."""
    texto = (
        "El informe fue elaborado fuera del plazo, "
        "aunque se remitio dentro del plazo."
    )
    eventos = engine._parsear_eventos(texto)
    assert eventos == [
        ("ELABORACION", "FUERA_DE_PLAZO"),
        ("REMISION", "DENTRO_DE_PLAZO"),
    ], eventos


def test_ni_no_duplica_remision():
    """La coordinacion 'ni' no debe duplicar eventos ya detectados."""
    texto = "El informe no fue elaborado ni remitido dentro del plazo."
    eventos = engine._parsear_eventos(texto)
    etapas = [etapa for etapa, _ in eventos]
    assert etapas.count("ELABORACION") == 1, eventos
    assert etapas.count("REMISION") == 1, eventos
