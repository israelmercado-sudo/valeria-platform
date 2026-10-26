"""
Test de plurales - verifica que el motor detecte verbos en plural.
Bug encontrado: 2026-10-26.
"""
from app.core.typification_engine import TypificationEngine

CASOS = [
    # (texto, tipo_esperado, temporal_esperado)
    ("Los informes fueron presentados dentro del plazo.", "CUMPLIMIENTO", "CUMPLIMIENTO DE PLAZO"),
    ("Los informes fueron presentados fuera del plazo.", "INCUMPLIMIENTO DE PLAZO (PRESENTACIÓN)", "INCUMPLIMIENTO DE PLAZO"),
    ("Los informes no fueron presentados.", "OMISIÓN - NO PRESENTACIÓN", "SIN INFORMACIÓN TEMPORAL"),
    ("Los informes no fueron presentados dentro del plazo.", "OMISIÓN - NO PRESENTACIÓN", "INCUMPLIMIENTO DE PLAZO"),
    ("Los informes fueron elaborados dentro del plazo.", "CUMPLIMIENTO", "CUMPLIMIENTO DE PLAZO"),
    ("Los informes fueron elaborados fuera del plazo.", "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)", "INCUMPLIMIENTO DE PLAZO"),
    ("Los informes no fueron remitidos.", "OMISIÓN - NO REMISIÓN", "SIN INFORMACIÓN TEMPORAL"),
    ("Las resoluciones fueron notificadas fuera del plazo.", "INCUMPLIMIENTO DE PLAZO (NOTIFICACIÓN)", "INCUMPLIMIENTO DE PLAZO"),
    ("Las resoluciones no fueron notificadas.", "OMISIÓN - NO NOTIFICACIÓN", "SIN INFORMACIÓN TEMPORAL"),
]


def main() -> int:
    motor = TypificationEngine()
    print("=" * 78)
    print("TEST PLURALES - bug encontrado 2026-10-26")
    print("=" * 78)
    print()

    fallos = 0
    for i, (texto, esperado_tipo, esperado_temp) in enumerate(CASOS, 1):
        r = motor.analizar(conducta=texto)
        ok = r.tipo_conducta == esperado_tipo and r.componente_temporal == esperado_temp
        if ok:
            print(f"CASO {i:02d}: OK    {texto}")
        else:
            fallos += 1
            print(f"CASO {i:02d}: FALLO {texto}")
            print(f"         tipo real: {r.tipo_conducta!r}")
            print(f"         tipo esp.: {esperado_tipo!r}")
            print(f"         temp real: {r.componente_temporal!r}")
            print(f"         temp esp.: {esperado_temp!r}")
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