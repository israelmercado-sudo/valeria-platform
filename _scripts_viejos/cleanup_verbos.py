from pathlib import Path
import shutil
import datetime

ruta = Path(r".\app\core\typification_engine.py")

fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup = ruta.with_name(f"typification_engine_backup_cleanup_{fecha}.py")
shutil.copy2(ruta, backup)

print(f"Backup creado: {backup}")

texto = ruta.read_text(encoding="utf-8-sig")

reemplazos = [
    (
        '''                "emitido", "emitida", "emitio", "emitió", "se emitio", "se emitió",
                "suscrito", "suscrita", "suscribio", "suscribió", "se suscribio", "se suscribió",
                "emitido", "emitida", "emitio", "emitió", "se emitio", "se emitió",
                "suscrito", "suscrita", "suscribio", "suscribió", "se suscribio", "se suscribió"''',
        '''                "emitido", "emitida", "emitio", "emitió", "se emitio", "se emitió",
                "suscrito", "suscrita", "suscribio", "suscribió", "se suscribio", "se suscribió"'''
    ),
    (
        '''                    "no fue emitido", "no fue emitida", "no se emitio", "no se emitió", "no emitio", "no emitió",
                    "no fue suscrito", "no fue suscrita", "no se suscribio", "no se suscribió",
                    "no fue emitido", "no fue emitida", "no se emitio", "no se emitió", "no emitio", "no emitió",
                    "no fue suscrito", "no fue suscrita", "no se suscribio", "no se suscribió"''',
        '''                    "no fue emitido", "no fue emitida", "no se emitio", "no se emitió", "no emitio", "no emitió",
                    "no fue suscrito", "no fue suscrita", "no se suscribio", "no se suscribió"'''
    ),
    (
        '''                "notificado", "notificada", "notifico", "notificó", "se notifico", "se notificó",
                "notificado", "notificada", "notifico", "notificó", "se notifico", "se notificó"''',
        '''                "notificado", "notificada", "notifico", "notificó", "se notifico", "se notificó"'''
    ),
    (
        '''                    "no fue notificado", "no fue notificada", "no se notifico", "no se notificó", "no notifico", "no notificó",
                    "no fue notificado", "no fue notificada", "no se notifico", "no se notificó", "no notifico", "no notificó"''',
        '''                    "no fue notificado", "no fue notificada", "no se notifico", "no se notificó", "no notifico", "no notificó"'''
    ),
]

for original, limpio in reemplazos:
    cantidad = texto.count(original)
    if cantidad != 1:
        raise SystemExit(
            f"ERROR: bloque esperado encontrado {cantidad} veces; "
            "no se modifica el archivo."
        )
    texto = texto.replace(original, limpio)

ruta.write_text(texto, encoding="utf-8-sig")

print("Limpieza completada correctamente.")
print("Se eliminaron únicamente las 4 duplicaciones conocidas.")
