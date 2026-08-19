#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit.py — mide el estado de un sistema ya construido y calcula el score.

    python3 audit.py --destino <sistema> [--screens <carpeta>]
    python3 audit.py --destino <sistema> --html outputs/audit/index.html
    python3 audit.py --destino <sistema> --romper DS-T07

`verificar.py` comprueba reglas mientras se construye; esto **mide estado**: coherencia
de nombres, cobertura de tokens y completitud de las piezas, con la fórmula de
`referencias/informe.md`.

Existe porque la skill definía la fórmula y la dejaba para que el agente la calculara a
mano, que es la manera más segura de que dos auditorías del mismo sistema den números
distintos. **Un score que no es reproducible no es una medida: es una opinión con
decimales.**

Y calcula la que ninguna de las dos hacía: **cuántas de las reglas de la base de conocimiento tienen
dueño**, leídas de la base de conocimiento y no de una lista copiada.

Solo biblioteca estándar.
"""

import argparse
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import CARCASA_ENTRADA  # noqa: E402
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import R, Reporte, cargar_reglas, raiz_plugin, tabla  # noqa: E402

# `informe.md` · la fórmula del score. Está acá una vez y se imprime desde acá:
# si cambia en el documento, cambia en un solo sitio del código.
PESOS = {"nombres": (2, 20), "crudos": (3, 30), "completitud": (1, 40)}
GRAVE = 5

# DS-T04 · un solo convenio en todo el sistema: minúsculas, puntos o guiones, sin
# mayúsculas ni guion bajo ni espacios.
CONVENIO_TOKEN = re.compile(r"^[a-z0-9]+(?:[.\-][a-z0-9]+)*$")
CONVENIO_PIEZA = re.compile(r"^\.?[a-z0-9]+(?:-[a-z0-9]+)*$")

# DS-T07 · ningún valor en crudo. Lo que delata uno.
HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
MEDIDA = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(px|rem|em)\b")

LECTURA = [(90, "Sano. El verificador es el guardián; la auditoría confirma"),
           (70, "Usable, con deuda. Las tres acciones la bajan"),
           (50, "Con deuda seria. Nombres o cobertura se le escaparon al verificador"),
           (0, "En riesgo. La cobertura de tokens está rota (DS-T07 violada a escala)")]


# ═══ Carga ═══════════════════════════════════════════════════════════════════

class Auditoria:
    def __init__(self, destino, pantallas=None):
        self.raiz = pathlib.Path(destino).resolve()
        self.marca = self._json("marca.json") or {}
        self.sem = self._json("tokens/2-semanticos.json") or {}
        self.comp_tok = self._json("tokens/3-componentes.json") or {}
        self.componentes = tabla(self._json("inventario/componentes.json"), "componentes")
        self.patrones = tabla(self._json("inventario/patrones.json"), "patrones")
        d = pathlib.Path(pantallas) if pantallas else self.raiz / "screens"
        self.screens = ({p.stem: json.loads(p.read_text(encoding="utf-8"))
                           for p in sorted(d.glob("*.json"))} if d.is_dir() else {})
        self.hallazgos = {"nombres": [], "crudos": [], "completitud": [], "graves": []}

    def _json(self, rel):
        f = self.raiz / rel
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None

    def piezas(self):
        return {k: v for k, v in self.componentes.items() if not k.startswith("_")}


# ═══ Medida 1 · coherencia de nombres ════════════════════════════════════════

def m1_nombres(a):
    """Un nombre fuera del convenio no rompe nada hoy. Rompe la búsqueda mañana.

    El costo real es que nadie encuentra la pieza: se declara otra igual con otro nombre,
    y ahí empieza la biblioteca con dos botones.
    """
    r = R("DS-T04", "los nombres siguen un solo convenio")
    revisados = 0
    for grupo, patron, que in ((a.sem, CONVENIO_TOKEN, "rol semántico"),
                               (a.comp_tok, CONVENIO_TOKEN, "token de componente"),
                               (a.piezas(), CONVENIO_PIEZA, "componente"),
                               (a.patrones, CONVENIO_PIEZA, "patrón"),
                               (a.screens, re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)*$"),
                                "pantalla")):
        for nombre in grupo:
            if str(nombre).startswith("_"):
                continue
            revisados += 1
            if not patron.match(str(nombre)):
                a.hallazgos["nombres"].append((str(nombre), que))
                r.mal(f"{que} «{nombre}» rompe el convenio")
    if not revisados:
        return r.saltar("no hay nombres que revisar")
    r.ok(revisados - len(a.hallazgos["nombres"]))
    return r


# ═══ Medida 2 · cobertura de tokens ══════════════════════════════════════════

def m2_crudos(a):
    """DS-T07 · ningún valor en crudo. Es lo que más baja el score, y con razón.

    Un `#3A45C9` escrito en una pieza es una pieza que no se puede volver a tematizar:
    el modo oscuro la deja atrás y nadie se entera hasta que alguien lo mira de noche.
    """
    r = R("DS-T07", "ningún valor en crudo en piezas ni pantallas")
    revisados = 0
    fuentes = [("componente " + n, json.dumps(v, ensure_ascii=False))
               for n, v in a.piezas().items()]
    fuentes += [("pantalla " + n, json.dumps(v, ensure_ascii=False))
                for n, v in a.screens.items()]
    fuentes += [("nivel 3 " + n, json.dumps(v, ensure_ascii=False))
                for n, v in a.comp_tok.items() if not str(n).startswith("_")]
    if not fuentes:
        return r.saltar("no hay piezas ni pantallas que revisar")
    for donde, texto in fuentes:
        revisados += 1
        for m in HEX.findall(texto) + [f"{n}{u}" for n, u in MEDIDA.findall(texto)]:
            a.hallazgos["crudos"].append((m, donde))
            r.mal(f"{donde}: «{m}» en crudo — va como token del nivel 3")
    r.ok(revisados - len({d for _, d in a.hallazgos["crudos"]}))
    return r


# ═══ Medida 3 · completitud ══════════════════════════════════════════════════

def m3_completitud(a):
    """Cuatro huecos por pieza: estados, variantes, documentación y foco.

    «Un sistema con 10 componentes todos documentados saca más que uno con 50 a medio
    documentar»: el score mide cobertura, no tamaño.
    """
    r = R("DS-C05", "cada pieza está completa: estados, variantes, docs y foco")
    piezas = a.piezas()
    if not piezas:
        return r.saltar("no hay componentes en el inventario")
    for nombre, c in piezas.items():
        huecos = []
        if not c.get("estados"):
            huecos.append("sin estados")
        if c.get("interactivo") and "foco" not in (c.get("estados") or []):
            huecos.append("interactivo sin foco — DS-C02")
        if c.get("espera_datos") and not c.get("datos"):
            huecos.append("espera datos y no declara carga/vacío/error — DS-C03")
        if len(str(c.get("descripcion") or "")) < 20:
            huecos.append("descripción vacía o mínima")
        # El campo que más se salta y el más útil: un «no» pelado no sirve, tiene que
        # decir qué usar en su lugar.
        cn = str(c.get("cuando_no") or "")
        if len(cn) < 20:
            huecos.append("sin «cuando_no» con sustancia — DS-C05")
        for h in huecos:
            a.hallazgos["completitud"].append((nombre, h))
            r.mal(f"{nombre}: {h}")
        if not huecos:
            r.ok()
    return r


def m3b_variantes(a):
    """DS-C09 · se agrupa como variantes SOLO lo que difiere de forma limitada.

    La regla avisa del **exceso**, no de la ausencia: una barra inferior sin variantes
    está bien, y doce variantes de botón no. Penalizar la ausencia sería inventarle a la
    base de conocimiento una regla que no escribió — y una auditoría que se inventa reglas mide su propio
    criterio, no el sistema.
    """
    r = R("DS-C09", "ninguna pieza agrupa más variantes de las que puede sostener")
    piezas = a.piezas()
    if not piezas:
        return r.saltar("no hay componentes en el inventario")
    for nombre, c in piezas.items():
        v = c.get("variantes") or []
        if len(v) > 6:
            a.hallazgos["completitud"].append(
                (nombre, f"{len(v)} variantes — tres o cuatro cubren cualquier producto"))
            r.mal(f"{nombre}: {len(v)} variantes — agrupa de más")
        else:
            r.ok()
    return r


def m4_inventario(a):
    """Una pieza usada por una pantalla y ausente del inventario es incidencia grave.

    No es un hueco de documentación: es una pieza que nadie declaró y que por lo tanto
    nadie mantiene. Baja 5 y se lista aparte — DS-C01.
    """
    r = R("DS-C01", "toda pieza usada está declarada en el inventario")
    if not a.screens:
        return r.saltar("no hay pantallas que revisar")
    declaradas = set(a.piezas())
    for nombre, p in a.screens.items():
        usadas = {c for zona in (p.get("zonas") or {}).values() for c in zona}
        for c in sorted(usadas - declaradas):
            a.hallazgos["graves"].append((c, f"usada en {nombre}"))
            r.mal(f"{nombre}: «{c}» no está en el inventario")
        r.ok(len(usadas & declaradas))
    return r


# ═══ Medida 4 · cobertura de las reglas de la base de conocimiento ══════════════════════════════

def cobertura_reglas(a):
    """Cuántas de las reglas tienen dueño, y quién es.

    Se leen de la base de conocimiento y se cruzan contra los guiones. Es la medida que hace que una regla
    no pueda quedar huérfana en silencio: si alguien agrega una regla al documento y
    ningún guion la comprueba, aparece acá sin que nadie tenga que acordarse de mirar.
    """
    raiz = raiz_plugin()
    reglas = cargar_reglas(raiz)
    guiones = {}
    for p in sorted((raiz / "skills").rglob("*.py")):
        for m in set(re.findall(r"DS-[A-Z][0-9]{2}", p.read_text(encoding="utf-8"))):
            guiones.setdefault(m, []).append(p.parent.parent.name)
    manual = {k: v for k, v in reglas.items() if v["verifica"] in ("semi", "manual", "—")}
    return reglas, guiones, manual


def m5_cobertura(a):
    r = R("DS-A01", "ninguna regla «auto» de la base de conocimiento queda sin guion")
    reglas, guiones, _ = cobertura_reglas(a)
    auto = [k for k, v in reglas.items() if v["verifica"] == "auto"]
    for k in auto:
        if k in guiones:
            r.ok()
        else:
            r.mal(f"{k} está marcada «auto» y ningún guion la comprueba: "
                  f"{reglas[k]['enunciado'][:56]}")
    return r



# ═══ Medida 6 · consistencia visual ══════════════════════════════════════════

def m6_contrato_entrada(a):
    """DS-C15 · las piezas que reciben datos citan el mismo contrato.

    **Es el eje que faltaba, y el que explica por qué una auditoría podía dar 100 sobre
    un catálogo que no se sentía de una pieza.** Los otros cuatro ejes miran estructura
    —nombres, tokens, completitud, cobertura—; ninguno comparaba las piezas ENTRE SÍ.

    Un sistema real llegó así: el campo con el borde a 3.91:1 contra su fondo y el
    desplegable a 1.30:1, que no se ve. Las dos piezas pasaban todas las reglas.
    """
    r = R("DS-C15", "las piezas de entrada citan el contrato de campo")
    piezas = {n: c for n, c in a.piezas().items() if c.get("grupo") == "entrada"}
    if not piezas:
        return r.saltar("no hay piezas que reciban datos")
    for nombre, c in piezas.items():
        for clave, esperado in CARCASA_ENTRADA.items():
            actual = (c.get("tokens") or {}).get(clave)
            if actual is None or actual == esperado:
                r.ok()
            else:
                a.hallazgos["completitud"].append(
                    (nombre, f"{clave} no cita el contrato de entrada: «{actual}»"))
                r.mal(f"{nombre}.{clave} apunta a «{actual}» en vez de «{esperado}»")
    return r


# ═══ Medida 7 · limpieza ═════════════════════════════════════════════════════

def m7_limpieza(a):
    """DS-X13 · el lienzo publicado no lleva nodos anónimos ni formas sin token.

    Lo que se ve al abrir el archivo: capas «Frame 42» que nadie encuentra, esquinas a
    escuadra porque el radio se quedó sin atar, y estados que se dibujaron idénticos
    porque la instancia no traía qué los distingue.
    """
    r = R("DS-X13", "el lienzo no lleva nodos anónimos ni formas sin token")
    doc = a.raiz / "outputs" / "lienzo.json"
    if not doc.exists():
        return r.saltar("todavía no se publicó lienzo.json")
    lienzo = json.loads(doc.read_text(encoding="utf-8"))

    def recorrer(n, ruta):
        tipo = n.get("tipo")
        if tipo == "instancia":
            r.ok() if "cambia" in n else r.mal(f"{ruta}: instancia sin «cambia»")
        elif tipo == "marco":
            r.ok() if str(n.get("nombre") or "").strip() else r.mal(f"{ruta}: marco sin nombre")
        forma = n.get("forma")
        if forma is not None:
            if isinstance(forma, str) and forma.startswith("{"):
                r.ok()
            else:
                a.hallazgos["crudos"].append((str(forma), f"{ruta} · forma sin token"))
                r.mal(f"{ruta}: forma «{forma}» no es un token — sale a escuadra")
        for h in n.get("hijos") or []:
            recorrer(h, f"{ruta}/{h.get('nombre') or h.get('tipo', '?')}")

    for pag in lienzo.get("paginas") or []:
        for n in pag.get("nodos") or []:
            recorrer(n, f"{pag.get('nombre')}/{n.get('nombre') or n.get('tipo', '?')}")
    return r



EJES = [
    ("Coherencia de nombres", [m1_nombres]),
    ("Cobertura de tokens", [m2_crudos]),
    ("Completitud de las piezas", [m3_completitud, m3b_variantes, m4_inventario]),
    ("Consistencia visual", [m6_contrato_entrada]),
    ("Limpieza", [m7_limpieza]),
    ("Cobertura de las reglas de la base de conocimiento", [m5_cobertura]),
]


# ═══ El score ════════════════════════════════════════════════════════════════

def score(a):
    """Arranca en 100 y se resta. Tres bloques con su tope, más lo grave aparte.

    El tope existe para que un sistema con 400 hexes en crudo no dé el mismo número que
    uno con 4000: por debajo de cierto punto la diferencia deja de informar, y lo que
    informa es la tabla.
    """
    detalle = []
    total = 100
    for bloque, (peso, tope) in PESOS.items():
        n = len(a.hallazgos[bloque])
        resta = min(n * peso, tope)
        total -= resta
        detalle.append((bloque, n, peso, tope, resta))
    graves = len(a.hallazgos["graves"])
    total -= graves * GRAVE
    detalle.append(("graves", graves, GRAVE, None, graves * GRAVE))
    # No se redondea hacia arriba, y no baja de 0.
    return max(0, int(total)), detalle


def lectura(n):
    return next(t for piso, t in LECTURA if n >= piso)


def acciones(a):
    """Tres, por impacto. No una lista: las que más destraban."""
    props = []
    if a.hallazgos["graves"]:
        props.append((100, f"Declarar en el inventario las {len(a.hallazgos['graves'])} "
                           f"piezas que las pantallas usan y nadie declaró — DS-C01"))
    if a.hallazgos["crudos"]:
        cuantos = len(a.hallazgos["crudos"])
        donde = len({d for _, d in a.hallazgos["crudos"]})
        props.append((90, f"Reemplazar los {cuantos} valores en crudo de {donde} piezas por "
                          f"tokens del nivel 3 — DS-T07. Es lo que más baja el score y lo "
                          f"que impide volver a tematizar"))
    faltan_foco = [n for n, h in a.hallazgos["completitud"] if "foco" in h]
    if faltan_foco:
        props.append((85, f"Declarar el estado de foco en {len(faltan_foco)} piezas "
                          f"interactivas — DS-C02. Sin foco visible la pieza no se puede "
                          f"usar con teclado"))
    faltan_datos = [n for n, h in a.hallazgos["completitud"] if "espera datos" in h]
    if faltan_datos:
        props.append((80, f"Declarar carga, vacío y error en {len(faltan_datos)} piezas — "
                          f"DS-C03. Entregar solo el caso feliz es entregar un cuarto"))
    faltan_cn = [n for n, h in a.hallazgos["completitud"] if "cuando_no" in h]
    if faltan_cn:
        props.append((60, f"Escribir el «cuando_no» de {len(faltan_cn)} piezas — DS-C05. "
                          f"Es el campo que más se salta y el que más evita el uso equivocado"))
    if a.hallazgos["nombres"]:
        props.append((50, f"Renombrar las {len(a.hallazgos['nombres'])} piezas fuera del "
                          f"convenio — DS-T04"))
    props.sort(key=lambda x: -x[0])
    return [t for _, t in props[:3]]


# ═══ El informe HTML ═════════════════════════════════════════════════════════

def a_html(a, n, detalle, tres, reglas, guiones, manual):
    e = html.escape

    def tabla(cabeceras, filas):
        if not filas:
            return "<p class=v>Nada que reportar acá.</p>"
        th = "".join(f"<th>{e(c)}</th>" for c in cabeceras)
        tr = "".join("<tr>" + "".join(f"<td>{e(str(c))}</td>" for c in f) + "</tr>"
                     for f in filas)
        return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"

    huerfanas = [(k, reglas[k]["enunciado"], reglas[k]["nivel"])
                 for k, v in reglas.items()
                 if v["verifica"] == "auto" and k not in guiones]
    return f"""<!doctype html><html lang=es><meta charset=utf-8>
