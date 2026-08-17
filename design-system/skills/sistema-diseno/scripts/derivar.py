#!/usr/bin/env python3
"""Deriva los tres niveles de token desde los parámetros de marca.

    marca.json                    un acento, una familia, una base
         ↓
    tokens/1-primitivos.json      las escalas — se llaman por lo que SON
         ↓  alias
    tokens/2-semanticos.json      los roles — con un valor POR MODO
         ↓  alias
    tokens/3-componentes.json     dónde se aplica cada uno

Un primitivo se llama por lo que es (`indigo.600`), no por lo que hace (`acento`).
Nombrarlos por su rol colapsa los niveles: el semántico sobra, se salta, y piezas
sin relación terminan compartiendo variable.

Los modos viven en el nivel 2. **Los primitivos nunca cambian por modo**: lo que
cambia es a qué primitivo apunta cada rol. Por eso los modos se estructuran desde
el primer día aunque solo uno esté activo.

    python3 derivar.py --destino <ruta>

Sin dependencias externas.
"""

import argparse
import colorsys
import json
import pathlib
import sys

MIN_TEXTO, MIN_NO_TEXTO = 4.5, 3.0

# Los peldaños de una escala y su claridad objetivo. El 600 es el que sostiene
# texto blanco encima, y por eso es donde se ancla el color que entra.
PELDAÑOS = {0: 1.00, 50: .965, 100: .925, 200: .855, 300: .765, 400: .665,
            500: .575, 600: None, 700: .395, 800: .305, 900: .215, 1000: .09}
ANCLA = 600


# ═══ Color ═══════════════════════════════════════════════════════════════════

def a_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def a_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02X}" for c in rgb)


def luminancia(h):
    c = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in a_rgb(h)]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def hsl(h):
    r, g, b = a_rgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh, ss, ll


def desde_hsl(h, s, l):
    return a_hex(colorsys.hls_to_rgb(h % 1., max(0, min(1, l)), max(0, min(1, s))))


def escala_color(base_hex, saturacion=None):
    """Una escala de 0 a 1000, anclada en el color que entra."""
    h, s, l = hsl(base_hex)
    if saturacion is not None:
        s = saturacion
    claros = [p for p in PELDAÑOS if p < ANCLA]
    oscuros = [p for p in PELDAÑOS if p > ANCLA]
    p_min, p_max = min(claros), max(oscuros)
    escala = {}
    for p in sorted(PELDAÑOS):
        if p == ANCLA:
            lp = l
        elif p < ANCLA:
            t = (p - p_min) / (ANCLA - p_min)
            lp = PELDAÑOS[p_min] + (l - PELDAÑOS[p_min]) * t
        else:
            t = (p - ANCLA) / (p_max - ANCLA)
            lp = l + (PELDAÑOS[p_max] - l) * t
        # los extremos claros con saturación plena se ven chillones
        sp = s * (.55 if p <= 100 else .8 if p <= 200 else 1.)
        escala[p] = desde_hsl(h, sp, lp)
    return escala


# ═══ Nivel 1 · primitivos ════════════════════════════════════════════════════

def primitivos(m):
    t, nom = {}, m["identidad"]["nombre_acento"]

    t[f"color.{nom}"] = escala_color(m["identidad"]["acento"])
    t["color.gris"] = escala_color(m["identidad"]["acento"],
                                   saturacion=m.get("grises", {}).get("tinte", 0))
    for rol, hexa in m.get("acentos_extra", {}).items():
        if not rol.startswith("_"):
            t[f"color.{rol}"] = escala_color(hexa["color"] if isinstance(hexa, dict) else hexa)
    for rol, hexa in m["estados"].items():
        if not rol.startswith("_"):
            t[f"color.{rol}"] = escala_color(hexa)

    esp = m["espaciado"]
    pasos = sorted(set(esp["pasos_principales"] + esp.get("medios_pasos", [])))
    t["medida"] = {str(round(esp["base"] * p)): f"{round(esp['base'] * p)}px" for p in pasos}

    tip = m["tipografia"]
    t["letra"] = {str(round(tip["base"] * tip["razon"] ** p)):
                  f"{round(tip['base'] * tip['razon'] ** p)}px"
                  for p in range(-tip["pasos_abajo"], tip["pasos_arriba"] + 1)}
    t["peso"] = {"regular": 400, "medio": 600, "fuerte": 700, "maximo": 800}
    t["radio"] = {k: f"{v}px" for k, v in m["forma"].items() if not k.startswith("_")}
    t["radio"]["circulo"] = "9999px"
    return t


