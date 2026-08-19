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

**El color de marca entra tal cual y no se modifica nunca**, sea un indigo o un
amarillo. Se ancla en el peldaño que le toca por lo claro que se ve, y lo que se
elige alrededor es en qué peldaño se apoya la acción y qué texto va encima —tinta
o blanco—. La alternativa era la de antes: cablear el 600 con blanco encima y
pedirle al usuario que oscurezca su marca cuando no cuadra, que es cambiar el
producto para que el script funcione.

    python3 derivar.py --destino <ruta>

Sin dependencias externas.
"""

import argparse
import colorsys
import json
import pathlib
import sys

MIN_TEXTO, MIN_NO_TEXTO = 4.5, 3.0

# Los peldaños de una escala y su claridad objetivo.
#
# El color que entra NO se fuerza a un peldaño: se ancla en el que le corresponde
# por su claridad. Anclar todo en el 600 daba por sentado que toda marca es
# oscura — un amarillo se declaraba «600» y de ahí salía una escala donde ni el
# 900 era oscuro de verdad, y la única salida era pedirle al usuario que
# oscureciera su marca. Cambiar el producto para que el script funcione.
PELDAÑOS = {0: 1.00, 50: .965, 100: .925, 200: .855, 300: .765, 400: .665,
            500: .575, 600: .485, 700: .395, 800: .305, 900: .215, 1000: .09}

# Cuánta saturación conserva el peldaño más claro de una escala.
AMORTIGUA = .55


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


def claridad_percibida(h):
    """La claridad del gris que tiene la misma luminancia que este color.

    Un amarillo y un azul con la misma L de HSL no se ven igual de claros: el
    amarillo deslumbra y el azul es casi negro. Esto los pone en la misma vara —
    la misma con la que se mide el contraste."""
    y = luminancia(h)
    return 1.055 * y ** (1 / 2.4) - .055 if y > .0031308 else y * 12.92


def ancla_natural(base_hex):
    """El peldaño que le corresponde a un color por lo claro que se ve."""
    c = claridad_percibida(base_hex)
    return min(PELDAÑOS, key=lambda p: abs(PELDAÑOS[p] - c))


def l_para(h, s, objetivo):
    """La L de HSL que da esa claridad percibida, con ese tono y saturación.

    La escala se interpola en claridad PERCIBIDA, no en L de HSL. Son cosas
    distintas en cuanto el color satura —un verde puro con L de .5 se ve más claro
    que un gris de .8— y mezclar las dos varas hace que un peldaño quede más claro
    que el que tiene encima. La luminancia sube con la L, así que se puede buscar
    partiendo el intervalo."""
    bajo, alto = 0., 1.
    for _ in range(24):
        medio = (bajo + alto) / 2
        if claridad_percibida(desde_hsl(h, s, medio)) < objetivo:
            bajo = medio
        else:
            alto = medio
    return (bajo + alto) / 2


def escala_color(base_hex, ancla=None):
    """Una escala de 0 a 1000 anclada en el color que entra, sin modificarlo.

    El color de marca aparece tal cual en su peldaño, sea claro u oscuro. Lo que
    se acomoda alrededor es la escala, nunca el color."""
    h, s, _ = hsl(base_hex)
    ancla = ancla if ancla is not None else ancla_natural(base_hex)
    claridad = claridad_percibida(base_hex)
    p_min, p_max = min(PELDAÑOS), max(PELDAÑOS)
    escala = {}
    for p in sorted(PELDAÑOS):
        if p == ancla:
            escala[p] = base_hex.upper()          # el color de marca, intacto
            continue
        if p < ancla:
            t = (p - p_min) / (ancla - p_min)
            objetivo = PELDAÑOS[p_min] + (claridad - PELDAÑOS[p_min]) * t
            # Los peldaños claros con saturación plena se ven chillones. La
            # amortiguación sube desde el extremo claro hasta 1 en el ancla: un
            # escalón fijo dejaba al vecino de un amarillo más apagado que la marca.
            sp = s * (AMORTIGUA + (1 - AMORTIGUA) * t)
        else:
            t = (p - ancla) / (p_max - ancla)
            objetivo = claridad + (PELDAÑOS[p_max] - claridad) * t
            sp = s
        escala[p] = desde_hsl(h, sp, l_para(h, sp, objetivo))
    return escala


def escala_neutra(base_hex, saturacion):
    """Los grises: el TONO del acento, nunca su claridad.

    Cuando heredaban también el ancla del acento, una marca clara producía grises
    claros, y el borde fuerte y el texto secundario dejaban de contrastar contra
    la superficie — un fallo que el color de marca no había causado."""
    h = hsl(base_hex)[0]
    return {p: desde_hsl(h, saturacion, l_para(h, saturacion, objetivo))
            for p, objetivo in PELDAÑOS.items()}


# ═══ Nivel 1 · primitivos ════════════════════════════════════════════════════

def primitivos(m):
    t, nom = {}, m["identidad"]["nombre_acento"]

    t[f"color.{nom}"] = escala_color(m["identidad"]["acento"])
    t["color.gris"] = escala_neutra(m["identidad"]["acento"],
                                    m.get("grises", {}).get("tinte", 0))
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

    # La altura de un control tiene su propio grupo, aparte de `medida`. No es una
    # coquetería de orden: la escala de espacio se comprueba entera —DS-F06, ningún
    # valor fuera de ella— y el piso de un objetivo táctil no sale de multiplicar la
    # base por un paso, sale de cuánto mide un dedo. Meterlas juntas obliga a inventar
    # pasos de espaciado que nadie va a usar como espaciado.
    alturas = {v for k, v in (m.get("tacto", {}).get("control") or {}).items()
               if not k.startswith("_")}
    if alturas:
        t["alto"] = {str(a): f"{a}px" for a in sorted(alturas)}
    return t


# ═══ Nivel 2 · semánticos, con modos ═════════════════════════════════════════

# A qué peldaño apunta cada rol, por modo. Es la tabla que hace el tema, y es la
# misma para cualquier producto: el gris siempre se comporta igual.
ROLES = {
    "superficie.base":       {"claro": ("gris", 0),    "oscuro": ("gris", 900)},
    "superficie.elevada":    {"claro": ("gris", 0),    "oscuro": ("gris", 800)},
    "superficie.hundida":    {"claro": ("gris", 50),   "oscuro": ("gris", 1000)},
    "borde.sutil":           {"claro": ("gris", 200),  "oscuro": ("gris", 700)},
    # El 500 se ve gris de borde, pero no llega a 3:1 contra el blanco con ningún
    # tinte —2.97 con el de omisión, 2.48 con el máximo—. El 600 lo cumple entero.
    "borde.fuerte":          {"claro": ("gris", 600),  "oscuro": ("gris", 400)},
    "texto.principal":       {"claro": ("gris", 900),  "oscuro": ("gris", 50)},
    "texto.secundario":      {"claro": ("gris", 700),  "oscuro": ("gris", 300)},
}

# Los roles de acción NO se cablean: dependen de qué color de marca entró.
# `accion.reposo → 600` con `texto.sobre-accion → blanco` da por sentado que toda
# marca es oscura, y cuando no lo es deja una sola salida —oscurecer la marca—.
# Acá el color entra tal cual y lo que se elige es en qué peldaño se apoya la
# acción y qué va encima, tinta o blanco. Es lo que hace que una marca amarilla
# dé un botón amarillo con texto negro en vez de un fallo de contraste.
TINTA, BLANCO = 1000, 0
# Cada color de estado genera su trío: texto, fondo y borde.
PELDAÑOS_ESTADO = {"": (700, 300), ".fondo": (50, 900), ".borde": (200, 700)}

ESPACIO = {"pegado": .5, "elementos": 1, "fila": 1.5, "interior": 2,
           "bloques": 3, "secciones": 4, "respiro": 6}
TIPO = {"display": (4, "maximo", 1.10), "titulo": (3, "fuerte", 1.20),
        "seccion": (2, "medio", 1.30), "subtitulo": (1, "medio", 1.35),
        "cuerpo": (0, "regular", 1.50), "apoyo": (-1, "regular", 1.40),
        "etiqueta": (-2, "medio", 1.30)}


def texto_encima(fondo, gris):
    """Tinta o blanco: el que más contraste da sobre ese fondo."""
    return max((TINTA, BLANCO), key=lambda p: contraste(gris[p], fondo))


def acciones(escala, gris, ancla, superficie, direccion):
    """Los roles de acción de un modo, elegidos por contraste.

    Se recorren los peldaños empezando por el más cercano al color de marca, y
    gana el primero que sostenga texto —4.5:1— y se despegue de la superficie
    —3:1—. Una marca oscura se apoya casi en su propio peldaño; una clara se
    corre lo justo. Lo que nunca se mueve es el color de marca.

    `direccion` es hacia dónde refuerza el presionado: más oscuro en modo claro,
    más claro en modo oscuro.
    """
    orden = sorted(PELDAÑOS)
    cercanos = sorted((p for p in orden if p > 0), key=lambda p: abs(p - ancla))

    reposo = texto = None
    for p in cercanos:
        encima = texto_encima(escala[p], gris)
        if (contraste(gris[encima], escala[p]) >= MIN_TEXTO
                and contraste(escala[p], superficie) >= MIN_NO_TEXTO):
            reposo, texto = p, encima
            break
    if reposo is None:  # no le pasa a ningún color real; que no reviente en silencio
        reposo = min(cercanos, key=lambda p: -contraste(escala[p], superficie))
        texto = texto_encima(escala[reposo], gris)

    # El presionado se aparta del reposo sin perder el texto que ya se eligió: el
    # texto del botón NO puede cambiar entre reposo y presionado.
    presionado = reposo
    for salto in (1, 2, -1, -2):
        j = orden.index(reposo) + salto * direccion
        if 0 <= j < len(orden) and contraste(gris[texto], escala[orden[j]]) >= MIN_TEXTO:
            presionado = orden[j]
            break

    # El fondo tenue vive del lado de la superficie, y encima va el peldaño más
    # cercano a la marca que se lea sobre él.
    tenue = 50 if direccion > 0 else 900
    sobre = next((p for p in cercanos
                  if contraste(escala[p], escala[tenue]) >= MIN_TEXTO), None)

    return {
        "accion.reposo":      ("@", reposo),
        "accion.presionado":  ("@", presionado),
        "accion.tenue":       ("@", tenue),
        "accion.sobre-tenue": ("@", sobre) if sobre else ("gris", TINTA if direccion > 0 else BLANCO),
        "texto.sobre-accion": ("gris", texto),
    }


def semanticos(m, modos, prim):
    nom = m["identidad"]["nombre_acento"]
    escala, gris = prim[f"color.{nom}"], prim["color.gris"]
    ancla = ancla_natural(m["identidad"]["acento"])
    t = {}

    for rol, por_modo in ROLES.items():
        t[rol] = {}
        for modo in modos:
            fam, peldaño = por_modo[modo]
            t[rol][modo] = f"{{color.{nom if fam == '@' else fam}.{peldaño}}}"

    for modo in modos:
        direccion = 1 if modo == "claro" else -1
        superficie = gris[ROLES["superficie.base"][modo][1]]
        for rol, (fam, peldaño) in acciones(escala, gris, ancla, superficie, direccion).items():
            t.setdefault(rol, {})[modo] = f"{{color.{nom if fam == '@' else fam}.{peldaño}}}"

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

    # La altura de cada tamaño de control. El inventario declara los nombres —`sm`, `md`,
    # `lg`— y hasta acá nada decía cuánto miden: cada componente lo elegía al dibujarse,
    # que es la forma más silenciosa de no tener escala. Salió a la luz construyendo el
    # primer botón, que es cuando estas cosas aparecen.
    for rol, alto in (m.get("tacto", {}).get("control") or {}).items():
        if rol.startswith("_"):
            continue
        t[f"control.{rol}"] = f"{{alto.{alto}}}"

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

    prim = primitivos(m)
    sem = semanticos(m, modos, prim)
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
    nom, acento = m["identidad"]["nombre_acento"], m["identidad"]["acento"]
    print(f"acento {acento} · entra tal cual en {nom}.{ancla_natural(acento)} · "
          f"modos: {', '.join(modos)}\n")

    # Qué se eligió y por qué. El color de marca no se toca: lo que se decide es
    # dónde se apoya la acción y qué texto va encima — y eso se dice, no se calla.
    ancla = ancla_natural(acento)
    escala, gris = prim[f"color.{nom}"], prim["color.gris"]
    for modo in modos:
        fondo = resolver(sem["accion.reposo"][modo], prim)
        encima = resolver(sem["texto.sobre-accion"][modo], prim)
        print(f"  acción en {modo:7} {sem['accion.reposo'][modo].strip('{}')} = {fondo}"
              f" · texto {'blanco' if encima == '#FFFFFF' else 'tinta'} {encima}"
              f" · {contraste(encima, fondo):.2f}:1")
        # Si la acción no se apoyó en el peldaño de la marca, se dice cuál fue el
        # número que lo impidió. El color sigue en la paleta: lo que se movió es
        # dónde se apoya el botón, no el color.
        if sem["accion.reposo"][modo] != f"{{color.{nom}.{ancla}}}":
            superficie = gris[ROLES["superficie.base"][modo][1]]
            r_sup = contraste(escala[ancla], superficie)
            r_txt = contraste(gris[texto_encima(escala[ancla], gris)], escala[ancla])
            motivo = (f"no se despega de la superficie ({r_sup:.2f}:1, mín {MIN_NO_TEXTO})"
                      if r_sup < MIN_NO_TEXTO
                      else f"no sostiene texto ({r_txt:.2f}:1, mín {MIN_TEXTO})")
            print(f"  {'':17} ↳ {nom}.{ancla} {motivo} — el color queda en la paleta")
    print()

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
