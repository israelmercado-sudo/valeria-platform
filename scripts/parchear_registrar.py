p = "registrar_verificacion.py"
s = open(p, encoding="utf-8-sig").read()
if "DOMINIOS" in s:
    raise SystemExit("El parche ya estaba aplicado")
s = s.replace(
    'TEXTOS = Path(',
    'DOMINIOS = ("spij.minjus.gob.pe", "elperuano.pe", "gob.pe", "congreso.gob.pe")\nTEXTOS = Path(',
    1,
)
viejo = 'if not a.url.startswith("https://") or "..." in a.url or len(a.url) < 20:\n        salir("la URL no parece una URL real y completa")'
nuevo = viejo + (
    '\n    host = a.url.split("/")[2].lower()'
    '\n    if not any(host == d or host.endswith("." + d) for d in DOMINIOS):'
    '\n        salir("el dominio " + host + " no es una fuente oficial conocida (SPIJ, El Peruano, gob.pe, Congreso)")'
    '\n    if "nombre" in a.por.lower() and "apellido" in a.por.lower():'
    '\n        salir("--por tiene el nombre de ejemplo")'
)
if viejo not in s:
    raise SystemExit("No encontre el bloque a reemplazar")
s = s.replace(viejo, nuevo, 1)
open(p, "w", encoding="utf-8").write(s)
print("Parche aplicado")
