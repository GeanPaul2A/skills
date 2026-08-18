#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir.py — publica el sistema a las plataformas que lo consumen.

    python3 construir.py --destino <carpeta> --salidas css,figma,lienzo
    python3 construir.py --destino <carpeta>              usa proyecto.json

Salidas:
    css        propiedades personalizadas, un bloque por modo
    figma      colecciones de variables, con modos y sintaxis por plataforma
    swift      constantes para iOS
    android    recursos XML
    lienzo     documento NEUTRAL de nodos — lo que consume un puente de diseño
    galeria    HTML por componente, listo para un puente que escriba

Los tokens son la fuente; todo esto es salida. Editar una salida a mano es
perder el cambio en la próxima construcción — DS-T01.

Solo biblioteca estándar.
"""

import argparse
import json
import pathlib
import re
import sys

SALIDAS = ["css", "figma", "swift", "android", "lienzo", "galeria"]


# ═══ Carga y resolución ══════════════════════════════════════════════════════

class Sistema:
    def __init__(self, destino):
        self.raiz = pathlib.Path(destino).resolve()
        self.marca = self._json("marca.json")
        self.proyecto = self._json("proyecto.json") or {}
        self.prim = self._json("tokens/1-primitivos.json") or {}
        self.sem = self._json("tokens/2-semanticos.json") or {}
        self.comp_tok = self._json("tokens/3-componentes.json") or {}
        self.componentes = (self._json("inventario/componentes.json") or {}).get("componentes", {})
        self.modos = self.marca["modos"]["activos"] + self.marca["modos"].get("preparados", [])
        self.activo = self.marca["modos"]["activos"][0]

    def _json(self, rel):
        f = self.raiz / rel
        if not f.exists():
            if rel == "marca.json":
                sys.exit(f"falta {f} — ¿es una carpeta de sistema de diseño?")
            return None
        return json.loads(f.read_text(encoding="utf-8"))

    def roles(self):
        return {k: v for k, v in self.sem.items() if not k.startswith("_")}

    def valor(self, alias, modo):
        """Resuelve una cadena de alias hasta el valor final, en el modo pedido."""
        v, vueltas = alias, 0
        while isinstance(v, str) and v.startswith("{") and v.endswith("}"):
            vueltas += 1
            if vueltas > 10:
                return None
            ruta = v.strip("{}").split(".")
            v = self._buscar(ruta)
            if v is None:
                return None
            if isinstance(v, dict) and modo in v:
                v = v[modo]
        return v

    def _buscar(self, ruta):
        clave = ".".join(ruta)
        for fuente in (self.prim, self.sem, self.comp_tok):
            if clave in fuente:
                return fuente[clave]
            grupo = fuente.get(".".join(ruta[:-1]))
            if isinstance(grupo, dict):
                if ruta[-1] in grupo:
                    return grupo[ruta[-1]]
                if ruta[-1].isdigit() and int(ruta[-1]) in grupo:
                    return grupo[int(ruta[-1])]
        return None

    def resueltos(self, modo):
        """Todos los roles semánticos con su valor final en ese modo."""
        out = {}
        for rol, v in self.roles().items():
            if isinstance(v, dict) and "tamaño" in v:
                out[rol] = {k: (self.valor(x, modo) if isinstance(x, str) else x)
                            for k, x in v.items()}
            else:
                out[rol] = self.valor(v if not isinstance(v, dict) else v.get(modo, ""), modo)
        return out


# ═══ Nombres por plataforma ══════════════════════════════════════════════════
# Una variable, tres nombres. Es lo que pide DS-T05 / DS-X03: el desarrollador
# copia el nombre de su plataforma y compila.

def kebab(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def camello(t):
    p = re.split(r"[^a-z0-9]+", t.lower())
    return p[0] + "".join(x.capitalize() for x in p[1:] if x)


def serpiente(t):
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")


def nombres(tok):
    return {"web": f"--{kebab(tok)}", "ios": camello(tok), "android": serpiente(tok)}


# ═══ CSS ═════════════════════════════════════════════════════════════════════

def salida_css(s, out):
    L = ["/* Generado por construir.py — no editar a mano. La fuente son los tokens. */", ""]

    def bloque(modo, selector):
        L.append(f"{selector} {{")
        for rol, v in s.resueltos(modo).items():
            if isinstance(v, dict):
                L.append(f"  --{kebab(rol)}-tamano: {v.get('tamaño')};")
                L.append(f"  --{kebab(rol)}-peso: {v.get('peso')};")
                L.append(f"  --{kebab(rol)}-interlineado: {v.get('interlineado')};")
            elif v is not None:
                L.append(f"  --{kebab(rol)}: {v};")
        L.append("}")
        L.append("")

    bloque(s.activo, ":root")
    for modo in s.modos:
        if modo == s.activo:
            continue
        L.append(f"/* modo «{modo}» — se activa poniendo data-modo=\"{modo}\" en la raíz */")
        bloque(modo, f'[data-modo="{modo}"]')

    L.append("/* nivel 3 · lo ÚNICO que una pantalla puede citar — DS-T02 */")
    L.append(":root {")
    for tok, alias in s.comp_tok.items():
        if not tok.startswith("_"):
            L.append(f"  --{kebab(tok)}: var(--{kebab(alias.strip('{}'))});")
    L.append("}")

    # DS-A09 · todo movimiento tiene alternativa reducida
    L += ["", "@media (prefers-reduced-motion: reduce) {",
          "  *, *::before, *::after {",
          "    animation-duration: .01ms !important;",
          "    transition-duration: .01ms !important;",
          "  }", "}"]
    return {"sistema.css": "\n".join(L) + "\n"}


# ═══ Figma · colecciones de variables ════════════════════════════════════════

def salida_figma(s, out):
    """Formato de importación: colecciones, modos y sintaxis por plataforma.

    Los primitivos van OCULTOS y sin alcance: solo se usan como alias — DS-T03 / DS-X02.
    """
    def var(nombre, tipo, valores, alcance, oculto=False):
        return {"nombre": nombre, "tipo": tipo, "valoresPorModo": valores,
                "alcance": alcance, "ocultoEnPublicacion": oculto,
                "sintaxisPorPlataforma": nombres(nombre)}

    primitivas = []
    for grupo, valores in s.prim.items():
        if grupo.startswith("_") or not isinstance(valores, dict):
            continue
        for peldaño, v in valores.items():
            tipo = ("COLOR" if str(v).startswith("#")
                    else "FLOAT" if isinstance(v, (int, float)) or str(v).endswith("px")
                    else "STRING")
            primitivas.append(var(f"{grupo}/{peldaño}", tipo, {"valor": v},
                                  ["NINGUNO"], oculto=True))

    semanticas, tipografia = [], []
    for rol, v in s.roles().items():
        if isinstance(v, dict) and "tamaño" in v:
            for parte in ("tamaño", "peso"):
                tipografia.append(var(f"{rol}/{parte}", "FLOAT",
                                      {m: v[parte] for m in s.modos},
                                      ["TAMANO_FUENTE" if parte == "tamaño" else "PESO_FUENTE"]))
            continue
        porModo = {m: (v[m] if isinstance(v, dict) else v) for m in s.modos}
        raiz = rol.split(".")[0]
        tipo = "COLOR" if raiz in ("superficie", "borde", "texto", "accion", "estado") else "FLOAT"
        alcance = {"superficie": ["RELLENO_FORMA"], "borde": ["COLOR_TRAZO"],
                   "texto": ["RELLENO_TEXTO"], "accion": ["RELLENO_FORMA", "COLOR_TRAZO"],
                   "estado": ["RELLENO_FORMA", "RELLENO_TEXTO", "COLOR_TRAZO"],
                   "espacio": ["ESPACIO", "RELLENO_INTERIOR"],
                   "forma": ["RADIO_ESQUINA"]}.get(raiz, ["TODOS"])
        semanticas.append(var(rol, tipo, porModo, alcance))

    doc = {
        "_lee": "Formato de importación de variables. Tres colecciones, una por nivel. "
                "Los primitivos van ocultos: solo se usan como alias — DS-T03.",
        "_generado_por": "construir.py",
        "colecciones": [
            {"nombre": "1 · Primitivos", "modos": ["valor"],
             "_lee": "Se llaman por lo que SON. No cambian por modo. Ocultos de publicación",
             "variables": primitivas},
            {"nombre": "2 · Semánticos", "modos": s.modos,
             "_lee": "Se llaman por lo que HACEN. Acá viven los modos",
             "variables": semanticas + tipografia},
            {"nombre": "3 · Componentes", "modos": ["valor"],
             "_lee": "Dónde se aplica. Es lo único que una pantalla cita",
             "variables": [var(t, "ALIAS", {"valor": a}, ["TODOS"])
                           for t, a in s.comp_tok.items() if not t.startswith("_")]},
        ]}
    return {"figma-variables.json": json.dumps(doc, indent=2, ensure_ascii=False) + "\n"}


# ═══ Swift · Android ═════════════════════════════════════════════════════════

def _hex_swift(h):
    r, g, b = (int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return f"Color(red: {r:.3f}, green: {g:.3f}, blue: {b:.3f})"


def salida_swift(s, out):
    L = ["// Generado por construir.py — no editar a mano.", "import SwiftUI", "",
         "enum Sistema {"]
    for modo in s.modos:
        L.append(f"    enum {modo.capitalize()} {{")
        for rol, v in s.resueltos(modo).items():
            if isinstance(v, dict):
                continue
            if isinstance(v, str) and v.startswith("#"):
                L.append(f"        static let {camello(rol)} = {_hex_swift(v)}")
            elif v is not None and str(v).endswith("px"):
                L.append(f"        static let {camello(rol)}: CGFloat = {str(v)[:-2]}")
        L.append("    }")
    L.append("}")
    return {"Sistema.swift": "\n".join(L) + "\n"}


def salida_android(s, out):
    arch = {}
    for modo in s.modos:
        col = ['<?xml version="1.0" encoding="utf-8"?>',
               "<!-- Generado por construir.py — no editar a mano. -->", "<resources>"]
        dim = list(col)
        for rol, v in s.resueltos(modo).items():
            if isinstance(v, dict) or v is None:
                continue
            if str(v).startswith("#"):
                col.append(f'    <color name="{serpiente(rol)}">{v}</color>')
            elif str(v).endswith("px"):
                dim.append(f'    <dimen name="{serpiente(rol)}">{str(v)[:-2]}dp</dimen>')
        col.append("</resources>")
        dim.append("</resources>")
        sufijo = "" if modo == s.activo else f"-{serpiente(modo)}"
        arch[f"values{sufijo}/colores.xml"] = "\n".join(col) + "\n"
        if modo == s.activo:
            arch["values/medidas.xml"] = "\n".join(dim) + "\n"
    return arch


# ═══ Lienzo · el documento neutral ═══════════════════════════════════════════

def salida_lienzo(s, out):
    """Describe QUÉ dibujar, sin decir con qué herramienta.

    Un puente lo traduce a sus llamadas. Si mañana cambia la herramienta, se cambia
    el traductor y el documento sigue siendo el mismo — DS-X01.

    Toda caja lleva disposición: es el equivalente de Auto Layout, y sin ella la
    herramienta emite coordenadas absolutas — DS-L01.
    """
    def caja(nombre, hijos=None, **k):
        n = {"tipo": "marco", "nombre": nombre,
             "disposicion": {"direccion": k.get("direccion", "columna"),
                             "espacio": k.get("espacio", "{espacio.elementos}"),
                             "relleno": k.get("relleno", "{espacio.interior}"),
                             "alineacion": k.get("alineacion", "inicio"),
                             "ancho": k.get("ancho", "abraza"),
                             "alto": k.get("alto", "abraza")}}
        for campo in ("fondo", "borde", "forma"):
            if k.get(campo):
                n[campo] = k[campo]
        if hijos:
            n["hijos"] = hijos
        return n

    def texto(t, rol="tipo.cuerpo", color="texto.principal"):
        return {"tipo": "texto", "contenido": t,
                "estilo": f"{{{rol}}}", "color": f"{{{color}}}",
                "disposicion": {"ancho": "abraza", "alto": "abraza"}}

    paginas = []

    # Página · fundamentos
    rampa = []
    for grupo, valores in s.prim.items():
        if not grupo.startswith("color.") or not isinstance(valores, dict):
            continue
        rampa.append(caja(grupo, direccion="fila", espacio="{espacio.pegado}", hijos=[
            caja(f"{grupo}.{p}", fondo=f"{{{grupo}.{p}}}", forma="{forma.distintivo}",
                 relleno="{espacio.interior}", hijos=[texto(str(p), "tipo.etiqueta")])
            for p in valores]))
    paginas.append({"nombre": "1 · Fundamentos", "nodos": [
        caja("Color", espacio="{espacio.bloques}", hijos=[texto("Color", "tipo.titulo")] + rampa),
        caja("Tipografía", espacio="{espacio.fila}", hijos=[texto("Tipografía", "tipo.titulo")] + [
            texto(f"{rol.split('.')[1]} — el veloz murciélago hindú", rol)
            for rol in s.roles() if rol.startswith("tipo.")]),
    ]})

    # Página · componentes, una fila por variante × estado
    nodos = []
    for nombre, c in s.componentes.items():
        if c.get("privado"):
            continue
        variantes = c.get("variantes") or ["única"]
        estados = c.get("estados") or ["reposo"]
        filas = []
        for v in variantes:
            filas.append(caja(f"{nombre}/{v}", direccion="fila", espacio="{espacio.elementos}",
                              hijos=[texto(v, "tipo.etiqueta", "texto.secundario")] + [
                                  {"tipo": "instancia", "componente": nombre,
                                   "propiedades": {"variante": v, "estado": e},
                                   "tokens": c.get("tokens", {})} for e in estados]))
        nodos.append(caja(nombre, espacio="{espacio.fila}", hijos=[
            texto(nombre, "tipo.seccion"),
            texto(c.get("descripcion", ""), "tipo.apoyo", "texto.secundario")] + filas))
    paginas.append({"nombre": "2 · Componentes", "nodos": nodos})

    doc = {
        "_lee": "Documento NEUTRAL de lienzo. Describe qué dibujar, no con qué herramienta. "
                "Un puente lo traduce a sus llamadas — DS-X01.",
        "_generado_por": "construir.py",
        "version": "1.0",
        "unidades": "px",
        "dimensionado": {"abraza": "se encoge a su contenido", "llena": "ocupa lo que le den",
                         "fijo": "tamaño invariable"},
        "variables": "figma-variables.json — se importan ANTES de dibujar",
        "paginas": paginas,
    }
    return {"lienzo.json": json.dumps(doc, indent=2, ensure_ascii=False) + "\n"}


# ═══ Galería · HTML por componente ═══════════════════════════════════════════

GALERIA_CSS = """
  *{box-sizing:border-box}
  body{margin:0;padding:var(--espacio-respiro);background:var(--superficie-base);
       color:var(--texto-principal);font-family:%(familia)s,system-ui,sans-serif;
       font-size:var(--tipo-cuerpo-tamano);line-height:var(--tipo-cuerpo-interlineado)}
  h1{font-size:var(--tipo-titulo-tamano);line-height:var(--tipo-titulo-interlineado);
     font-weight:var(--tipo-titulo-peso);margin:0 0 var(--espacio-elementos)}
  .nota{color:var(--texto-secundario);font-size:var(--tipo-apoyo-tamano);
        margin:0 0 var(--espacio-secciones);max-width:60ch}
  .fila{display:flex;flex-wrap:wrap;gap:var(--espacio-fila);align-items:center;
        margin-bottom:var(--espacio-bloques)}
  .celda{display:flex;flex-direction:column;gap:var(--espacio-pegado)}
  .et{font-size:var(--tipo-etiqueta-tamano);color:var(--texto-secundario);
      text-transform:uppercase;letter-spacing:.04em}
  .muestra{display:inline-flex;align-items:center;justify-content:center;
           padding:var(--espacio-elementos) var(--espacio-interior);
           border-radius:var(--forma-control);border:1px solid transparent;min-height:44px}
  .foco{outline:2px solid var(--accion-reposo);outline-offset:2px}
