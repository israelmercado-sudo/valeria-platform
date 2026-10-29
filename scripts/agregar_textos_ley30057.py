import json
from pathlib import Path

RUTA = Path("app/data/normas_textos_literales.json")

FUENTE = (
    "Ley 30057, El Peruano 4-jul-2013 (texto original). Fuente consultada: "
    "PDF del Congreso de la República "
    "https://www.congreso.gob.pe/Docs/DGP/DIDP/files/ley_30057.pdf. "
    "Pendiente de cotejo literal y de verificación de modificaciones y vigencia."
)

TEXTOS = {
    "LEY30057_ART87": """Artículo 87. Determinación de la sanción a las faltas
La sanción aplicable debe ser proporcional a la falta cometida y se determina evaluando la existencia de las condiciones siguientes:
a) Grave afectación a los intereses generales o a los bienes jurídicamente protegidos por el Estado.
b) Ocultar la comisión de la falta o impedir su descubrimiento.
c) El grado de jerarquía y especialidad del servidor civil que comete la falta, entendiendo que cuanto mayor sea la jerarquía de la autoridad y más especializadas sus funciones, en relación con las faltas, mayor es su deber de conocerlas y apreciarlas debidamente.
d) Las circunstancias en que se comete la infracción.
e) La concurrencia de varias faltas.
f) La participación de uno o más servidores en la comisión de la falta o faltas.
g) La reincidencia en la comisión de la falta.
h) La continuidad en la comisión de la falta.
i) El beneficio ilícitamente obtenido, de ser el caso.
Las autoridades deben prever que la comisión de la conducta sancionable no resulte más ventajosa para el infractor que cumplir las normas infringidas o asumir la sanción.
La destitución acarrea la inhabilitación automática para el ejercicio de la función pública. El servidor civil que se encuentre en este supuesto, no puede reingresar a prestar servicios a favor del Estado por un plazo de cinco (5) años, contados a partir de que la resolución administrativa que causa estado es eficaz.
Si un servidor civil es declarado responsable de un delito doloso, mediante sentencia que cause estado, o que haya quedado consentida, o ejecutoriada, culmina su relación con la entidad.""",

    "LEY30057_ART88": """Artículo 88. Sanciones aplicables
Las sanciones por faltas disciplinarias pueden ser:
a) Amonestación verbal o escrita.
b) Suspensión sin goce de remuneraciones desde un día hasta por doce (12) meses.
c) Destitución.
Toda sanción impuesta al servidor debe constar en el legajo.""",

    "LEY30057_ART90": """Artículo 90. La suspensión y la destitución
La suspensión sin goce de remuneraciones se aplica hasta por un máximo de trescientos sesenta y cinco (365) días calendario previo procedimiento administrativo disciplinario. El número de días de suspensión es propuesto por el jefe inmediato y aprobado por el jefe de recursos humanos o quien haga sus veces, el cual puede modificar la sanción propuesta. La sanción se oficializa por resolución del jefe de recursos humanos o quien haga su veces. La apelación es resuelta por el Tribunal del Servicio Civil.
La destitución se aplica previo proceso administrativo disciplinario por el jefe de recursos humanos o quien haga sus veces. Es propuesta por el jefe de recursos humanos o quien haga sus veces y aprobada por el titular de la entidad pública, el cual puede modificar la sanción propuesta. Se oficializa por resolución del titular de la entidad pública. La apelación es resuelta por el Tribunal del Servicio Civil.""",

    "LEY30057_ART91": """Artículo 91. Graduación de la sanción
Los actos de la Administración Pública que impongan sanciones disciplinarias deben estar debidamente motivados de modo expreso y claro, identificando la relación entre los hechos y las faltas, y los criterios para la determinación de la sanción establecidos en la presente Ley.
La sanción corresponde a la magnitud de las faltas, según su menor o mayor gravedad. Su aplicación no es necesariamente correlativa ni automática. En cada caso la entidad pública debe contemplar no sólo la naturaleza de la infracción sino también los antecedentes del servidor.
Los descuentos por tardanzas e inasistencia no tienen naturaleza disciplinaria, por lo que no eximen de la aplicación de la debida sanción.""",

    "LEY30057_ART92": """Artículo 92. Autoridades
Son autoridades del procedimiento administrativo disciplinario:
a) El jefe inmediato del presunto infractor.
b) El jefe de recursos humanos o quien haga sus veces.
c) El titular de la entidad.
d) El Tribunal del Servicio Civil.
Las autoridades del procedimiento cuentan con el apoyo de un secretario técnico, que es de preferencia abogado y designado mediante resolución del titular de la entidad. El secretario técnico puede ser un servidor civil de la entidad que se desempeña como tal, en adición a sus funciones. El secretario técnico es el encargado de precalificar las presuntas faltas, documentar la actividad probatoria, proponer la fundamentación y administrar los archivos emanados del ejercicio de la potestad sancionadora disciplinaria de la entidad pública. No tiene capacidad de decisión y sus informes u opiniones no son vinculantes.
La secretaría técnica depende de la oficina de recursos humanos de la entidad o la que haga sus veces.
Cualquier persona que considere que un servidor civil ha incurrido en una conducta que tenga las características de falta disciplinaria, debe informarlo de manera verbal o escrita ante la Secretaría Técnica. La denuncia debe expresar claramente los hechos y adjuntar las pruebas pertinentes.""",

    "LEY30057_ART93": """Artículo 93. El procedimiento administrativo disciplinario
93.1 La autoridad del procedimiento administrativo disciplinario de primera instancia inicia el procedimiento de oficio o a pedido de una denuncia, debiendo comunicar al servidor por escrito las presuntas faltas y otorgarle un plazo de cinco (5) días hábiles para presentar el descargo y las pruebas que crea conveniente para su defensa. Para tal efecto, el servidor civil tiene derecho a conocer los documentos y antecedentes que dan lugar al procedimiento.
Vencido el plazo sin la presentación de los descargos, el proceso queda listo para ser resuelto.
Cuando la comunicación de la presunta falta es a través de una denuncia, el rechazo a iniciar un proceso administrativo disciplinario debe ser motivado y notificado al que puso en conocimiento la presunta falta, si estuviese individualizado.
93.2 Previo al pronunciamiento de las autoridades del proceso administrativo disciplinario de primera instancia y luego de presentado los descargos, el servidor civil procesado puede ejercer su derecho de defensa a través de un informe oral, efectuado personalmente o por medio de un abogado, para lo cual se señala fecha y hora única.
93.3 La autoridad del procedimiento administrativo disciplinario de primera instancia realiza las investigaciones del caso, solicita los informes respectivos, examina las pruebas que se presenten e impone las sanciones que sean de aplicación.
93.4 Durante el tiempo que dura el procedimiento administrativo disciplinario el servidor civil procesado, según la falta cometida, puede ser separado de su función y puesto a disposición de la oficina de recursos humanos. Mientras se resuelve su situación, el servidor civil tiene derecho al goce de sus remuneraciones, estando impedido de hacer uso de sus vacaciones, licencias por motivos particulares mayores a cinco (5) días o presentar renuncia.""",

    "LEY30057_ART96": """Artículo 96. Medidas cautelares
96.1 Luego de comunicar por escrito al servidor civil sobre las presuntas faltas, la autoridad del proceso administrativo disciplinario puede, mediante decisión motivada, y con el objeto de prevenir afectaciones mayores a la entidad pública o a los ciudadanos, separarlo de su función y ponerlo a disposición de la Oficina de Personal para realizar trabajos que le sean asignados de acuerdo con su especialidad, o exonerarlo de su obligación de asistir al centro de trabajo.
96.2 Las medidas cautelares se ejercitan durante el tiempo que dura el proceso administrativo disciplinario, siempre que ello no perjudique el derecho de defensa del servidor civil y se le abone la remuneración y demás derechos y beneficios que pudieran corresponderle. Excepcionalmente, cuando la falta presuntamente cometida por el servidor civil afecte gravemente los intereses generales, la medida cautelar puede imponerse de modo previo al inicio del procedimiento administrativo disciplinario. La validez de dicha medida está condicionada al inicio del procedimiento correspondiente.
96.3 Las medidas cautelares pueden ser modificadas o levantadas durante el curso del procedimiento administrativo disciplinario, de oficio o a instancia de parte, en virtud de circunstancias sobrevenidas o que no pudieron ser consideradas en el momento de su adopción.
96.4 Las medidas caducan de pleno derecho cuando se emite la resolución que pone fin al procedimiento administrativo disciplinario en la instancia que impuso la medida, cuando haya transcurrido el plazo fijado para su ejecución, o para la emisión de la resolución que pone fin al procedimiento.""",
}


def main():
    datos = json.loads(RUTA.read_text(encoding="utf-8-sig"))
    agregadas, omitidas = [], []
    for _id, texto in TEXTOS.items():
        num = _id.replace("LEY30057_ART", "")
        if not texto.startswith(f"Artículo {num}."):
            raise SystemExit(f"{_id}: el texto no empieza con 'Artículo {num}.'")
        if _id in datos:
            omitidas.append(_id)
            continue
        datos[_id] = {"texto_literal": texto, "fuente_del_texto": FUENTE}
        agregadas.append(_id)
    RUTA.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Agregadas:", agregadas)
    print("Omitidas (ya existían):", omitidas)
    print("Total de entradas en el JSON:", len(datos))


main()
