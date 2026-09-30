# motor_tipificacion.py
from dataclasses import dataclass, field
from typing import List, Dict
import json

def fix_encoding(s):
    return (s.replace("jur?dicamente", "juridicamente")
             .replace("documentaci?n", "documentacion")
             .replace("descripci?n", "descripcion")
             .replace("corroboraci?n", "corroboracion"))

@dataclass
class Evento:
    etapa: str
    estado: str

@dataclass
class TypificationResult:
    conducta_identificada: str
    tipo_conducta: str
    deber_presuntamente_incumplido: str
    fuente_del_deber: str
    posible_falta: str
    norma_tipificacion: List[str] = field(default_factory=list)
    subsuncion_preliminar: str = ""
    elementos_tipo: List[str] = field(default_factory=list)
    elementos_acreditados: List[str] = field(default_factory=list)
    elementos_no_acreditados: List[str] = field(default_factory=list)
    elementos_a_acreditar: List[str] = field(default_factory=list)
    hechos_relevantes: List[str] = field(default_factory=list)
    evidencia_necesaria: List[str] = field(default_factory=list)
    informacion_faltante: List[str] = field(default_factory=list)
    nivel_conclusion: str = ""
    requiere_verificacion: bool = True
    observaciones: List[str] = field(default_factory=list)
    matriz_subsuncion: List[Dict] = field(default_factory=list)

def parsear_eventos(texto):
    t = texto.lower()

    separadores = [" y posteriormente ", " posteriormente ", " pero ", " y luego ", " y "]
    fragmentos = [t]
    for sep in separadores:
        nuevos = []
        for f in fragmentos:
            nuevos.extend(f.split(sep))
        fragmentos = nuevos
    fragmentos = [f.strip().strip(",").strip(".") for f in fragmentos if f.strip()]

    eventos = []
    for f in fragmentos:
        if "elaborado" in f or "elaboro" in f:
            if "no fue elaborado" in f or "no se elaboro" in f:
                eventos.append(Evento("ELABORACION", "NO_EJECUTADO"))
            elif "fuera del plazo" in f:
                eventos.append(Evento("ELABORACION", "FUERA_DE_PLAZO"))
            elif "dentro del plazo" in f:
                eventos.append(Evento("ELABORACION", "DENTRO_DE_PLAZO"))

        if "remitido" in f or "presentado" in f:
            if "no fue remitido" in f or "no remitido" in f or "no fue presentado" in f or "no fue remitida" in f:
                eventos.append(Evento("REMISION", "NO_EJECUTADO"))
            elif "fuera del plazo" in f:
                eventos.append(Evento("REMISION", "FUERA_DE_PLAZO"))
            elif "dentro del plazo" in f:
                eventos.append(Evento("REMISION", "DENTRO_DE_PLAZO"))

    return eventos

def tipificar(texto):
    texto = fix_encoding(texto)
    eventos = parsear_eventos(texto)
    etapas_incumplidas = [e for e in eventos if e.estado in ("FUERA_DE_PLAZO", "NO_EJECUTADO")]

    if not etapas_incumplidas:
        tipo = "SIN INDICIO DE INCUMPLIMIENTO (SUJETO A VERIFICACION)"
        deber = "Ninguno identificado preliminarmente."
        nivel = "SIN MERITO PRELIMINAR - REQUIERE VERIFICACION DOCUMENTAL"
        posible = "No corresponde tipificar. El enunciado afirma cumplimiento."
    else:
        nombres = []
        for e in etapas_incumplidas:
            if e.etapa == "ELABORACION" and e.estado == "FUERA_DE_PLAZO":
                nombres.append("INCUMPLIMIENTO DE PLAZO (ELABORACION)")
            elif e.etapa == "REMISION" and e.estado == "FUERA_DE_PLAZO":
                nombres.append("INCUMPLIMIENTO DE PLAZO (REMISION)")
            elif e.etapa == "REMISION" and e.estado == "NO_EJECUTADO":
                nombres.append("OMISION (NO REMISION)")
            elif e.etapa == "ELABORACION" and e.estado == "NO_EJECUTADO":
                nombres.append("OMISION (NO ELABORACION)")
        tipo = " + ".join(nombres)
        deber = "Deber funcional asociado a la etapa incumplida (a individualizar normativamente)."
        nivel = "INDICIO PRELIMINAR DE INCUMPLIMIENTO - REQUIERE VERIFICACION NORMATIVA Y PROBATORIA"
        posible = "No corresponde tipificacion definitiva con la informacion actual."

    acreditados = []
    if "dentro del plazo" in texto.lower():
        acreditados.append("Afirmacion preliminar de cumplimiento de plazo (a verificar documentalmente).")
    if "fuera del plazo" in texto.lower():
        acreditados.append("Afirmacion preliminar de incumplimiento de plazo (a verificar documentalmente).")
    if "no fue remitido" in texto.lower():
        acreditados.append("Afirmacion preliminar de no remision (a verificar).")

    matriz = []
    for e in eventos:
        matriz.append({
            "dimension": "ETAPA",
            "contenido": e.etapa + " - " + e.estado,
            "fundamento": "Evento identificado preliminarmente; requiere contraste con fechas y norma.",
            "prioridad": "ALTA" if e.estado != "DENTRO_DE_PLAZO" else "MEDIA",
            "hecho_origen": texto,
        })

    return TypificationResult(
        conducta_identificada=texto,
        tipo_conducta=tipo,
        deber_presuntamente_incumplido=deber,
        fuente_del_deber="No determinada. Debe identificarse la disposicion normativa.",
        posible_falta=posible,
        elementos_acreditados=acreditados,
        elementos_a_acreditar=[
            "Norma que fija el plazo aplicable.",
            "Fecha cierta del evento (elaboracion y/o remision).",
            "Intervencion del servidor obligado.",
            "Causas de la demora o no ejecucion (relevantes para culpabilidad).",
        ],
        informacion_faltante=[
            "Norma que fija el deber y el plazo.",
            "Constancia documental de fechas.",
            "Identificacion del servidor obligado por etapa.",
        ],
        hechos_relevantes=[texto],
        evidencia_necesaria=[
            "Documento con fecha cierta de elaboracion.",
            "Cargo o constancia de remision/recepcion.",
            "Norma vigente al momento de los hechos.",
        ],
        nivel_conclusion=nivel,
        requiere_verificacion=True,
        observaciones=[
            "La informacion es insumo preliminar, no hecho acreditado.",
            "Debe distinguirse deber de elaborar y deber de remitir.",
            "RIESGO 1: plazo no individualizado normativamente.",
            "RIESGO 2: falta constancia documental de fechas.",
            "RIESGO 3: intervencion del servidor no verificada.",
        ],
        matriz_subsuncion=matriz,
    )

def cargar_casos(ruta):
    with open(ruta, "r", encoding="utf-8-sig") as f:
        contenido = f.read()
    casos = []
    for linea in contenido.splitlines():
        linea = linea.strip()
        if linea.startswith("CASO:"):
            casos.append(linea.replace("CASO:", "").strip())
    return casos

if __name__ == "__main__":
    casos = cargar_casos("casos.txt")
    for c in casos:
        r = tipificar(c)
        print("=" * 70)
        print("CASO:", c)
        print("TIPO:", r.tipo_conducta)
        print("NIVEL:", r.nivel_conclusion)
        print("ACREDITADOS:", r.elementos_acreditados)
        print("MATRIZ:", json.dumps(r.matriz_subsuncion, ensure_ascii=False, indent=2))



