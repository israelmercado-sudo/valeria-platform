"""
Casos reales obligatorios — criterios_aceptacion.md
5 casos que el motor DEBE acertar para considerarse aceptado.
"""
from app.core.typification_engine import TypificationEngine

CASOS = [
    (
        "El informe fue elaborado fuera del plazo.",
        "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)",
        "Caso real 1: elaboración fuera de plazo",
    ),
    (
        "El informe no se remitió.",
        "OMISIÓN - NO REMISIÓN",
        "Caso real 2: omisión de remisión",
    ),
    (
        "La resolución fue notificada fuera del plazo.",
        "INCUMPLIMIENTO DE PLAZO (NOTIFICACIÓN)",
        "Caso real 3: notificación fuera de plazo (etapa independiente)",
    ),
    (
        "El informe fue elaborado dentro del plazo y remitido fuera del plazo.",
        "INCUMPLIMIENTO DE PLAZO (REMISIÓN)",
        "Caso real 4: dos etapas, prevalece la incumplida",
    ),
    (
        "Omitió notificar la resolución.",
        "OMISIÓN - NO NOTIFICACIÓN",
        "Caso real 5: omisión de notificación con verbo conjugado",
    ),
]


def main() -> int:
    motor = TypificationEngine()
    print("=" * 78)
    print("TEST CASOS REALES - criterios_aceptacion.md")
    print("=" * 78)
    print()

    fallos = 0
    for i, (texto, esperado, descripcion) in enumerate(CASOS, 1):
        resultado = motor.analizar(conducta=texto)
        devuelto = resultado.tipo_conducta

        if devuelto == esperado:
            print(f"CASO {i:02d}: OK  ({descripcion})")
        else:
            fallos += 1
            print(f"CASO {i:02d}: FALLO  ({descripcion})")
        print(f"  Texto:    {texto}")
        print(f"  Devuelto: {devuelto}")
        if devuelto != esperado:
            print(f"  Esperado: {esperado}")
        print()

    print("=" * 78)
    if fallos == 0:
        print(f"RESULTADO: {len(CASOS)}/{len(CASOS)} casos correctos")
    else:
        print(f"RESULTADO: {len(CASOS) - fallos}/{len(CASOS)} correctos, {fallos} fallos")
    print("=" * 78)
    return 0 if fallos == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())