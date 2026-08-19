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
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import contrato_estados, contrato_figma  # noqa: E402

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
        inv_p = self._json("inventario/plantillas.json") or {}
        self.plantillas = inv_p.get("plantillas", {})
        self.patrones = inv_p.get("patrones", {}) or (
            self._json("inventario/patrones.json") or {}).get("patrones", {})
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

    def rol_tipografico(self, alias):
        """Si el alias apunta a un rol tipográfico completo, devuelve su nombre.

        **Un rol tipográfico no es un valor: son tres** —tamaño, peso e interlineado—.
        `{tipo.cuerpo}` no se puede volcar en una sola variable, y por eso los veinte
        tokens de componente que lo citan necesitan un trato aparte en cada salida:
        el CSS los abre en tres propiedades y Figma los manda a un estilo de texto,
        que es donde una tipografía compuesta vive en el lienzo — DS-X04.

        Escribirlos como si fueran un valor produce salidas que se ven bien y no
        resuelven: `--boton-texto: var(--tipo-cuerpo)` contra un CSS que solo define
        `--tipo-cuerpo-tamano`. **El navegador no avisa: usa el valor por omisión.**
        """
        if not (isinstance(alias, str) and alias.startswith("{")):
            return None
        rol = alias.strip("{}")
        v = self.sem.get(rol)
        return rol if isinstance(v, dict) and "tamaño" in v else None

    def partes_tipograficas(self, rol):
        """Las claves de un rol tipográfico, en el orden en que se escriben."""
        return [k for k in ("tamaño", "peso", "interlineado") if k in self.sem.get(rol, {})]

    def resueltos(self, modo):
        """Todos los roles semánticos con su valor final en ese modo."""
        out = {}
        for rol, v in self.roles().items():
            if isinstance(v, dict) and "tamaño" in v:
                out[rol] = {k: (self.valor(x, modo) if isinstance(x, str) else x)
                            for k, x in v.items()}
            elif es_sombra(v):
                out[rol] = dict(v)          # ya son números; no hay alias que resolver
            else:
                out[rol] = self.valor(v if not isinstance(v, dict) else v.get(modo, ""), modo)
        return out


# ═══ Nombres por plataforma ══════════════════════════════════════════════════
# Una variable, tres nombres. Es lo que pide DS-T05 / DS-X03: el desarrollador
# copia el nombre de su plataforma y compila.

def sin_tildes(t):
    """«tamaño» → «tamano». La letra acentuada se TRADUCE, no se tira.

    Descartarla parte la palabra en dos —`tama` y `o`— y el nombre resultante es
    `--tipo-cuerpo-tama-o`, que no existe en ninguna salida: la hoja de estilo define
    `--tipo-cuerpo-tamano`. **El desarrollador copiaba de Figma un nombre inventado.**

    Se descompone en letra base más acento (`NFKD`) y se descartan solo los acentos,
    que es lo que deja la eñe en `n` y la a con tilde en `a`.
    """
    return "".join(c for c in unicodedata.normalize("NFKD", t)
                   if not unicodedata.combining(c))


def kebab(t):
    return re.sub(r"[^a-z0-9]+", "-", sin_tildes(t).lower()).strip("-")


def camello(t):
    p = re.split(r"[^a-z0-9]+", sin_tildes(t).lower())
    return p[0] + "".join(x.capitalize() for x in p[1:] if x)


def serpiente(t):
    return re.sub(r"[^a-z0-9]+", "_", sin_tildes(t).lower()).strip("_")


def nombres(tok):
    """Los tres nombres, con la clave EXACTA que pide `setVariableCodeSyntax`.

    `iOS` lleva la i minúscula y las otras dos van enteras en mayúscula. No es un
    capricho de estilo: pasar `IOS` devuelve «Invalid enum value». Se escriben así acá
    para que quien consuma el archivo copie la clave y no tenga que acordarse.
    """
    return {"WEB": f"--{kebab(tok)}", "iOS": camello(tok), "ANDROID": serpiente(tok)}


_ESTADOS = None


