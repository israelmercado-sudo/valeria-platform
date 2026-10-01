from pathlib import Path

p = Path.cwd() / "app" / "core" / "typification_engine_v352_work.py"
lines = p.read_text(encoding="utf-8").splitlines()

# Verificación previa
assert lines[709].strip() == '(r"\\bpresentó\\b|\\bpresento\\b", "Presentación de documento"),'
assert lines[710].strip() == '(r"\\belaboró\\b|\\belaboro\\b", "Elaboración de documento"),'
assert lines[711].strip() == '(r"\\bemitió\\b|\\bemitio\\b", "Emisión de documento o acto"),'

# Insertar formas pasivas positivas
lines.insert(
    710,
    '            (r"\\bfue presentado\\b|\\bfue presentada\\b|\\bfueron presentados\\b|\\bfueron presentadas\\b", "Presentación de documento"),'
)

lines.insert(
    712,
    '            (r"\\bfue elaborado\\b|\\bfue elaborada\\b|\\bfueron elaborados\\b|\\bfueron elaboradas\\b", "Elaboración de documento"),'
)

lines.insert(
    714,
    '            (r"\\bfue remitido\\b|\\bfue remitida\\b|\\bfueron remitidos\\b|\\bfueron remitidas\\b", "Remisión de documento o expediente"),'
)

p.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("CAMBIO APLICADO")