# ═══ Nivel 2 · semánticos, con modos ═════════════════════════════════════════

# A qué peldaño apunta cada rol, por modo. `@` es la familia del acento.
# Es la tabla que hace el tema, y es la misma para cualquier producto.
ROLES = {
    "superficie.base":       {"claro": ("gris", 0),    "oscuro": ("gris", 900)},
    "superficie.elevada":    {"claro": ("gris", 0),    "oscuro": ("gris", 800)},
    "superficie.hundida":    {"claro": ("gris", 50),   "oscuro": ("gris", 1000)},
    "borde.sutil":           {"claro": ("gris", 200),  "oscuro": ("gris", 700)},
    "borde.fuerte":          {"claro": ("gris", 500),  "oscuro": ("gris", 400)},
    "texto.principal":       {"claro": ("gris", 900),  "oscuro": ("gris", 50)},
    "texto.secundario":      {"claro": ("gris", 700),  "oscuro": ("gris", 300)},
    "texto.sobre-accion":    {"claro": ("gris", 0),    "oscuro": ("gris", 1000)},
    "accion.reposo":         {"claro": ("@", 600),     "oscuro": ("@", 400)},
    "accion.presionado":     {"claro": ("@", 700),     "oscuro": ("@", 300)},
    "accion.tenue":          {"claro": ("@", 50),      "oscuro": ("@", 900)},
    "accion.sobre-tenue":    {"claro": ("@", 800),     "oscuro": ("@", 100)},
}
# Cada color de estado genera su trío: texto, fondo y borde.
PELDAÑOS_ESTADO = {"": (700, 300), ".fondo": (50, 900), ".borde": (200, 700)}

ESPACIO = {"pegado": .5, "elementos": 1, "fila": 1.5, "interior": 2,
           "bloques": 3, "secciones": 4, "respiro": 6}
TIPO = {"display": (4, "maximo", 1.10), "titulo": (3, "fuerte", 1.20),
        "seccion": (2, "medio", 1.30), "subtitulo": (1, "medio", 1.35),
        "cuerpo": (0, "regular", 1.50), "apoyo": (-1, "regular", 1.40),
        "etiqueta": (-2, "medio", 1.30)}


def semanticos(m, modos):
    nom = m["identidad"]["nombre_acento"]
    t = {}

    for rol, por_modo in ROLES.items():
        t[rol] = {}
        for modo in modos:
            fam, peldaño = por_modo[modo]
            t[rol][modo] = f"{{color.{nom if fam == '@' else fam}.{peldaño}}}"

    for estado in (k for k in m["estados"] if not k.startswith("_")):
        for sufijo, (claro, oscuro) in PELDAÑOS_ESTADO.items():
            t[f"estado.{estado}{sufijo}"] = {
                modo: f"{{color.{estado}.{claro if modo == 'claro' else oscuro}}}"
                for modo in modos}

    base = m["espaciado"]["base"]
    for rol, paso in ESPACIO.items():
        t[f"espacio.{rol}"] = f"{{medida.{round(base * paso)}}}"
    for rol in (k for k in m["forma"] if not k.startswith("_")):
        t[f"forma.{rol}"] = f"{{radio.{rol}}}"
    t["forma.marcador"] = "{radio.circulo}"

    tip = m["tipografia"]
    for rol, (paso, peso, interlineado) in TIPO.items():
        px = round(tip["base"] * tip["razon"] ** paso)
        t[f"tipo.{rol}"] = {"tamaño": f"{{letra.{px}}}", "peso": f"{{peso.{peso}}}",
                            "interlineado": interlineado}
    return t


# ═══ Nivel 3 · de componente ═════════════════════════════════════════════════

def componentes(inv):
    t = {}
    for nombre, c in inv.items():
        mapeo = c.get("tokens")
        if isinstance(mapeo, dict):
            for parte, rol in mapeo.items():
                t[f"{nombre.lstrip('.')}.{parte}"] = f"{{{rol}}}"
    return t


# ═══ La comprobación, en TODOS los modos ═════════════════════════════════════

