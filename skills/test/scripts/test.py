#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py — prueba pantallas y flujos: momentos, estados, valores límite y accesibilidad.

    python3 test.py --sistema <sistema> --screens <carpeta>
    python3 test.py --sistema <s> --screens <p> --html outputs/pruebas/index.html
    python3 test.py --sistema <s> --screens <p> --romper DS-F02

Existe porque la skill `test` era, hasta ahora, **una lista que revisa una persona** —
exactamente lo que este plugin existe para reemplazar. La base de conocimiento lo dice del libro que la
originó `[Extensión G1]`: su control de calidad son reuniones y listas manuales. Y el revisor
técnico del propio libro apunta a dónde debería ir:

    «Muchos de estos puntos deberían idealmente automatizarse mediante marcos de prueba
     en lugar de comprobarse a mano. La automatización garantiza consistencia, ahorra
     tiempo y detecta problemas de forma más confiable que las revisiones manuales.»

Comprueba: DS-F02, DS-L03, DS-L06, DS-P03, DS-C03, DS-A05, DS-A07, DS-A08.

**Lo que NO hace, y se dice:** no ejecuta un navegador. Las comprobaciones son estáticas
—sobre la declaración de la pantalla y el CSS publicado—. `DS-A12` («axe-core en la
tubería cuando exista la aplicación») sigue siendo la mejora pendiente, y esto no la
reemplaza: la prepara.

