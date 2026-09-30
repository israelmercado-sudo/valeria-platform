# Estado del motor de tipificación - 2026-09-29

## Motor activo
- `app/core/typification_engine.py` — TypificationEngine

## Cambios aplicados
1. Añadido `_parsear_eventos`: segmenta la conducta por conectores.
2. Reescrito `_determinar_tipo_conducta`: usa segmentación por eventos.
3. Tipos con acentos: ELABORACIÓN, REMISIÓN, OMISIÓN.
4. Detección ampliada: formas pasivas, reflexivas ("se elaboró"), sin acentos.
5. Archivados 53 archivos duplicados en `app/core/_archive/`.

## Tests
- `test_casos_extendidos.py` — 20/20 OK
  Cubre: acentos, sin acentos, formas reflexivas, doble incumplimiento, texto con ruido.

## Pendientes (para futuras sesiones)
- [ ] Decidir si el endpoint `/analizar` debe hacer tipificación.
- [ ] Refactorizar `_extraer_modalidades_conducta` para usar `_parsear_eventos`.
- [ ] Ampliar tests con verbos alternativos (emitió, autorizó, verificó).
- [ ] Documentar la lógica de segmentación para futuros mantenedores.

## Backups
- `_backup_core_20260929_082814` — antes de los fixes
- `_backup_core_post_fix_20260929_095228` — después de los fixes
