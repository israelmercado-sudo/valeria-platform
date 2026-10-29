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


# --- TEXTOS LITERALES (aplicar_textos_normas.py) ---
# Cargan el texto literal desde app/data/normas_textos_literales.json.
# Esto NO verifica nada: una norma sigue siendo candidata hasta tener URL oficial,
# fecha de consulta, responsable y vigencia confirmada.
import json as _json
from pathlib import Path as _Path

_NUEVAS = {
    "TUO27444_DEBERES_AUTORIDADES": (
        "TUO de la Ley 27444 (DS 006-2026-JUS), art. 75 - Deberes de las autoridades en los procedimientos",
        "Deberes de las autoridades respecto del procedimiento administrativo "
        "(texto aportado por el usuario; sin verificar contra fuente oficial).",
    ),
    "TUO27444_ART239": (
        "TUO de la Ley 27444 (DS 006-2026-JUS), art. 239 - Faltas administrativas",
        "Faltas administrativas de autoridades y personal en el tramite de procedimientos "
        "(texto aportado por el usuario; sin verificar contra fuente oficial).",
    ),
}
for _id, (_cita, _res) in _NUEVAS.items():
    NORMAS.setdefault(_id, {
        "id": _id, "cita_completa": _cita, "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None, "url_fuente": None, "fecha_consulta": None,
        "verificado_por": None, "vigencia": None, "resumen_secundario": _res,
        "conductas_aplicables": [], "conductas_validadas_por": None,
    })


def _cargar_textos_literales():
    ruta = _Path(__file__).resolve().parent.parent / "data" / "normas_textos_literales.json"
    if not ruta.exists():
        return
    with open(ruta, encoding="utf-8-sig") as f:
        datos = _json.load(f)
    for _id, d in datos.items():
        n = NORMAS.get(_id)
        if n is not None and not n.get("texto_literal"):
            n["texto_literal"] = d["texto_literal"]
            n["fuente_del_texto"] = d.get("fuente_del_texto")




# --- Ley 30057: régimen sancionador (candidatas, pendientes de verificación) ---
NORMAS.update({
    "LEY30057_ART87": {
        "id": "LEY30057_ART87",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 87 - Determinación de la sanción a las faltas",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "La sanción debe ser proporcional a la falta y se determina evaluando condiciones como afectación grave a intereses generales, ocultamiento de la falta, jerarquía y especialidad del servidor, concurrencia, reincidencia, continuidad y beneficio ilícito. La destitución inhabilita para reingresar al Estado por 5 años.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART88": {
        "id": "LEY30057_ART88",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 88 - Sanciones aplicables",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "Sanciones por faltas disciplinarias: amonestación verbal o escrita, suspensión sin goce de remuneraciones y destitución. Toda sanción consta en el legajo.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART90": {
        "id": "LEY30057_ART90",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 90 - La suspensión y la destitución",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "Suspensión sin goce de remuneraciones hasta 365 días calendario, previo procedimiento administrativo disciplinario. Destitución propuesta por el jefe de recursos humanos y aprobada por el titular de la entidad. La apelación la resuelve el Tribunal del Servicio Civil.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART91": {
        "id": "LEY30057_ART91",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 91 - Graduación de la sanción",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "Los actos que imponen sanciones deben estar motivados de modo expreso y claro, identificando la relación entre hechos y faltas y los criterios de determinación. La sanción no es necesariamente correlativa ni automática.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART92": {
        "id": "LEY30057_ART92",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 92 - Autoridades",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "Autoridades del procedimiento disciplinario: jefe inmediato, jefe de recursos humanos, titular de la entidad y Tribunal del Servicio Civil. El secretario técnico precalifica las faltas y no tiene capacidad de decisión.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART93": {
        "id": "LEY30057_ART93",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 93 - El procedimiento administrativo disciplinario",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "Se comunica por escrito al servidor las presuntas faltas y se le otorga 5 días hábiles para presentar descargo y pruebas. Prevé informe oral y la posibilidad de separar al servidor de su función durante el procedimiento.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
    "LEY30057_ART96": {
        "id": "LEY30057_ART96",
        "cita_completa": "Ley 30057 - Ley del Servicio Civil, art. 96 - Medidas cautelares",
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": "Tras comunicar por escrito las presuntas faltas, la autoridad puede, con decisión motivada, separar al servidor de su función o exonerarlo de asistir al centro de trabajo, abonándole su remuneración.",
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
    },
})


# --- Relaciones de remisión disciplinaria ---
# Registro estructural: no acredita por sí solo responsabilidad disciplinaria.

for _id, _articulo, _tipo in (
    ("LEY27815_ART6", "6", "principios"),
    ("LEY27815_ART7", "7", "deberes"),
    ("LEY27815_ART8", "8", "prohibiciones"),
):
    NORMAS.setdefault(_id, {
        "id": _id,
        "cita_completa": (
            f"Ley 27815 - Código de Ética de la Función Pública, "
            f"art. {_articulo}"
        ),
        "jurisdiccion": JURISDICCION_PE,
        "texto_literal": None,
        "url_fuente": None,
        "fecha_consulta": None,
        "verificado_por": None,
        "vigencia": None,
        "resumen_secundario": (
            f"Artículo {_articulo}: { _tipo }. "
            "Texto y vigencia pendientes de verificación oficial."
        ),
        "conductas_aplicables": [],
        "conductas_validadas_por": None,
        "sancionable_via": ["LEY30057_ART85_Q"],
    })

NORMAS["LEY30057_ART85_Q"].update({
    "es_norma_de_remision": True,
    "remite_a": [
        "LEY27815_ART6",
        "LEY27815_ART7",
        "LEY27815_ART8",
        "RGLEY30057_ART100",
    ],
})

NORMAS["RGLEY30057_ART100"]["remite_a"] = [
    "LEY27815_ART6",
    "LEY27815_ART7",
    "LEY27815_ART8",
]


def problemas_remision(norma: dict) -> list[str]:
    """Comprueba la integridad estructural de las referencias normativas."""
    problemas: list[str] = []

    for campo in ("remite_a", "sancionable_via"):
        destinos = norma.get(campo, [])

        if not isinstance(destinos, list):
            problemas.append(f"{campo} debe ser una lista")
            continue

        for destino in destinos:
            if not isinstance(destino, str) or destino not in NORMAS:
                problemas.append(f"{campo}: destino inexistente {destino}")

    if norma.get("es_norma_de_remision") is True:
        if not norma.get("remite_a"):
            problemas.append("norma de remisión sin destinos")

    return problemas


# --- VERIFICACIONES (normas_verificaciones.json) ---
# Solo copia los 4 campos de verificación. La decisión de "verificada"
# sigue siendo de esta_verificada(); aquí no se marca nada a mano.
def _cargar_verificaciones():
    ruta = _Path(__file__).resolve().parent.parent / "data" / "normas_verificaciones.json"
    if not ruta.exists():
        return
    with open(ruta, encoding="utf-8-sig") as f:
        datos = _json.load(f)
    for _id, d in datos.items():
        n = NORMAS.get(_id)
        if n is None:
            continue
        for campo in ("url_fuente", "fecha_consulta", "verificado_por", "vigencia"):
            if campo in d:
                n[campo] = d[campo]


_cargar_textos_literales()
_cargar_verificaciones()
