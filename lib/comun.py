#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comun.py — lo que comparten los verificadores del plugin.

Existe por la regla 3 de `system-design`: «nada se escribe a mano dos veces. Si un
valor aparece en dos archivos, uno de los dos va a quedar viejo». Cuatro guiones
—verificar, verificar-screen, entregar, probar, auditar— necesitaban el mismo
resultado, el mismo veredicto y el mismo cálculo de contraste. Ahora lo toman de acá.

Y la parte que más importa: `cargar_reglas()` **lee las reglas de la base de conocimiento**, no de
una copia. Una regla que exista en `09-rules/README.md` y que ningún guion compruebe
aparece sola en el informe de cobertura. Es lo que impide que una regla quede
huérfana sin que nadie se entere.

Solo biblioteca estándar.
"""

import json
import pathlib
import re
import sys

# ═══ Color ═══════════════════════════════════════════════════════════════════

MIN_TEXTO, MIN_NO_TEXTO = 4.5, 3.0


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
    """Lo que devuelve una comprobación: cuántas cosas miró, cuáles fallaron, o por qué no corrió.

    Los tres estados no son decorativos. `saltada` existe porque una comprobación que
    no corrió **no es un verde**: es una pregunta que quedó sin hacer, y callarla la
    convierte en un verde que miente.
    """

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


# ═══ El veredicto de --romper ════════════════════════════════════════════════

def juzgar(regla, resultados, fallos_ajenos):
    """El veredicto es de la regla que se rompió, no del total.

    Un fallo de otra comprobación no prueba nada: si el veredicto mirara el total, una
    comprobación rota daría verde porque falló su vecina. Y una comprobación saltada no
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


# ═══ El informe ══════════════════════════════════════════════════════════════

class Reporte:
    """Acumula resultados por eje, los imprime y devuelve el código de salida.

    Lo comparten los cinco guiones para que un fallo se lea igual en todos. Un usuario
    que aprendió a leer la salida de `verificar.py` ya sabe leer la de `deliver.py`.
    """

    def __init__(self, titulo, romper=None, solo=None):
        self.romper, self.solo = romper, solo
        self.ok = self.mal = 0
        self.saltadas, self.del_objetivo, self.ajenos = [], [], 0
        if titulo:
            print(f"{titulo}\n")

    def eje(self, nombre, resultados):
        filas = []
        for r in resultados:
            # Cero elementos comprobados no es un éxito: la comprobación corrió sin nada
            # que mirar. Contarlo en verde es el salto disfrazado.
            if r.saltada is None and not r.fallos and r.n == 0:
                r.saltada = "corrió sin nada que comprobar"
            if self.romper:
                if r.regla == self.romper:
                    self.del_objetivo.append(r)
                else:
                    self.ajenos += len(r.fallos)
            if self.solo and r.regla != self.solo:
                continue
            filas.append(r)
        if not filas:
            return
        print(f"── {nombre}")
        for r in filas:
            if r.saltada:
                self.saltadas.append((r.regla, r.nombre, r.saltada))
                print(f"   ·  {r.regla:8} {r.nombre:52} saltada")
            elif r.fallos:
                self.mal += len(r.fallos)
                self.ok += r.n
                print(f"   ✗  {r.regla:8} {r.nombre:52} {len(r.fallos)} fallos")
                for f in r.fallos[:8]:
                    print(f"        {f}")
                if len(r.fallos) > 8:
                    print(f"        … y {len(r.fallos) - 8} más")
            else:
                self.ok += r.n
                print(f"   ✓  {r.regla:8} {r.nombre:52} {r.n}")
        print()

    def cerrar(self):
        print(f"{self.ok} comprobaciones en verde · {self.mal} fallos"
              + (f" · {len(self.saltadas)} saltadas" if self.saltadas else ""))
        if self.saltadas:
            print("\nSaltadas — no son verdes, son preguntas sin hacer:")
            for regla, nombre, motivo in self.saltadas:
                print(f"   {regla:8} {nombre:52} {motivo}")
        if self.romper:
            return juzgar(self.romper, self.del_objetivo, self.ajenos)
        return 1 if self.mal else 0


