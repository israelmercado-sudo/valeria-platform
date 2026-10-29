import argparse
import json
import sys
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse

DOMINIOS = ("spij.minjus.gob.pe", "elperuano.pe", "gob.pe", "congreso.gob.pe")
TEXTOS = Path("app/data/normas_textos_literales.json")
DISCIPLINARIAS = Path("app/data/normas_disciplinarias.json")
VERIF = Path("app/data/normas_verificaciones.json")


def salir(msg):
    print("NO SE GUARDO NADA:", msg)
    sys.exit(1)


def validar_url(url):
    if "..." in url or len(url) < 20:
        salir("la URL no parece una URL real y completa")
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        salir("la URL debe ser https:// con host valido")
    host = parsed.hostname.lower()
    if not any(host == d or host.endswith("." + d) for d in DOMINIOS):
        salir("el dominio " + host + " no es una fuente oficial conocida (SPIJ, El Peruano, gob.pe, Congreso)")
    return host


def validar_por(nombre):
    limpio = nombre.strip()
    if len(limpio) < 5 or "?" in limpio:
        salir("revisa el nombre en --por (muy corto o con tildes danadas)")
    prohibidos = {"nombre apellido", "n n", "xxx", "test", "admin", "usuario"}
    if limpio.lower() in prohibidos:
        salir("--por parece un nombre de ejemplo, no una persona real")


def validar_fecha(txt):
    try:
        f = datetime.strptime(txt, "%Y-%m-%d").date()
    except ValueError:
        salir("la fecha debe tener el formato AAAA-MM-DD")
    if f > date.today():
        salir("la fecha de consulta no puede ser futura")


def validar_vigencia(vigente, derogada_por, modificaciones, ids_validos):
    if vigente == "no" and not derogada_por:
        salir("si --vigente no, hay que indicar --derogada-por")
    if derogada_por and derogada_por not in ids_validos:
        salir("--derogada-por " + derogada_por + " no existe en el registro de normas")
    for m in modificaciones:
        if m not in ids_validos:
            salir("--modificaciones incluye " + m + " que no existe en el registro de normas")


def main():
    p = argparse.ArgumentParser(
        description="Registra la verificacion de una norma ya contrastada con la fuente oficial."
    )
    p.add_argument("id", help="Ejemplo: LEY30057_ART94")
    p.add_argument("--url", required=True)
    p.add_argument("--fecha", required=True)
    p.add_argument("--por", required=True)
    p.add_argument("--vigente", required=True, choices=["si", "no"])
    p.add_argument("--modificaciones", nargs="*", default=[])
    p.add_argument("--derogada-por", default=None)
    p.add_argument("--reemplazar", action="store_true")
    a = p.parse_args()

    textos = json.loads(TEXTOS.read_text(encoding="utf-8-sig"))
    disciplinarias = json.loads(DISCIPLINARIAS.read_text(encoding="utf-8-sig"))
    ids_validos = set(disciplinarias.keys()) if isinstance(disciplinarias, dict) else set()

    if a.id not in textos or not textos[a.id].get("texto_literal"):
        salir(a.id + " no tiene texto literal cargado en normas_textos_literales.json")
    if a.id not in ids_validos:
        salir(a.id + " no existe en normas_disciplinarias.json")

    validar_url(a.url)
    validar_por(a.por)
    validar_fecha(a.fecha)
    validar_vigencia(a.vigente, a.derogada_por, a.modificaciones, ids_validos)

    datos = {}
    if VERIF.exists():
        datos = json.loads(VERIF.read_text(encoding="utf-8-sig"))

    anterior = datos.get(a.id)
    if anterior and not a.reemplazar:
        salir(a.id + " ya tiene verificacion registrada. Usa --reemplazar si es a proposito")

    datos[a.id] = {
        "url_fuente": a.url,
        "fecha_consulta": a.fecha,
        "verificado_por": a.por.strip(),
        "vigencia": {
            "vigente": a.vigente == "si",
            "modificaciones": a.modificaciones,
            "derogada_por": a.derogada_por,
        },
    }
    if anterior and a.reemplazar:
        datos[a.id]["_reemplaza_a"] = anterior

    VERIF.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Guardado:")
    print(json.dumps({a.id: datos[a.id]}, ensure_ascii=False, indent=2))


main()