def delta(estado, variante, toks):
    """Qué cambia este estado, resuelto contra los tokens del componente.

    **Una sola definición, y la leen los dos consumidores** — la galería y el lienzo. Un
    valor «@.algo» se resuelve contra la variante que se dibuja: al dibujar el primario,
    «@.fondo-presionado» es «primario.fondo-presionado». Si el componente no declara ese
    token, el estado no cambia esa propiedad: **no se inventa un valor**.
    """
    global _ESTADOS
    if _ESTADOS is None:
        _ESTADOS = contrato_estados()
    out = {}
    for prop, v in _ESTADOS.get(estado, {}).items():
        if prop.startswith("_") or prop == "visual":
            continue
        if prop == "cambia":
            # La instrucción de un estado NO visual —«aparece el botón de cerrar a la
            # derecha», «las iniciales en lugar de la imagen»—. Se emite: es lo único que
            # distingue ese estado, y tirarla deja al que dibuja adivinando lo que el
            # contrato ya decía. Sin ella salieron `descartable` y `sin-foto` idénticos
            # a su reposo.
            out["nota"] = v
            continue
        if isinstance(v, dict):                       # compuesto, como el anillo de foco
            out[prop] = {k: x.strip("{}") for k, x in v.items()}
        elif isinstance(v, str) and v.startswith("@."):
            # Primero contra la variante —`primario.fondo-presionado`—, y si el componente
            # no lo namespacea, contra el token pelado —`elegida.fondo`—. Sin esa segunda
            # búsqueda, `opcion` y `tarjeta` perdían el estado `elegido` ENTERO y en
            # silencio, porque el `if destino` descarta sin avisar.
            destino = toks.get(f"{variante}{v[1:]}") or toks.get(v[2:])
            if destino:
                out[prop] = destino
        elif isinstance(v, str):
            out[prop] = v.strip("{}")
    return out


def es_sombra(v):
    """Una sombra es compuesta —desplazamiento, desenfoque y opacidad—, así que NO es una
    variable: es un estilo de efecto, igual que una tipografía es un estilo de texto.

    Una variable guarda un valor. Meter una sombra en una obliga a inventar tres variables
    sueltas que nadie vuelve a juntar, y la pieza termina con la sombra escrita adentro."""
    return isinstance(v, dict) and "desenfoque" in v


# ═══ CSS ═════════════════════════════════════════════════════════════════════

