RUTA = r"app\core\typification_engine.py"

with open(RUTA, "rb") as f:
    crudo = f.read().decode("utf-8")

eol = "\r\n" if "\r\n" in crudo else "\n"
src = crudo.replace("\r\n", "\n")

a = src.index("def _determinar_tipo_conducta")
b = src.index("def _extraer_modalidades_conducta")
bloque = src[a:b]

cambios = [
    ('"PRESENTACION": "PRESENTACI\u00d3N"', '"PRESENTACION": "REMISI\u00d3N"'),
    ('"PRESENTACION": "NO PRESENTACI\u00d3N"', '"PRESENTACION": "NO REMISI\u00d3N"'),
]

for viejo, nuevo in cambios:
    n = bloque.count(viejo)
    print(f"{n} ocurrencia(s): {viejo}")
    bloque = bloque.replace(viejo, nuevo)

src = src[:a] + bloque + src[b:]

with open(RUTA, "wb") as f:
    f.write(src.replace("\n", eol).encode("utf-8"))
