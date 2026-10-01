from pathlib import Path

ruta = Path(r".\app\core\typification_engine.py")

texto = ruta.read_text(encoding="utf-8")

inicio = texto.index("    def _generar_matriz_subsuncion(")
fin = texto.index("    def _determinar_tipo_conducta(", inicio)

print("INICIO EN:", inicio)
print("FIN EN:", fin)
print("LONGITUD ORIGINAL:", fin - inicio)

bloque = texto[inicio:fin]

print("CONTIENE V3.2.1:", "V3.2.1" in bloque)
print("CONTIENE V3.4:", "V3.4" in bloque)

Path(r".\parche_diagnostico.txt").write_text(
    bloque,
    encoding="utf-8"
)

print("=== DIAGNOSTICO CREADO ===")
print("Archivo: parche_diagnostico.txt")
