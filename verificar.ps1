$ErrorActionPreference = "Stop"
Set-Location "$HOME\Documents\ValeriaPlatform\backend"
$py = ".\venv\Scripts\python.exe"
if (-not (Test-Path $py)) { Write-Host "No hay venv: $py" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 1. SINTAXIS ===" -ForegroundColor Cyan
& $py -c "from pathlib import Path; import ast, sys; archivos=[Path('app/core/negaciones.py'),Path('app/core/typification_engine.py')]; errores=0; [print(f'OK: {p}') or ast.parse(p.read_bytes().decode('utf-8-sig'), filename=str(p)) for p in archivos]; sys.exit(0)"
if ($LASTEXITCODE -ne 0) { Write-Host "SINTAXIS ROTA" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 2. TEST VERBOS ===" -ForegroundColor Cyan
& $py .\test_casos_verbos.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON VERBOS" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 3. TEST EXTENDIDOS ===" -ForegroundColor Cyan
& $py .\test_casos_extendidos.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON EXTENDIDOS" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 4. TEST CASOS REALES ===" -ForegroundColor Cyan
& $py .\test_casos_reales.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON CASOS REALES" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 5. TEST TILDES ===" -ForegroundColor Cyan
& $py .\test_tildes.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON TILDES" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 6. TEST TEMPORAL + OMISION ===" -ForegroundColor Cyan
& $py .\test_temporal_omision.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON TEMPORAL_OMISION" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 7. TEST REGRESION EVENTOS ===" -ForegroundColor Cyan
& $py .\test_regresion_eventos.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON REGRESION_EVENTOS" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 8. TEST V3431 (autorizacion/verificacion/suscripcion) ===" -ForegroundColor Cyan
& $py .\test_v3431_final.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON V3431" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 9. TEST PRESENTACION ===" -ForegroundColor Cyan
& $py .\test_presentacion_v3431.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON PRESENTACION" -ForegroundColor Red; exit 1 }

Write-Host "`n=== 10. TEST PLURALES (bug 2026-10-26) ===" -ForegroundColor Cyan
& $py .\test_plurales.py
if ($LASTEXITCODE -ne 0) { Write-Host "FALLARON PLURALES" -ForegroundColor Red; exit 1 }

Write-Host "`nTODO EN VERDE." -ForegroundColor Green