def salida_css(s, out):
    L = ["/* Generado por construir.py — no editar a mano. La fuente son los tokens. */", ""]

    def bloque(modo, selector):
        L.append(f"{selector} {{")
        for rol, v in s.resueltos(modo).items():
            if es_sombra(v):
                L.append(f"  --{kebab(rol)}: 0 {v['y']}px {v['desenfoque']}px "
                         f"rgba(0,0,0,{v['opacidad']});")
            elif isinstance(v, dict):
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
        if tok.startswith("_"):
            continue
        rol = s.rol_tipografico(alias)
        if rol:
            # Un rol tipográfico se abre en sus partes: escribirlo como un solo
            # `var(--tipo-cuerpo)` deja una referencia que el archivo no define.
            for parte in s.partes_tipograficas(rol):
                p = "tamano" if parte == "tamaño" else parte
                L.append(f"  --{kebab(tok)}-{p}: var(--{kebab(rol)}-{p});")
        else:
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
    """Formato de importación de Figma: colecciones, modos y sintaxis por plataforma.

    **Todo campo enumerado sale en el vocabulario de Figma, no en el del sistema.** Es lo
    que estuvo mal desde el principio: el archivo decía ser «formato de importación» y
    llevaba `RELLENO_FORMA` como alcance y `ALIAS` como tipo, que Figma no conoce. Se
    importaba igual **porque alguien lo traducía a mano cada vez**, y esa traducción no
    estaba escrita en ninguna parte ni se comprobaba — así que cada tanda la reinventaba.

    El vocabulario válido vive en `referencias/figma-api.json`, verificado contra el
    servidor. Se lee, no se copia: si Figma agrega un alcance, se edita ese archivo y
    tanto el generador como el verificador lo ven — DS-X12.
    """
    api = contrato_figma()
    ALCANCE_VALIDO = set(api["alcances"]["valores"])

    def var(nombre, tipo, valores, alcance, oculto=False):
        # El punto se traduce a barra: Figma responde «invalid variable name» al punto y
        # solo agrupa con barra. El sistema nombra con puntos —`superficie.base`— y la
        # traducción va acá, porque el JSON es la fuente y Figma es una salida — DS-X01.
        malos = [a for a in alcance if a not in ALCANCE_VALIDO]
        if malos:
            sys.exit(f"alcance que Figma no conoce en «{nombre}»: {malos}. "
                     f"Los válidos están en referencias/figma-api.json")
        # Una referencia entre llaves nombra a la variable DE FIGMA, con barra: quien lea
        # el archivo la busca tal cual. Dejarla con punto obliga a traducir al leer, y esa
        # traducción es la que nadie escribió y cada tanda reinventaba.
        valores = {m: (f"{{{v.strip('{}').replace('.', '/')}}}"
                       if isinstance(v, str) and v.startswith("{") else v)
                   for m, v in valores.items()}
        # Figma expresa la opacidad en PORCENTAJE (0–100); el sistema y el CSS la guardan
        # como proporción (0–1). Sin esta conversión, un 0.45 se resuelve como 0.0045 y el
        # estado deshabilitado se dibuja al medio por ciento: invisible. No da ningún error
        # —la variable queda atada y el verificador da verde—, así que solo se ve mirando
        # el archivo, o midiendo `node.opacity`.
        # Alcanza al PRIMITIVO además del semántico: el semántico solo lo aliasa, así que
        # convertir el alias no cambiaría nada — el valor real vive abajo.
        # El primitivo llega con BARRA —`opacidad/deshabilitado`— y el semántico con
        # punto: hay que partir por los dos o la conversión se salta justo el que guarda
        # el valor real.
        if "OPACITY" in alcance or re.split(r"[./]", nombre)[0] == "opacidad":
            valores = {m: (round(v * 100, 4) if isinstance(v, (int, float)) and v <= 1 else v)
                       for m, v in valores.items()}
        return {"nombre": nombre.replace(".", "/"), "tipo": tipo,
                "valoresPorModo": valores, "alcance": alcance,
                "ocultoEnPublicacion": oculto,
                "sintaxisPorPlataforma": nombres(nombre)}

    primitivas = []
    for grupo, valores in s.prim.items():
        if grupo.startswith("_") or not isinstance(valores, dict):
            continue
        for peldaño, v in valores.items():
            tipo = ("COLOR" if str(v).startswith("#")
                    else "FLOAT" if isinstance(v, (int, float)) or str(v).endswith("px")
                    else "STRING")
            # Sin alcance y ocultas: la lista vacía es lo que Figma entiende por
            # «no la ofrezcas en ningún sitio» — DS-X02. No hay valor «NINGUNO».
            primitivas.append(var(f"{grupo}/{peldaño}", tipo, {"valor": v},
                                  [], oculto=True))

    # Qué puede hacer cada familia de roles, en el vocabulario de Figma.
    ALCANCE = {"superficie": ["FRAME_FILL", "SHAPE_FILL"],
               "borde": ["STROKE_COLOR"],
               "texto": ["TEXT_FILL"],
               "accion": ["FRAME_FILL", "SHAPE_FILL", "STROKE_COLOR"],
               "estado": ["FRAME_FILL", "SHAPE_FILL", "TEXT_FILL", "STROKE_COLOR"],
               "espacio": ["GAP", "WIDTH_HEIGHT"],
               "forma": ["CORNER_RADIUS"]}

    # Y los que no se pueden deducir de la familia, porque la familia mezcla: `foco` lleva
    # un color y dos grosores, `campo` lleva colores, rellenos y un radio. El alcance va
    # por rol, que es donde de verdad se sabe qué puede hacer cada uno.
    ALCANCE_ROL = {
        "foco.color": ["STROKE_COLOR"],
        "foco.grosor": ["STROKE_FLOAT"], "foco.separacion": ["STROKE_FLOAT"],
        "borde.grosor": ["STROKE_FLOAT"],
        "entrada.fondo": ["FRAME_FILL", "SHAPE_FILL"],
        "entrada.fondo-deshabilitado": ["FRAME_FILL", "SHAPE_FILL"],
        "entrada.borde": ["STROKE_COLOR"], "entrada.borde-foco": ["STROKE_COLOR"],
        "entrada.borde-error": ["STROKE_COLOR"],
        "entrada.texto": ["TEXT_FILL"], "entrada.marcador": ["TEXT_FILL"],
        "entrada.relleno-x": ["GAP", "WIDTH_HEIGHT"],
        "entrada.relleno-y": ["GAP", "WIDTH_HEIGHT"],
        "entrada.forma": ["CORNER_RADIUS"], "entrada.alto": ["WIDTH_HEIGHT"],
        "opacidad.deshabilitado": ["OPACITY"],
        "velo.opacidad": ["OPACITY"], "velo.opacidad-saliendo": ["OPACITY"],
    }

    semanticas, tipografia, efectos = [], [], []
    for rol, v in s.roles().items():
        if es_sombra(v):
            # Un estilo de efecto, no una variable — mismo motivo que el estilo de texto.
            efectos.append({"nombre": rol.replace(".", "/"), "tipo": "DROP_SHADOW",
                            "desplazamientoX": 0, "desplazamientoY": v["y"],
                            "desenfoque": v["desenfoque"], "opacidad": v["opacidad"]})
            continue
        if isinstance(v, dict) and "tamaño" in v:
            for parte in ("tamaño", "peso"):
                tipografia.append(var(f"{rol}/{parte}", "FLOAT",
                                      {m: v[parte] for m in s.modos},
                                      ["FONT_SIZE"] if parte == "tamaño" else ["FONT_WEIGHT"]))
            continue
        porModo = {m: (v[m] if isinstance(v, dict) else v) for m in s.modos}
        raiz = rol.split(".")[0]
        # El tipo lo dicta el VALOR, no el prefijo del nombre. Deducirlo de la familia
        # funcionaba mientras cada familia era de un solo tipo; en cuanto una mezcla
        # —`foco.color` junto a `foco.grosor`— el prefijo miente, y Figma rechaza la
        # importación con «Mismatched variable resolved type».
        resuelto = s.valor(porModo[s.activo], s.activo)
        tipo = ("COLOR" if isinstance(resuelto, str) and resuelto.startswith("#")
                else "FLOAT" if isinstance(resuelto, (int, float))
                or str(resuelto).endswith("px") else "STRING")
        semanticas.append(var(rol, tipo, porModo,
                              ALCANCE_ROL.get(rol) or ALCANCE.get(raiz, ["ALL_SCOPES"])))

    # Un token de componente que cita un rol tipográfico completo NO es una variable:
    # en Figma una tipografía compuesta es un estilo de texto — DS-X04. Va en su propia
    # lista para que la etapa de componentes lo ate al estilo, no a un alias imposible.
    #
    # Y el tipo de un token de componente **lo dicta el semántico al que alias**: `ALIAS`
    # no existe como tipo en Figma, y una variable que aliasa a otra de distinto tipo se
    # rechaza con «Mismatched variable resolved type».
    tipo_de_semantico = {v["nombre"]: v["tipo"] for v in semanticas + tipografia}
    de_componente, a_estilo = [], []
    for t, a in s.comp_tok.items():
        if t.startswith("_"):
            continue
        rol = s.rol_tipografico(a)
        if rol:
            a_estilo.append({"token": t.replace(".", "/"), "estiloDeTexto": rol.replace(".", "/")})
            continue
        destino = a.strip("{}").replace(".", "/")
        tipo = tipo_de_semantico.get(destino)
        if tipo is None:
            sys.exit(f"«{t}» alias a «{a}», que no es un rol semántico. "
                     f"El nivel 3 solo cita el nivel 2 — DS-T02")
        de_componente.append(var(t, tipo, {"valor": a}, ["ALL_SCOPES"]))

    doc = {
        "_lee": "Formato de importación de variables. Tres colecciones, una por nivel. "
                "Los primitivos van ocultos: solo se usan como alias — DS-T03.",
        "_generado_por": "construir.py",
        "estilosDeTexto": a_estilo,
        "_lee_estilos": "Tokens de componente que citan un rol tipográfico entero. "
                        "No son variables: son estilos de texto. Una tipografía son tres "
                        "valores —tamaño, peso e interlineado— y una variable guarda uno.",
        "estilosDeEfecto": efectos,
        "_lee_efectos": "Las sombras, por el mismo motivo: son compuestas. Se crean con "
                        "figma.createEffectStyle() y su color es negro con la opacidad "
                        "declarada — DS-F08, solo sombra difusa.",
        "colecciones": [
            {"nombre": "1 · Primitivos", "modos": ["valor"],
             "_lee": "Se llaman por lo que SON. No cambian por modo. Ocultos de publicación",
             "variables": primitivas},
            {"nombre": "2 · Semánticos", "modos": s.modos,
             "_lee": "Se llaman por lo que HACEN. Acá viven los modos",
             "variables": semanticas + tipografia},
            {"nombre": "3 · Componentes", "modos": ["valor"],
             "_lee": "Dónde se aplica. Es lo único que una pantalla cita",
             "variables": de_componente},
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
        rampa.append(caja(grupo, direccion="fila", espacio="{espacio.pegado}",
                          alineacion="centro", hijos=[
            # El nombre de la rampa, DIBUJADO. El nombre del marco vive en el panel de
            # capas, y un archivo se lee mirando: sin esto son cinco filas de cuadrados
            # sin saber cuál es cuál.
            texto(grupo.split(".", 1)[1], "tipo.etiqueta")] + [
            # Con borde SIEMPRE: el peldaño 0 es blanco y el 1000 casi negro. Sin borde,
            # el extremo que coincide con la superficie desaparece y la rampa parece
            # empezar en 50.
            caja(f"{grupo}.{p}", fondo=f"{{{grupo}.{p}}}", forma="{forma.distintivo}",
                 borde="{borde.sutil}",
                 relleno="{espacio.interior}", hijos=[texto(str(p), "tipo.etiqueta")])
            for p in valores]))
    # Página · para empezar. Se abre sola la primera vez, y dice qué es el archivo.
    # El nombre está ANIDADO —`proyecto.proyecto.nombre`—: `s.proyecto` es el archivo
    # entero. Leerlo plano devuelve None y cae siempre al nombre del acento, así que la
    # portada de VIP se titulaba «cobalto».
    nom = ((s.proyecto.get("proyecto") or {}).get("nombre")
           or s.proyecto.get("nombre")
           or s.marca.get("identidad", {}).get("nombre_acento", "Sistema"))
    paginas.append({"nombre": "Para empezar", "nodos": [
        caja("Portada", espacio="{espacio.bloques}", relleno="{espacio.respiro}",
             fondo="{superficie.base}", hijos=[
                 texto(nom, "tipo.display"),
                 texto(f"Sistema de diseño · versión {s.marca.get('version', '1.0.0')}",
                       "tipo.subtitulo", "texto.secundario"),
                 texto("Los tokens mandan. Esta es una salida: si algo no cuadra, "
                       "se corrige en el JSON y se vuelve a publicar — DS-X01.",
                       "tipo.cuerpo", "texto.secundario")])]})

    paginas.append({"nombre": "Tokens", "nodos": [
        caja("Color", espacio="{espacio.bloques}", fondo="{superficie.base}",
             hijos=[texto("Color", "tipo.titulo")] + rampa),
        caja("Tipografía", espacio="{espacio.fila}", fondo="{superficie.base}",
             hijos=[texto("Tipografía", "tipo.titulo")] + [
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
        tamanos = c.get("tamanos") or []
        ejemplo = c.get("ejemplo") or ""
        filas = []
        for v in variantes:
            # Cada instancia va con SU delta ya resuelto. Sin esto el nodo solo decía
            # «estado: foco» y quien dibujaba no tenía de dónde sacar qué significa, así
            # que dibujaba el mismo nodo una vez por estado — DS-C03.
            muestras = []
            for e in estados:
                muestras.append(caja(f"{nombre}/{v}/{e}", espacio="{espacio.pegado}", hijos=[
                    texto(e, "tipo.etiqueta", "texto.secundario"),
                    {"tipo": "instancia", "componente": nombre,
                     "propiedades": {"variante": v, "estado": e},
                     "contenido": ejemplo,
                     "tokens": c.get("tokens", {}),
                     "cambia": delta(e, v, c.get("tokens") or {})}]))
            filas.append(caja(f"{nombre}/{v}", direccion="fila", espacio="{espacio.fila}",
                              hijos=[texto(v, "tipo.etiqueta", "texto.secundario")] + muestras))
        # Los tamaños van en su propia fila, no como tercer eje de variante: cruzarlos
        # multiplicaría la matriz —`boton` pasaría de 20 a 60— y el propio contrato la
        # topa en 30. Una fila basta para que se vea que `sm`, `md` y `lg` NO miden igual,
        # que es lo que la lista de comprobación pide y antes no se podía cumplir porque
        # el tamaño no se emitía en ninguna parte.
        if tamanos:
            base = variantes[0]
            filas.append(caja(f"{nombre}/tamaños", direccion="fila", espacio="{espacio.fila}",
                              hijos=[texto("tamaños", "tipo.etiqueta", "texto.secundario")] + [
                caja(f"{nombre}/tamaño/{t}", espacio="{espacio.pegado}", hijos=[
                    texto(t, "tipo.etiqueta", "texto.secundario"),
                    {"tipo": "instancia", "componente": nombre,
                     "propiedades": {"variante": base, "estado": estados[0], "tamaño": t},
                     "contenido": ejemplo,
                     "tokens": c.get("tokens", {}),
                     "alto": f"{{control.{t}}}",
                     "cambia": {}}]) for t in tamanos]))
        nodos.append(caja(nombre, espacio="{espacio.fila}", fondo="{superficie.base}", hijos=[
            texto(nombre, "tipo.seccion"),
            texto(c.get("descripcion", ""), "tipo.apoyo", "texto.secundario"),
            texto(f"{len(variantes)} variantes × {len(estados)} estados = "
                  f"{len(variantes) * len(estados)}", "tipo.etiqueta", "texto.secundario")] + filas))
    paginas.append({"nombre": "Componentes", "nodos": nodos})

    # Las tres que faltaban para las seis de DS-H01. Se emiten aunque vengan vacías: una
    # página con su nombre y su hueco dice dónde va lo que falta; no emitirla deja al que
    # dibuja apilándolo todo en «Componentes», que es como quedó el archivo que motivó esto.
    def catalogo(titulo, entradas, vacio):
        # `proposito` es la clave de un patrón o una plantilla; `descripcion` la de un
        # componente. Sin el segundo intento se emitían nodos de texto vacíos — DS-X13.
        cuerpo = []
        for n, d in entradas.items():
            if n.startswith("_"):
                continue
            pie = (d or {}).get("descripcion") or (d or {}).get("proposito") or ""
            cuerpo.append(caja(n, espacio="{espacio.pegado}", hijos=[texto(n, "tipo.seccion")]
                               + ([texto(pie, "tipo.apoyo", "texto.secundario")] if pie else [])))
        # Con fondo: un marco raíz sin fondo se dibuja transparente sobre el gris del
        # lienzo, y ahí la mitad de la paleta —`superficie.hundida`, `accion.tenue`— no
        # se distingue del vacío.
        return [caja(titulo, espacio="{espacio.fila}", fondo="{superficie.base}",
                     hijos=[texto(titulo, "tipo.titulo")]
                     + (cuerpo or [texto(vacio, "tipo.cuerpo", "texto.secundario")]))]

    paginas.append({"nombre": "Patrones", "nodos": catalogo(
        "Patrones", s.patrones, "Todavía no hay patrones. Un patrón es una combinación "
        "de componentes que se repite — la skill extend-system los agrega.")})
    paginas.append({"nombre": "Plantillas", "nodos": catalogo(
        "Plantillas", s.plantillas, "Todavía no hay plantillas.")})
    paginas.append({"nombre": "Anotaciones", "nodos": catalogo(
        "Anotaciones", {}, "Los ayudantes de documentación: notas de medida, de "
        "comportamiento y de accesibilidad que acompañan a las pantallas.")})

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
                d = delta(e, v, toks)
                fondo = d.get("fondo") or toks.get(f"{v}.fondo") or toks.get("fondo") \
                    or "superficie.elevada"
                col = d.get("texto") or toks.get(f"{v}.texto") or toks.get("texto") \
                    or "texto.principal"
                borde = d.get("borde") or toks.get("borde") or "borde.sutil"
                estilo = (f"background:var(--{kebab(fondo)});color:var(--{kebab(col)});"
                          + f"border-color:var(--{kebab(borde)});")
                if "opacidad" in d:
                    estilo += f"opacity:var(--{kebab(d['opacidad'])});"
                celdas.append(f'<div class="celda"><span class="et">{e}</span>'
                              f'<span class="muestra{" foco" if "anillo" in d else ""}" '
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
        pedidas = [k for k, v in (s.proyecto.get("outputs") or {}).items()
                   if v is True and k in GENERADORES]
    desconocidas = [p for p in pedidas if p not in GENERADORES]
    if desconocidas:
        sys.exit(f"no sé generar: {', '.join(desconocidas)}. Conozco: {', '.join(SALIDAS)}")
    if not pedidas:
        sys.exit("ninguna salida pedida — usa --salidas o activa alguna en proyecto.json")

    # css primero: la galería lo reutiliza en vez de volver a derivarlo
    pedidas.sort(key=lambda x: 0 if x == "css" else 1)

    base = s.raiz / "outputs"
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
