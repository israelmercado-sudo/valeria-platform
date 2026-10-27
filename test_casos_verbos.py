# -*- coding: utf-8 -*-
# test_casos_verbos.py
# Verifica verbos alternativos. Los "esperado" son HIPOTESIS iniciales.
import sys
sys.path.insert(0, '.')

from app.core.typification_engine import TypificationEngine

E = "\u00d3"  # Ó  (para armar strings sin depender del encoding del archivo)

CASOS = [
    ("El informe fue emitido dentro del plazo establecido.",
     "CUMPLIMIENTO", "emitir = elaborar"),
    ("El informe fue emitido fuera del plazo establecido.",
     f"INCUMPLIMIENTO DE PLAZO (EMISI{E}N)", "emitir = elaborar"),
    ("El informe no fue emitido.",
     f"OMISI{E}N - NO EMISI{E}N", "emitir = elaborar"),

    ("La resoluci\u00f3n fue notificada dentro del plazo establecido.",
     "CUMPLIMIENTO", "notificar = notificacion"),
    ("La resoluci\u00f3n fue notificada fuera del plazo establecido.",
     f"INCUMPLIMIENTO DE PLAZO (NOTIFICACI{E}N)", "notificar = notificacion"),
    ("La resoluci\u00f3n no fue notificada.",
     f"OMISI{E}N - NO NOTIFICACI{E}N", "notificar = notificacion"),

    ("El documento fue suscrito fuera del plazo.",
     f"INCUMPLIMIENTO DE PLAZO (ELABORACI{E}N)", "suscribir = elaborar"),

    ("El tr\u00e1mite fue autorizado fuera del plazo.",
     "NO DETERMINADO", "autorizar: sin etapa asignada"),
    ("La verificaci\u00f3n fue realizada fuera del plazo.",
     "NO DETERMINADO", "verificar: sin etapa asignada"),

    # Caso 10 — CORREGIDO: "emitio" es EMISION, no ELABORACION
    ("El informe se emiti\u00f3 fuera del plazo.",
     f"INCUMPLIMIENTO DE PLAZO (EMISI{E}N)", "reflexivo: emitir"),
    ("La resoluci\u00f3n no se notific\u00f3.",
     f"OMISI{E}N - NO NOTIFICACI{E}N", "reflexivo: notificar"),
]


def main():
    motor = TypificationEngine()
    print("=" * 78)
    print("TEST VERBOS ALTERNATIVOS - TypificationEngine")
    print("=" * 78)

    ok = 0
    fallos = []

    for i, (texto, esperado, nota) in enumerate(CASOS, 1):
        try:
            resultado = motor.analizar(conducta=texto)
            tipo = resultado.tipo_conducta
        except Exception as e:
            tipo = f"<ERROR: {e}>"

        estado = "OK" if tipo == esperado else "FALLO"
        if estado == "OK":
            ok += 1
        else:
            fallos.append((i, texto, tipo, esperado, nota))

        print(f"\nCASO {i:02d}: {estado}  ({nota})")
        print(f"  Texto:    {texto}")
        print(f"  Devuelto: {tipo}")
        if estado == "FALLO":
            print(f"  Esperado: {esperado}")

    print("\n" + "=" * 78)
    print(f"RESULTADO: {ok}/{len(CASOS)} casos correctos")
    print("=" * 78)

    if fallos:
        print("\nCASOS FALLIDOS:")
        for i, texto, tipo, esperado, nota in fallos:
            print(f"  CASO {i} [{nota}]: '{texto}'")
            print(f"    Devuelto: {tipo}")
            print(f"    Esperado: {esperado}")


if __name__ == "__main__":
    main()