<title>Auditoría · {e(a.raiz.name)}</title>
<style>
 :root{{--t:#16161a;--s:#6b6b76;--l:#e6e6ea;--b:#fff;--a:#3a45c9;--r:#b4232a;--g:#1d7a45}}
 *{{box-sizing:border-box}}
 body{{margin:0;padding:48px 32px;background:var(--b);color:var(--t);
   font:16px/1.55 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
 main{{max-width:56rem;margin:0 auto}}
 h1{{font-size:1.6rem;margin:0 0 .25rem}}
 h2{{font-size:1.05rem;margin:2.5rem 0 .75rem;padding-bottom:.4rem;
   border-bottom:1px solid var(--l)}}
 .sub{{color:var(--s);margin:0 0 2rem}}
 .marco{{display:flex;gap:2rem;align-items:baseline;padding:1.25rem 1.5rem;
   border:1px solid var(--l);border-radius:12px;margin-bottom:.75rem}}
 .n{{font-size:3rem;font-weight:650;line-height:1;letter-spacing:-.02em}}
 .n small{{font-size:1rem;font-weight:400;color:var(--s)}}
 table{{width:100%;border-collapse:collapse;font-size:.9rem}}
 th,td{{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--l);
   vertical-align:top}}
 th{{color:var(--s);font-weight:550;font-size:.8rem;text-transform:uppercase;
   letter-spacing:.04em}}
 ol{{padding-left:1.2rem}} ol li{{margin:.5rem 0}}
 .v{{color:var(--s);font-style:italic}}
 code{{font:.85em ui-monospace,SFMono-Regular,Menlo,monospace;background:#f4f4f7;
   padding:.1em .35em;border-radius:4px}}
 .nota{{color:var(--s);font-size:.85rem;margin-top:.5rem}}
</style>
<main>
<h1>Auditoría · {e(a.raiz.name)}</h1>
<p class=sub>{len(a.piezas())} componentes · {len(a.screens)} pantallas ·
 {len(a.patrones)} patrones</p>

<div class=marco>
  <div class=n>{n}<small>/100</small></div>
  <div><strong>{e(lectura(n))}</strong>
  <p class=nota>El score no es el objetivo; es el pulso. Lo que importa son las tablas.</p></div>
</div>

<h2>De dónde sale el score</h2>
{tabla(["Bloque", "Hallazgos", "Resta por cada", "Tope", "Restado"],
       [(b, c, f"−{p}", f"−{t}" if t else "sin tope", f"−{res}")
        for b, c, p, t, res in detalle])}

<h2>Acciones priorizadas</h2>
{"<ol>" + "".join(f"<li>{e(t)}</li>" for t in tres) + "</ol>" if tres
 else "<p class=v>Sin hallazgos: no hay nada que priorizar.</p>"}

<h2>Coherencia de nombres</h2>
{tabla(["Nombre", "Qué es"], a.hallazgos["nombres"])}

<h2>Cobertura de tokens · DS-T07</h2>
{tabla(["Valor en crudo", "Dónde"], a.hallazgos["crudos"])}

<h2>Completitud de las piezas</h2>
{tabla(["Pieza", "Hueco"], a.hallazgos["completitud"])}

<h2>Piezas sin declarar · DS-C01</h2>
{tabla(["Pieza", "Dónde se usa"], a.hallazgos["graves"])}

<h2>Cobertura de las {len(reglas)} reglas de la base de conocimiento</h2>
<p class=nota>Leídas de <code>09-rules/README.md</code>, no de una copia. Una regla que
alguien agregue al documento y ningún guion compruebe aparece acá sola.</p>
{tabla(["Regla", "Enunciado", "Nivel"], huerfanas) if huerfanas
 else "<p class=v>Las " + str(len([1 for v in reglas.values() if v["verifica"] == "auto"]))
      + " reglas «auto» tienen guion que las comprueba.</p>"}

<h2>Lo que ningún guion puede comprobar</h2>
<p class=nota>{len(manual)} reglas son <code>semi</code>, <code>manual</code> o sin
método automático. <strong>Manual no significa opcional:</strong> significa que el
verificador no puede, y por eso las marca una persona.</p>
{tabla(["Regla", "Enunciado", "Método", "Nivel"],
       [(k, v["enunciado"], v["verifica"], v["nivel"]) for k, v in manual.items()])}
</main></html>
"""


# ═══ Romper a propósito ══════════════════════════════════════════════════════

def romper(a, regla):
    """Mete un error a propósito. Una comprobación que nunca falló no está probada."""
    piezas = a.piezas()
    daños = {
        "DS-T04": lambda: a.sem.__setitem__("Rol_Mal_Escrito", "{color.gris.900}"),
        "DS-T07": lambda: next(iter(piezas.values())).__setitem__("_colado", "#BADA55"),
        "DS-C05": lambda: next(iter(piezas.values())).__setitem__("cuando_no", "no"),
        "DS-C09": lambda: next(iter(piezas.values())).__setitem__(
            "variantes", [f"v{i}" for i in range(12)]),
        "DS-C01": lambda: (a.screens or {"x": {}}).setdefault(
            next(iter(a.screens), "pantalla-de-prueba"), {}).setdefault(
            "zonas", {}).__setitem__("colada", ["pieza-que-nadie-declaro"]),
    }
    if regla == "lista":
        print(" ".join(sorted(daños)))
        sys.exit(0)
    if regla not in daños:
        sys.exit(f"no sé cómo romper {regla}. Conozco: {', '.join(sorted(daños))}")
    daños[regla]()
    return regla


# ═══ Principal ═══════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Mide el estado de un sistema y calcula el score.")
    ap.add_argument("--destino", required=True)
    ap.add_argument("--screens", help="carpeta de pantallas, si no es <destino>/screens")
    ap.add_argument("--html", help="además del informe en texto, escribe el HTML acá")
    ap.add_argument("--regla")
    ap.add_argument("--romper", metavar="DS-XXX")
    a_ = ap.parse_args()

    a = Auditoria(a_.destino, a_.screens)
    if a_.romper:
        print(f"⚠  error inyectado a propósito en {romper(a, a_.romper)} — "
              f"se espera que la comprobación FALLE\n")

    rep = Reporte(f"auditoría · {a.raiz.name}", romper=a_.romper, solo=a_.regla)
    for eje, checks in EJES:
        rep.eje(eje, [fn(a) for fn in checks])

    n, detalle = score(a)
    tres = acciones(a)
    print(f"\nScore {n}/100 — {lectura(n)}")
    for b, c, p, t, res in detalle:
        if c:
            print(f"   {b:14} {c:4} × −{p}" + (f" (tope −{t})" if t else "") + f"  →  −{res}")
    if tres:
        print("\nLas tres acciones, por impacto:")
        for i, t in enumerate(tres, 1):
            print(f"   {i}. {t}")

    if a_.html:
        reglas, guiones, manual = cobertura_reglas(a)
        f = pathlib.Path(a_.html)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(a_html(a, n, detalle, tres, reglas, guiones, manual), encoding="utf-8")
        print(f"\nInforme: {f}")

    salida = rep.cerrar()
    # El score acompaña al detalle, nunca lo reemplaza — y no decide el código de salida:
    # lo deciden los fallos, igual que en los otros verificadores.
    return salida


if __name__ == "__main__":
    sys.exit(main())
