# fix_verbos.py
# Agrega verbos alternativos a las 4 listas de deteccion dentro de
# _parsear_eventos: emitir/suscribir -> ELABORACION, notificar -> REMISION.
# Hace backup automatico del archivo antes de tocarlo.

import shutil
import datetime

RUTA = r".\app\core\typification_engine.py"

# ---- Backup ----
fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup = f".\\app\\core\\typification_engine_backup_{fecha}.py"
shutil.copy(RUTA, backup)
print(f"Backup creado: {backup}")

# ---- Leer archivo ----
with open(RUTA, encoding="utf-8-sig") as f:
    content = f.read()

o_acute = "\u00f3"  # o con tilde

def buscar(texto, desde=0):
    idx = content.find(texto, desde)
    if idx == -1:
        raise SystemExit(f"ERROR: no se encontro el marcador: {texto!r}")
    return idx

# LISTA 1: tiene_elab (positivo) -> agregar emitir / suscribir
idx1 = buscar("tiene_elab = any(x in f for x in [")
end1 = buscar("\n            ])", idx1)

nuevos_1 = (
    ',\n'
    '                "emitido", "emitida", "emitio", "emiti' + o_acute + '", '
    '"se emitio", "se emiti' + o_acute + '",\n'
    '                "suscrito", "suscrita", "suscribio", "suscribi' + o_acute + '", '
    '"se suscribio", "se suscribi' + o_acute + '"'
)

# LISTA 2: negacion de ELABORACION
idx2 = buscar('"no fue elaborado"', end1)
end2 = buscar("\n                ]):", idx2)

nuevos_2 = (
    ',\n'
    '                    "no fue emitido", "no fue emitida", "no se emitio", '
    '"no se emiti' + o_acute + '", "no emitio", "no emiti' + o_acute + '",\n'
    '                    "no fue suscrito", "no fue suscrita", "no se suscribio", '
    '"no se suscribi' + o_acute + '"'
)

# LISTA 3: tiene_rem (positivo) -> agregar notificar
idx3 = buscar("tiene_rem = any(x in f for x in [", end2)
end3 = buscar("\n            ])", idx3)

nuevos_3 = (
    ',\n'
    '                "notificado", "notificada", "notifico", "notific' + o_acute + '", '
    '"se notifico", "se notific' + o_acute + '"'
)

# LISTA 4: negacion de REMISION
idx4 = buscar('"no fue remitido"', end3)
end4 = buscar("\n                ]):", idx4)

nuevos_4 = (
    ',\n'
    '                    "no fue notificado", "no fue notificada", "no se notifico", '
    '"no se notific' + o_acute + '", "no notifico", "no notific' + o_acute + '"'
)

# ---- Aplicar los 4 inserts, de atras hacia adelante ----
partes = [
    (end4, nuevos_4),
    (end3, nuevos_3),
    (end2, nuevos_2),
    (end1, nuevos_1),
]
partes.sort(key=lambda p: p[0], reverse=True)

for pos, texto in partes:
    content = content[:pos] + texto + content[pos:]

with open(RUTA, "w", encoding="utf-8-sig") as f:
    f.write(content)

print("Verbos alternativos agregados: emitir, suscribir -> ELABORACION | notificar -> REMISION")