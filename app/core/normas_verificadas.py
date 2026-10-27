# app/core/normas_verificadas.py
"""
Registro de normas de Valeria.

Regla: `verificado` NO se escribe a mano. Se calcula con `esta_verificada()`.
Una norma solo cuenta como verificada si tiene texto literal real, fuente oficial
con URL válida, fecha de consulta, responsable y vigencia confirmada.

Los campos de verificación se llenan SOLO después de contrastar con la fuente
oficial (SPIJ / El Peruano). Mientras estén en None, la norma es "candidata".
"""
from __future__ import annotations

import re
from datetime import date

MARCADORES_PLACEHOLDER = ("...", "…", "<<VERIFICAR>>", "TODO", "XXX", "PENDIENTE")

CAMPOS_OBLIGATORIOS = (
    "id",
    "cita_completa",
    "jurisdiccion",
    "texto_literal",
    "url_fuente",
    "fecha_consulta",
    "verificado_por",
    "vigencia",
)

ADVERTENCIA_CANDIDATA = (
    "Norma candidata, pendiente de verificación por operador jurídico. "
    "No presentar como sustento confirmado."
)

JURISDICCION_PE = {"pais": "Perú", "ordenamiento": "Régimen disciplinario del Servicio Civil"}

NORMAS = {
    "LEY30057_ART85_A": {
        "id": "LEY30057_ART85_A",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 85, literal a)",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,       # "AAAA-MM-DD"
        "verificado_por": None,
        "vigencia": None,             # {"vigente": True, "modificaciones": [], "derogada_por": None}
        "resumen_secundario": (
            "Falta por incumplimiento de las normas de la Ley 30057 y su Reglamento "
            "(según resoluciones administrativas que la citan)."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART85_D": {
        "id": "LEY30057_ART85_D",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 85, literal d)",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": (
            "Falta por negligencia en el desempeño de las funciones "
            "(según resoluciones administrativas que la citan)."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART85_Q": {
        "id": "LEY30057_ART85_Q",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 85, literal q)",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": (
            "Cláusula de remisión a otras faltas previstas por ley; se vincula con "
            "el art. 100 del Reglamento General (DS 040-2014-PCM) respecto de "
            "incumplimientos de las Leyes 27444 y 27815."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "RGLEY30057_ART100": {
        "id": "RGLEY30057_ART100",
        "cita_completa": "Reglamento General de la Ley 30057 (DS 040-2014-PCM), art. 100",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": (
            "Faltas por incumplimiento de la Ley 27444 y de la Ley 27815."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART94": {
        "id": "LEY30057_ART94",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 94",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": (
            "Prescripci\u00f3n de la potestad para iniciar el procedimiento "
            "administrativo disciplinario (seg\u00fan el fundamento actual de "
            "prescription_engine; sin verificar contra fuente oficial)."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "RGLEY30057_ART97_1": {
        "id": "RGLEY30057_ART97_1",
        "cita_completa": "Reglamento General de la Ley 30057 (DS 040-2014-PCM), art. 97.1",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": (
            "Plazos de prescripci\u00f3n del procedimiento disciplinario "
            "(seg\u00fan el fundamento actual de prescription_engine; sin "
            "verificar contra fuente oficial)."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    # El artículo concreto del TUO 27444 aún no está identificado.
    # No se agrega con "<<VERIFICAR>>": se incorpora cuando se confirme.
}


def _tiene_placeholder(valor) -> bool:
    if isinstance(valor, str):
        return any(m in valor for m in MARCADORES_PLACEHOLDER)
    return False


def _url_valida(url) -> bool:
    return isinstance(url, str) and re.match(r"^https://[^\s/]+\.[^\s/]+/\S+$", url) is not None and not _tiene_placeholder(url)


def _fecha_valida(f) -> bool:
    if not isinstance(f, str):
        return False
    try:
        date.fromisoformat(f)
        return True
    except ValueError:
        return False


def problemas_verificacion(norma: dict) -> list[str]:
    """Devuelve la lista de razones por las que la norma NO está verificada."""
    p: list[str] = []
    for campo in CAMPOS_OBLIGATORIOS:
        v = norma.get(campo)
        if v in (None, "", {}):
            p.append(f"falta {campo}")
        elif _tiene_placeholder(v):
            p.append(f"{campo} contiene placeholder")
    if norma.get("url_fuente") and not _url_valida(norma["url_fuente"]):
        p.append("url_fuente inválida")
    if norma.get("fecha_consulta") and not _fecha_valida(norma["fecha_consulta"]):
        p.append("fecha_consulta inválida (usar AAAA-MM-DD)")
    vig = norma.get("vigencia")
    if isinstance(vig, dict):
        if vig.get("vigente") is not True:
            p.append("vigencia no confirmada como vigente")
    elif vig not in (None, "", {}):
        p.append("vigencia debe ser un dict")
    return p


def esta_verificada(norma: dict) -> bool:
    return not problemas_verificacion(norma)


def como_candidata(norma_id: str) -> dict:
    """Vista pública de una norma, con `verificado` calculado y trazabilidad."""
    n = NORMAS[norma_id]
    probs = problemas_verificacion(n)
    salida = {
        "id": n["id"],
        "cita": n["cita_completa"],
        "jurisdiccion": n["jurisdiccion"],
        "verificado": not probs,
    }
    if probs:
        salida["advertencia"] = ADVERTENCIA_CANDIDATA
        salida["pendiente"] = probs
        salida["resumen_secundario"] = n["resumen_secundario"]
    else:
        salida["texto"] = n["texto_literal"]
        salida["fuente"] = n["url_fuente"]
        salida["fecha_consulta"] = n["fecha_consulta"]
    return salida


def verificada_por_id(norma_id: str) -> bool:
    """True solo si el id existe en el registro y esa norma pasa todos los controles."""
    n = NORMAS.get(norma_id)
    return n is not None and esta_verificada(n)
