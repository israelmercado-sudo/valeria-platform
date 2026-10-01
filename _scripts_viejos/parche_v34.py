from pathlib import Path
import shutil

ruta = Path(r".\app\core\typification_engine.py")
backup = Path(r".\app\core\typification_engine_v333_pre_v34_matrix_backup.py")

texto = ruta.read_text(encoding="utf-8")

# ---------------------------------------------------------
# 1. BACKUP
# ---------------------------------------------------------
shutil.copy2(ruta, backup)
print("BACKUP CREADO:", backup)

# ---------------------------------------------------------
# 2. UBICAR EXACTAMENTE EL MÉTODO
# ---------------------------------------------------------
inicio = texto.index("    def _generar_matriz_subsuncion(")
fin = texto.index("    def _determinar_tipo_conducta(", inicio)

print("INICIO:", inicio)
print("FIN:", fin)

# ---------------------------------------------------------
# 3. NUEVA MATRIZ V3.4
# ---------------------------------------------------------
nuevo_metodo = '''    def _generar_matriz_subsuncion(
        self,
        conducta: str,
        deber: str,
        posible_falta: str,
        normas: List[str],
        hechos: List[str],
        evidencia: List[str],
        tipo_conducta: str,
    ) -> List[Dict[str, Any]]:
        """
        V3.4 - Matriz multidimensional de subsunción preliminar.

        Objetivos:
        - Permitir que un mismo hecho tenga varias dimensiones jurídicas.
        - No reducir cada hecho a una sola categoría.
        - Relacionar hechos y evidencia por relevancia textual.
        - Evitar atribuir intervención o participación automáticamente.
        - Mantener carácter preliminar y sujeto a verificación.
        """

        matriz: List[Dict[str, Any]] = []

        def normalizar(texto: str) -> str:
            return " ".join((texto or "").lower().split())

        def contiene_alguno(texto: str, patrones: List[str]) -> bool:
            t = normalizar(texto)
            return any(p in t for p in patrones)

        def relevancia_evidencia(hecho: str, item: str) -> int:
            """
            Calcula una relevancia simple entre hecho y evidencia.
            No pretende sustituir análisis jurídico.
            """
            h = set(normalizar(hecho).replace(",", " ").replace(".", " ").split())
            e = set(normalizar(item).replace(",", " ").replace(".", " ").split())

            if not h or not e:
                return 0

            comunes = h.intersection(e)

            # Ignorar palabras excesivamente genéricas.
            comunes -= {
                "el", "la", "los", "las", "un", "una",
                "de", "del", "y", "o", "en", "por",
                "para", "con", "que", "se", "su"
            }

            return len(comunes)

        def agregar(
            dimension: str,
            contenido: str,
            fundamento: str = "",
            prioridad: str = "MEDIA",
            hecho_origen: str = "",
        ) -> None:
            if not contenido:
                return

            clave = (
                normalizar(dimension),
                normalizar(contenido),
                normalizar(hecho_origen),
            )

            for item in matriz:
                clave_existente = (
                    normalizar(item.get("dimension", "")),
                    normalizar(item.get("contenido", "")),
                    normalizar(item.get("hecho_origen", "")),
                )

                if clave == clave_existente:
                    return

            matriz.append(
                {
                    "dimension": dimension,
                    "contenido": contenido,
                    "fundamento": fundamento,
                    "prioridad": prioridad,
                    "hecho_origen": hecho_origen,
                }
            )

        # -------------------------------------------------
        # A. ANALISIS MULTIDIMENSIONAL DE CADA HECHO
        # -------------------------------------------------
        for hecho in hechos or []:

            hecho_l = normalizar(hecho)

            # ---------------------------------------------
            # HECHO IMPUTADO
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "no elaboró",
                    "no elaboro",
                    "no fue elaborado",
                    "no fue elaborada",
                    "omitió elaborar",
                    "omitir elaborar",
                    "no presentó",
                    "no presento",
                    "no fue presentado",
                    "no fue presentada",
                    "omitió presentar",
                    "no remitió",
                    "no remitio",
                    "no fue remitido",
                    "no fue remitida",
                    "omitió remitir",
                    "no envió",
                    "no envio",
                    "no fue enviado",
                    "no fue enviada",
                    "omitió enviar",
                    "incumplió",
                    "incumplio",
                    "incumplimiento",
                ],
            ):
                contenido = hecho

                agregar(
                    "HECHO IMPUTADO",
                    contenido,
                    "El hecho describe una conducta u omisión que requiere contraste con el deber y la norma tipificadora.",
                    "ALTA",
                    hecho,
                )

            # ---------------------------------------------
            # CIRCUNSTANCIA TEMPORAL
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "plazo",
                    "dentro del plazo",
                    "fuera del plazo",
                    "plazo establecido",
                    "plazo señalado",
                    "fecha",
                    "venció",
                    "vencio",
                    "vencimiento",
                    "días",
                    "dias",
                    "día",
                    "dia",
                ],
            ):
                agregar(
                    "CIRCUNSTANCIA TEMPORAL",
                    hecho,
                    "La dimensión temporal debe ser contrastada con las fechas y el plazo jurídicamente aplicable.",
                    "ALTA",
                    hecho,
                )

            # ---------------------------------------------
            # CONOCIMIENTO / COMUNICACION
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "comunicó",
                    "comunico",
                    "comunicación",
                    "comunicacion",
                    "notificó",
                    "notifico",
                    "notificación",
                    "notificacion",
                    "informó",
                    "informo",
                    "tomó conocimiento",
                    "tomo conocimiento",
                    "tuvo conocimiento",
                    "recibió",
                    "recibio",
                ],
            ):
                agregar(
                    "CONOCIMIENTO / COMUNICACIÓN",
                    hecho,
                    "Debe determinarse quién conoció, qué conoció, cuándo y mediante qué actuación o documento.",
                    "MEDIA",
                    hecho,
                )

            # ---------------------------------------------
            # ACTUACION DEL SERVIDOR
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "suscribió",
                    "suscribio",
                    "firmó",
                    "firmo",
                    "derivó",
                    "derivo",
                    "remitió",
                    "remitio",
                    "presentó",
                    "presento",
                    "elaboró",
                    "elaboro",
                    "emitió",
                    "emitio",
                    "solicitó",
                    "solicito",
                    "requirió",
                    "requirio",
                    "registró",
                    "registro",
                ],
            ):
                agregar(
                    "ACTUACIÓN DEL SERVIDOR",
                    hecho,
                    "La actuación debe contrastarse con las funciones, competencias y documentación que correspondan.",
                    "MEDIA",
                    hecho,
                )

            # ---------------------------------------------
            # DEBER / FUNCION
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "tenía asignada la función",
                    "tenia asignada la funcion",
                    "tenía la función",
                    "tenia la funcion",
                    "su función era",
                    "su funcion era",
                    "su obligación era",
                    "su obligacion era",
                    "tenía la obligación de",
                    "tenia la obligacion de",
                    "tenía el deber de",
                    "tenia el deber de",
                    "debía",
                    "debia",
                    "deber de",
                    "función de",
                    "funcion de",
                    "conforme a sus funciones",
                ],
            ):
                agregar(
                    "DEBER / FUNCIÓN",
                    hecho,
                    "Debe verificarse la fuente concreta del deber y su vigencia para el servidor investigado.",
                    "ALTA",
                    hecho,
                )

            # ---------------------------------------------
            # POSIBLE INTERVENCION
            # Solo indicadores fuertes.
            # ---------------------------------------------
            if contiene_alguno(
                hecho_l,
                [
                    "ordenó",
                    "ordeno",
                    "dispuso",
                    "instruyó",
                    "instruyo",
                    "indujo",
                    "concertó",
                    "concerto",
                    "coordinó conjuntamente",
                    "coordino conjuntamente",
                    "acordó conjuntamente",
                    "acordo conjuntamente",
                    "participó conjuntamente",
                    "participo conjuntamente",
                    "intervino conjuntamente",
                    "intervino directamente",
                ],
            ):
                agregar(
                    "POSIBLE PARTICIPACIÓN / INTERVENCIÓN",
                    hecho,
                    "La posible intervención requiere acreditar concretamente la conducta de intervención y su relación con el hecho imputado.",
                    "ALTA",
                    hecho,
                )

        # -------------------------------------------------
        # B. CONDUCTA ATRIBUIDA
        # -------------------------------------------------
        if conducta and normalizar(conducta):
            agregar(
                "CONDUCTA ATRIBUIDA",
                conducta,
                "Hipótesis preliminar de conducta que debe ser contrastada con los hechos, funciones, evidencia y norma tipificadora.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # C. DEBER PROPORCIONADO POR EL ANALISIS
        # -------------------------------------------------
        if deber and normalizar(deber):
            agregar(
                "DEBER / FUNCIÓN",
                deber,
                "Deber invocado para efectuar la comparación preliminar con la conducta atribuida.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # D. POSIBLE FALTA
        # -------------------------------------------------
        if posible_falta and normalizar(posible_falta):
            agregar(
                "SUBSUNCIÓN",
                posible_falta,
                "La posible falta constituye una hipótesis de subsunción preliminar y no una declaración de responsabilidad.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # E. NORMAS
        # -------------------------------------------------
        for norma in normas or []:
            if norma and normalizar(norma):
                agregar(
                    "NORMA A CONTRASTAR",
                    norma,
                    "La norma debe ser verificada respecto de su vigencia, ámbito de aplicación y correspondencia con el hecho.",
                    "ALTA",
                    "",
                )

        # -------------------------------------------------
        # F. EVIDENCIA RELEVANTE
        # -------------------------------------------------
        for hecho in hechos or []:

            candidatos = []

            for item in evidencia or []:
                score = relevancia_evidencia(hecho, item)

                if score > 0:
                    candidatos.append((score, item))

            candidatos.sort(key=lambda x: x[0], reverse=True)

            for score, item in candidatos[:3]:
                agregar(
                    "EVIDENCIA RELACIONADA",
                    item,
                    f"Elemento de evidencia relacionado con el hecho; relevancia textual aproximada: {score}.",
                    "MEDIA" if score < 3 else "ALTA",
                    hecho,
                )

        # -------------------------------------------------
        # G. INFORMACION QUE AUN DEBE ACREDITARSE
        # -------------------------------------------------
        if deber:
            agregar(
                "VERIFICACIÓN DEL DEBER",
                "Acreditar documentalmente la asignación, contenido y vigencia del deber funcional.",
                "La sola invocación del deber no acredita por sí misma su asignación concreta al servidor.",
                "ALTA",
                "",
            )

        if conducta:
            agregar(
                "VERIFICACIÓN DE LA CONDUCTA",
                "Acreditar objetivamente la conducta u omisión atribuida mediante los medios probatorios pertinentes.",
                "La hipótesis de conducta requiere corroboración probatoria.",
                "ALTA",
                "",
            )

        # -------------------------------------------------
        # H. ORDEN DE PRIORIDAD
        # -------------------------------------------------
        prioridades = {
            "ALTA": 0,
            "MEDIA": 1,
            "BAJA": 2,
        }

        matriz.sort(
            key=lambda x: (
                prioridades.get(x.get("prioridad", "MEDIA"), 1),
                x.get("dimension", ""),
                x.get("contenido", ""),
            )
        )

        return matriz

'''

# ---------------------------------------------------------
# 4. REEMPLAZO EXACTO
# ---------------------------------------------------------
texto_nuevo = texto[:inicio] + nuevo_metodo + texto[fin:]

ruta.write_text(texto_nuevo, encoding="utf-8")

print("LONGITUD NUEVA:", len(texto_nuevo))
print("V3.4 PRESENTE:", "V3.4 - Matriz multidimensional" in texto_nuevo)
print("V3.2.1 EN MATRIZ:", "V3.2.1 - Matriz de subsunción preliminar." in texto_nuevo)

# ---------------------------------------------------------
# 5. COMPROBACION DE UNA SOLA DEFINICION
# ---------------------------------------------------------
print(
    "DEFINICIONES EN ARCHIVO:",
    texto_nuevo.count("def _generar_matriz_subsuncion(")
)

print("=== V3.4 MATRIZ REEMPLAZADA ===")
