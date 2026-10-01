import re
import sys

RUTA = r"app\core\typification_engine.py"

with open(RUTA, encoding="utf-8", newline="") as f:
    crudo = f.read()

crlf = "\r\n" in crudo
src = crudo.replace("\r\n", "\n")

if "contexto_niega" in src:
    sys.exit("El archivo ya tiene el parche. No se hizo nada.")


def reemplazar(texto, viejo, nuevo, nombre):
    n = texto.count(viejo)
    if n != 1:
        sys.exit(f"ERROR en '{nombre}': se esperaba 1 coincidencia y hay {n}. No se modifico nada.")
    return texto.replace(viejo, nuevo)


# --- A. Import --------------------------------------------------------
IMPORT = "from app.core.negaciones import contexto_niega, omisiones, accion_positiva"
lineas = src.split("\n")
pos = None
for i, l in enumerate(lineas[:80]):
    if re.match(r"(import |from )", l):
        pos = i + 1 if l.startswith("from __future__") else i
        break
if pos is None:
    sys.exit("ERROR: no encontre ningun import al inicio del archivo.")
lineas.insert(pos, IMPORT)
src = "\n".join(lineas)

# --- B. Negacion por contexto en _parsear_eventos ---------------------
viejo = '                ocurrencias.append({\n                    "inicio": inicio_accion,'
nuevo = (
    '                if contexto_niega(contexto_previo):\n'
    '                    negada = True\n\n' + viejo
)
src = reemplazar(src, viejo, nuevo, "B - negacion por contexto")

# --- C. Omisiones con infinitivo --------------------------------------
viejo = '        ocurrencias.sort(key=lambda x: x["inicio"])'
bloque = '''        claves_por_etapa = {
            "ELABORACION": ["ELABORACION", "EMISION", "SUSCRIPCION"],
            "REMISION": ["REMISION", "NOTIFICACION"],
            "PRESENTACION": ["PRESENTACION"],
        }
        for etapa_om, claves_om in claves_por_etapa.items():
            for clave_om in claves_om:
                for ini_om, fin_om in omisiones(t, clave_om):
                    ocurrencias.append({
                        "inicio": ini_om,
                        "fin": fin_om,
                        "etapa": etapa_om,
                        "negada": True,
                    })

'''
src = reemplazar(src, viejo, bloque + viejo, "C - omisiones")

# --- D. Conductas positivas -------------------------------------------
pares = [
    (r'''        if contiene(r"\bremiti[oó]\b") and not contiene(r"\bno remiti[oó]\b"):''',
     '        if accion_positiva(texto, "REMISION"):'),
    (r'''        if contiene(r"\belabor[oó]\b") and not contiene(r"\bno elabor[oó]\b"):''',
     '        if accion_positiva(texto, "ELABORACION"):'),
    (r'''        if contiene(r"\bautoriz[oó]\b") and not contiene(r"\bno autoriz[oó]\b"):''',
     '        if accion_positiva(texto, "AUTORIZACION"):'),
    (r'''        if contiene(r"\bsuscribi[oó]\b") and not contiene(r"\bno suscribi[oó]\b"):''',
     '        if accion_positiva(texto, "SUSCRIPCION"):'),
    (r'''        if contiene(r"\bemit[ií]\b") and not contiene(r"\bno emit[ií]\b"):''',
     '        if accion_positiva(texto, "EMISION"):'),
    (r'''        if contiene(r"\bverific[oó]\b") and not contiene(r"\bno verific[oó]\b"):''',
     '        if accion_positiva(texto, "VERIFICACION"):'),
]
for viejo, nuevo in pares:
    src = reemplazar(src, viejo, nuevo, "D - " + nuevo.strip())

# --- Guardar ----------------------------------------------------------
if crlf:
    src = src.replace("\n", "\r\n")
with open(RUTA, "w", encoding="utf-8", newline="") as f:
    f.write(src)

print("Parche aplicado correctamente.")