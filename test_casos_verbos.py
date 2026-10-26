# test_casos_verbos.py
# Test de verbos alternativos para TypificationEngine
# Objetivo: verificar si el motor reconoce verbos administrativos distintos
# de "elaborar" / "remitir" / "presentar" (que ya están cubiertos en
# test_casos_extendidos.py).
#
# IMPORTANTE: los valores "esperado" aquí son una HIPÓTESIS de cómo debería
# clasificar el motor cada verbo, según su significado en un procedimiento
# administrativo disciplinario. La primera corrida de este test sirve para
# descubrir qué reconoce el motor hoy (probablemente casi nada de esta
# lista), no para que pase en verde a la primera. Luego se ajusta el
# diccionario de verbos del motor caso por caso.
 
import sys
sys.path.insert(0, '.')
 
from app.core.typification_engine import TypificationEngine
 
 
# (texto, tipo esperado, comentario sobre el verbo)
CASOS = [
    # --- "emitir" (equivalente a elaborar/producir un documento) ---
    ("El informe fue emitido dentro del plazo establecido.",
     "CUMPLIMIENTO", "emitir = elaborar"),
    ("El informe fue emitido fuera del plazo establecido.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)", "emitir = elaborar"),
    ("El informe no fue emitido.",
     "OMISIÓN - NO ELABORACIÓN", "emitir = elaborar"),
 
    # --- "notificar" (etapa independiente) ---
    ("La resolución fue notificada dentro del plazo establecido.",
     "CUMPLIMIENTO", "notificar = notificaci?n"),
    ("La resolución fue notificada fuera del plazo establecido.",
     "INCUMPLIMIENTO DE PLAZO (NOTIFICACIÓN)", "notificar = notificación"),
    ("La resolución no fue notificada.",
     "OMISIÓN - NO NOTIFICACIÓN", "notificar = notificación"),
 
    # --- "suscribir" (equivalente a elaborar/firmar) ---
    ("El documento fue suscrito fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)", "suscribir = elaborar"),
 
    # --- "autorizar" (acción administrativa, no encaja claramente en
    #     elaboración/remisión; se marca como caso a definir) ---
    ("El trámite fue autorizado fuera del plazo.",
     "NO DETERMINADO", "autorizar: sin etapa asignada, no tipifica plazo"),
 
    # --- "verificar" (acción de control, probablemente NO deba tipificar
    #     como incumplimiento de plazo salvo que el reglamento lo exija) ---
    ("La verificación fue realizada fuera del plazo.",
     "NO DETERMINADO", "verificar: sin etapa asignada, no tipifica plazo"),
 
    # --- formas reflexivas de los nuevos verbos ---
    ("El informe se emitió fuera del plazo.",
     "INCUMPLIMIENTO DE PLAZO (ELABORACIÓN)", "reflexivo: emitir"),
    ("La resolución no se notificó.",
     "OMISIÓN - NO NOTIFICACIÓN", "reflexivo: notificar"),
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
        print("\nCASOS FALLIDOS (verbos que el motor aún no reconoce o clasifica distinto):")
        for i, texto, tipo, esperado, nota in fallos:
            print(f"  CASO {i} [{nota}]: '{texto}'")
            print(f"    Devuelto: {tipo}")
            print(f"    Esperado: {esperado}")
 
 
if __name__ == "__main__":
    main()