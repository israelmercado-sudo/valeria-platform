import shutil
import sys

RUTA = r"app\core\typification_engine.py"
NEG = r"app\core\negaciones.py"

with open(RUTA, encoding="utf-8", newline="") as f:
    crudo = f.read()
crlf = "\r\n" in crudo
src = crudo.replace("\r\n", "\n")

if "accion_negada" in src:
    sys.exit("El parche 2 ya esta aplicado. No se hizo nada.")


def reemplazar(texto, viejo, nuevo, nombre):
    n = texto.count(viejo)
    if n != 1:
        sys.exit(f"ERROR en '{nombre}': se esperaba 1 coincidencia y hay {n}. No se modifico nada.")
    return texto.replace(viejo, nuevo)


# Respaldo con nombre propio
shutil.copy(RUTA, "typification_engine_respaldo2.txt")

# A. Import
src = reemplazar(
    src,
    "from app.core.negaciones import contexto_niega, omisiones, accion_positiva",
    "from app.core.negaciones import contexto_niega, omisiones, accion_positiva, accion_negada",
    "A - import",
)

# B. Revision general de modalidades negativas
ancla = (
    "        # ============================================================\n"
    "        # 3. CONDUCTAS POSITIVAS"
)
bloque = '''        # Revision general de negaciones (pronombres, coordinacion
        # activa, omitio/dejo de + infinitivo, notificar, etc.)
        for _clave, _modalidad in [
            ("ELABORACION", "NO ELABORACIÓN"),
            ("REMISION", "NO REMISIÓN"),
            ("PRESENTACION", "NO PRESENTACIÓN"),
            ("VERIFICACION", "NO VERIFICACIÓN"),
            ("NOTIFICACION", "NO NOTIFICACIÓN"),
            ("EMISION", "NO EMISIÓN"),
            ("SUSCRIPCION", "NO SUSCRIPCIÓN"),
            ("AUTORIZACION", "NO AUTORIZACIÓN"),
        ]:
            if accion_negada(texto, _clave):
                agregar(_modalidad)

'''
src = reemplazar(src, ancla, bloque + ancla, "B - revision general")

# C. Funcion nueva en negaciones.py
with open(NEG, encoding="utf-8", newline="") as f:
    neg = f.read()
if "def accion_negada" not in neg:
    neg += '''

def accion_negada(texto: str, clave: str) -> bool:
    """True si el verbo aparece negado (no/ni/sin) o con omitio/dejo de + infinitivo."""
    inf, pm, pf, pret = VERBOS[clave]
    if omisiones(texto, clave):
        return True
    t = sin_acentos(texto)
    for m in re.finditer(rf"\\b(?:{pret}|{pm}|{pf})\\b", t):
        if contexto_niega(t[max(0, m.start() - 100):m.start()]):
            return True
    return False
'''
    with open(NEG, "w", encoding="utf-8", newline="") as f:
        f.write(neg)

if crlf:
    src = src.replace("\n", "\r\n")
with open(RUTA, "w", encoding="utf-8", newline="") as f:
    f.write(src)

print("Parche 2 aplicado correctamente.")