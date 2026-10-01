from app.core.typification_engine import TypificationEngine

engine = TypificationEngine()

print("==============================================")
print(" PRUEBA BASE PARA V3.5 - ANALISIS JURIDICO")
print("==============================================")

casos = [
    {
        "nombre": "CASO 1 - INCUMPLIMIENTO DE PLAZO",
        "conducta": "El informe no fue elaborado ni remitido dentro del plazo establecido.",
        "deber": "El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo establecido.",
        "posible_falta": "Posible incumplimiento de obligaciones funcionales.",
        "normas": [
            "Norma que establece el deber funcional",
            "Norma que tipifica la falta disciplinaria"
        ],
        "hechos": [
            "El servidor tenía la obligación de elaborar y remitir el informe dentro del plazo.",
            "El informe no fue elaborado ni remitido dentro del plazo establecido."
        ],
        "evidencia": [
            "Documento que establece la obligación funcional.",
            "Informe no elaborado ni remitido.",
            "Documentación que acredita el vencimiento del plazo."
        ]
    },
    {
        "nombre": "CASO 2 - AUTORIZACION SIN VERIFICACION",
        "conducta": "El funcionario autorizó el pago sin verificar la documentación correspondiente.",
        "deber": "El funcionario debía verificar la documentación antes de autorizar el pago.",
        "posible_falta": "Posible incumplimiento de obligaciones funcionales.",
        "normas": [
            "Norma que establece el deber de verificación",
            "Norma que regula la autorización del pago"
        ],
        "hechos": [
            "El funcionario tenía a su cargo la autorización del pago.",
            "La documentación debía ser verificada previamente.",
            "El funcionario autorizó el pago sin verificar la documentación."
        ],
        "evidencia": [
            "Documento de asignación de funciones.",
            "Expediente de pago.",
            "Documento mediante el cual se autorizó el pago."
        ]
    },
    {
        "nombre": "CASO 3 - INFORMACION INSUFICIENTE",
        "conducta": "El servidor no presentó la documentación.",
        "deber": "",
        "posible_falta": "",
        "normas": [],
        "hechos": [
            "El servidor no presentó la documentación."
        ],
        "evidencia": []
    }
]

for caso in casos:
    print("\n----------------------------------------------")
    print(caso["nombre"])
    print("----------------------------------------------")

    resultado = engine.analizar(
        conducta=caso["conducta"],
        deber=caso["deber"],
        posible_falta=caso["posible_falta"],
        normas=caso["normas"],
        hechos=caso["hechos"],
        evidencia=caso["evidencia"]
    )

    print("CONDUCTA:", resultado.conducta_identificada)
    print("TIPO:", resultado.tipo_conducta)
    print("DEBER:", resultado.deber_presuntamente_incumplido)
    print("FALTA:", resultado.posible_falta)
    print("SUBSUNCIÓN:", resultado.subsuncion_preliminar)
    print("NIVEL:", resultado.nivel_conclusion)
    print("REQUIERE VERIFICACIÓN:", resultado.requiere_verificacion)

    print("\nMATRIZ DE SUBSUNCIÓN:")
    for item in resultado.matriz_subsuncion:
        print(" -", item)

    print("\nINFORMACIÓN FALTANTE:")
    for item in resultado.informacion_faltante:
        print(" -", item)

print("\n==============================================")
print(" PRUEBA V3.5 BASE COMPLETADA")
print("==============================================")