# ═══ El inventario ═══════════════════════════════════════════════════════════

def tabla(datos, clave):
    """Una tabla del inventario, sin las notas.

    **Las claves que empiezan con guion bajo son notas, no entradas.** Se filtran acá,
    una vez, en vez de en cada comprobación: la que se olvide de saltarlas recibe una
    cadena donde espera un objeto y revienta con un error que no dice qué pasó.

    Lo aprendimos rompiéndolo: agregar un `_lee` a `plantillas.json` tumbó cuatro
    verificadores de golpe.
    """
    crudo = (datos or {}).get(clave) or {}
    return {k: v for k, v in crudo.items()
            if not str(k).startswith("_") and isinstance(v, dict)}


# ═══ Las reglas, leídas de la base de conocimiento ═════════════════════════════════════════════

FAMILIAS = {"F": "Fundamentos", "T": "Tokens", "C": "Componentes", "L": "Disposición",
            "P": "Patrones", "A": "Accesibilidad", "H": "Entrega", "X": "Puente con Figma"}

_FILA = re.compile(
    r"^\|\s*\*\*([FTCLPAHX]\d\d)\*\*\s*\|\s*(.+?)\s*\|\s*(OBLIGATORIO|RECOMENDADO)\s*\|\s*(.*?)\s*\|\s*(.+?)\s*\|\s*$")


def raiz_plugin():
    """La raíz del plugin, desde este archivo. `lib/comun.py` → dos niveles arriba."""
    return pathlib.Path(__file__).resolve().parents[1]


def contrato_figma(raiz=None):
    """El contrato de la API de variables de Figma, verificado contra el servidor.

    **Lo leen el generador y el verificador, del mismo archivo.** Mientras cada uno
    supuso por su cuenta qué acepta Figma, el generador emitía un vocabulario propio
    —`RELLENO_FORMA`, `ALIAS`— y el verificador daba verde, porque comprobaba las reglas
    del sistema y nunca las de Figma. El archivo se importaba igual **solo porque alguien
    lo traducía a mano en cada tanda**, y esa traducción no estaba escrita en ningún lado.

    Devuelve el JSON tal cual: alcances, plataformas, tipos, reglas de nombre y de valor,
    y la lista explícita de lo que NO se verificó.
    """
    doc = (raiz or raiz_plugin()) / "skills/system-design/referencias/figma-api.json"
    if not doc.exists():
        sys.exit(f"falta el contrato de la API de Figma: {doc}")
    return json.loads(doc.read_text(encoding="utf-8"))


def cargar_reglas(raiz=None):
    """Las reglas tal como están escritas en `09-rules/README.md`.

    Se leen, no se copian. Una copia se desincroniza en la primera edición de la base de conocimiento —
    y entonces el guion comprueba una regla que ya no dice lo que dice el documento.

    Devuelve {id: {enunciado, nivel, verifica, origen, familia}}.
    """
    doc = (raiz or raiz_plugin()) / "conocimiento/DESIGN/09-rules/README.md"
    if not doc.exists():
        sys.exit(f"falta la base de conocimiento: {doc}")
    reglas = {}
    for linea in doc.read_text(encoding="utf-8").splitlines():
        m = _FILA.match(linea)
        if not m:
            continue
        num, enunciado, nivel, verifica, origen = m.groups()
        reglas["DS-" + num] = {
            "enunciado": enunciado.replace("**", "").strip(),
            "nivel": nivel,
            # La base de conocimiento marca en negrita las que más le importan; la negrita no es un valor.
            "verifica": verifica.replace("*", "").strip() or "—",
            "origen": origen.strip(),
            "familia": FAMILIAS[num[0]],
        }
    if len(reglas) < 70:
        sys.exit(f"la tabla de reglas de la base de conocimiento no se pudo leer entera: {len(reglas)} filas")
    return reglas
