#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entregar.py — comprueba el paquete de entrega: estructura, recursos y movimiento.

    python3 entregar.py --destino <carpeta>
    python3 entregar.py --destino <carpeta> --iniciar        crea el esqueleto
    python3 entregar.py --destino <carpeta> --romper DS-F10  prueba el verificador

`verificar.py` comprueba el sistema; este comprueba **lo que sale de él hacia
desarrollo** — la sección `07-handoff` de la base de conocimiento, que hasta ahora no tenía dueño.

La frase que gobierna la sección, del libro:

    «Puedes diseñar el mejor producto del planeta, pero si no se desarrolla
     correctamente, se quedará solo en Figma para tu próxima publicación de Dribbble.»

Nueve reglas: DS-H01, H02, H04, H05, H06, H07, H08 · DS-F09, F10.
Siete de las nueve no las comprobaba nadie.

Solo biblioteca estándar.
"""

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import R, Reporte  # noqa: E402

# ── Lo que fija la base de conocimiento, y no se negocia ───────────────────────────────────────

# `07-handoff` §7.2 — la estructura que el libro usa en todos sus proyectos.
PAGINAS_PRODUCTO = ["para-empezar", "proyecto", "documentacion", "componentes",
                    "pruebas", "archivo", "portada"]
PAGINAS_SISTEMA = ["para-empezar", "tokens", "componentes", "patrones",
                   "plantillas", "anotaciones"]

# `07-handoff` §7.5 — el formato dice para qué sirve, y la base de conocimiento midió el ahorro:
# WebP 87 %, AVIF 93.9 % sobre la misma imagen.
ICONO_OK = {".svg"}
FOTO_OK = {".webp", ".avif"}
FOTO_MAL = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

# `07-handoff` §7.6 — los cinco datos con los que se entrega toda animación.
DATOS_ANIMACION = ["clase", "duracion", "curva", "disparador", "propiedad"]

# La regla técnica que el libro subraya: `transform` usa aceleración por hardware y no
# dispara recálculos de disposición. Las de posición obligan al navegador a recalcular,
# «especialmente en móviles».
PROP_BARATA = {"transform", "opacity", "filter"}
PROP_CARA = {"left", "top", "right", "bottom", "width", "height", "margin", "padding"}

# `01-foundations` §1.8 — la prueba de calidad del icono, tal como la escribe la base de conocimiento.
ICONO_MAX_BYTES = 2048
ICONO_PROHIBIDO = ("<mask", "<filter", "<clipPath", "<clippath",
                   "linearGradient", "radialGradient")
FORMAS = ("<path", "<rect", "<circle", "<ellipse", "<polygon", "<polyline", "<line")

# DS-H02 — el mismo convenio que los tokens (DS-T04): minúsculas, guiones, barras
# para agrupar. Sin espacios, sin mayúsculas, sin guion bajo.
CONVENIO = re.compile(r"^[a-z0-9]+(?:[-./][a-z0-9]+)*$")

# DS-H07 — §7.7. Por hito es el recomendado; la fecha sirve de desempate.
VERSION = re.compile(r"^[A-Za-z0-9]+_(?:[A-Za-z0-9-]+_v[\d-]+|\d{4}-\d{2}-\d{2})$")

# DS-H09 — semántico. `1.0.0`, sin prefijo: la «v» va en el nombre del hito, no acá.
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


# ═══ Carga ═══════════════════════════════════════════════════════════════════

class Entrega:
    def __init__(self, destino):
        self.raiz = pathlib.Path(destino).resolve()
        self.estructura = self._json("entrega/estructura.json")
        self.movimiento = self._json("movimiento.json")
        self.versiones = self._json("entrega/versiones.json")
        self.marca = self._json("marca.json") or {}
        self.recursos = self.raiz / "recursos"
        self._css = None

    def version_sistema(self):
        """La versión vigente del sistema. Vive en marca.json, con lo demás que es fuente."""
        return str(self.marca.get("version") or "")

    def entregas(self):
        return (self.versiones or {}).get("entregas") or []

    def _json(self, rel):
        f = self.raiz / rel
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None

    def iconos(self):
        d = self.recursos / "iconos"
        return sorted(p for p in d.rglob("*") if p.is_file()) if d.is_dir() else []

    def imagenes(self):
        d = self.recursos / "imagenes"
        return sorted(p for p in d.rglob("*") if p.is_file()) if d.is_dir() else []

    def css(self):
        """El CSS publicado. Se lee una vez: DS-H06 lo mira entero."""
        if self._css is None:
            f = self.raiz / "salidas/sistema.css"
            self._css = f.read_text(encoding="utf-8") if f.exists() else ""
        return self._css

    def animaciones(self):
        return (self.movimiento or {}).get("animaciones", {})


# ═══ Eje A · La estructura del archivo ═══════════════════════════════════════

def h01_siete_paginas(e):
    """DS-H01 — el archivo de producto sigue la estructura de siete páginas.

    La base de conocimiento no la propone por gusto: «esta estructura inamovible me ayuda a duplicar
    archivos y empezar proyectos nuevos rápido, mientras que los desarrolladores saben
    exactamente dónde encontrar lo que necesitan». Y la analogía que la explica: los
    desarrolladores son los compradores nuevos en tu supermercado.
    """
    r = R("DS-H01", "el archivo declara sus siete páginas")
    if not e.estructura:
        return r.saltar("no hay entrega/estructura.json — córrelo con --iniciar")
    for ambito, esperadas in (("producto", PAGINAS_PRODUCTO), ("sistema", PAGINAS_SISTEMA)):
        declaradas = [p.get("id") for p in (e.estructura.get(ambito) or [])]
        if not declaradas:
            r.mal(f"«{ambito}» no declara ninguna página")
            continue
        faltan = [p for p in esperadas if p not in declaradas]
        sobran = [p for p in declaradas if p not in esperadas]
        if faltan:
            r.mal(f"«{ambito}» sin las páginas: {', '.join(faltan)}")
        if sobran:
            r.mal(f"«{ambito}» declara páginas ajenas a la estructura: {', '.join(sobran)}")
        if declaradas != esperadas and not faltan and not sobran:
            r.mal(f"«{ambito}» tiene las páginas en otro orden: {', '.join(declaradas)}")
        if not faltan and not sobran and declaradas == esperadas:
            r.ok(len(esperadas))
    return r


def h08_nada_se_borra(e):
    """DS-H08 — lo descartado va a la página de archivo, no a la papelera.

    «Nunca borres trabajo que pueda ser valioso después.» La base de conocimiento la marca `manual`;
    acá se vuelve comprobable porque la página existe o no existe en el manifiesto.
    """
    r = R("DS-H08", "existe la página de archivo, y lo descartado va ahí")
    if not e.estructura:
        return r.saltar("no hay entrega/estructura.json")
    pagina = next((p for p in (e.estructura.get("producto") or [])
                   if p.get("id") == "archivo"), None)
    if not pagina:
        return r.mal("no hay página «archivo»: lo descartado no tiene dónde ir")
    descartado = e.estructura.get("descartado")
    if descartado is None:
        return r.saltar("la estructura no lleva registro de lo descartado todavía")
    for d in descartado:
        if not d.get("motivo"):
            r.mal(f"«{d.get('nombre', '?')}» se archivó sin motivo escrito")
        else:
            r.ok()
    return r


def h07_version_por_hito(e):
    """DS-H07 — versión manual al cerrar un ciclo, con nombre por hito.

    Recomendada, no obligatoria. Pero un nombre libre no se puede cruzar con los
    cierres de fase que el proyecto ya registra en otro lado, y ahí muere su utilidad.
    """
    r = R("DS-H07", "las versiones llevan nombre estructurado")
    if not e.versiones:
        return r.saltar("no hay entrega/versiones.json — todavía no se cerró ningún ciclo")
    for v in e.versiones.get("versiones", []):
        nombre = v.get("nombre", "")
        if not VERSION.match(nombre):
            r.mal(f"«{nombre}» no sigue Proyecto_Hito_vN ni Proyecto_AAAA-MM-DD")
        else:
            r.ok()
    return r


# ═══ Eje B · Los recursos ════════════════════════════════════════════════════

def h04_formatos(e):
    """DS-H04 — iconos en SVG; fotografías en WebP o AVIF.

    La base de conocimiento midió el ahorro sobre una misma imagen: WebP 87 %, AVIF 93.9 %, «con
    compresión increíble y sin pérdida visible de calidad». Un PNG en la carpeta de
    fotografías no es una preferencia de formato: son 87 puntos de peso regalados.
    """
    r = R("DS-H04", "iconos en SVG, fotografías en WebP o AVIF")
    iconos, imagenes = e.iconos(), e.imagenes()
    if not iconos and not imagenes:
        return r.saltar("no hay carpeta recursos/ — el sistema todavía no exporta nada")
    for p in iconos:
        if p.suffix.lower() not in ICONO_OK:
            r.mal(f"icono {p.name}: {p.suffix} — los iconos van en SVG")
        else:
            r.ok()
    for p in imagenes:
        ext = p.suffix.lower()
        if ext in FOTO_MAL:
            r.mal(f"imagen {p.name}: {ext} — va en WebP o AVIF")
        elif ext not in FOTO_OK and ext not in ICONO_OK:
            r.mal(f"imagen {p.name}: {ext} no es un formato de entrega")
        else:
            r.ok()
    return r


def h02_convenio(e):
    """DS-H02 — capas y recursos siguen el mismo convenio que los tokens.

    «Si quieres que los desarrolladores exporten fácilmente los recursos desde Figma,
    necesitan saber qué exportar. La nomenclatura unificada es la clave del éxito.»

    Un recurso llamado `Icon Copy 2.svg` obliga a alguien a abrirlo para saber qué es.
    """
    r = R("DS-H02", "los recursos siguen el convenio de los tokens")
    archivos = e.iconos() + e.imagenes()
    if not archivos:
        return r.saltar("no hay recursos que nombrar")
    for p in archivos:
        if not CONVENIO.match(p.stem):
            r.mal(f"{p.name}: fuera del convenio (minúsculas, guiones, sin espacios)")
        else:
            r.ok()
    return r


def f10_icono_liviano(e):
    """DS-F10 — un icono no supera 2 base de conocimiento ni lleva máscara, filtro o recorte.

    Es la comprobación más barata de todas y era la que faltaba. La base de conocimiento la escribe como
    una prueba manual —«exportarlo y abrir el SVG en un editor de texto»— con su tabla
    de señales de alarma. Abrirlo y buscar tres cadenas es justo lo que hace un guion.
    """
    r = R("DS-F10", "ningún icono pasa de 2 base de conocimiento ni lleva máscara o filtro")
    iconos = [p for p in e.iconos() if p.suffix.lower() == ".svg"]
    if not iconos:
        return r.saltar("no hay iconos SVG que medir")
    for p in iconos:
        texto = p.read_text(encoding="utf-8", errors="replace")
        peso = len(texto.encode("utf-8"))
        malo = [t for t in ICONO_PROHIBIDO if t in texto]
        if peso > ICONO_MAX_BYTES:
            r.mal(f"{p.name}: {peso} B — el techo es {ICONO_MAX_BYTES} B")
        if malo:
            r.mal(f"{p.name}: lleva {', '.join(sorted(set(malo)))}")
        if peso <= ICONO_MAX_BYTES and not malo:
            r.ok()
    return r


def f09_trazados_combinados(e):
    """DS-F09 — los iconos combinan trazados, no agrupan formas.

    «Produce trazados únicos y limpios en lugar de capas superpuestas, reduce
    drásticamente la complejidad del SVG exportado.» Lo que delata lo contrario es un
    `<g>` con varias formas adentro: eso es un grupo, no una combinación.
    """
    r = R("DS-F09", "los iconos combinan trazados en vez de agrupar formas")
    iconos = [p for p in e.iconos() if p.suffix.lower() == ".svg"]
    if not iconos:
        return r.saltar("no hay iconos SVG que inspeccionar")
    for p in iconos:
        texto = p.read_text(encoding="utf-8", errors="replace")
        formas = sum(texto.count(f) for f in FORMAS)
        grupos = re.findall(r"<g[\s>].*?</g>", texto, re.S)
        agrupados = [g for g in grupos if sum(g.count(f) for f in FORMAS) > 1]
        if agrupados:
            r.mal(f"{p.name}: un <g> agrupa {sum(agrupados[0].count(f) for f in FORMAS)} "
                  f"formas — se combinan con Union/Subtract, no se agrupan")
        elif formas > 4:
            r.mal(f"{p.name}: {formas} formas sueltas — combínalas en un trazado")
        else:
            r.ok()
    return r


# ═══ Eje C · El movimiento ═══════════════════════════════════════════════════

def h05_cinco_datos(e):
    """DS-H05 — toda animación se entrega con sus cinco datos.

    Sin los cinco, quien la implementa adivina — y adivinar la curva o el disparador es
    lo que produce animaciones que se sienten distintas de las diseñadas.
    """
    r = R("DS-H05", "toda animación declara sus cinco datos")
    anim = e.animaciones()
    if not anim:
        return r.saltar("no hay movimiento.json — el sistema todavía no declara animación")
    for nombre, a in anim.items():
        faltan = [d for d in DATOS_ANIMACION if not a.get(d)]
        if faltan:
            r.mal(f"«{nombre}» sin {', '.join(faltan)}")
        elif a["clase"] not in ("esencial", "adorno"):
            r.mal(f"«{nombre}»: clase «{a['clase']}» — es «esencial» o «adorno»")
        else:
            r.ok()
    return r


def h06_transform(e):
    """DS-H06 — el movimiento se anima con `transform`, nunca con propiedades de posición.

    «Las animaciones con transform usan aceleración por hardware y no disparan
    recálculos de disposición… Las basadas en posición obligan al navegador a recalcular
    la disposición, lo que puede causar tirones, especialmente en móviles.»

    Se comprueba dos veces: en lo declarado y en el CSS que de verdad se publicó. Una
    declaración correcta con un CSS que anima `left` sigue siendo un tirón en el móvil.
    """
    r = R("DS-H06", "el movimiento se anima con transform, no con posición")
    anim, css = e.animaciones(), e.css()
    if not anim and not css:
        return r.saltar("no hay animación declarada ni CSS publicado")
    for nombre, a in anim.items():
        props = [p.strip() for p in str(a.get("propiedad", "")).split(",") if p.strip()]
        caras = [p for p in props if p in PROP_CARA]
        if caras:
            r.mal(f"«{nombre}» anima {', '.join(caras)} — usa transform")
        elif props and all(p in PROP_BARATA for p in props):
            r.ok()
        elif props:
            r.mal(f"«{nombre}» anima «{', '.join(props)}»: no es transform ni opacity")
    for decl in re.findall(r"(?:transition|animation)(?:-property)?\s*:\s*([^;}]+)", css):
        for p in PROP_CARA:
            if re.search(rf"\b{p}\b", decl):
                r.mal(f"sistema.css anima «{p}» en «{decl.strip()[:48]}» — usa transform")
                break
        else:
            r.ok()
    return r


def h09_version_sistema(e):
    """DS-H09 · el sistema declara su versión, y es semántica.

    Sin número, «la versión vigente» es lo que alguien recuerde. Con número, una pantalla
    puede declarar contra qué se dibujó — y eso es lo único que permite saber, cuando el
    sistema cambie, **qué hay que volver a mirar y qué no**.
    """
    r = R("DS-H09", "el sistema declara su versión, y es semántica")
    if not e.marca:
        return r.saltar("no hay marca.json en el destino")
    v = e.version_sistema()
    if not v:
        return r.mal("marca.json no declara «version» — sin ella, ninguna entrega puede "
                     "decir contra qué sistema se dibujó")
    if not SEMVER.match(v):
        return r.mal(f"la versión del sistema es «{v}» — va como 1.0.0, sin «v» delante")
    return r.ok()


def h10_entregas_atadas(e):
    """DS-H10 · toda entrega declara contra qué versión del sistema se dibujó.

    Es la regla que hace que el esquema sirva para algo. Cuando el sistema salte a una
    mayor, una mirada a esta tabla dice qué entregas hay que revisar — en vez de abrirlas
    todas y comparar a ojo.
    """
    r = R("DS-H10", "toda entrega se ata a una versión del sistema")
    entregas = e.entregas()
    if not entregas:
        return r.saltar("no hay entregas cerradas todavía en entrega/versiones.json")
    actual = e.version_sistema()
    mayor_actual = actual.split(".")[0] if SEMVER.match(actual or "") else None
    for ent in entregas:
        nombre = ent.get("nombre", "?")
        propia, contra = str(ent.get("version") or ""), str(ent.get("sistema") or "")
        if not SEMVER.match(propia):
            r.mal(f"«{nombre}» no declara su propia versión, o no es semántica")
            continue
        if not SEMVER.match(contra):
            r.mal(f"«{nombre}» no declara contra qué versión del sistema se dibujó")
            continue
        # Una entrega dibujada contra una MAYOR anterior no está mal: está sin migrar, y
        # eso se dice en voz alta en vez de fallar. Lo que sí falla es no saberlo.
        if mayor_actual and contra.split(".")[0] != mayor_actual:
            if not ent.get("migracion"):
                r.mal(f"«{nombre}» se dibujó contra el sistema {contra} y hoy va por "
                      f"{actual}: cambió una mayor y no declara «migracion»")
                continue
        r.ok()
    return r


EJES = [
    ("La estructura del archivo", [h01_siete_paginas, h08_nada_se_borra, h07_version_por_hito]),
    ("El versionado", [h09_version_sistema, h10_entregas_atadas]),
    ("Los recursos", [h04_formatos, h02_convenio, f10_icono_liviano, f09_trazados_combinados]),
    ("El movimiento", [h05_cinco_datos, h06_transform]),
]


# ═══ El esqueleto ════════════════════════════════════════════════════════════

TITULOS = {
    "para-empezar": "Para empezar", "proyecto": "Nombre del proyecto",
    "documentacion": "Documentación", "componentes": "Componentes",
    "pruebas": "Pruebas y exploración", "archivo": "Archivo", "portada": "Portada",
    "tokens": "Tokens", "patrones": "Patrones", "plantillas": "Plantillas",
    "anotaciones": "Anotaciones",
}
CONTIENE = {
    "para-empezar": "Se abre sola la primera vez. Cómo usar el archivo",
    "proyecto": "Las pantallas, organizadas por secciones lógicas del producto",
    "documentacion": "Encargo, requisitos, investigación, personas, notas",
    "componentes": "Biblioteca local y su documentación",
    "pruebas": "Alternativas, trabajo en curso, experimentos",
    "archivo": "Versiones anteriores y conceptos descartados",
    "portada": "Nombre, estado, equipo, descripción breve",
    "tokens": "La biblioteca de tokens y estilos",
    "patrones": "Combinaciones",
    "plantillas": "Estructuras de pantalla",
    "anotaciones": "Los ayudantes de documentación",
}


def iniciar(e):
    """Crea el esqueleto de la entrega. No inventa contenido: crea los huecos con su nombre."""
    (e.raiz / "entrega").mkdir(parents=True, exist_ok=True)
    (e.raiz / "recursos/iconos").mkdir(parents=True, exist_ok=True)
    (e.raiz / "recursos/imagenes").mkdir(parents=True, exist_ok=True)

    f = e.raiz / "entrega/estructura.json"
    if not f.exists():
        f.write_text(json.dumps({
            "_lee": "La estructura de siete páginas — 07-handoff §7.2. El orden importa: "
                    "es lo que hace que un desarrollador sepa dónde buscar sin preguntar.",
            "producto": [{"id": p, "titulo": TITULOS[p], "contiene": CONTIENE[p]}
                         for p in PAGINAS_PRODUCTO],
            "sistema": [{"id": p, "titulo": TITULOS[p], "contiene": CONTIENE[p]}
                        for p in PAGINAS_SISTEMA],
            "descartado": [],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  creado  {f.relative_to(e.raiz)}")

    f = e.raiz / "movimiento.json"
    if not f.exists():
        f.write_text(json.dumps({
            "_lee": "Los cinco datos de toda animación — 07-handoff §7.6. "
                    "propiedad: transform u opacity; nunca left/top/width/height.",
            "animaciones": {
                "entrada-superposicion": {
                    "clase": "adorno", "duracion": "200ms", "curva": "ease-out",
                    "disparador": "al abrir la superposición; si se dispara dos veces "
                                  "seguidas, la segunda reemplaza a la primera",
                    "propiedad": "opacity, transform",
                },
            },
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  creado  {f.relative_to(e.raiz)}")
    print("\nEsqueleto listo. Pon los iconos en recursos/iconos/ y vuelve a correr sin --iniciar.")


# ═══ Romper a propósito ══════════════════════════════════════════════════════

SVG_SANO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M4 4h16v16H4z"/></svg>')


def romper(e, regla):
    """Mete un error a propósito, en memoria. Una comprobación que nunca falló no está probada."""

    def con_iconos(contenido, nombre="prueba.svg"):
        """Sustituye la lista de iconos por uno inventado, sin tocar el disco.

        Sin esto, un sistema que todavía no exporta iconos no podría probar nunca estas
        comprobaciones: quedarían saltadas para siempre, que es el estado que la doctrina
        del plugin llama «una prueba que no corrió».
        """
        tmp = e.raiz / ".prueba"
        tmp.mkdir(exist_ok=True)
        p = tmp / nombre
        p.write_text(contenido, encoding="utf-8")
        e.iconos = lambda: [p]

    daños = {
        "DS-H01": lambda: (e.estructura or {}).get("producto", []).pop()
        if e.estructura else sys.exit("hace falta entrega/estructura.json para romper DS-H01"),
        "DS-H08": lambda: [p for p in (e.estructura or {}).get("producto", [])
                           if p.get("id") == "archivo"] and
        e.estructura["producto"].remove(
            next(p for p in e.estructura["producto"] if p["id"] == "archivo")),
        "DS-H07": lambda: e.__setattr__(
            "versiones", {"versiones": [{"nombre": "cambios finales FINAL v2"}],
                          "entregas": e.entregas()}),
        "DS-H09": lambda: e.marca.__setitem__("version", "v1"),
        "DS-H10": lambda: e.entregas() and e.entregas()[0].pop("sistema", None),
        "DS-H04": lambda: e.__setattr__("imagenes", lambda: [pathlib.Path("foto-portada.png")]),
        "DS-H02": lambda: con_iconos(SVG_SANO, "Icon Copy 2.svg"),
        "DS-F10": lambda: con_iconos(
            '<svg xmlns="http://www.w3.org/2000/svg"><filter id="f"/>'
            '<path d="M0 0h1v1H0z"/></svg>'),
        "DS-F09": lambda: con_iconos(
            '<svg xmlns="http://www.w3.org/2000/svg"><g><path d="M0 0h1v1H0z"/>'
            '<circle cx="2" cy="2" r="1"/></g></svg>'),
        "DS-H05": lambda: e.__setattr__(
            "movimiento", {"animaciones": {"colada": {"clase": "adorno", "duracion": "200ms"}}}),
        "DS-H06": lambda: e.__setattr__(
            "movimiento", {"animaciones": {"colada": {
                "clase": "adorno", "duracion": "200ms", "curva": "ease-out",
                "disparador": "al abrir", "propiedad": "left, top"}}}),
    }
    # La suite pregunta qué se puede romper en vez de adivinarlo leyendo el código.
    # Una lista escrita a mano en otro archivo se desincroniza en el primer agregado.
    if regla == "lista":
        print(" ".join(sorted(daños)))
        sys.exit(0)
    if regla not in daños:
        sys.exit(f"no sé cómo romper {regla}. Conozco: {', '.join(sorted(daños))}")
    daños[regla]()
    return regla


# ═══ Principal ═══════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Comprueba el paquete de entrega.")
    ap.add_argument("--destino", required=True)
    ap.add_argument("--iniciar", action="store_true", help="crea el esqueleto de la entrega")
    ap.add_argument("--regla", help="ejecuta solo las comprobaciones de esa regla")
    ap.add_argument("--romper", metavar="DS-XXX",
                    help="inyecta un error a propósito para probar el verificador")
    a = ap.parse_args()

    e = Entrega(a.destino)
    if a.iniciar:
        iniciar(e)
        return 0
    if a.romper:
        print(f"⚠  error inyectado a propósito en {romper(e, a.romper)} — "
              f"se espera que la comprobación FALLE\n")

    rep = Reporte(f"entrega · {e.raiz.name}", romper=a.romper, solo=a.regla)
    for eje, checks in EJES:
        rep.eje(eje, [fn(e) for fn in checks])
    salida = rep.cerrar()

    tmp = e.raiz / ".prueba"
    if tmp.is_dir():
        for p in tmp.iterdir():
            p.unlink()
        tmp.rmdir()
    return salida


if __name__ == "__main__":
    sys.exit(main())
