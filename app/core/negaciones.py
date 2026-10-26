import re
import unicodedata

def sin_acentos(texto: str) -> str:
    n = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in n if unicodedata.category(c) != "Mn")

# (infinitivo, participio masc., participio fem., pretérito 3ª persona), todo sin tilde
VERBOS = {
    "ELABORACION":  ("elaborar",  "elaborado",  "elaborada",  "elaboro"),
    "EMISION":      ("emitir",    "emitido",    "emitida",    "emitio"),
    "SUSCRIPCION":  ("suscribir", "suscrito",   "suscrita",   "suscribio"),
    "REMISION":     ("remitir",   "remitido",   "remitida",   "remitio"),
    "NOTIFICACION": ("notificar", "notificado", "notificada", "notifico"),
    "COMUNICACION": ("comunicar", "comunicado", "comunicada", "comunico"),
    "ENVIO":        ("enviar",    "enviado",    "enviada",    "envio"),
    "AUTORIZACION": ("autorizar", "autorizado", "autorizada", "autorizo"),
    "VERIFICACION": ("verificar", "verificado", "verificada", "verifico"),
    "PRESENTACION": ("presentar", "presentado", "presentada", "presento"),
}

def patrones_negacion(clave: str) -> list[str]:
    inf, pm, pf, pret = VERBOS[clave]
    part = rf"(?:{pm}|{pf})"
    return [
        rf"\bno fue {part}\b",
        rf"\bno (?:se )?{pret}\b",
        rf"\b(?:omitio|dejo de|se abstuvo de|incumplio con|no pudo|no logro|no llego a)\s+{inf}\b",
        rf"\bsin (?:haber )?(?:{pm}|{inf})\b",
        rf"\bno se (?:ha )?{pm}\b",
        rf"\bni (?:{pm}|{pf})\b",
    ]

def patron_coordinacion_negativa(a: str, b: str) -> str:
    _, am, af, _ = VERBOS[a]
    _, bm, bf, _ = VERBOS[b]
    return rf"\bno fue (?:{am}|{af})\s+ni\s+(?:{bm}|{bf})\b"

def hay_negacion(texto: str, clave: str) -> bool:
    t = sin_acentos(texto)

    return any(re.search(p, t) for p in patrones_negacion(clave))

def contexto_niega(contexto: str) -> bool:
    """True si el texto inmediatamente anterior a un verbo lo niega."""
    c = sin_acentos(contexto)
    return bool(re.search(
        r"\b(?:no(?:\s+(?:fue|fueron|se|ha\s+sido|han\s+sido))?|tampoco(?:\s+(?:fue|fueron|se|ha\s+sido|han\s+sido))?|ni|nunca|jamas|sin(?:\s+haber(?:\s+sido)?|\s+ser)?)"
        r"(?:\s+(?:lo|la|los|las|le|les|se|me|te|nos))?\s*$",
        c,
    ))

def omisiones(texto: str, clave: str) -> list[tuple[int, int]]:
    """Posiciones de 'omitió/dejó de/se abstuvo de + infinitivo'."""
    inf = VERBOS[clave][0]
    t = sin_acentos(texto)
    patron = rf"\b(?:omitio|dejo de|se abstuvo de|incumplio con|no pudo|no logro|no llego a)\s+{inf}\b"
    return [(m.start(), m.end()) for m in re.finditer(patron, t)]

def accion_positiva(texto: str, clave: str) -> bool:
    """True si hay un pretérito del verbo que NO esté negado por su contexto."""
    pret = VERBOS[clave][3]
    t = sin_acentos(texto)
    for m in re.finditer(rf"\b{pret}\b", t):
        if not contexto_niega(t[max(0, m.start() - 100):m.start()]):
            return True
    return False

def accion_negada(texto: str, clave: str) -> bool:
    """True si el verbo aparece negado (no/ni/sin) o con omitio/dejo de + infinitivo."""
    inf, pm, pf, pret = VERBOS[clave]
    if omisiones(texto, clave):
        return True
    t = sin_acentos(texto)
    for m in re.finditer(rf"\b(?:{pret}|{pm}|{pf})\b", t):
        if contexto_niega(t[max(0, m.start() - 100):m.start()]):
            return True
    return False

# clave de verbo -> etapa del evento
ETAPA_DE = {
    "ELABORACION": "ELABORACION",
    "SUSCRIPCION": "ELABORACION",
    "EMISION": "EMISION",
    "REMISION": "REMISION",
    "ENVIO": "REMISION",
    "NOTIFICACION": "NOTIFICACION",
    "COMUNICACION": "NOTIFICACION",
    "AUTORIZACION": "AUTORIZACION",
    "VERIFICACION": "VERIFICACION",
    "PRESENTACION": "PRESENTACION",
}

def patron_positivo(clave: str) -> str:
    inf, pm, pf, pret = VERBOS[clave]
    # Formas plurales del participio:
    #   presentado -> presentados
    #   presentada -> presentadas
    pm_pl = pm + "s"
    pf_pl = pf + "s"
    # Preterito plural (3a persona plural).
    # Verbos -ar: presento -> presentaron
    # Verbos -er/-ir: remitio -> remitieron
    if pret.endswith("o"):
        raiz = pret[:-1]
    else:
        raiz = pret
    if inf.endswith("ar"):
        pret_pl = raiz + "aron"
    else:
        pret_pl = raiz + "ieron"
    return (
        rf"\b(?:"
        rf"{pm}|{pm_pl}|"
        rf"{pf}|{pf_pl}|"
        rf"se {pret}|{pret}|"
        rf"se {pret_pl}|{pret_pl}|"
        rf"{clave.lower()}"
        rf")\b"
    )
