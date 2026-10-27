import copy

import pytest

from app.core.normas_verificadas import (
    NORMAS,
    como_candidata,
    esta_verificada,
    problemas_verificacion,
)


def _norma_completa():
    return {
        "id": "TEST_ART1",
        "cita_completa": "Norma de prueba, art. 1",
        "jurisdiccion": {"pais": "Perú", "ordenamiento": "Prueba"},
        "texto_literal": "Texto completo de prueba sin marcadores.",
        "url_fuente": "https://spij.minjus.gob.pe/ejemplo/norma",
        "fecha_consulta": "2026-10-27",
        "verificado_por": "Revisor de prueba",
        "vigencia": {"vigente": True, "modificaciones": [], "derogada_por": None},
    }


def test_norma_completa_es_verificada():
    assert esta_verificada(_norma_completa())


@pytest.mark.parametrize("marcador", ["...", "…", "<<VERIFICAR>>", "TODO"])
def test_texto_con_placeholder_no_se_verifica(marcador):
    n = _norma_completa()
    n["texto_literal"] = f"Incurre en falta el servidor que {marcador}"
    assert not esta_verificada(n)


@pytest.mark.parametrize("url", ["https://www.gob.pe/...", "gob.pe/x", "", None])
def test_url_invalida_no_se_verifica(url):
    n = _norma_completa()
    n["url_fuente"] = url
    assert not esta_verificada(n)


@pytest.mark.parametrize("campo", [
    "texto_literal", "url_fuente", "fecha_consulta", "verificado_por", "vigencia", "jurisdiccion",
])
def test_campo_faltante_no_se_verifica(campo):
    n = copy.deepcopy(_norma_completa())
    n[campo] = None
    assert not esta_verificada(n)


def test_fecha_invalida_no_se_verifica():
    n = _norma_completa()
    n["fecha_consulta"] = "27/10/2026"
    assert not esta_verificada(n)


def test_norma_derogada_no_se_verifica():
    n = _norma_completa()
    n["vigencia"] = {"vigente": False, "derogada_por": "Norma X"}
    assert not esta_verificada(n)


def test_toda_norma_tiene_estructura_minima():
    for nid, n in NORMAS.items():
        assert n["id"] == nid
        assert n["cita_completa"]
        assert n["jurisdiccion"]


def test_ninguna_norma_marcada_verificada_con_placeholder():
    for nid in NORMAS:
        vista = como_candidata(nid)
        if vista["verificado"]:
            assert not problemas_verificacion(NORMAS[nid])
            for k in ("texto", "fuente", "fecha_consulta"):
                assert vista[k]


def test_candidata_no_verificada_lleva_advertencia():
    for nid in NORMAS:
        vista = como_candidata(nid)
        if not vista["verificado"]:
            assert vista["advertencia"]
            assert vista["pendiente"]
            assert "texto" not in vista
