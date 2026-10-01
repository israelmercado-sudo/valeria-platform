# VALERIA PLATFORM - REGLAS DE TRABAJO CODEX

## Objetivo
Desarrollar y mejorar Valeria Platform, una IA especializada en Derecho Administrativo Peruano, Procedimientos Administrativos Disciplinarios (PAD) y gestión pública.

## Rama de trabajo
feature/v352-codex

## Motor experimental actual
app/core/typification_engine_v352_work.py

Este archivo es el laboratorio principal de V3.5.2.

## REGLAS CRITICAS

1. NO modificar main directamente.
2. NO eliminar archivos de respaldo.
3. NO sobrescribir versiones históricas.
4. NO modificar typification_engine.py salvo instrucción expresa.
5. Antes de modificar código, inspeccionar el código existente.
6. Mantener compatibilidad con Python 3.14.
7. Después de cada modificación ejecutar py_compile.
8. Ejecutar las pruebas relacionadas antes de considerar terminada una modificación.
9. No eliminar funcionalidades existentes para solucionar un caso nuevo.
10. Toda mejora debe preservar las pruebas que ya funcionan.
11. Si existe conflicto entre una mejora nueva y una funcionalidad existente, detenerse y reportarlo.
12. No inventar normas jurídicas, artículos, precedentes, informes o criterios de SERVIR.
13. En materia jurídica, separar extracción de hechos, clasificación de conducta, subsunción y conclusión jurídica.
14. No asumir que una palabra aislada determina por sí sola la tipificación.
15. Priorizar trazabilidad: Valeria debe poder explicar por qué clasificó una conducta de determinada manera.

## VERSIONES EXISTENTES

V3.4.3.1 fue una versión estable de referencia para pruebas de modalidades de conducta.

V3.5.1 incorporó mejoras posteriores y cuenta con respaldo.

V3.5.2 es la línea experimental actual.

## PRINCIPIO DE DESARROLLO

No buscar únicamente que el ejemplo de prueba pase.

Buscar que el motor generalice correctamente a casos equivalentes y que no produzca falsos positivos por coincidencias superficiales.

## FLUJO OBLIGATORIO

1. Diagnosticar.
2. Identificar causa.
3. Proponer modificación mínima.
4. Aplicar modificación.
5. Compilar.
6. Ejecutar pruebas.
7. Comparar resultados.
8. Reportar exactamente qué cambió.
9. No hacer commits automáticamente salvo instrucción expresa.

## OBJETIVO DE V3.5.2

Construir una matriz de subsunción robusta que permita relacionar:

HECHO
→ OBLIGACIÓN
→ CONDUCTA
→ MODALIDAD
→ RESULTADO
→ FUNCIÓN/DEBER
→ NORMA
→ SUBSUNCIÓN
→ CONCLUSIÓN

La clasificación debe distinguir especialmente entre:

- acción
- omisión
- no elaboración
- no remisión
- presentación
- no presentación
- presentación fuera de plazo
- incumplimiento de plazo
- cumplimiento
- situaciones indeterminadas

Nunca concluir una infracción únicamente por detectar palabras como "informe", "plazo", "no", "remitir" o similares.

## ESTADO ACTUAL

El archivo experimental:
app/core/typification_engine_v352_work.py

debe ser inspeccionado antes de cualquier cambio.

Primero comprender su arquitectura actual y sus métodos.

No reescribir el motor completo sin justificación técnica.

## FORMATO DE REPORTE

Después de cada tarea indicar:

- Archivos revisados
- Problema encontrado
- Causa
- Cambio realizado
- Pruebas ejecutadas
- Resultado
- Riesgos o efectos secundarios
- Siguiente paso recomendado
