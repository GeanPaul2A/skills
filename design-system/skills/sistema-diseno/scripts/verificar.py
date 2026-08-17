#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar.py — comprueba un sistema de diseño contra las reglas que dice cumplir.

    python3 verificar.py --destino <carpeta>
    python3 verificar.py --destino <carpeta> --regla DS-C03    una sola
    python3 verificar.py --destino <carpeta> --romper DS-T02   prueba el verificador

Es AGNÓSTICO: no sabe nada del producto. Lo que ata el sistema a un producto vive
en proyecto.json, y este guion lo lee de ahí.

Lo que no puede comprobar, lo dice. Una comprobación saltada se REPORTA saltada:
callarla la convierte en un verde que miente.

Solo biblioteca estándar.
"""

import argparse
import json
import pathlib
import re
import sys

MIN_TEXTO, MIN_NO_TEXTO = 4.5, 3.0
CAMPOS_COMPONENTE = ["grupo", "descripcion", "cuando_no", "variantes", "tamanos",
                     "estados", "tokens", "reglas", "interactivo", "espera_datos"]
# El rango de DS-F03 es de TEXTO CORRIDO: párrafos que se leen seguido. Un titular
# con 1.5 se desarma — las líneas dejan de leerse como una unidad. Por eso los roles
# de titular llevan un piso tipográfico, no el rango de lectura.
TEXTO_CORRIDO = {"tipo.cuerpo", "tipo.apoyo"}
INTERLINEADO_CORRIDO = (1.40, 1.60)
INTERLINEADO_PISO = 1.10


# ═══ Color ═══════════════════════════════════════════════════════════════════

def luminancia(h):
    def c(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = (int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return .2126 * c(r) + .7152 * c(g) + .0722 * c(b)


def contraste(a, b):
    x, y = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (x + .05) / (y + .05)


def numero(v):
    """«16px» → 16. Los primitivos guardan la unidad; las comparaciones necesitan el número."""
    if isinstance(v, (int, float)):
        return v
    m = re.match(r"^(-?\d+(?:\.\d+)?)", str(v or ""))
    return float(m.group(1)) if m else None


# ═══ El resultado de una comprobación ════════════════════════════════════════

class R:
    def __init__(self, regla, nombre):
        self.regla, self.nombre = regla, nombre
        self.fallos, self.n, self.saltada = [], 0, None

    def ok(self, cuantos=1):
        self.n += cuantos
        return self

    def mal(self, msg):
        self.fallos.append(msg)
        return self

    def saltar(self, motivo):
        self.saltada = motivo
        return self


# ═══ Carga ═══════════════════════════════════════════════════════════════════

class Sistema:
    def __init__(self, destino):
        self.raiz = pathlib.Path(destino).resolve()
        self.marca = self._json("marca.json", obligatorio=True)
        self.proyecto = self._json("proyecto.json") or {}
        self.prim = self._json("tokens/1-primitivos.json") or {}
        self.sem = self._json("tokens/2-semanticos.json") or {}
        self.comp_tok = self._json("tokens/3-componentes.json") or {}
        self.componentes = (self._json("inventario/componentes.json") or {}).get("componentes", {})
        self.patrones = (self._json("inventario/patrones.json") or {}).get("patrones", {})
        self.plantillas = (self._json("inventario/plantillas.json") or {}).get("plantillas", {})
        self.modos = self.marca["modos"]["activos"] + self.marca["modos"].get("preparados", [])
        self.plataformas = self.proyecto.get("proyecto", {}).get("plataformas", ["movil"])
        # Solo lo usa --romper: sustituye las salidas del disco por unas inventadas,
        # para que las comprobaciones que dependen de lo publicado se puedan probar.
        self.salidas_falsas = None

    def _json(self, rel, obligatorio=False):
        f = self.raiz / rel
        if not f.exists():
            if obligatorio:
                sys.exit(f"falta {f}")
            return None
        return json.loads(f.read_text(encoding="utf-8"))

    def roles(self):
        return {k: v for k, v in self.sem.items() if not k.startswith("_")}

    def resolver(self, alias, modo=None):
        """Sigue la cadena de alias hasta un valor. Devuelve None si se rompe."""
        visto = 0
        v = alias
        while isinstance(v, str) and v.startswith("{") and v.endswith("}"):
            visto += 1
            if visto > 10:
                return None
            ruta = v.strip("{}").split(".")
            for fuente in (self.prim, self.sem, self.comp_tok):
                if ".".join(ruta) in fuente:
                    v = fuente[".".join(ruta)]
                    break
                grupo = fuente.get(".".join(ruta[:-1]))
                if isinstance(grupo, dict) and ruta[-1] in grupo:
                    v = grupo[ruta[-1]]
                    break
                if isinstance(grupo, dict) and ruta[-1].isdigit() and int(ruta[-1]) in grupo:
                    v = grupo[int(ruta[-1])]
                    break
                if isinstance(grupo, list) and ruta[-1].isdigit():
                    v = grupo[int(ruta[-1])]
                    break
            else:
                return None
            if isinstance(v, dict) and modo and modo in v:
                v = v[modo]
        return v


# ═══ Eje A · Tokens ══════════════════════════════════════════════════════════

def a01_tres_niveles(s):
    """DS-T02 · Un componente nunca referencia un primitivo."""
    r = R("DS-T02", "los tres niveles no se colapsan")
    roles = set(s.roles())
    for tok, alias in s.comp_tok.items():
        if tok.startswith("_"):
            continue
        destino = alias.strip("{}") if isinstance(alias, str) else ""
        if destino in roles:
            r.ok()
        else:
            r.mal(f"{tok} → {alias}   no apunta a un rol semántico")
    return r


def a02_alias_resuelven(s):
    """DS-T02 · Toda cadena de alias termina en un valor."""
    r = R("DS-T02", "toda cadena de alias resuelve")
    for nivel, tabla in (("2", s.sem), ("3", s.comp_tok)):
        for tok, v in tabla.items():
            if tok.startswith("_"):
                continue
            for modo in (s.modos if isinstance(v, dict) else [None]):
                val = v.get(modo) if isinstance(v, dict) else v
                if not isinstance(val, str) or not val.startswith("{"):
                    continue
                if s.resolver(val, modo) is None:
                    r.mal(f"nivel {nivel} · {tok}{f' [{modo}]' if modo else ''} → {val}   roto")
                else:
                    r.ok()
    return r


def a03_convenio(s):
    """DS-T04 · Un solo convenio de nombres."""
    r = R("DS-T04", "el convenio de nombres es uno solo")
    patron = re.compile(r"^[a-z0-9]+([.-][a-z0-9]+)*$")
    for tabla in (s.sem, s.comp_tok):
        for tok in tabla:
            if tok.startswith("_"):
                continue
            r.ok() if patron.match(tok) else r.mal(f"{tok}   minúsculas, puntos y guiones")
    return r


def a04_generados(s):
    """DS-T01 · Los tokens son salida, no fuente."""
    r = R("DS-T01", "los tokens están generados, no escritos a mano")
    for f, d in (("1-primitivos", s.prim), ("2-semanticos", s.sem),
                 ("3-componentes", s.comp_tok)):
        if not d:
            r.mal(f"falta tokens/{f}.json")
        elif "_generado_por" not in d:
            r.mal(f"tokens/{f}.json sin marca de generación — ¿se editó a mano?")
        else:
            r.ok()
    return r


def a05_escala_espacio(s):
    """DS-F06 · Ningún valor de espaciado fuera de la escala."""
    r = R("DS-F06", "todo espacio sale de la escala")
    escala = set(s.prim.get("medida", {}).values() if isinstance(s.prim.get("medida"), dict)
                 else s.prim.get("medida", []))
    for tok, v in s.sem.items():
        if not tok.startswith("espacio."):
            continue
        val = s.resolver(v)
        r.ok() if val in escala else r.mal(f"{tok} = {val}   fuera de la escala {sorted(escala)}")
    return r


def a06_tipografia(s):
    """DS-F03 · Cuerpo ≥ 16 px, interlineado entre 1.4 y 1.6."""
    r = R("DS-F03", "el cuerpo cumple el mínimo de accesibilidad")
    cuerpo = s.sem.get("tipo.cuerpo")
    if not cuerpo:
        return r.mal("no existe tipo.cuerpo")
    px = numero(s.resolver(cuerpo["tamaño"]))
    r.ok() if px and px >= 16 else r.mal(f"tipo.cuerpo = {px}   el mínimo es 16px — DS-F03")
    for tok, v in s.sem.items():
        if not tok.startswith("tipo.") or not isinstance(v, dict):
            continue
        il = v.get("interlineado")
        if il is None:
            r.mal(f"{tok} sin interlineado")
        elif tok in TEXTO_CORRIDO:
            lo, hi = INTERLINEADO_CORRIDO
            r.ok() if lo <= il <= hi else r.mal(
                f"{tok} interlineado {il}   el texto corrido va entre {lo} y {hi} — DS-F03")
        elif il < INTERLINEADO_PISO:
            r.mal(f"{tok} interlineado {il}   por debajo del piso {INTERLINEADO_PISO}")
        else:
            r.ok()
    return r


PARES = [
    ("texto sobre superficie",        "texto.principal",    "superficie.base",    MIN_TEXTO),
    ("secundario sobre superficie",   "texto.secundario",   "superficie.base",    MIN_TEXTO),
    ("texto sobre elevada",           "texto.principal",    "superficie.elevada", MIN_TEXTO),
    ("texto sobre hundida",           "texto.principal",    "superficie.hundida", MIN_TEXTO),
    ("sobre-accion sobre acción",     "texto.sobre-accion", "accion.reposo",      MIN_TEXTO),
    ("sobre-accion sobre presionado", "texto.sobre-accion", "accion.presionado",  MIN_TEXTO),
    ("acción sobre superficie",       "accion.reposo",      "superficie.base",    MIN_NO_TEXTO),
    ("sobre-tenue sobre tenue",       "accion.sobre-tenue", "accion.tenue",       MIN_TEXTO),
    ("borde fuerte sobre superficie", "borde.fuerte",       "superficie.base",    MIN_NO_TEXTO),
]


def a07_contraste(s):
    """DS-A02 · Contraste comprobado en TODOS los modos, incluidos los inactivos."""
    r = R("DS-A02", "el contraste cumple AA en todos los modos")
    pares = list(PARES)
    for estado in (k for k in s.marca["estados"] if not k.startswith("_")):
        pares += [(f"{estado} sobre su fondo", f"estado.{estado}",
                   f"estado.{estado}.fondo", MIN_TEXTO),
                  (f"{estado} sobre superficie", f"estado.{estado}",
                   "superficie.base", MIN_TEXTO)]
    for modo in s.modos:
        for etiqueta, a, b, minimo in pares:
            va, vb = s.resolver(f"{{{a}}}", modo), s.resolver(f"{{{b}}}", modo)
            if not (isinstance(va, str) and va.startswith("#")):
                r.mal(f"[{modo}] {etiqueta}: no resuelve {a}")
                continue
            # El fondo se comprueba igual que el texto: sin esto, un fondo que no
            # resuelve revienta el verificador en vez de reportar el fallo.
            if not (isinstance(vb, str) and vb.startswith("#")):
                r.mal(f"[{modo}] {etiqueta}: no resuelve {b}")
                continue
            c = contraste(va, vb)
            r.ok() if c >= minimo else r.mal(f"[{modo}] {etiqueta}: {c:.2f}:1   mínimo {minimo}")
    return r


def a08_forma(s):
    """DS-F07 · El radio completo se reserva a lo que no es un control."""
    r = R("DS-F07", "el radio completo no se usa en controles")
    forma = s.marca["forma"]
    vals = {k: v for k, v in forma.items() if not k.startswith("_")}
    for k, v in vals.items():
        if isinstance(v, (int, float)) and v >= 999:
            r.mal(f"forma.{k} = {v}   radio completo en un rol de control")
        else:
            r.ok()
    orden = ["distintivo", "control", "tarjeta", "contenedor"]
    presentes = [k for k in orden if k in vals]
    series = [vals[k] for k in presentes]
    if series == sorted(series):
        r.ok()
    else:
        r.mal(f"el radio no crece de forma monótona: {dict(zip(presentes, series))}")
    return r


# ═══ Eje B · Componentes ═════════════════════════════════════════════════════

def b01_contrato(s):
    """DS-C01 · Todo componente declara los mismos campos."""
    r = R("DS-C01", "todo componente lleva su contrato completo")
    if not s.componentes:
        return r.saltar("no hay inventario/componentes.json")
    for nombre, c in s.componentes.items():
        faltan = [k for k in CAMPOS_COMPONENTE if k not in c]
        r.ok() if not faltan else r.mal(f"{nombre}: falta {', '.join(faltan)}")
    return r


def b02_foco(s):
    """DS-C02 · Todo interactivo declara su estado de foco."""
    r = R("DS-C02", "todo interactivo declara foco")
    if not s.componentes:
        return r.saltar("no hay inventario")
    for nombre, c in s.componentes.items():
        if not c.get("interactivo"):
            continue
        r.ok() if "foco" in c.get("estados", []) else r.mal(f"{nombre}: interactivo sin 'foco'")
    return r


def b03_datos(s):
    """DS-C03 · Lo que espera datos declara carga, vacío y error."""
    r = R("DS-C03", "lo que espera datos declara sus tres estados")
    if not s.componentes:
        return r.saltar("no hay inventario")
    for nombre, c in s.componentes.items():
        if not c.get("espera_datos"):
            continue
        d = c.get("datos")
        if not isinstance(d, dict):
            r.mal(f"{nombre}: espera datos y no declara 'datos'")
            continue
        for est in ("cargando", "vacio", "error"):
            v = d.get(est, "")
            if not v:
                r.mal(f"{nombre}.datos: falta '{est}'")
            elif v.strip().startswith("no aplica") and "—" not in v and "-" not in v:
                r.mal(f"{nombre}.datos.{est}: dice «no aplica» sin decir por qué")
            else:
                r.ok()
    return r


def b04_privados(s):
    """DS-C04 · Los auxiliares se prefijan con punto y no se publican."""
    r = R("DS-C04", "los auxiliares llevan punto y no se publican")
    if not s.componentes:
        return r.saltar("no hay inventario")
    for nombre, c in s.componentes.items():
        priv, punto = c.get("privado", False), nombre.startswith(".")
        r.ok() if priv == punto else r.mal(
            f"{nombre}: privado={priv} pero {'lleva' if punto else 'no lleva'} punto")
    return r


def b05_descripcion(s):
    """DS-C05 · Cada componente dice cuándo usarlo y cuándo no."""
    r = R("DS-C05", "cada componente dice cuándo NO usarlo")
    if not s.componentes:
        return r.saltar("no hay inventario")
    for nombre, c in s.componentes.items():
        for campo in ("descripcion", "cuando_no"):
            v = (c.get(campo) or "").strip()
            r.ok() if len(v) >= 20 else r.mal(f"{nombre}.{campo}: vacío o demasiado corto")
    return r


def b06_hover(s):
    """DS-C10 · 'hover' no se declara para móvil."""
    r = R("DS-C10", "no se declara 'hover' donde no hay puntero")
    if not s.componentes:
        return r.saltar("no hay inventario")
    if set(s.plataformas) - {"movil"}:
        return r.saltar(f"hay plataforma con puntero: {', '.join(s.plataformas)}")
    for nombre, c in s.componentes.items():
        estados = [e.lower() for e in c.get("estados", [])]
        if any(e in ("hover", "sobrevuelo") for e in estados):
            r.mal(f"{nombre}: declara 'hover' y el producto es solo móvil")
        else:
            r.ok()
    return r


def b07_tokens_existen(s):
    """DS-T02 · Toda parte de un componente mapea a un rol semántico que existe."""
    r = R("DS-T02", "las partes mapean a roles que existen")
    if not s.componentes:
        return r.saltar("no hay inventario")
    roles = set(s.roles())
    for nombre, c in s.componentes.items():
        for parte, rol in (c.get("tokens") or {}).items():
            r.ok() if rol in roles else r.mal(f"{nombre}.{parte} → {rol}   no existe ese rol")
    return r


def b08_accesibilidad(s):
    """DS-C02 · Todo interactivo declara su contrato de accesibilidad: rol, teclado y lector."""
    r = R("DS-C02", "todo interactivo declara rol, teclado y lector")
    if not s.componentes:
        return r.saltar("no hay inventario")
    for nombre, c in s.componentes.items():
        if not c.get("interactivo"):
            continue
        a = c.get("accesibilidad")
        if not isinstance(a, dict):
            r.mal(f"{nombre}: interactivo sin 'accesibilidad' — falta rol, teclado y lector")
            continue
        for campo in ("rol", "teclado", "lector"):
            v = (a.get(campo) or "").strip()
            r.ok() if v else r.mal(f"{nombre}.accesibilidad: falta '{campo}'")
    return r


def b09_props(s):
    """DS-C05 · Las props, si existen, declaran nombre, tipo y valor por omisión."""
    r = R("DS-C05", "toda prop declara nombre, tipo y valor por omisión")
    if not s.componentes:
        return r.saltar("no hay inventario")
    con_props = [(n, c) for n, c in s.componentes.items() if c.get("props")]
    if not con_props:
        return r.saltar("ningún componente declara props todavía")
    for nombre, c in con_props:
        for p in c.get("props"):
            if not isinstance(p, dict):
                r.mal(f"{nombre}.props: entrada sin forma de objeto")
                continue
            for campo in ("nombre", "tipo", "default"):
                if campo not in p:
                    r.mal(f"{nombre}.props: falta '{campo}'")
                else:
                    r.ok()
    return r


def b10_codigo(s):
    """DS-T07 · El ejemplo de código no lleva valores en crudo: hex ni píxeles sueltos."""
    r = R("DS-T07", "el ejemplo de código no lleva valores en crudo")
    if not s.componentes:
        return r.saltar("no hay inventario")
    con_codigo = [(n, c) for n, c in s.componentes.items() if c.get("ejemplo_codigo")]
    if not con_codigo:
        return r.saltar("ningún componente declara ejemplo_codigo todavía")
    crudo = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b\d+px\b")
    for nombre, c in con_codigo:
        m = crudo.search(c.get("ejemplo_codigo") or "")
        r.ok() if not m else r.mal(f"{nombre}.ejemplo_codigo: valor en crudo «{m.group(0)}» — DS-T07")
    return r


# ═══ Eje C · Patrones y plantillas ═══════════════════════════════════════════

# Un patrón declara de dónde salen sus datos y cómo se dispone en DOS formas, y las dos
# valen. La propia: 'dominio' con sus 'tablas', 'lee_tambien' con lo que lee de otros
# dominios, y 'plantilla' con 'componentes' — es la de un patrón de una sola pantalla, y
# distingue la tabla propia de la que solo se consulta. La genérica: 'datos' y 'pasos' —
# es la que necesita un flujo de varios pasos, donde cada paso lleva su plantilla.
#
# Leer solo una de las dos es lo que hacía que estas comprobaciones iteraran una lista
# vacía y salieran en verde sin comprobar nada.

def entidades_citadas(p):
    """Las entidades que un patrón nombra, en cualquiera de las dos formas."""
    dom = p.get("dominio")
    tablas = p.get("tablas") or []
    ent = [f"{dom}.{t}" for t in tablas] if dom else list(tablas)
    ent += list(p.get("lee_tambien") or {})
    ent += (p.get("datos") or {}).get("entidades") or []
    for paso in pasos_de(p):
        ent += (paso.get("datos") or {}).get("entidades") or []
    return ent


def campos_citados(p):
    """Los campos que un patrón nombra. Un patrón puede no citar ninguno: los campos
    son cosa de la pantalla, no del patrón."""
    campos = list((p.get("datos") or {}).get("campos") or [])
    campos += list(p.get("campos") or [])
    for paso in pasos_de(p):
        campos += (paso.get("datos") or {}).get("campos") or []
    return campos


def reglas_citadas(p):
    """Las reglas de negocio que un patrón cita, en cualquiera de las dos formas."""
    reglas = list(p.get("reglas") or [])
    reglas += (p.get("datos") or {}).get("reglas") or []
    for paso in pasos_de(p):
        reglas += (paso.get("datos") or {}).get("reglas") or []
    return reglas


def pasos_de(p):
    """Los pasos del patrón. Cuando declara su plantilla arriba, es un paso solo."""
    pasos = [x for x in (p.get("pasos") or []) if isinstance(x, dict)]
    if pasos:
        return pasos
    if p.get("plantilla"):
        return [{"plantilla": p["plantilla"], "componentes": p.get("componentes") or []}]
    return []


def c01_patron_contrato(s):
    """DS-P01 · Todo patrón declara para qué es, sus estados, de dónde salen sus datos
    y cómo se dispone. Las dos últimas admiten las dos formas."""
    r = R("DS-P01", "todo patrón declara de dónde salen sus datos")
    if not s.patrones:
        return r.saltar("no hay inventario/patrones.json")
    exigencias = (("un propósito", lambda p: p.get("proposito")),
                  ("sus estados", lambda p: p.get("estados")),
                  ("de dónde salen sus datos", entidades_citadas),
                  ("cómo se dispone", lambda p: p.get("plantilla") or p.get("pasos")))
    for nombre, p in s.patrones.items():
        for que, lee in exigencias:
            r.ok() if lee(p) else r.mal(f"{nombre}: no declara {que}")
    return r


def c02_patron_fallo(s):
    """DS-P03 · Todo patrón enumera estados, y al menos uno es un fallo."""
    r = R("DS-P03", "todo patrón contempla que algo salga mal")
    if not s.patrones:
        return r.saltar("no hay patrones")
    # "sin-" y "sin " son la misma señal escrita de dos maneras. Buscar solo la del
    # espacio da fallos falsos contra estados como 'sin-conexion' o 'sin-destino'.
    señales = ("error", "fallo", "rechaz", "sin-", "sin ", "vencid", "expir",
               "cancel", "vacio", "vacío")
    for nombre, p in s.patrones.items():
        estados = p.get("estados") or {}
        claves = list(estados) if isinstance(estados, dict) else list(estados)
        if any(any(x in str(k).lower() for x in señales) for k in claves):
            r.ok()
        else:
            r.mal(f"{nombre}: ningún estado de fallo entre {claves}")
    return r


def c03_plantilla_admite(s):
    """Los componentes que un patrón usa caben en la plantilla que declara."""
    r = R("DS-C01", "cada patrón cabe en la plantilla que declara")
    if not (s.patrones and s.plantillas):
        falta = " y ".join(x for x, hay in (("patrones", s.patrones),
                                           ("plantillas", s.plantillas)) if not hay)
        return r.saltar(f"no hay {falta}")
    for nombre, p in s.patrones.items():
        for paso in pasos_de(p):
            if not isinstance(paso, dict):
                continue
            pl = paso.get("plantilla")
            if not pl:
                continue
            if pl not in s.plantillas:
                r.mal(f"{nombre}: plantilla '{pl}' no existe")
                continue
            admite = set()
            for z in s.plantillas[pl].get("zonas", []):
                admite |= set(z.get("admite", []))
            for comp in paso.get("componentes") or []:
                r.ok() if comp in admite else r.mal(
                    f"{nombre} → {pl}: '{comp}' no cabe en ninguna zona")
    return r


def c04_tabulacion(s):
    """DS-A07 · Cuando el orden de foco no sigue al visual, se documenta."""
    r = R("DS-A07", "las plantillas documentan su orden de foco")
    if not s.plantillas:
        return r.saltar("no hay plantillas")
    for nombre, p in s.plantillas.items():
        orden = (p.get("orden_tabulacion") or "").lower()
        if not orden:
            r.mal(f"{nombre}: sin 'orden_tabulacion'")
        elif "no coincide" in orden or "atrapado" in orden:
            r.ok() if p.get("_por_que_no_coincide") else r.mal(
                f"{nombre}: el foco diverge del visual y no explica por qué")
        else:
            r.ok()
    return r


# ═══ Eje D · Contra el modelo del producto ═══════════════════════════════════

class Modelo:
    """Lee el modelo del producto según lo que proyecto.json declare. No sabe de dominios."""

    def __init__(self, s):
        cfg = s.proyecto.get("modelo_de_datos") or {}
        self.tipo = cfg.get("tipo")
        self.motivo = None
        self.entidades, self.reglas = {}, set()
        if not self.tipo:
            self.motivo = "proyecto.json declara 'modelo_de_datos.tipo': null"
            return
        raiz = (s.raiz / cfg.get("raiz", "")).resolve()
        if not raiz.exists():
            self.motivo = f"la raíz del modelo no existe: {raiz}"
            return
        self._entidades(raiz, cfg)
        self._reglas(raiz, cfg)

    def _dominios(self, raiz, cfg):
        d = cfg.get("dominios", {})
        if d.get("descubrir") == "plano":
            return [""]
        excluir = set(d.get("excluir", []))
        return sorted(p.name for p in raiz.iterdir()
                      if p.is_dir() and not p.name.startswith(".") and p.name not in excluir)

    def _entidades(self, raiz, cfg):
        e = cfg.get("entidades", {})
        ext, fmt = e.get("extension", ".csv"), e.get("formato", "csv-cabecera")
        for dom in self._dominios(raiz, cfg):
            carpeta = raiz / e.get("ruta", "").replace("{dominio}", dom)
            if not carpeta.exists():
                continue
            for f in sorted(carpeta.glob(f"*{ext}")):
                campos = self._campos(f, fmt)
                if campos is not None:
                    self.entidades[f"{dom}.{f.stem}" if dom else f.stem] = campos

    @staticmethod
    def _campos(f, fmt):
        try:
            if fmt == "csv-cabecera":
                linea = f.read_text(encoding="utf-8").splitlines()[0]
                return set(c.strip().strip('"') for c in linea.split(","))
            if fmt == "json-esquema":
                d = json.loads(f.read_text(encoding="utf-8"))
                return set(d.get("properties", d).keys())
            if fmt == "sql-ddl":
                txt = f.read_text(encoding="utf-8")
                return set(re.findall(r"^\s{2,}([a-z_][a-z0-9_]*)\s+[A-Z]", txt, re.M))
        except (OSError, ValueError, IndexError):
            return None
        return None

    def _reglas(self, raiz, cfg):
        c = cfg.get("reglas") or {}
        ruta, patron = c.get("ruta"), c.get("patron")
        if not (ruta and patron):
            return
        rx = re.compile(patron, re.M)
        for dom in self._dominios(raiz, cfg):
            f = raiz / ruta.replace("{dominio}", dom)
            if f.exists():
                plantilla = c.get("cita", "{dominio}.{regla}")
                for m in rx.finditer(f.read_text(encoding="utf-8")):
                    self.reglas.add(plantilla.replace("{dominio}", dom).replace("{regla}", m.group(1)))


def d01_entidades(s, mod):
    """DS-P02 · Ningún patrón nombra una entidad que el producto no tiene."""
    r = R("DS-P02", "las entidades citadas existen en el modelo")
    if mod.motivo:
        return r.saltar(mod.motivo)
    if not s.patrones:
        return r.saltar("no hay patrones")
    for nombre, p in s.patrones.items():
        for ent in (p.get("datos") or {}).get("entidades", []):
            r.ok() if ent in mod.entidades else r.mal(f"{nombre}: '{ent}' no existe en el modelo")
    return r


def d02_campos(s, mod):
    """DS-P02 · Ningún dato mostrado carece de campo que lo respalde."""
    r = R("DS-P02", "los campos citados existen en su entidad")
    if mod.motivo:
        return r.saltar(mod.motivo)
    if not s.patrones:
        return r.saltar("no hay patrones")
    for nombre, p in s.patrones.items():
        for cita in (p.get("datos") or {}).get("campos", []):
            if "." not in cita:
                r.mal(f"{nombre}: '{cita}' no dice de qué entidad es")
                continue
            ent, campo = cita.rsplit(".", 1)
            if ent not in mod.entidades:
                r.mal(f"{nombre}: '{ent}' no existe")
            elif campo not in mod.entidades[ent]:
                r.mal(f"{nombre}: '{ent}' no tiene el campo '{campo}'")
            else:
                r.ok()
    return r


def d03_reglas(s, mod):
    """DS-P01 · Las reglas de negocio citadas existen."""
    r = R("DS-P01", "las reglas de negocio citadas existen")
    if mod.motivo:
        return r.saltar(mod.motivo)
    if not mod.reglas:
        return r.saltar("proyecto.json no declara dónde viven las reglas")
    for nombre, p in s.patrones.items():
        for cita in (p.get("datos") or {}).get("reglas", []):
            r.ok() if cita in mod.reglas else r.mal(f"{nombre}: la regla '{cita}' no existe")
    return r


# ═══ Eje A · Tokens · lo que faltaba ═════════════════════════════════════════

def a09_estilos_agrupan(s):
    """DS-F04 · Los estilos de texto se nombran para que agrupen."""
    r = R("DS-F04", "todo estilo de texto agrupa bajo un prefijo")
    tipograficos = {k: v for k, v in s.roles().items()
                    if isinstance(v, dict) and {"tamaño", "peso"} & set(v)}
    if not tipograficos:
        return r.saltar("el sistema no declara estilos de texto")
    for k in tipograficos:
        if "." not in k:
            r.mal(f"{k}: estilo de texto sin prefijo de grupo — queda suelto en la lista")
        elif k.split(".")[0] != "tipo":
            r.mal(f"{k}: agrupa bajo '{k.split('.')[0]}' y no bajo 'tipo'")
        else:
            r.ok()
    return r


def a10_color_medible(s):
    """DS-F05 · Ningún par texto/fondo entra sin pasar el comprobador de contraste.

    Lo que se comprueba acá no es el contraste —eso es DS-A02— sino que **todo rol de
    color resuelva a un valor medible en todos los modos**. Un rol que no resuelve se
    saltea la medición en silencio: no falla, simplemente no se mide.
    """
    r = R("DS-F05", "todo rol de color resuelve a un valor medible")
    coloridos = [k for k, v in s.roles().items()
                 if isinstance(v, dict) and set(v) & set(s.modos)]
    if not coloridos:
        return r.saltar("el sistema no declara roles de color por modo")
    for k in coloridos:
        for modo in s.modos:
            v = s.resolver(f"{{{k}}}", modo)
            if isinstance(v, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
                r.ok()
            else:
                r.mal(f"{k} en {modo}: no resuelve a color ({v!r}) — escapa a la medición")
    return r


def a11_elevacion(s):
    """DS-F08 · La elevación se expresa solo con sombra difusa."""
    r = R("DS-F08", "la elevación es solo sombra difusa")
    elev = {k: v for k, v in (s.marca.get("elevacion") or {}).items()
            if not k.startswith("_")}
    if not elev:
        return r.saltar("la marca no declara elevación")
    # 'x' e 'y' son desplazamiento y siguen siendo sombra difusa. Expansión e interior
    # no se pueden implementar de forma realista en código — [B2, cap. 3].
    PROHIBIDO = {"expansion", "spread", "interior", "inset"}
    for nivel, cfg in elev.items():
        if not isinstance(cfg, dict):
            r.mal(f"elevacion.{nivel}: no es un objeto")
        elif PROHIBIDO & set(cfg):
            sobra = ", ".join(sorted(PROHIBIDO & set(cfg)))
            r.mal(f"elevacion.{nivel}: lleva {sobra} — solo se admite sombra difusa")
        elif not cfg.get("desenfoque"):
            r.mal(f"elevacion.{nivel}: sin desenfoque, no es una sombra difusa")
        else:
            r.ok()
    return r


def a12_peso_numero(s):
    """DS-T09 · El peso tipográfico se guarda como número, no como nombre."""
    r = R("DS-T09", "el peso tipográfico es un número")
    pesos = s.prim.get("peso")
    if not isinstance(pesos, dict) or not pesos:
        return r.saltar("el sistema no declara pesos tipográficos")
    for nombre, valor in pesos.items():
        if isinstance(valor, bool) or not isinstance(valor, int):
            r.mal(f"peso.{nombre} = {valor!r}: es un nombre, no un número")
        elif not 100 <= valor <= 950:
            r.mal(f"peso.{nombre} = {valor}: fuera del rango 100–950")
        else:
            r.ok()
    return r


def a13_familia_exacta(s):
    """DS-X05 · La familia se guarda como cadena exacta, no como pila."""
    r = R("DS-X05", "la familia tipográfica es una cadena exacta")
    tipo = s.marca.get("tipografia") or {}
    familias = {k: v for k, v in tipo.items()
                if k.startswith("familia") and not k.startswith("_") and v is not None}
    if not familias:
        return r.saltar("la marca no declara familia tipográfica")
    for k, v in familias.items():
        if not isinstance(v, str) or not v.strip():
            r.mal(f"tipografia.{k} = {v!r}: no es una cadena con contenido")
        elif "," in v:
            r.mal(f"tipografia.{k} = {v!r}: es una pila, no una familia — el puente no la resuelve")
        elif v != v.strip():
            r.mal(f"tipografia.{k} = {v!r}: lleva espacios al borde")
        else:
            r.ok()
    return r


def a14_valor_repetido(s):
    """DS-T08 · Un valor merece token si aparece en tres o más lugares."""
    r = R("DS-T08", "ningún valor literal se repite sin token")
    literales = {}
    for fuente, nivel in ((s.sem, "2"), (s.comp_tok, "3")):
        for k, v in fuente.items():
            if k.startswith("_"):
                continue
            campos = v if isinstance(v, dict) else {None: v}
            for clave, val in campos.items():
                if not isinstance(val, str) or (val.startswith("{") and val.endswith("}")):
                    continue
                if re.fullmatch(r"#[0-9A-Fa-f]{3,8}|\d+(px|rem|%)", val):
                    donde = f"{k}.{clave}" if clave else k
                    literales.setdefault(val, []).append(f"{donde} (nivel {nivel})")
    if not literales:
        return r.ok()
    for val, donde in sorted(literales.items()):
        if len(donde) >= 3:
            r.mal(f"{val} aparece {len(donde)} veces sin token: {', '.join(donde[:3])}…")
        else:
            r.ok()
    return r


def salidas_publicadas(s):
    """Los archivos ya publicados, como pares (nombre, contenido).

    Pasa por acá para que `--romper` pueda inyectar una salida inventada y las dos
    comprobaciones que dependen del disco se puedan probar de verdad, con su lógica
    real corriendo sobre el contenido inyectado.
    """
    if s.salidas_falsas is not None:
        return s.salidas_falsas
    raiz = s.raiz / "salidas"
    if not raiz.is_dir():
        return []
    fuera = []
    for f in sorted(raiz.rglob("*")):
        if f.is_file() and f.suffix in (".css", ".json", ".swift", ".xml"):
            try:
                fuera.append((str(f.relative_to(raiz)), f.read_text(encoding="utf-8")))
            except (OSError, UnicodeDecodeError):
                fuera.append((str(f.relative_to(raiz)), ""))
    return fuera


def a15_salidas_generadas(s):
    """DS-X01 · La fuente de verdad es el JSON; lo demás son salidas."""
    r = R("DS-X01", "toda salida se declara generada, no fuente")
    archivos = salidas_publicadas(s)
    if not archivos:
        return r.saltar("todavía no se publicó ninguna salida")
    for nombre, contenido in archivos:
        cabeza = contenido[:400].lower()
        if "generado" in cabeza or "_generado_por" in cabeza:
            r.ok()
        else:
            r.mal(f"salidas/{nombre}: no se declara generada — alguien la va a editar a mano")
    return r


def a16_movimiento_reducido(s):
    """DS-A09 · Todo movimiento tiene alternativa reducida."""
    r = R("DS-A09", "el movimiento declara alternativa reducida")
    css = [(n, c) for n, c in salidas_publicadas(s) if n.endswith(".css")]
    if not css:
        return r.saltar("todavía no se publicó el CSS donde vive el movimiento")
    for nombre, contenido in css:
        if not re.search(r"transition|animation", contenido):
            r.ok()
        elif "prefers-reduced-motion" in contenido:
            r.ok()
        else:
            r.mal(f"salidas/{nombre}: declara movimiento y no lleva prefers-reduced-motion")
    return r


# ═══ Eje B · Componentes · lo que faltaba ════════════════════════════════════

def b11_espacio_escala(s):
    """DS-L02 · Espacio y relleno salen de la escala."""
    r = R("DS-L02", "todo relleno de componente sale de la escala")
    if not s.componentes:
        return r.saltar("no hay inventario")
    escala = {str(v).replace("px", "") for v in (s.prim.get("medida") or {}).values()}
    if not escala:
        return r.saltar("el sistema no declara escala de medida")
    # 'relleno' es ambiguo en castellano: es el padding de una caja y también el fill
    # de una forma. Solo se mide lo que resuelve a una medida; lo que resuelve a un
    # color es un relleno de pintura y no le toca esta regla.
    ESPACIALES = ("relleno", "espacio", "hueco", "margen", "separacion")
    mirados = 0
    for nombre, c in s.componentes.items():
        for clave, alias in (c.get("tokens") or {}).items():
            if not any(p in clave for p in ESPACIALES):
                continue
            crudo = alias if str(alias).startswith("{") else "{" + str(alias) + "}"
            v = s.resolver(crudo)
            if isinstance(v, (dict, list)) or (isinstance(v, str) and v.startswith("#")):
                continue
            mirados += 1
            if v is None:
                r.mal(f"{nombre}.{clave}: '{alias}' no resuelve")
            elif str(v).replace("px", "") not in escala:
                r.mal(f"{nombre}.{clave} = {v}: fuera de la escala de espaciado")
            else:
                r.ok()
    if not mirados:
        return r.saltar("ningún componente declara relleno o espacio")
    return r


def b12_etiqueta(s):
    """DS-A04 · Todo campo lleva etiqueta persistente."""
    r = R("DS-A04", "todo campo declara etiqueta persistente")
    entradas = {n: c for n, c in s.componentes.items()
                if c.get("grupo") == "entrada" and not n.startswith(".")}
    if not entradas:
        return r.saltar("el inventario no declara componentes de entrada")
    for nombre, c in entradas.items():
        etiqueta = str((c.get("accesibilidad") or {}).get("etiqueta") or "").strip()
        # Que el marcador NO haga de etiqueta no se puede leer de la prosa sin
        # equivocarse. Lo que sí se comprueba: que el campo exista, y que no se haya
        # rellenado con el nombre del antipatrón.
        if not etiqueta:
            r.mal(f"{nombre}: no declara 'etiqueta' — sin ella el marcador termina haciendo de etiqueta")
        elif etiqueta.lower() in ("marcador", "placeholder", "el marcador", "—", "-"):
            r.mal(f"{nombre}: su etiqueta es «{etiqueta}» — el marcador desaparece al escribir")
        else:
            r.ok()
    return r


def b13_icono_alt(s):
    """DS-A06 · Todo icono con significado lleva texto alternativo de función."""
    r = R("DS-A06", "todo icono con significado declara su alternativo")
    con_icono = {n: c for n, c in s.componentes.items() if "icono" in n}
    if not con_icono:
        return r.saltar("el inventario no declara componentes con icono")
    for nombre, c in con_icono.items():
        if c.get("privado") or nombre.startswith("."):
            # Un auxiliar no se publica y no lo anuncia nadie — DS-C04.
            continue
        lector = str((c.get("accesibilidad") or {}).get("lector", "")).lower()
        if not lector:
            r.mal(f"{nombre}: sin 'lector' — un icono sin alternativo no comunica su función")
        elif not any(p in lector for p in ("alternativo", "etiqueta", "anuncia")):
            r.mal(f"{nombre}: su 'lector' no nombra el texto alternativo de función")
        else:
            r.ok()
    return r


def b14_region_viva(s):
    """DS-A10 · Los cambios dinámicos se anuncian con región en vivo."""
    r = R("DS-A10", "lo que cambia solo declara región en vivo")
    # No alcanza con esperar datos: un avatar que carga su foto no anuncia nada. Lo que
    # tiene que anunciarse es el componente cuyo contenido CAMBIA en el sitio — el que
    # declara 'cargando' o 'error' y después se rellena.
    dinamicos = {n: c for n, c in s.componentes.items()
                 if c.get("espera_datos") and not n.startswith(".")
                 and {"cargando", "error"} & set(c.get("estados") or [])}
    if not dinamicos:
        return r.saltar("ningún componente declara carga o error en el sitio")
    for nombre, c in dinamicos.items():
        vivo = (c.get("accesibilidad") or {}).get("vivo")
        if not vivo:
            r.mal(f"{nombre}: cambia en el sitio y no declara 'vivo' — el cambio pasa en silencio")
        else:
            r.ok()
    return r


def b15_nombre_concepto(s):
    """DS-H03 · El nombre de un componente deriva del concepto que representa."""
    r = R("DS-H03", "el nombre nombra el concepto, no el aspecto")
    if not s.componentes:
        return r.saltar("no hay inventario")
    ASPECTO = ("azul", "rojo", "verde", "amarillo", "naranja", "gris", "negro", "blanco",
               "grande", "pequeno", "pequeño", "chico", "redondo", "cuadrado",
               "izquierda", "derecha", "arriba", "abajo",
               "nuevo", "viejo", "final", "copia", "temp", "prueba")
    for nombre, c in s.componentes.items():
        base = nombre.lstrip(".")
        malas = [p for p in ASPECTO if p in base.lower()]
        if malas:
            r.mal(f"{nombre}: '{malas[0]}' describe su aspecto, no su concepto")
        elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", base):
            r.mal(f"{nombre}: no sigue el convenio kebab-case del sistema")
        else:
            r.ok()
    return r


# ═══ Registro ════════════════════════════════════════════════════════════════

EJES = [
    ("Tokens", [a01_tres_niveles, a02_alias_resuelven, a03_convenio, a04_generados,
                a05_escala_espacio, a06_tipografia, a07_contraste, a08_forma,
                a09_estilos_agrupan, a10_color_medible, a11_elevacion,
                a12_peso_numero, a13_familia_exacta, a14_valor_repetido,
                a15_salidas_generadas, a16_movimiento_reducido]),
    ("Componentes", [b01_contrato, b02_foco, b03_datos, b04_privados,
                     b05_descripcion, b06_hover, b07_tokens_existen,
                     b08_accesibilidad, b09_props, b10_codigo,
                     b11_espacio_escala, b12_etiqueta, b13_icono_alt,
                     b14_region_viva, b15_nombre_concepto]),
    ("Patrones y plantillas", [c01_patron_contrato, c02_patron_fallo,
                               c03_plantilla_admite, c04_tabulacion]),
    ("Contra el modelo del producto", [d01_entidades, d02_campos, d03_reglas]),
]


# ═══ El error inyectado ══════════════════════════════════════════════════════

def primera(tabla):
    """La primera clave de verdad. Las que empiezan con guion bajo son notas, no tokens."""
    return next(k for k in tabla if not str(k).startswith("_"))


def peldaño(escala, n):
    """La clave tal como está guardada. En JSON los peldaños son texto, no entero."""
    return n if n in escala else str(n)


def juzgar(regla, resultados, fallos_ajenos):
    """El veredicto es de la regla que se rompió, no del total.

    Un fallo de otra comprobación no prueba nada: si el veredicto mira el total, una
    comprobación rota da verde porque falló su vecina. Y una comprobación saltada no
    se puede probar — no es un verde ni un rojo, es una prueba que no corrió.
    """
    if fallos_ajenos:
        print(f"\n   ({fallos_ajenos} fallos de otras reglas, ajenos a la inyección)")

    if not resultados:
        print(f"\n⚠  ninguna comprobación lleva la regla {regla}: no hay nada que probar")
        return 2

    fallaron = [r for r in resultados if r.fallos]
    if fallaron:
        print(f"\n✓  el error inyectado en {regla} lo detectó «{fallaron[0].nombre}»")
        return 0

    saltadas = [r for r in resultados if r.saltada]
    if len(saltadas) == len(resultados):
        print(f"\n⚠  no se pudo probar {regla}: su comprobación está saltada "
              f"— {saltadas[0].saltada}")
        print("   No es un verde ni un rojo: es una prueba que no corrió.")
        return 2

    print(f"\n✗  el error inyectado en {regla} PASÓ SIN DETECTARSE "
          f"— la comprobación no sirve")
    return 1


def romper(s, regla):
    """Mete un error a propósito, en memoria. Una comprobación que nunca falló no está probada."""
    roles = list(s.roles())
    espacios = [k for k in s.sem if k.startswith("espacio.")]

    def patron_manco(falta):
        """Un patrón al que le falta justo lo que la regla exige.

        Se inventa acá a propósito: sin él, un sistema sin patrones no puede probar
        nunca estas dos comprobaciones — y quedarían sin usar para siempre.
        """
        p = {"proposito": "probar el verificador", "pasos": [], "estados": {"entrada": "x"},
             "datos": {"entidades": []}}
        p.pop(falta, None) if falta else p.__setitem__("estados", {"entrada": "x", "exito": "y"})
        s.patrones["patron-de-prueba"] = p

    daños = {
        "DS-T02": lambda: s.comp_tok.__setitem__(primera(s.comp_tok), "{color.gris.600}"),
        "DS-T04": lambda: s.sem.__setitem__("Rol_Mal_Escrito", s.sem[roles[0]]),
        "DS-T01": lambda: s.prim.pop("_generado_por", None),
        "DS-F03": lambda: s.sem["tipo.cuerpo"].__setitem__("tamaño", "{letra.12}"),
        "DS-A02": lambda: s.prim["color.gris"].__setitem__(
            peldaño(s.prim["color.gris"], 900), "#F0F0F0"),
        "DS-F07": lambda: s.marca["forma"].__setitem__("control", 9999),
        "DS-C01": lambda: next(iter(s.componentes.values())).pop("cuando_no", None),
        # DS-C02 y DS-C05 llevan DOS comprobaciones (la original y la de documentación).
        # Romper ambas dimensiones de un golpe prueba las dos.
        "DS-C02": lambda: [c["estados"].remove("foco") or c.pop("accesibilidad", None)
                           for c in s.componentes.values()
                           if c.get("interactivo") and "foco" in c.get("estados", [])][:1],
        "DS-C03": lambda: [c.pop("datos", None)
                           for c in s.componentes.values() if c.get("espera_datos")][:1],
        "DS-C04": lambda: s.componentes.__setitem__(
            "impostor", dict(next(iter(s.componentes.values())), privado=True)),
        "DS-C05": lambda: (next(iter(s.componentes.values())).__setitem__("cuando_no", "no"),
                           [p.pop("tipo", None) for c in s.componentes.values()
                            for p in c.get("props", [])]),
        "DS-T07": lambda: [c.__setitem__("ejemplo_codigo", "color:#F00; 12px")
                           for c in s.componentes.values() if c.get("ejemplo_codigo")][:1],
        "DS-P02": lambda: (s.patrones and next(iter(s.patrones.values()))
                           .setdefault("datos", {}).setdefault("entidades", [])
                           .append("entidad.que.no.existe")),
        "DS-F06": lambda: s.sem.__setitem__(espacios[0] if espacios else "espacio.colado", 13),
        "DS-A07": lambda: next(iter(s.plantillas.values())).pop("orden_tabulacion", None),
        "DS-C10": lambda: (s.__setattr__("plataformas", ["movil"]),
                           next(iter(s.componentes.values()))
                           .setdefault("estados", []).append("hover")),
        "DS-P01": lambda: patron_manco("datos"),
        "DS-P03": lambda: patron_manco(None),
        "DS-F04": lambda: s.sem.__setitem__(
            "cuerpoGrande", {"tamaño": "{letra.16}", "peso": "{peso.regular}"}),
        "DS-F05": lambda: s.sem[next(k for k, v in s.roles().items()
                                     if isinstance(v, dict) and set(v) & set(s.modos))
                                ].__setitem__(s.modos[0], "{color.que.no.existe}"),
        "DS-F08": lambda: next(v for k, v in s.marca["elevacion"].items()
                               if not k.startswith("_")).__setitem__("expansion", 4),
        "DS-T09": lambda: s.prim["peso"].__setitem__(
            next(iter(s.prim["peso"])), "semibold"),
        "DS-X05": lambda: s.marca["tipografia"].__setitem__(
            "familia", "Inter, Helvetica, sans-serif"),
        "DS-T08": lambda: [s.comp_tok.__setitem__(f"colado.{i}", "#BADA55")
                           for i in range(3)],
        "DS-L02": lambda: next(c for c in s.componentes.values()
                               if any("relleno" in k or "espacio" in k
                                      for k in (c.get("tokens") or {})))["tokens"
                          ].__setitem__("relleno", "{medida.13}"),
        "DS-A04": lambda: [(c.pop("accesibilidad", None), c.__setitem__("props", []))
                           for n, c in s.componentes.items()
                           if c.get("grupo") == "entrada"][:1],
        "DS-A06": lambda: [c.pop("accesibilidad", None)
                           for n, c in s.componentes.items()
                           if "icono" in n and not n.startswith(".")][:1],
        "DS-A10": lambda: [c.pop("accesibilidad", None)
                           for c in s.componentes.values() if c.get("espera_datos")][:1],
        "DS-H03": lambda: s.componentes.__setitem__(
            "boton-azul", dict(next(iter(s.componentes.values())))),
        # Estas dos leen lo publicado. Se les inyecta una salida inventada para que su
        # lógica real corra sobre contenido que sí incumple.
        "DS-X01": lambda: s.__setattr__(
            "salidas_falsas", [("sistema.css", ":root{--accion:#3A45C9}")]),
        "DS-A09": lambda: s.__setattr__(
            "salidas_falsas", [("sistema.css", "/* generado */\na{transition:all .2s}")]),
    }
    if regla not in daños:
        sys.exit(f"no sé cómo romper {regla}. Conozco: {', '.join(sorted(daños))}")
    daños[regla]()
    return regla


# ═══ Principal ═══════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Verifica un sistema de diseño.")
    ap.add_argument("--destino", required=True)
    ap.add_argument("--regla", help="ejecuta solo las comprobaciones de esa regla")
    ap.add_argument("--romper", metavar="DS-XXX",
                    help="inyecta un error a propósito para probar el verificador")
    a = ap.parse_args()

    s = Sistema(a.destino)
    if a.romper:
        print(f"⚠  error inyectado a propósito en {romper(s, a.romper)} — "
              f"se espera que la comprobación FALLE\n")

    mod = Modelo(s)
    total_ok = total_mal = 0
    saltadas = []
    del_objetivo = []      # los resultados de la regla que se rompió, para juzgarla aparte
    fallos_ajenos = 0
    print(f"{s.proyecto.get('proyecto', {}).get('nombre') or s.raiz.name}   "
          f"modos: {', '.join(s.modos)}\n")

    for eje, checks in EJES:
        filas = []
        for fn in checks:
            r = fn(s, mod) if fn.__name__.startswith("d0") else fn(s)
            # Cero elementos comprobados no es un éxito: la comprobación corrió sin
            # nada que mirar. Contarlo en verde es exactamente el salto disfrazado
            # contra el que avisa el Paso 5.
            if r.saltada is None and not r.fallos and r.n == 0:
                r.saltada = "corrió sin nada que comprobar"
            if a.romper:
                del_objetivo.append(r) if r.regla == a.romper else None
                if r.regla != a.romper:
                    fallos_ajenos += len(r.fallos)
            if a.regla and r.regla != a.regla:
                continue
            filas.append(r)
        if not filas:
            continue
        print(f"── {eje}")
        for r in filas:
            if r.saltada:
                saltadas.append((r.regla, r.nombre, r.saltada))
                print(f"   ·  {r.regla:8} {r.nombre:52} saltada")
            elif r.fallos:
                total_mal += len(r.fallos)
                total_ok += r.n
                print(f"   ✗  {r.regla:8} {r.nombre:52} {len(r.fallos)} fallos")
                for f in r.fallos[:8]:
                    print(f"        {f}")
                if len(r.fallos) > 8:
                    print(f"        … y {len(r.fallos) - 8} más")
            else:
                total_ok += r.n
                print(f"   ✓  {r.regla:8} {r.nombre:52} {r.n}")
        print()

    print(f"{total_ok} comprobaciones en verde · {total_mal} fallos"
          + (f" · {len(saltadas)} saltadas" if saltadas else ""))

    if saltadas:
        print("\nSaltadas — no son verdes, son preguntas sin hacer:")
        for regla, nombre, motivo in saltadas:
            print(f"   {regla:8} {nombre:52} {motivo}")

    if a.romper:
        return juzgar(a.romper, del_objetivo, fallos_ajenos)

    return 1 if total_mal else 0


if __name__ == "__main__":
    sys.exit(main())
