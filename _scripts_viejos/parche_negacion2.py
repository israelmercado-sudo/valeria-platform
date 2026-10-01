from pathlib import Path

p = Path(r".\app\core\typification_engine_v352_work.py")
s = p.read_text(encoding="utf-8")

old = r'''                        prefijo = texto_local[:match.start()]

                        if re.search(
                            r"\b(?:no|ni)\s*$",
                            prefijo,
                            flags=re.IGNORECASE,
                        ):
                            continue
'''

new = r'''                        prefijo = texto_local[:match.start()]

                        # Evitar falsos positivos de acciones positivas
                        # dentro de construcciones negativas.
                        if re.search(
                            r"\b(?:no|ni)\s+(?:se\s+)?$",
                            prefijo,
                            flags=re.IGNORECASE,
                        ):
                            continue

                        # Evitar atribuir una acción positiva cuando
                        # el texto solo señala falta de acreditación.
                        contexto_previo = prefijo[-80:]

                        if re.search(
                            r"\bno\s+se\s+acredita\b.{0,60}$",
                            contexto_previo,
                            flags=re.IGNORECASE,
                        ):
                            continue

                        if re.search(
                            r"\b(?:no|ni)\s+fue\s*$",
                            contexto_previo,
                            flags=re.IGNORECASE,
                        ):
                            continue
'''

if s.count(old) != 1:
    raise SystemExit(
        f"ERROR: se esperaba 1 bloque objetivo y se encontraron {s.count(old)}"
    )

s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")

print("PARCHE APLICADO: 1 bloque reemplazado")