PARES = [
    ("texto sobre superficie",        "texto.principal",    "superficie.base",     MIN_TEXTO),
    ("secundario sobre superficie",   "texto.secundario",   "superficie.base",     MIN_TEXTO),
    ("texto sobre elevada",           "texto.principal",    "superficie.elevada",  MIN_TEXTO),
    ("texto sobre hundida",           "texto.principal",    "superficie.hundida",  MIN_TEXTO),
    ("sobre-accion sobre acción",     "texto.sobre-accion", "accion.reposo",       MIN_TEXTO),
    ("sobre-accion sobre presionado", "texto.sobre-accion", "accion.presionado",   MIN_TEXTO),
    ("acción sobre superficie",       "accion.reposo",      "superficie.base",     MIN_NO_TEXTO),
    ("sobre-tenue sobre tenue",       "accion.sobre-tenue", "accion.tenue",        MIN_TEXTO),
    ("borde fuerte sobre superficie", "borde.fuerte",       "superficie.base",     MIN_NO_TEXTO),
]


def resolver(alias, prim):
    ruta = alias.strip("{}").split(".")
    return prim[".".join(ruta[:-1])][int(ruta[-1])]


def comprobar(m, sem, prim, modos):
    fallos = []
    pares = list(PARES)
    for estado in (k for k in m["estados"] if not k.startswith("_")):
        pares += [
            (f"{estado} sobre su fondo", f"estado.{estado}", f"estado.{estado}.fondo", MIN_TEXTO),
            (f"{estado} sobre superficie", f"estado.{estado}", "superficie.base", MIN_TEXTO)]

    for modo in modos:
        for etiqueta, a, b, minimo in pares:
            r = contraste(resolver(sem[a][modo], prim), resolver(sem[b][modo], prim))
            if r < minimo:
                fallos.append(f"[{modo}] {etiqueta}: {r:.2f}:1 (mín {minimo})")
    return fallos, len(pares) * len(modos)


# ═══ Principal ═══════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Deriva los tres niveles de token.")
    ap.add_argument("--destino", required=True, help="carpeta del sistema de diseño")
    a = ap.parse_args()

    destino = pathlib.Path(a.destino).resolve()
    marca = destino / "marca.json"
    if not marca.exists():
        print(f"no existe {marca}", file=sys.stderr)
        return 2

    m = json.loads(marca.read_text(encoding="utf-8"))
    modos = m["modos"]["activos"] + m["modos"].get("preparados", [])

    inv_f = destino / "inventario" / "componentes.json"
    inv = json.loads(inv_f.read_text(encoding="utf-8"))["componentes"] if inv_f.exists() else {}

    prim, sem = primitivos(m), semanticos(m, modos)
    comp = componentes(inv)
    fallos, n_pruebas = comprobar(m, sem, prim, modos)

    tokens = destino / "tokens"
    tokens.mkdir(parents=True, exist_ok=True)
    for viejo in tokens.glob("*.json"):
        viejo.unlink()

    cabecera = "derivar.py — generado, no editar a mano"
    (tokens / "1-primitivos.json").write_text(json.dumps({
        "_generado_por": cabecera, "_nivel": 1, "_oculto": True,
        "_lee": "Se llaman por lo que SON. Van ocultos de publicación: solo se usan "
                "como alias del nivel 2 — DS-T03",
        **prim}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (tokens / "2-semanticos.json").write_text(json.dumps({
        "_generado_por": cabecera, "_nivel": 2, "_modos": modos,
        "_lee": "Se llaman por lo que HACEN, y llevan un valor por modo.",
        **sem}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (tokens / "3-componentes.json").write_text(json.dumps({
        "_generado_por": cabecera, "_nivel": 3,
        "_lee": "Dónde se aplica. Es lo ÚNICO que una pantalla puede citar — DS-T02.",
        **comp}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    n_col = sum(len(v) for k, v in prim.items() if k.startswith("color."))
    print(f"acento {m['identidad']['acento']} · modos: {', '.join(modos)}\n")
    print(f"  1 · primitivos    {n_col} colores · {len(prim['medida'])} medidas · "
          f"{len(prim['letra'])} tamaños")
    print(f"  2 · semánticos    {len(sem)} roles × {len(modos)} modos")
    print(f"  3 · componentes   {len(comp)} tokens"
          + ("   ← vacío: falta poblar el inventario" if not comp else ""))
    print(f"\n  {n_pruebas} comprobaciones de contraste")
    for f in fallos:
        print(f"  ✗ {f}", file=sys.stderr)
    print(f"  {len(fallos)} fallos")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