Solo biblioteca estándar.
"""

import argparse
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import R, Reporte, tabla  # noqa: E402

# `pantalla/referencias/patrones.md` — los cinco momentos de un flujo `[Libro 2, capítulo 9]`.
# El cuarto es el que siempre falta.
MOMENTOS = ["entrada", "decision", "exito", "error", "salida"]
ESTADOS = ["lleno", "cargando", "vacio", "error"]

# El vocabulario de dimensionado, tal como lo usan las plantillas base. `fijo` es el
# único que corta el texto al crecer; `resto` es lo que ocupa lo que sobra.
DIMENSION_OK = {"abraza", "llena", "resto", ""}

# DS-F02 · ninguna etiqueta traducible usa tamaño fijo.
FIJO = re.compile(r'"(?:dimension|ancho|alto)"\s*:\s*"fijo"')

# DS-A08 · al 200 % de texto. Lo que lo delata en el HTML renderizado: una altura fija
# en algo que lleva texto, o un desbordamiento oculto que se lo come.
ALTURA_FIJA = re.compile(r"\b(?:height|max-height)\s*:\s*\d+(?:px|rem|em)\b")
OCULTO = re.compile(r"\boverflow\s*:\s*hidden\b")


# ═══ Carga ═══════════════════════════════════════════════════════════════════

class Prueba:
    def __init__(self, sistema, pantallas):
        self.raiz = pathlib.Path(sistema).resolve()
        d = pathlib.Path(pantallas)
        if not d.is_dir():
            sys.exit(f"no existe la carpeta de pantallas: {d}")
        self.screens = {p.stem: json.loads(p.read_text(encoding="utf-8"))
                          for p in sorted(d.glob("*.json"))}
        self.patrones = tabla(self._json("inventario/patrones.json"), "patrones")
        self.plantillas = tabla(self._json("inventario/plantillas.json"), "plantillas")
        self.componentes = tabla(self._json("inventario/componentes.json"), "componentes")
        self._css = None

    def _json(self, rel):
        f = self.raiz / rel
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None

    def css(self):
        if self._css is None:
            f = self.raiz / "outputs/sistema.css"
            self._css = f.read_text(encoding="utf-8") if f.exists() else ""
        return self._css


# ═══ Eje A · Los cinco momentos ══════════════════════════════════════════════

def p03_momentos(p):
    """DS-P03 · un flujo tiene cinco momentos, y el cuarto es el que siempre falta.

    entrada · decisión · éxito · **error** · salida. Un patrón cuyos estados son todos
    felices no está incompleto por descuido: está incompleto porque el error es el único
    momento que hay que imaginar en vez de recordar.
    """
    r = R("DS-P03", "todo flujo recorre sus cinco momentos")
    flujos = {n: pat for n, pat in p.patrones.items()
              if len(pat.get("estados") or []) >= 4 or "pasos" in pat}
    if not flujos:
        return r.saltar("no hay patrones que sean flujos — un patrón de un solo paso no "
                        "tiene cinco momentos")
    for nombre, pat in flujos.items():
        estados = {str(e).lower() for e in (pat.get("estados") or [])}
        faltan = [m for m in MOMENTOS if m not in estados]
        # Un flujo puede declarar los momentos con otro vocabulario; lo que no puede es
        # no tener ninguno que sea un fallo.
        if not estados & {"error", "fallo", "rechazo"}:
            r.mal(f"«{nombre}» no contempla que algo salga mal — es el momento que "
                  f"siempre falta")
        elif faltan:
            r.ok()  # tiene el fallo; los otros nombres pueden variar
        else:
            r.ok()
    return r


def c03_estados(p):
    """DS-C03 · cuatro estados, no uno. Entregar solo el caso feliz es entregar un cuarto.

    «No aplica» vale, **con su motivo**. Sin motivo es un estado olvidado con permiso.
    """
    r = R("DS-C03", "toda pantalla declara sus cuatro estados")
    if not p.screens:
        return r.saltar("no hay pantallas que probar")
    for nombre, pan in p.screens.items():
        estados = pan.get("estados") or {}
        for e in ESTADOS:
            v = str(estados.get(e) or "")
            if not v:
                r.mal(f"{nombre}: falta el estado «{e}»")
            elif v.lower().startswith("no aplica") and "—" not in v and "-" not in v:
                r.mal(f"{nombre}: «{e}» dice «no aplica» sin motivo")
            else:
                r.ok()
    return r


# ═══ Eje B · Los valores límite ══════════════════════════════════════════════

def l06_extremos(p):
    """DS-L06 · se prueba con el valor más largo y el más corto.

    Es donde las maquetas se rompen. Lo que se puede comprobar sin inventar un umbral:
    que los dos extremos estén, que el «largo» no sea **más corto** que el «corto», y que
    un «no aplica» traiga su motivo.

    **Lo que NO se comprueba, a propósito:** que el «largo» sea *suficientemente* largo.
    Un enum de tres letras tiene corto y largo iguales con toda razón, y un precio topa
    donde topa. Poner un mínimo de caracteres sería medir un umbral que la base de conocimiento nunca
    escribió — y eso es la auditoría midiendo su propio criterio. Queda en la lista de
    lo que mira una persona.
    """
    r = R("DS-L06", "los extremos declarados de verdad son extremos")
    if not p.screens:
        return r.saltar("no hay pantallas que probar")
    for nombre, pan in p.screens.items():
        extremos = (pan.get("datos") or {}).get("extremos") or {}
        campos = (pan.get("datos") or {}).get("campos") or []
        for campo in campos:
            e = extremos.get(campo)
            if e is None:
                r.mal(f"{nombre}: «{campo}» no declara sus extremos")
                continue
            if isinstance(e, str):
                # «no aplica — <motivo>», y el motivo no es opcional.
                if not e.lower().startswith("no aplica") or len(e) < 20:
                    r.mal(f"{nombre}: «{campo}» → «{e[:30]}» no es un extremo ni un "
                          f"«no aplica» con motivo")
                else:
                    r.ok()
                continue
            corto, largo = str(e.get("corto", "")), str(e.get("largo", ""))
            if not corto or not largo:
                r.mal(f"{nombre}: «{campo}» declara solo uno de los dos extremos")
            elif len(largo) < len(corto):
                r.mal(f"{nombre}: «{campo}» — el «largo» ({len(largo)}) es más corto que "
                      f"el «corto» ({len(corto)}): están al revés")
            else:
                r.ok()
    return r


def f02_texto_sin_tamano_fijo(p):
    """DS-F02 · ningún texto traducible usa tamaño fijo.

    «Casi nunca. **El texto se corta si crece.**» Y crece: la expansión entre idiomas es
    del 30 % largo desde el inglés, y el alemán se lleva la peor parte `[Libro 1, capítulo 3]`.

    Se mira en dos lados: la zona que contiene texto no puede ser de dimensión `fijo`, y
    los textos declarados tienen que ser los más largos, no los más cómodos.
    """
    r = R("DS-F02", "ningún contenedor de texto usa tamaño fijo")
    if not p.screens:
        return r.saltar("no hay pantallas que probar")
    # Qué zonas de qué plantilla llevan texto: las que admiten un componente que lo tiene.
    con_texto = set()
    for nombre, pl in p.plantillas.items():
        for z in pl.get("zonas") or []:
            admite = z.get("admite") or []
            if any(c in admite for c in ("mensaje", "campo", "tarjeta", "opcion", "enlace",
                                         "barra-superior", "boton", "vacio", "chip")):
                con_texto.add((nombre, z.get("nombre")))
    for nombre, pan in p.screens.items():
        plantilla = pan.get("plantilla")
        pl = p.plantillas.get(plantilla) or {}
        for z in pl.get("zonas") or []:
            if (plantilla, z.get("nombre")) not in con_texto:
                continue
            if str(z.get("dimension", "")).lower() not in DIMENSION_OK:
                r.mal(f"{nombre}: la zona «{z.get('nombre')}» de «{plantilla}» lleva "
                      f"texto y es de dimensión fija — el texto se corta al traducir")
            else:
                r.ok()
        # Y un texto declarado en su versión cómoda es la otra mitad de la misma regla.
        for clave, texto in (pan.get("textos") or {}).items():
            if texto is None:
                continue
            if FIJO.search(json.dumps(pan, ensure_ascii=False)):
                r.mal(f"{nombre}: hay un dimensionado «fijo» declarado en la pantalla")
                break
        else:
            r.ok()
    return r


def l03_eje_del_texto(p):
    """DS-L03 · ningún contenedor de texto usa `Fixed` en el eje del texto.

    Es la versión de disposición de la regla anterior. La base de conocimiento las separa porque una vive
    en los fundamentos y la otra en el armado, pero lo que se rompe es lo mismo: el texto
    crece al traducir y el contenedor no lo deja.
    """
    r = R("DS-L03", "ninguna zona de texto está fija en el eje del texto")
    if not p.plantillas:
        return r.saltar("no hay plantillas que revisar")
    usadas = {pan.get("plantilla") for pan in p.screens.values()}
    if not usadas:
        return r.saltar("ninguna pantalla declara plantilla")
    for nombre in usadas:
        pl = p.plantillas.get(nombre)
        if not pl:
            continue
        for z in pl.get("zonas") or []:
            dim = str(z.get("dimension", "")).lower()
            if dim == "fijo":
                r.mal(f"«{nombre}»: la zona «{z.get('nombre')}» es fija — si lleva texto, "
                      f"lo corta")
            elif dim in DIMENSION_OK:
                r.ok()
            else:
                r.mal(f"«{nombre}»: la zona «{z.get('nombre')}» dice «{dim}» — "
                      f"el vocabulario es abraza, llena, resto o fijo")
    return r


# ═══ Eje C · Accesibilidad ═══════════════════════════════════════════════════

def a05_un_solo_h1(p):
    """DS-A05 · un solo H1 por pantalla, con jerarquía descendente.

    Dos titulares del mismo peso es el error que un lector de pantalla convierte en dos
    documentos donde había uno.
    """
    r = R("DS-A05", "cada pantalla declara un solo titular")
    if not p.screens:
        return r.saltar("no hay pantallas que probar")
    for nombre, pan in p.screens.items():
        h1 = pan.get("h1")
        if not h1:
            r.mal(f"{nombre}: no declara cuál texto es el titular")
        elif isinstance(h1, list):
            r.mal(f"{nombre}: declara {len(h1)} titulares — uno solo")
        elif h1 not in (pan.get("textos") or {}):
            r.mal(f"{nombre}: el titular «{h1}» no existe en «textos»")
        else:
            r.ok()
    return r


def a07_teclado(p):
    """DS-A07 · lo que se hace con ratón se hace con teclado, y el foco se ve.

    Dos condiciones, y la segunda es la que se olvida: un orden de tabulación que diverge
    del visual **se explica**, y todo interactivo declara su foco. Un foco declarado que
    el CSS publicado no dibuja es un foco que no existe.
    """
    r = R("DS-A07", "el recorrido por teclado está declarado y el foco se dibuja")
    if not p.screens:
        return r.saltar("no hay pantallas que probar")
    for nombre, pan in p.screens.items():
        orden = str(pan.get("orden_tabulacion") or "")
        if not orden:
            r.mal(f"{nombre}: no declara orden de tabulación")
        elif "coincide" not in orden.lower() and len(orden) < 25:
            r.mal(f"{nombre}: el orden diverge del visual y no lo explica — «{orden}»")
        else:
            r.ok()
    # Y la otra mitad: un foco declarado en el inventario que el sistema no publica es un
    # foco que quien implementa no puede dibujar. `sistema.css` es un archivo de TOKENS,
    # no una hoja con selectores — así que lo que se comprueba acá es que el token exista,
    # no que haya una regla `:focus`. Pedirle selectores a un archivo de variables sería
    # comprobar contra el archivo equivocado.
    css = p.css()
    interactivos = [n for n, c in p.componentes.items()
                    if isinstance(c, dict) and c.get("interactivo")]
    if not interactivos:
        return r
    if not css:
        return r.saltar("no hay outputs/sistema.css: el foco declarado no se puede confirmar")
    if not re.search(r"--[\w-]*foco[\w-]*\s*:", css):
        r.mal(f"{len(interactivos)} componentes declaran foco y el sistema no publica "
              f"ningún token de foco — quien implementa no tiene con qué dibujarlo")
    else:
        r.ok()
    return r


def a08_zoom(p):
    """DS-A08 · toda pantalla se revisa al 200 % de texto.

    No se puede renderizar acá, pero **sí se puede detectar lo que la rompe**: una altura
    fija en algo que lleva texto, o un desbordamiento oculto que se come lo que crece.

    Se mira la **galería** —el HTML de cada componente, que sí tiene selectores y estilos
    reales— y no `sistema.css`, que es un archivo de variables. Es una comprobación
    estática, y se dice: **no reemplaza abrir la pantalla y ampliar el texto.**
    """
    r = R("DS-A08", "nada en lo publicado impide que el texto crezca al 200 %")
    galeria = p.raiz / "outputs/galeria"
    archivos = sorted(galeria.glob("*.html")) if galeria.is_dir() else []
    if not archivos:
        return r.saltar("no hay outputs/galeria: corré construir.py --salidas galeria")
    for f in archivos:
        texto = f.read_text(encoding="utf-8", errors="replace")
        malo = False
        for selector, cuerpo in re.findall(r"([^{}]+)\{([^{}]*)\}", texto):
            if not re.search(r"font|text|line-height", cuerpo):
                continue
            sel = selector.strip().splitlines()[-1][:40]
            if ALTURA_FIJA.search(cuerpo):
                r.mal(f"{f.name}: «{sel}» fija la altura de algo con texto — al 200 % corta")
                malo = True
            elif OCULTO.search(cuerpo):
                r.mal(f"{f.name}: «{sel}» oculta el desbordamiento de algo con texto")
                malo = True
        if not malo:
            r.ok()
    return r


EJES = [
    ("Los cinco momentos y los cuatro estados", [p03_momentos, c03_estados]),
    ("Los valores límite y la traducción", [l06_extremos, f02_texto_sin_tamano_fijo,
                                            l03_eje_del_texto]),
    ("Accesibilidad", [a05_un_solo_h1, a07_teclado, a08_zoom]),
]


# ═══ El informe HTML ═════════════════════════════════════════════════════════

# Lo que ninguna comprobación estática detecta. Va al informe para que una persona lo
# marque: `manual` no significa opcional — significa que el guion no puede.
A_OJO = [
    ("DS-A03", "Ninguna información se comunica solo con color"),
    ("DS-A07", "Recorrer la pantalla entera con Tab, sin tocar el ratón"),
    ("DS-A08", "Abrirla y ampliar el texto al 200 %: ¿se entiende todo?"),
    ("DS-A11", "Abrirla en un dispositivo de gama baja"),
    ("DS-A12", "«axe-core en la tubería cuando exista la aplicación» — la mejora pendiente"),
    ("DS-L05", "¿Se diseñó móvil primero, o se encogió el escritorio?"),
    ("DS-P05", "¿Alguna superficie continua es el único portador de algo necesario?"),
    ("—", "¿Lo que distingue al producto se ve SIN desplazar?"),
    ("—", "¿El espaciado agrupa lo que va junto?"),
]


def a_html(p, resultados):
    e = html.escape
    filas = ""
    for eje, rs in resultados:
        filas += f"<tr class=eje><td colspan=4>{e(eje)}</td></tr>"
        for r in rs:
            if r.saltada:
                estado, det = "<span class=s>saltada</span>", e(r.saltada)
            elif r.fallos:
                estado = f"<span class=x>{len(r.fallos)} fallos</span>"
                det = "<ul>" + "".join(f"<li>{e(f)}</li>" for f in r.fallos[:10]) + "</ul>"
            else:
                estado, det = f"<span class=v>✓ {r.n}</span>", ""
            filas += (f"<tr><td><code>{e(r.regla)}</code></td><td>{e(r.nombre)}</td>"
                      f"<td>{estado}</td><td>{det}</td></tr>")
    ojo = "".join(f"<li><code>{e(k)}</code> {e(t)}</li>" for k, t in A_OJO)
    pans = "".join(f"<li><strong>{e(n)}</strong> — {e(str(v.get('proposito', '')))}</li>"
                   for n, v in p.screens.items())
    return f"""<!doctype html><html lang=es><meta charset=utf-8>
