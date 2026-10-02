# test_casos_extendidos.py
# Test extendido del motor TypificationEngine
# Cubre variantes: acentos, doble incumplimiento, coordinación negativa, ruido, etc.

import sys
sys.path.insert(0, '.')

from app.core.typification_engine import TypificationEngine


# (texto, tipo esperado)
CASOS = [
    # --- Casos golden (ya validados) ---
    ("El informe fue presentado dentro del plazo establecido.",
     "CUMPLIMIENTO"),
    ("El informe fue presentado fuera del plazo establecido.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),
    ("El informe fue elaborado dentro del plazo establecido y posteriormente remitido fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (PRESENTACIÓN)"),
    ("El informe fue elaborado dentro del plazo establecido, pero no fue remitido.",
     "OMISIÓN - NO REMISIÓN"),
    ("El informe fue elaborado fuera del plazo y posteriormente remitido.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)"),

    # --- Variantes con acentos ---
    ("El informe fue elaborado dentro del plazo y remitido fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),
    ("El informe se elaboró fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)"),
    ("El informe se remitió fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),
    ("El informe no se remitió.",
     "OMISIÓN - NO REMISIÓN"),
    ("El informe no se elaboró.",
     "OMISIÓN - NO ELABORACIÓN"),

    # --- Variantes sin acentos ---
    ("El informe se elaboro fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)"),
    ("El informe se remitio fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),
    ("El informe no se remitio.",
     "OMISIÓN - NO REMISIÓN"),

    # --- Doble incumplimiento ---
    ("El informe fue elaborado fuera del plazo y remitido fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN) + INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),

    # --- Solo elaboración ---
    ("El informe fue elaborado dentro del plazo.",
     "CUMPLIMIENTO"),
    ("El informe fue elaborado fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)"),

    # --- Solo remisión ---
    ("El informe fue remitido dentro del plazo.",
     "CUMPLIMIENTO"),
    ("El informe fue remitido fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),

    # --- Texto con ruido ---
    ("En el marco del procedimiento administrativo, el informe fue elaborado dentro del plazo establecido y luego remitido fuera del plazo por el servidor responsable.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),

    # --- Verbos alternativos ---
    ("El documento fue presentado fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (REMISIÓN)"),
]


def main():
    motor = TypificationEngine()

    print("=" * 78)
    print("TEST EXTENDIDO - TypificationEngine")
    print("=" * 78)

    ok = 0
    fallos = []

    for i, (texto, esperado) in enumerate(CASOS, 1):
        try:
            resultado = motor.analizar(conducta=texto)
            tipo = resultado.tipo_conducta
        except Exception as e:
            tipo = f"<ERROR: {e}>"

        estado = "OK" if tipo == esperado else "FALLO"

        if estado == "OK":
            ok += 1
        else:
            fallos.append((i, texto, tipo, esperado))

        print(f"\nCASO {i:02d}: {estado}")
        print(f"  Texto:    {texto}")
        print(f"  Devuelto: {tipo}")
        if estado == "FALLO":
            print(f"  Esperado: {esperado}")

    print("\n" + "=" * 78)
    print(f"RESULTADO: {ok}/{len(CASOS)} casos correctos")
    print("=" * 78)

    if fallos:
        print("\nCASOS FALLIDOS:")
        for i, texto, tipo, esperado in fallos:
            print(f"  CASO {i}: '{texto}'")
            print(f"    Devuelto: {tipo}")
            print(f"    Esperado: {esperado}")


if __name__ == "__main__":
    main()