# Criterios de aceptación

Un caso se considera aceptado si el motor devuelve la modalidad esperada
para los 5 casos reales de abajo, Y los 31 tests existentes siguen en verde.

## Casos reales obligatorios

| # | Texto (extracto)                                       | Esperado                                |
|---|--------------------------------------------------------|-----------------------------------------|
| 1 | El informe fue elaborado fuera del plazo.              | INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)   |
| 2 | El informe no se remitió.                              | OMISIÓN - NO REMISIÓN                   |
| 3 | La resolución fue notificada fuera del plazo.          | INCUMPLIMIENTO DE PLAZO (NOTIFICACIÓN)  |
| 4 | El informe fue elaborado dentro del plazo y remitido fuera del plazo. | INCUMPLIMIENTO DE PLAZO (REMISIÓN) |
| 5 | Omitió notificar la resolución.                        | OMISIÓN - NO NOTIFICACIÓN               |

## Criterios de "terminado"

- [ ] 31/31 tests en test_casos_verbos.py + test_casos_extendidos.py verdes
- [ ] Los 5 casos reales de arriba pasan
- [ ] DOMINIO.md documentado con fuente normativa
- [ ] Raíz del repo sin scripts oneoff ni backups manuales
- [ ] Respaldo ZIP del estado estable guardado

## Estado de cobertura (2026-10-26)

El motor cubre **81 casos verdes** distribuidos en 9 tests:

| Test | Casos |
|------|-------|
| test_casos_verbos.py | 11 |
| test_casos_extendidos.py | 20 |
| test_casos_reales.py | 5 |
| test_tildes.py | 10 |
| test_temporal_omision.py | 5 |
| test_regresion_eventos.py | 12 |
| test_v3431_final.py | 9 |
| test_presentacion_v3431.py | 9 |

Ejecución: `powershell -ExecutionPolicy Bypass -File .\verificar.ps1`
