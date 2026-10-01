from app.core.negaciones import hay_negacion

casos = [
    ("El informe no fue elaborado ni emitido", "EMISION", True),
    ("Omitió notificar el informe", "NOTIFICACION", True),
    ("El informe fue emitido oportunamente", "EMISION", False),
    ("No notificó la decisión", "NOTIFICACION", True),
    ("Dejó de remitir el oficio", "REMISION", True),
    ("Sin haber verificado los datos", "VERIFICACION", True),
]

for texto, clave, esperado in casos:
    obtenido = hay_negacion(texto, clave)
    estado = "OK " if obtenido == esperado else "MAL"
    print(estado, clave, "|", texto)

from app.core.negaciones import contexto_niega, omisiones, accion_positiva

assert contexto_niega("el servidor no fue ")
assert contexto_niega("no elaboró ni ")
assert contexto_niega("actuó sin haber ")
assert not contexto_niega("el servidor ")
assert omisiones("Omitió notificar el informe", "NOTIFICACION")
assert accion_positiva("El servidor emitió la resolución", "EMISION")
assert not accion_positiva("No elaboró ni remitió el informe", "REMISION")
print("Pruebas nuevas OK")