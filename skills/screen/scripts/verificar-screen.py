#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar-screen.py — comprueba pantallas declaradas contra el sistema y contra el modelo.

    python3 verificar-screen.py --sistema <carpeta> --screens <carpeta>
    python3 verificar-screen.py --sistema <s> --screens <p> --romper DS-P02

El sistema aporta las plantillas, los componentes y los tokens.
El modelo del producto —si el proyecto lo declara— aporta las entidades y las reglas.
Si no lo declara, esas comprobaciones SE SALTAN Y SE REPORTAN saltadas.

Solo biblioteca estándar.
"""

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import R, juzgar, tabla  # noqa: E402,F401

OBLIGATORIOS = ["proposito", "plantilla", "datos", "zonas", "estados", "textos", "h1"]
ESTADOS = ["lleno", "cargando", "vacio", "error"]

# `R` y `juzgar` estaban copiados acá. Viven en `lib/comun.py`: la regla 3 de la skill
# dice que si un valor aparece en dos archivos, uno de los dos va a quedar viejo — y el
# veredicto de --romper es justo lo que no puede divergir entre verificadores.


# ═══ Carga ═══════════════════════════════════════════════════════════════════

class Contexto:
    def __init__(self, sistema, pantallas):
        self.sis = pathlib.Path(sistema).resolve()
        self.dir = pathlib.Path(pantallas).resolve()
        if not (self.sis / "marca.json").exists():
            sys.exit(f"no encuentro un sistema de diseño en {self.sis} "
                     f"— falta marca.json. Construilo con la skill system-design")

        self.proyecto = self._j(self.sis / "proyecto.json") or {}
        self.comp_tok = self._j(self.sis / "tokens" / "3-componentes.json") or {}
        self.componentes = tabla(self._j(self.sis / "inventario" / "componentes.json"), "componentes")
        self.plantillas = tabla(self._j(self.sis / "inventario" / "plantillas.json"), "plantillas")
        self.patrones = tabla(self._j(self.sis / "inventario" / "patrones.json"), "patrones")

        # Una carpeta ausente o vacía no es «todo bien»: es que no hay nada que
        # verificar. Callarlo devolvía cero fallos y código 0 — un verde que miente.
        if not self.dir.exists():
            sys.exit(f"no encuentro pantallas en {self.dir} — la carpeta no existe. "
                     f"Declaralas con la skill screen antes de verificar")

        self.screens = {}
        for f in sorted(self.dir.glob("*.json")):
            self.screens[f.stem] = self._j(f)
        if not self.screens:
            sys.exit(f"no hay ninguna pantalla declarada en {self.dir} — "
                     f"nada que verificar")

        self.modelo = Modelo(self.sis, self.proyecto)

    @staticmethod
    def _j(f):
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


class Modelo:
    """El modelo del producto, leído según lo que proyecto.json declare. Agnóstico."""

    def __init__(self, sis, proyecto):
        cfg = (proyecto or {}).get("modelo_de_datos") or {}
        self.motivo, self.entidades, self.reglas = None, {}, set()
        if not cfg.get("tipo"):
            self.motivo = "proyecto.json declara 'modelo_de_datos.tipo': null"
            return
        raiz = (sis / cfg.get("raiz", "")).resolve()
        if not raiz.exists():
            self.motivo = f"la raíz del modelo no existe: {raiz}"
            return
        self._leer(raiz, cfg)

    def _dominios(self, raiz, cfg):
        d = cfg.get("domains", {})
        if d.get("descubrir") == "plano":
            return [""]
        excl = set(d.get("excluir", []))
        return sorted(p.name for p in raiz.iterdir()
                      if p.is_dir() and not p.name.startswith(".") and p.name not in excl)

    def _leer(self, raiz, cfg):
        e = cfg.get("entidades", {})
        ext, fmt = e.get("extension", ".csv"), e.get("formato", "csv-cabecera")
        rc = cfg.get("reglas") or {}
        rx = re.compile(rc["patron"], re.M) if rc.get("patron") and rc.get("ruta") else None

        for dom in self._dominios(raiz, cfg):
            carpeta = raiz / e.get("ruta", "").replace("{dominio}", dom)
            if carpeta.exists():
                for f in sorted(carpeta.glob(f"*{ext}")):
                    campos = self._campos(f, fmt)
                    if campos:
                        self.entidades[f"{dom}.{f.stem}" if dom else f.stem] = campos
            if rx:
                rf = raiz / rc["ruta"].replace("{dominio}", dom)
                if rf.exists():
                    cita = rc.get("cita", "{dominio}.{regla}")
                    for m in rx.finditer(rf.read_text(encoding="utf-8")):
                        self.reglas.add(cita.replace("{dominio}", dom).replace("{regla}", m.group(1)))

    @staticmethod
    def _campos(f, fmt):
        try:
            if fmt == "csv-cabecera":
                return set(c.strip().strip('"')
                           for c in f.read_text(encoding="utf-8").splitlines()[0].split(","))
            if fmt == "json-esquema":
                d = json.loads(f.read_text(encoding="utf-8"))
                return set(d.get("properties", d).keys())
            if fmt == "sql-ddl":
                return set(re.findall(r"^\s{2,}([a-z_][a-z0-9_]*)\s+[A-Z]",
                                      f.read_text(encoding="utf-8"), re.M))
        except (OSError, ValueError, IndexError):
            return None
        return None


# ═══ Comprobaciones ══════════════════════════════════════════════════════════

def p01_contrato(c):
    """Toda pantalla declara los campos que la hacen verificable."""
    r = R("DS-C01", "toda pantalla lleva su declaración completa")
    if not c.screens:
        return r.saltar(f"no hay pantallas en {c.dir}")
    for n, p in c.screens.items():
        faltan = [k for k in OBLIGATORIOS if k not in p]
        r.ok() if not faltan else r.mal(f"{n}: falta {', '.join(faltan)}")
    return r


def p02_plantilla(c):
    """Toda pantalla sale de una plantilla que existe."""
    r = R("DS-C01", "la plantilla declarada existe")
    if not c.screens:
        return r.saltar("no hay pantallas")
    if not c.plantillas:
        return r.saltar("el sistema no tiene inventario/plantillas.json")
    for n, p in c.screens.items():
        pl = p.get("plantilla")
        r.ok() if pl in c.plantillas else r.mal(f"{n}: la plantilla '{pl}' no existe")
    return r


def p03_zonas(c):
    """Cada componente va en una zona que lo admite."""
    r = R("DS-C01", "cada componente cabe en su zona")
    if not (c.screens and c.plantillas):
        return r.saltar("hacen falta pantallas y plantillas")
    for n, p in c.screens.items():
        pl = c.plantillas.get(p.get("plantilla"))
        if not pl:
            continue
        zonas = {z["nombre"]: set(z.get("admite", [])) for z in pl.get("zonas", [])}
        for zona, comps in (p.get("zonas") or {}).items():
            if zona not in zonas:
                r.mal(f"{n}: la zona '{zona}' no existe en '{p['plantilla']}'")
                continue
            for comp in comps:
                if comp not in c.componentes:
                    r.mal(f"{n}: el componente '{comp}' no está en el inventario")
                elif comp not in zonas[zona]:
                    r.mal(f"{n}: '{comp}' no lo admite la zona '{zona}'")
                else:
                    r.ok()
    return r


def p04_estados(c):
    """DS-C03 · Los cuatro estados. «No aplica» vale con su motivo."""
    r = R("DS-C03", "los cuatro estados están cubiertos")
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        est = p.get("estados") or {}
        for e in ESTADOS:
            v = (est.get(e) or "").strip()
            if not v:
                r.mal(f"{n}: falta el estado '{e}'")
            elif v.lower().startswith("no aplica") and not re.search(r"[—:-]\s*\S", v):
                r.mal(f"{n}.{e}: dice «no aplica» sin decir por qué")
            else:
                r.ok()
    return r


def p05_extremos(c):
    """DS-L06 · Cada campo visible declara su valor más largo y más corto.

    Un campo que no es texto —un icono, una imagen— no tiene valor largo ni corto.
    Se declara "no aplica — <motivo>", igual que un estado: exigirle extremos a un
    icono obliga a inventar un dato que no existe. El motivo no es opcional.
    """
    r = R("DS-L06", "cada campo declara su valor más largo")
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        d = p.get("datos") or {}
        ext = d.get("extremos") or {}
        for campo in d.get("campos") or []:
            v = ext.get(campo)
            if isinstance(v, str) and v.strip().lower().startswith("no aplica"):
                if len(v.strip()) > len("no aplica") + 3:
                    r.ok()
                else:
                    r.mal(f"{n}: '{campo}' dice 'no aplica' sin decir por qué")
            elif not isinstance(v, dict) or not v.get("largo"):
                r.mal(f"{n}: '{campo}' sin su valor más largo — es donde revienta la maqueta")
            else:
                r.ok()
    return r


def p06_h1(c):
    """DS-A05 · Un solo H1, y apunta a un texto que existe."""
    r = R("DS-A05", "un solo titular por pantalla")
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        h1, textos = p.get("h1"), p.get("textos") or {}
        if not h1:
            r.mal(f"{n}: no dice cuál texto es el titular")
        elif isinstance(h1, list):
            r.mal(f"{n}: declara {len(h1)} titulares — DS-A05 pide uno")
        elif h1 not in textos:
            r.mal(f"{n}: el titular '{h1}' no está en 'textos'")
        else:
            r.ok()
    return r


def p07_tabulacion(c):
    """DS-A07 · Si el orden de foco diverge del visual, se explica."""
    r = R("DS-A07", "el orden de foco está declarado")
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        o = (p.get("orden_tabulacion") or "").lower()
        if not o:
            r.mal(f"{n}: sin 'orden_tabulacion'")
        elif "no coincide" in o or "atrapado" in o:
            r.ok() if p.get("_por_que_no_coincide") else r.mal(
                f"{n}: el foco diverge del visual y no explica por qué")
        else:
            r.ok()
    return r


def p08_crudos(c):
    """DS-T07 · Ningún valor en crudo en una pantalla."""
    r = R("DS-T07", "ningún valor en crudo")
    if not c.screens:
        return r.saltar("no hay pantallas")
    color = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
    medida = re.compile(r"\b\d+(?:\.\d+)?(px|rem|pt|dp)\b")
    for n, p in c.screens.items():
        crudo = json.dumps(p, ensure_ascii=False)
        for rx, que in ((color, "color"), (medida, "medida")):
            hallados = set(rx.findall(crudo) if que == "color" else
                           [m.group(0) for m in medida.finditer(crudo)])
            if hallados:
                r.mal(f"{n}: {que} en crudo — {', '.join(sorted(hallados)[:4])}   usá un token")
            else:
                r.ok()
    return r


def p09_si_no_llega(c):
    """DS-P04 · Lo que viene de otra fuente dice qué se muestra si no llega."""
    r = R("DS-P04", "toda fuente externa tiene plan B")
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        d = p.get("datos") or {}
        if not d.get("entidades"):
            continue
        v = (d.get("si_no_llega") or "").strip()
        r.ok() if len(v) >= 15 else r.mal(f"{n}: no dice qué se muestra si los datos no llegan")
    return r


def p10_entidades(c):
    """DS-P02 · Las entidades citadas existen en el modelo."""
    r = R("DS-P02", "las entidades citadas existen")
    if c.modelo.motivo:
        return r.saltar(c.modelo.motivo)
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        for e in (p.get("datos") or {}).get("entidades", []):
            r.ok() if e in c.modelo.entidades else r.mal(f"{n}: '{e}' no existe en el modelo")
    return r


def p11_campos(c):
    """DS-P02 · Ningún dato se muestra sin un campo que lo respalde."""
    r = R("DS-P02", "los campos citados existen en su entidad")
    if c.modelo.motivo:
        return r.saltar(c.modelo.motivo)
    if not c.screens:
        return r.saltar("no hay pantallas")
    for n, p in c.screens.items():
        for cita in (p.get("datos") or {}).get("campos", []):
            if "." not in cita:
                r.mal(f"{n}: '{cita}' no dice de qué entidad es")
                continue
            ent, campo = cita.rsplit(".", 1)
            if ent not in c.modelo.entidades:
                r.mal(f"{n}: la entidad '{ent}' no existe")
            elif campo not in c.modelo.entidades[ent]:
                r.mal(f"{n}: '{ent}' no tiene el campo '{campo}'")
            else:
                r.ok()
    return r


def p12_reglas(c):
    """DS-P01 · Las reglas de negocio citadas existen."""
    r = R("DS-P01", "las reglas de negocio citadas existen")
    if c.modelo.motivo:
        return r.saltar(c.modelo.motivo)
    if not c.modelo.reglas:
        return r.saltar("proyecto.json no declara dónde viven las reglas")
    for n, p in c.screens.items():
        for cita in (p.get("datos") or {}).get("reglas", []):
            r.ok() if cita in c.modelo.reglas else r.mal(f"{n}: la regla '{cita}' no existe")
    return r


def p13_patrones(c):
    """DS-P03 · Todo patrón contempla que algo salga mal."""
    r = R("DS-P03", "todo patrón contempla el fallo")
    if not c.patrones:
        return r.saltar("el sistema no tiene inventario/patrones.json")
    señales = ("error", "fallo", "rechaz", "sin-", "sin ", "vencid", "expir", "cancel", "vacio")
    for n, p in c.patrones.items():
        claves = list(p.get("estados") or {})
        if any(any(x in str(k).lower() for x in señales) for k in claves):
            r.ok()
        else:
            r.mal(f"{n}: ningún estado de fallo entre {claves}")
    return r


def p14_foco_unico(c):
    """DS-A13 · toda pantalla tiene un solo foco visual primario, y declara cuál.

    Es el error que produce pantallas «prolijas pero que no dicen nada»: todo alineado,
    todo con el mismo peso, y sin saber qué hay que hacer. Dos primarios en una pantalla
    es no haber decidido cuál es la tarea.

    Si de verdad hay dos caminos igual de válidos —aceptar y rechazar una solicitud—,
    entonces la pantalla tiene UNA decisión, y el foco es esa decisión: se declara como
    una lista de dos, y nada más compite con ellos.
    """
    r = R("DS-A13", "cada pantalla declara un solo foco primario")
    for nombre, p in c.screens.items():
        foco = p.get("foco")
        if not foco:
            r.mal(f"{nombre}: no declara «foco» — cuál es la acción o el dato primario")
            continue
        piezas = foco if isinstance(foco, list) else [foco]
        if len(piezas) > 2:
            r.mal(f"{nombre}: declara {len(piezas)} focos primarios — uno, o dos solo si "
                  f"son las dos caras de una misma decisión")
            continue
        # El foco tiene que existir en alguna zona: un foco que no está en la pantalla
        # es una intención, no una decisión de diseño.
        enpantalla = {x for zona in (p.get("zonas") or {}).values() for x in zona}
        enpantalla |= set(p.get("textos") or {})
        for pieza in piezas:
            if pieza not in enpantalla:
                r.mal(f"{nombre}: el foco «{pieza}» no está en ninguna zona ni en textos")
            else:
                r.ok()
    return r


def p15_desborde(c):
    """DS-C13 · un hijo no puede ser más ancho que el espacio útil de su padre.

    La cuenta: ancho del padre − rellenos − espacio entre hijos × (hijos − 1). Si la suma
    de los mínimos de los hijos la supera, hay tres salidas —uno abraza y otro llena, el
    texto se corta declarando cuál, o el contenedor cambia de dirección— y **achicar la
    letra no es ninguna de las tres**: rompe DS-F03 y garantiza el desborde al traducir.
    """
    r = R("DS-C13", "ningún hijo desborda el espacio útil de su zona")
    conmedidas = 0
    for nombre, p in c.screens.items():
        plantilla = c.plantillas.get(p.get("plantilla")) or {}
        anchos = {z.get("nombre"): z for z in (plantilla.get("zonas") or [])}
        # Las piezas que una zona lista NO conviven: `.esqueleto` es el estado cargando,
        # `vacio` el vacío, `mensaje` el error. Sumar sus anchos mediría una pantalla que
        # no existe. Lo que sí es cierto en cualquier disposición: **cada pieza, sola,
        # tiene que caber**.
        for zona, piezas in (p.get("zonas") or {}).items():
            z = anchos.get(zona) or {}
            util = z.get("ancho_util")
            if not isinstance(util, (int, float)):
                continue
            libre = util - (z.get("relleno") or 0) * 2
            conmedidas += 1
            for pieza in piezas:
                minimo = (c.componentes.get(pieza) or {}).get("ancho_minimo") or 0
                if minimo > libre:
                    r.mal(f"{nombre}/{zona}: «{pieza}» pide {minimo} px y el espacio útil "
                          f"es {libre} ({util} − {(z.get('relleno') or 0) * 2} de relleno)")
                else:
                    r.ok()
        # Y la suma solo se comprueba donde la pantalla declara que esas piezas SÍ van en
        # la misma fila. Sin esa declaración, la suma es una suposición sobre la
        # disposición — y una comprobación que supone mide su propia suposición.
        for fila in (p.get("filas") or []):
            zona, piezas = fila.get("zona"), fila.get("piezas") or []
            z = anchos.get(zona) or {}
            util = z.get("ancho_util")
            if not isinstance(util, (int, float)):
                continue
            conmedidas += 1
            relleno = (z.get("relleno") or 0) * 2
            entre = (z.get("espacio") or 0) * max(0, len(piezas) - 1)
            libre = util - relleno - entre
            minimos = sum((c.componentes.get(x) or {}).get("ancho_minimo") or 0
                          for x in piezas)
            if minimos > libre:
                r.mal(f"{nombre}/{zona}: la fila {piezas} pide {minimos} px y hay {libre} "
                      f"({util} − {relleno} relleno − {entre} entre) — uno tiene que "
                      f"llenar y los otros abrazar")
            else:
                r.ok()
    if not conmedidas:
        return r.saltar("ninguna zona declara «ancho_util»: sin medidas no hay desborde "
                        "que calcular")
    return r


COMPROBACIONES = [p01_contrato, p02_plantilla, p03_zonas, p04_estados, p05_extremos,
                  p06_h1, p07_tabulacion, p08_crudos, p09_si_no_llega,
                  p10_entidades, p11_campos, p12_reglas, p13_patrones,
                  p14_foco_unico, p15_desborde]


# ═══ El error inyectado ══════════════════════════════════════════════════════

def romper(c, regla):
    """Una comprobación que nunca falló no está probada: está sin usar."""
    if not c.screens:
        sys.exit("no hay pantallas donde inyectar el error")
    n = next(iter(c.screens))
    p = c.screens[n]
    daños = {
        "DS-C01": lambda: p.pop("proposito", None),
        "DS-C03": lambda: (p.get("estados") or {}).pop("error", None),
        "DS-L06": lambda: (p.get("datos") or {}).pop("extremos", None),
        "DS-A05": lambda: p.__setitem__("h1", "texto-que-no-existe"),
        "DS-A07": lambda: p.pop("orden_tabulacion", None),
        "DS-T07": lambda: (p.get("textos") or {}).__setitem__("colado", "fondo #3A45C9 y 13px"),
        "DS-P04": lambda: (p.get("datos") or {}).__setitem__("si_no_llega", ""),
        "DS-P02": lambda: (p.get("datos") or {}).setdefault("entidades", [])
                           .append("entidad.inexistente"),
        "DS-P01": lambda: (p.get("datos") or {}).setdefault("reglas", [])
                           .append("dominio.R999"),
        # Sin este patrón inventado, un sistema sin patrones no puede probar nunca
        # DS-P03 — y la comprobación quedaría sin usar para siempre.
        "DS-P03": lambda: c.patrones.__setitem__(
            "patron-de-prueba", {"proposito": "probar el verificador",
                                 "estados": {"entrada": "x", "exito": "y"}}),
        "DS-A13": lambda: next(iter(c.screens.values())).__setitem__(
            "foco", ["titulo", "accion", "vacio"]),
        # El desborde se inyecta agrandando el mínimo de una pieza que la pantalla ya usa:
        # es el caso real —un texto que creció al traducir— y no un número inventado.
        "DS-C13": lambda: [
            c.componentes.setdefault(pieza, {}).__setitem__("ancho_minimo", 9999)
            for p in list(c.screens.values())[:1]
            for zona in list((p.get("zonas") or {}).values())[:1]
            for pieza in zona[:1]],
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
    ap = argparse.ArgumentParser(description="Verifica pantallas contra el sistema y el modelo.")
    ap.add_argument("--sistema", required=True, help="carpeta con marca.json y tokens/")
    ap.add_argument("--screens", required=True, help="carpeta con las pantallas declaradas")
    ap.add_argument("--regla")
    ap.add_argument("--romper", metavar="DS-XXX")
    a = ap.parse_args()

    c = Contexto(a.sistema, a.screens)
    if a.romper:
        print(f"⚠  error inyectado a propósito en {romper(c, a.romper)} — "
              f"se espera que la comprobación FALLE\n")

    print(f"{len(c.screens)} pantallas · sistema en {c.sis.name}\n")
    ok = mal = 0
    saltadas = []
    del_objetivo = []      # los resultados de la regla que se rompió, para juzgarla aparte
    fallos_ajenos = 0
    for fn in COMPROBACIONES:
        r = fn(c)
        if a.romper:
            del_objetivo.append(r) if r.regla == a.romper else None
            if r.regla != a.romper:
                fallos_ajenos += len(r.fallos)
        if a.regla and r.regla != a.regla:
            continue
        if r.saltada:
            saltadas.append((r.regla, r.nombre, r.saltada))
            print(f"   ·  {r.regla:8} {r.nombre:48} saltada")
        elif r.fallos:
            mal += len(r.fallos)
            ok += r.n
            print(f"   ✗  {r.regla:8} {r.nombre:48} {len(r.fallos)} fallos")
            for f in r.fallos[:8]:
                print(f"        {f}")
            if len(r.fallos) > 8:
                print(f"        … y {len(r.fallos) - 8} más")
        else:
            ok += r.n
            print(f"   ✓  {r.regla:8} {r.nombre:48} {r.n}")

    print(f"\n{ok} comprobaciones en verde · {mal} fallos"
          + (f" · {len(saltadas)} saltadas" if saltadas else ""))
    if saltadas:
        print("\nSaltadas — no son verdes, son preguntas sin hacer:")
        for regla, nombre, motivo in saltadas:
            print(f"   {regla:8} {nombre:48} {motivo}")

    print("\nLo que ningún guion detecta, y hay que mirar:")
    for x in ("si se entiende qué hay que hacer sin leer todo",
              "si lo importante se ve SIN desplazar",
              "si el espaciado agrupa lo que va junto",
              "si se entiende al 200 % de texto"):
        print(f"   □  {x}")

    if a.romper:
        return juzgar(a.romper, del_objetivo, fallos_ajenos)
    return 1 if mal else 0


if __name__ == "__main__":
    sys.exit(main())
