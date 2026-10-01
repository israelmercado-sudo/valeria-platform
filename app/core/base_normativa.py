import json
from pathlib import Path

RUTA = Path(__file__).resolve().parent.parent / "data" / "normas_disciplinarias.json"


class BaseNormativa:
    def __init__(self, ruta=RUTA):
        with open(ruta, encoding="utf-8") as f:
            self.normas = json.load(f)

    def candidatas(self, tipo_conducta, regimen=None):
        """Devuelve normas cuyo gatillo coincide con algún componente del tipo_conducta."""
        partes = [p.strip() for p in tipo_conducta.split(" + ")]
        resultado = []
        for n in self.normas:
            if regimen and regimen not in n["regimen"]:
                continue
            if any(p in n["gatillos"] for p in partes):
                resultado.append(n)
        return resultado