from pathlib import Path

p = Path.cwd() / "app" / "core" / "typification_engine_v352_work.py"
lines = p.read_text(encoding="utf-8").splitlines()

print("ARCHIVO:", p)
print("LINEA 710:", repr(lines[709]))
print("LINEA 711:", repr(lines[710]))
print("LINEA 712:", repr(lines[711]))