"""


def salida_galeria(s, out):
    """Un HTML por componente, con marcador de tarjeta para un puente que escriba."""
    familia = s.marca["tipografia"]["familia"]
    css = (out.get("sistema.css") or salida_css(s, {})["sistema.css"])
    arch = {}
    for nombre, c in s.componentes.items():
        if c.get("privado"):
            continue
        variantes = c.get("variantes") or ["única"]
        estados = c.get("estados") or ["reposo"]
        toks = c.get("tokens") or {}
        filas = []
        for v in variantes:
            celdas = []
            for e in estados:
                fondo = toks.get(f"{v}.fondo") or toks.get("fondo") or "superficie.elevada"
                col = toks.get(f"{v}.texto") or toks.get("texto") or "texto.principal"
                if e == "presionado":
                    fondo = toks.get(f"{v}.fondo-presionado", fondo)
                estilo = (f"background:var(--{kebab(fondo)});color:var(--{kebab(col)});"
                          + ("opacity:.4;" if e == "deshabilitado" else "")
                          + f"border-color:var(--{kebab(toks.get('borde', 'borde-sutil'))});")
                celdas.append(f'<div class="celda"><span class="et">{e}</span>'
                              f'<span class="muestra{" foco" if e == "foco" else ""}" '
                              f'style="{estilo}">{nombre}</span></div>')
            filas.append(f'<div class="fila"><span class="et" style="width:8rem">{v}</span>'
                         + "".join(celdas) + "</div>")
        html = (f'<!-- @dsCard group="Componentes" -->\n'
                f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{nombre}</title><style>{css}\n{GALERIA_CSS % {"familia": familia}}'
                f'</style></head><body>'
                f'<h1>{nombre}</h1>'
                f'<p class="nota"><strong>Cuándo:</strong> {c.get("descripcion", "")}<br>'
                f'<strong>Cuándo no:</strong> {c.get("cuando_no", "")}</p>'
                + "".join(filas) + '</body></html>\n')
        arch[f"galeria/{kebab(nombre)}.html"] = html
    arch["galeria/index.html"] = hoja_del_sistema(s, css, familia, arch)
    return arch


def hoja_del_sistema(s, css, familia, arch):
    """La portada de la galería: paleta, escalas, tipografía y el índice de componentes.

    Es lo que el Paso 7 manda mostrarle al usuario. Los HTML por componente muestran
    los componentes; la paleta y las escalas no aparecían en ninguna salida.
    """
    bloques = []

    tiras = []
    for tok, escala in s.prim.items():
        if not tok.startswith("color.") or not isinstance(escala, dict):
            continue
        celdas = "".join(
            f'<div class="celda"><span class="muestra" style="background:{hex_};'
            f'border-color:var(--borde-sutil)">&nbsp;</span>'
            f'<span class="et">{peldaño}<br>{hex_}</span></div>'
            for peldaño, hex_ in escala.items())
        tiras.append(f'<div class="fila"><span class="et" style="width:8rem">'
                     f'{tok.split(".", 1)[1]}</span>{celdas}</div>')
    bloques.append("<h2>Paleta</h2><p class=\"nota\">Primitivos: se llaman por lo que SON. "
                   "Una pantalla nunca los cita — cita el nivel 3.</p>" + "".join(tiras))

    for titulo, tok in (("Espaciado", "medida"), ("Tamaños de letra", "letra"),
                        ("Radios", "radio")):
        escala = s.prim.get(tok)
        if not isinstance(escala, dict):
            continue
        celdas = "".join(f'<div class="celda"><span class="et">{k}<br>{v}</span></div>'
                         for k, v in escala.items())
        bloques.append(f'<h2>{titulo}</h2><div class="fila">{celdas}</div>')

    escala = s.prim.get("letra") or {}
    muestras = "".join(
        f'<p style="font-size:{v};margin:.4rem 0">{v} · Texto de muestra para ver la escala</p>'
        for v in escala.values())
    bloques.append(f'<h2>Tipografía</h2><p class="nota">{familia}</p>{muestras}')

    enlaces = "".join(
        f'<li><a href="{p.split("/", 1)[1]}">{p.split("/", 1)[1][:-5]}</a></li>'
        for p in sorted(arch) if p != "galeria/index.html")
    bloques.append(f'<h2>Componentes</h2><ul>{enlaces}</ul>')

    nombre = s.proyecto.get("proyecto", {}).get("nombre") or s.raiz.name
    return (f'<!-- @dsCard group="Sistema" -->\n'
            f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{nombre} · sistema de diseño</title>'
            f'<style>{css}\n{GALERIA_CSS % {"familia": familia}}</style></head><body>'
            f'<h1>{nombre}</h1>'
            f'<p class="nota">Modos: {", ".join(s.modos)}</p>'
            + "".join(bloques) + '</body></html>\n')


# ═══ Principal ═══════════════════════════════════════════════════════════════

GENERADORES = {"css": salida_css, "figma": salida_figma, "swift": salida_swift,
               "android": salida_android, "lienzo": salida_lienzo, "galeria": salida_galeria}


def main():
    ap = argparse.ArgumentParser(description="Publica el sistema de diseño.")
    ap.add_argument("--destino", required=True)
    ap.add_argument("--salidas", help=f"coma-separadas: {', '.join(SALIDAS)}")
    a = ap.parse_args()

    s = Sistema(a.destino)
    if a.salidas:
        pedidas = [x.strip() for x in a.salidas.split(",") if x.strip()]
    else:
        pedidas = [k for k, v in (s.proyecto.get("salidas") or {}).items()
                   if v is True and k in GENERADORES]
    desconocidas = [p for p in pedidas if p not in GENERADORES]
    if desconocidas:
        sys.exit(f"no sé generar: {', '.join(desconocidas)}. Conozco: {', '.join(SALIDAS)}")
    if not pedidas:
        sys.exit("ninguna salida pedida — usa --salidas o activa alguna en proyecto.json")

    # css primero: la galería lo reutiliza en vez de volver a derivarlo
    pedidas.sort(key=lambda x: 0 if x == "css" else 1)

    base = s.raiz / "salidas"
    archivos = {}
    for p in pedidas:
        archivos.update(GENERADORES[p](s, archivos))

    for rel, contenido in archivos.items():
        f = base / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(contenido, encoding="utf-8")

    print(f"{s.proyecto.get('proyecto', {}).get('nombre') or s.raiz.name}"
          f"   modos: {', '.join(s.modos)}\n")
    for p in pedidas:
        de_esta = [r for r in archivos if p in r or r.startswith(("sistema", "figma", "Sistema",
                                                                 "values", "lienzo"))]
        print(f"  {p:9} {len(GENERADORES[p](s, archivos))} archivos")
    print(f"\n  en {base}")
    print("\n  Son salidas: editarlas a mano pierde el cambio en la próxima construcción — DS-T01.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