<title>Pruebas · {e(p.raiz.name)}</title>
<style>
 :root{{--t:#16161a;--s:#6b6b76;--l:#e6e6ea;--b:#fff;--r:#b4232a;--g:#1d7a45;--a:#8a6d1f}}
 *{{box-sizing:border-box}}
 body{{margin:0;padding:48px 32px;background:var(--b);color:var(--t);
  font:16px/1.55 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
 main{{max-width:60rem;margin:0 auto}}
 h1{{font-size:1.6rem;margin:0 0 .25rem}}
 h2{{font-size:1.05rem;margin:2.5rem 0 .75rem;padding-bottom:.4rem;
  border-bottom:1px solid var(--l)}}
 .sub{{color:var(--s);margin:0 0 2rem}}
 table{{width:100%;border-collapse:collapse;font-size:.9rem}}
 th,td{{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--l);
  vertical-align:top}}
 th{{color:var(--s);font-weight:550;font-size:.8rem;text-transform:uppercase;
  letter-spacing:.04em}}
 tr.eje td{{background:#f7f7fa;font-weight:600;font-size:.82rem;
  text-transform:uppercase;letter-spacing:.05em;color:var(--s)}}
 .v{{color:var(--g);font-weight:600}} .x{{color:var(--r);font-weight:600}}
 .s{{color:var(--a);font-weight:600}}
 ul{{margin:.2rem 0;padding-left:1.1rem}} li{{margin:.15rem 0}}
 code{{font:.85em ui-monospace,SFMono-Regular,Menlo,monospace;background:#f4f4f7;
  padding:.1em .35em;border-radius:4px}}
 .nota{{color:var(--s);font-size:.85rem}}
 .caja{{border:1px solid var(--l);border-radius:12px;padding:1rem 1.25rem;
  margin-top:.75rem}}
</style>
<main>
<h1>Pruebas · {e(p.raiz.name)}</h1>
<p class=sub>{len(p.screens)} pantallas · {len(p.patrones)} patrones</p>

<h2>Qué se probó</h2>
<ul>{pans}</ul>

<h2>Resultado, regla por regla</h2>
<table><thead><tr><th>Regla</th><th>Comprobación</th><th>Estado</th><th>Detalle</th>
</tr></thead><tbody>{filas}</tbody></table>

<h2>Lo que ningún guion detecta</h2>
<div class=caja>
<p class=nota><strong>Manual no significa opcional:</strong> significa que el verificador
no puede, y por eso lo marca una persona. Estas comprobaciones son estáticas — sobre la
declaración y el CSS. <strong>No reemplazan abrir la pantalla.</strong></p>
<ul>{ojo}</ul>
</div>
</main></html>
"""


# ═══ Romper a propósito ══════════════════════════════════════════════════════

SUCIO = "outputs/galeria/prueba-a08.html"


def romper(p, regla):
    """Mete un error a propósito. Una comprobación que nunca falló no está probada."""

    def primera_pantalla():
        if not p.screens:
            sys.exit("hacen falta pantallas para romper esta regla")
        return next(iter(p.screens.values()))

    def zona_fija():
        pan = primera_pantalla()
        pl = p.plantillas.get(pan.get("plantilla"))
        if not pl or not pl.get("zonas"):
            sys.exit("hace falta una plantilla con zonas")
        pl["zonas"][0]["dimension"] = "fijo"

    daños = {
        "DS-P03": lambda: p.patrones.__setitem__(
            "flujo-de-prueba", {"proposito": "probar el verificador",
                                "estados": ["entrada", "decision", "exito", "salida"]}),
        "DS-C03": lambda: primera_pantalla().get("estados", {}).__setitem__("error", ""),
        # Los extremos al revés: el «largo» más corto que el «corto». Es el error que de
        # verdad se comete al copiar y pegar la entrada de otro campo.
        "DS-L06": lambda: primera_pantalla()["datos"]["extremos"].update(
            {next(iter(primera_pantalla()["datos"]["campos"])):
             {"corto": "María de los Ángeles Fernández", "largo": "Ana"}}),
        "DS-F02": zona_fija,
        "DS-L03": zona_fija,
        "DS-A05": lambda: primera_pantalla().__setitem__("h1", ["titulo", "accion"]),
        "DS-A07": lambda: primera_pantalla().__setitem__("orden_tabulacion", "otro"),
        # DS-A08 lee la galería del disco, así que el daño se inyecta ahí: un archivo de
        # más con una altura fija sobre texto. Se limpia al terminar.
        "DS-A08": lambda: (p.raiz / "outputs/galeria").mkdir(parents=True, exist_ok=True) or
        (p.raiz / SUCIO).write_text(
            "<style>.t{font-size:16px;line-height:1.5;height:32px}</style><p class=t>x",
            encoding="utf-8"),
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
    ap = argparse.ArgumentParser(description="Prueba pantallas y flujos.")
    ap.add_argument("--sistema", required=True)
    ap.add_argument("--screens", required=True)
    ap.add_argument("--html", help="escribe el reporte HTML acá")
    ap.add_argument("--regla")
    ap.add_argument("--romper", metavar="DS-XXX")
    a = ap.parse_args()

    p = Prueba(a.sistema, a.screens)
    if a.romper:
        print(f"⚠  error inyectado a propósito en {romper(p, a.romper)} — "
              f"se espera que la comprobación FALLE\n")

    rep = Reporte(f"pruebas · {p.raiz.name}", romper=a.romper, solo=a.regla)
    resultados = []
    for eje, checks in EJES:
        rs = [fn(p) for fn in checks]
        resultados.append((eje, rs))
        rep.eje(eje, rs)

    if a.html:
        f = pathlib.Path(a.html)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(a_html(p, resultados), encoding="utf-8")
        print(f"Reporte: {f}")

    salida = rep.cerrar()
    print("\nLo que ningún guion detecta, y hay que mirar:")
    for k, t in A_OJO:
        print(f"   □  {k:8} {t}")

    # El daño de DS-A08 se escribe en el disco porque la comprobación lee de ahí.
    # Se borra siempre: una prueba que deja basura ensucia la siguiente corrida.
    sucio = p.raiz / SUCIO
    if sucio.exists():
        sucio.unlink()
    return salida


if __name__ == "__main__":
    sys.exit(main())
