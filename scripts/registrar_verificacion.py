import argparse
import json
import sys
from datetime import datetime, date
from pathlib import Path

DOMINIOS = ("spij.minjus.gob.pe", "elperuano.pe", "gob.pe", "congreso.gob.pe")
TEXTOS = Path("app/data/normas_textos_literales.json")
VERIF = Path("app/data/normas_verificaciones.json")


def salir(msg):
    print("NO SE GUARDO NADA:", msg)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser(
        description="Registra la verificacion de una norma ya contrastada con la fuente oficial."
    )
    p.add_argument("id", help="Ejemplo: LEY30057_ART94")
    p.add_argument("--url", required=True, help="URL oficial consultada (SPIJ, El Peruano, gob.pe)")
    p.add_argument("--fecha", required=True, help="AAAA-MM-DD, dia en que consulto la fuente")
    p.add_argument("--por", required=True, help="Nombre de quien hizo el cotejo")
    p.add_argument("--vigente", required=True, choices=["si", "no"])
    p.add_argument("--modificaciones", nargs="*", default=[],
                   help="Normas que modificaron el articulo, si las hay")
    p.add_argument("--derogada-por", default=None)
    p.add_argument("--reemplazar", action="store_true")
    a = p.parse_args()

    textos = json.loads(TEXTOS.read_text(encoding="utf-8-sig"))
    if a.id not in textos or not textos[a.id].get("texto_literal"):
        salir(a.id + " no tiene texto literal cargado en normas_textos_literales.json")

    if not a.url.startswith("https://") or "..." in a.url or len(a.url) < 20:
        salir("la URL no parece una URL real y completa")
    host = a.url.split("/")[2].lower()
    if not any(host == d or host.endswith("." + d) for d in DOMINIOS):
        salir("el dominio " + host + " no es una fuente oficial conocida (SPIJ, El Peruano, gob.pe, Congreso)")
    if "nombre" in a.por.lower() and "apellido" in a.por.lower():
        salir("--por tiene el nombre de ejemplo")

    try:
        f = datetime.strptime(a.fecha, "%Y-%m-%d").date()
    except ValueError:
        salir("la fecha debe tener el formato AAAA-MM-DD")
    if f > date.today():
        salir("la fecha de consulta no puede ser futura")

    if len(a.por.strip()) < 5 or "?" in a.por:
        salir("revisa el nombre en --por (muy corto o con tildes danadas)")

    datos = {}
    if VERIF.exists():
        datos = json.loads(VERIF.read_text(encoding="utf-8-sig"))
    if a.id in datos and not a.reemplazar:
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
    VERIF.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Guardado:")
    print(json.dumps({a.id: datos[a.id]}, ensure_ascii=False, indent=2))


main()
