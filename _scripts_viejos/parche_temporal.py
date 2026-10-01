from pathlib import Path

archivo = Path(r".\app\core\typification_engine_v352_work.py")

texto = archivo.read_text(encoding="utf-8")

viejo = '''        if any(contiene(p) for p in patrones_cumplimiento):
            resultado["componente_temporal"] = "CUMPLIMIENTO DE PLAZO"
'''

nuevo = '''        if any(contiene(p) for p in patrones_cumplimiento):
            # La presencia de "oportunamente" no debe prevalecer
            # cuando la conducta está expresamente negada.
            negacion_oportuna = re.search(
                r"\\bno\\s+(?:fue\\s+|se\\s+)?(?:elaborad[oa]|remitid[oa]|presentad[oa]|realizad[oa]|cumpli[oó])\\b.{0,80}\\b(?:oportunamente|de manera oportuna)\\b",
                texto,
                flags=re.IGNORECASE,
            )

            if not negacion_oportuna:
                resultado["componente_temporal"] = "CUMPLIMIENTO DE PLAZO"
'''

if texto.count(viejo) != 1:
    print(f"ERROR: bloque esperado encontrado {texto.count(viejo)} veces. NO se modificó el archivo.")
    raise SystemExit(1)

archivo.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
print("OK: parche temporal aplicado correctamente.")
