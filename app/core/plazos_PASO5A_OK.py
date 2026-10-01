import json
from datetime import date, datetime, timedelta
from pathlib import Path

RUTA = Path(__file__).resolve().parent.parent / "data" / "feriados_peru.json"


class CalculadorPlazos:
    def __init__(self, ruta=RUTA):
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        self.verificado = datos.get("verificado", False)
        self.fijos = set(datos.get("fijos", []))
        self.extra = {
            datetime.strptime(d, "%Y-%m-%d").date() for d in datos.get("extra", [])
        }

    def es_feriado(self, d: date) -> bool:
        return d in self.extra or d.strftime("%d-%m") in self.fijos

    def es_habil(self, d: date) -> bool:
        return d.weekday() < 5 and not self.es_feriado(d)

    def vencimiento(self, fecha_inicio, dias_habiles: int) -> date:
        """Vence el dia habil N contado desde el dia SIGUIENTE a fecha_inicio."""
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        d = fecha_inicio
        contados = 0
        while contados < dias_habiles:
            d += timedelta(days=1)
            if self.es_habil(d):
                contados += 1
        return d

    def dias_de_retraso(self, vencimiento, fecha_real) -> int:
        """Dias habiles de retraso. 0 si fue dentro del plazo."""
        if isinstance(vencimiento, str):
            vencimiento = datetime.strptime(vencimiento, "%Y-%m-%d").date()
        if isinstance(fecha_real, str):
            fecha_real = datetime.strptime(fecha_real, "%Y-%m-%d").date()
        d = vencimiento
        retraso = 0
        while d < fecha_real:
            d += timedelta(days=1)
            if self.es_habil(d):
                retraso += 1
        return retraso