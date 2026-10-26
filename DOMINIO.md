# DOMINIO — Etapas del procedimiento disciplinario

Fuente normativa:
- Ley N° 30057, Ley del Servicio Civil, Título V (Régimen Disciplinario y Procedimiento Sancionador).
- Reglamento General de la Ley N° 30057, aprobado por D.S. N° 040-2014-PCM, artículo 106 (Fases del procedimiento administrativo disciplinario: instructiva y sancionadora).
- Directiva N° 02-2015-SERVIR/GPGSC, "Régimen Disciplinario y Procedimiento Sancionador de la Ley N° 30057", aprobada por Resolución de Presidencia Ejecutiva N° 101-2015-SERVIR-PE (actos procedimentales dentro de cada fase).

Fecha de fijación: 2026-10-26
Responsable: Israel Mercado

## Etapas reconocidas por el motor

| Etapa        | Verbos equivalentes             | Notas                              |
|--------------|---------------------------------|------------------------------------|
| ELABORACION  | elaborar, emitir, suscribir     |                                    |
| REMISION     | remitir, enviar                 |                                    |
| NOTIFICACION | notificar, comunicar            | Independiente (decisión 2026-10-23)|
| PRESENTACION | presentar                       |                                    |
| AUTORIZACION | autorizar                       | Sin plazo automático               |
| VERIFICACION | verificar                       | Sin plazo automático               |

## Decisiones de dominio registradas

### 2026-10-23 — Notificación es etapa independiente
Antes, NOTIFICACION estaba mapeado a REMISION en negaciones.py.
Se separó porque el reglamento las distingue. Los tests se alinearon:
notificar fuera de plazo devuelve INCUMPLIMIENTO DE PLAZO (NOTIFICACIÓN),
no (REMISIÓN).

## Reglas de negación

- `no fue <participio>` → acción negada
- `no (se) <pretérito>` → acción negada
- `omitio / dejo de / se abstuvo de / incumplio con / no pudo / no logro / no llego a + <infinitivo>` → omisión
- `sin (haber) <participio|infinitivo>` → negación
- `tampoco`, `ni`, `nunca`, `jamas` → contexto niega

## Nota sobre la fuente normativa

El artículo 85 de la Ley N° 30057 tipifica las faltas disciplinarias (conductas sancionables). No regula las etapas del procedimiento. Las etapas que este motor reconoce (ELABORACION, REMISION, NOTIFICACION, PRESENTACION, etc.) se derivan de las normas procedimentales citadas arriba, y constituyen una decisión de diseño del motor para tipificar incumplimientos de plazo por acto procedimental.

## Qué NO hace el motor

- No decide sanciones.
- No interpreta normas: solo mapea verbos a etapas.
- Si no reconoce la etapa, devuelve NO DETERMINADO (correcto, no error).
## Decisiones de dominio registradas

### 2026-10-26 — Soporte de plurales y negaciones plurales

**Problema detectado**: El motor no detectaba verbos en plural
(presentados, elaborados, emitidos, 
otificadas) ni negaciones
con plural (
o fueron presentados). Devolvía NO DETERMINADO.

**Fix aplicado en pp/core/negaciones.py**:
- patron_positivo: incluye plurales de participio (pm + 's', pf + 's')
  y pretérito plural (según conjugación: -ar → ron, -er/-ir → ieron).
- contexto_niega: agrega ueron a los patrones de negación
  (
o fueron, 	ampoco fueron).

**Cobertura**: 	est_plurales.py con 9 casos. Integrado a erificar.ps1
como Paso 10.

**Total de casos verdes**: 90 (81 anteriores + 9 nuevos).
