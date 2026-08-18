#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paquete.py — comprueba que el complemento lleve consigo lo que sus guiones necesitan.

    python3 pruebas/paquete.py

**Dejar un archivo en la carpeta correcta no es lo mismo que empaquetarlo.** Un guion que
abre `referencias/figma-api.json` funciona perfecto acá, donde el archivo está al lado, y
falla en la máquina de quien instale el complemento si ese archivo no viajó — por quedar
fuera de `.gitignore`, o por no estar donde la ruta lo busca.

Es el mismo error que ya costó caro dos veces en este repositorio, con otra ropa: **algo
que se da por cierto y nadie ejecuta**. El puente de Figma se escribió leyendo el manual
y nunca se corrió contra Figma; las cifras de `plugin.json` se escribieron a mano y nadie
las volvió a mirar. Acá se comprueban las tres cosas:

1. **Todo archivo que un guion abre en ejecución existe** donde la ruta dice.
2. **Todo archivo que una skill manda leer existe** — los que se citan como
   `${CLAUDE_SKILL_DIR}/referencias/…` en prosa. Son la mitad silenciosa: no los abre
   ningún guion, los abre el agente, y `enlaces.py` no los ve porque no son enlaces de
   Markdown sino texto entre comillas invertidas.
3. **Ninguno está excluido del control de versiones** — si `.gitignore` lo tapa, no viaja.
4. **Las cifras que `plugin.json` anuncia son las reales**, contadas de la base de
   conocimiento en vez de recordadas.

Solo biblioteca estándar.
"""

import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from comun import cargar_reglas, raiz_plugin  # noqa: E402

VERDE, GRIS, ROJO, FIN = "\033[32m", "\033[90m", "\033[31m", "\033[0m"

# Las rutas se descubren leyendo el código, no se enumeran acá. Una lista escrita a mano
# falla de las dos maneras de siempre: deja fuera lo que nadie agregó, y calla cuando un
# archivo cambia de nombre.
_RUTA = re.compile(r'raiz_plugin\(\)\s*/\s*"([^"]+)"|'
                   r'raiz or raiz_plugin\(\)\)\s*/\s*"([^"]+)"')

# Lo que una skill manda leer. Se escribe entre comillas invertidas y con la variable
# de ruta delante, y por eso no es un enlace de Markdown y `enlaces.py` no lo revisa.
_CITA = re.compile(r'\$\{(CLAUDE_SKILL_DIR|CLAUDE_PLUGIN_ROOT)\}/([A-Za-z0-9_./-]+)')


def rutas_en_ejecucion(raiz):
    """Los archivos que los guiones abren relativos a la raíz del complemento."""
    encontradas = {}
    for py in sorted(raiz.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        for m in _RUTA.finditer(py.read_text(encoding="utf-8")):
            ruta = m.group(1) or m.group(2)
            encontradas.setdefault(ruta, []).append(str(py.relative_to(raiz)))
    return encontradas


# `docs/90-…` es el informe de una auditoría: cita rutas rotas **como hallazgo**, y
# corregirlas ahí borraría lo que el documento denuncia. Se excluye por eso, no por
# comodidad. `__pycache__` no es documentación.
EXCLUIDOS = {"__pycache__"}
INFORMES = ("docs/90-",)


def raiz_de_la_skill(raiz, doc):
    """La carpeta de la skill a la que pertenece un documento, o None si no es de una.

    Es la que está justo debajo de `skills/`. Se busca subiendo, no adivinando por el
    nombre: un documento puede estar a cualquier profundidad dentro de la skill.
    """
    partes = doc.relative_to(raiz).parts
    if len(partes) < 2 or partes[0] != "skills":
        return None
    return raiz / "skills" / partes[1]


def rutas_citadas(raiz):
    """Los archivos que una skill o un comando manda leer.

    `${CLAUDE_SKILL_DIR}` es **la raíz de la skill**, no la carpeta del archivo que lo
    escribe: una referencia dentro de `referencias/` que cite `${CLAUDE_SKILL_DIR}/scripts/x.py`
    apunta a `skills/<skill>/scripts/x.py`, no a `skills/<skill>/referencias/scripts/x.py`.
    Resolverlo contra la carpeta del archivo inventa rutas que no existen y reporta
    fallos falsos — pasó en la primera versión de esta comprobación.

    `${CLAUDE_PLUGIN_ROOT}` se resuelve contra la raíz del complemento.
    """
    encontradas = {}
    for doc in sorted(raiz.rglob("*.md")):
        rel = str(doc.relative_to(raiz))
        if EXCLUIDOS & set(doc.parts) or "conocimiento/sources" in rel:
            continue
        if rel.startswith(INFORMES):
            continue
        texto = doc.read_text(encoding="utf-8")
        for var, cola in _CITA.findall(texto):
            if var == "CLAUDE_SKILL_DIR":
                base = raiz_de_la_skill(raiz, doc)
                if base is None:
                    continue               # lo cita algo que no es una skill: no aplica
            else:
                base = raiz
            destino = (base / cola).resolve()
            try:
                ruta = str(destino.relative_to(raiz))
            except ValueError:
                continue                   # apunta fuera del complemento: no es cosa nuestra
            encontradas.setdefault(ruta, []).append(str(doc.relative_to(raiz)))
    return encontradas


def ignorados(raiz, rutas):
    """Cuáles de esas rutas quedarían fuera del control de versiones."""
    if not (raiz / ".git").exists():
        return None  # todavía no es un repositorio: no hay nada que preguntar
    fuera = []
    for r in rutas:
        p = subprocess.run(["git", "-C", str(raiz), "check-ignore", "-q", r],
                           capture_output=True)
        if p.returncode == 0:
            fuera.append(r)
    return fuera


def cifras_del_manifiesto(raiz, reglas):
    """¿Lo que `plugin.json` anuncia coincide con lo que hay?"""
    doc = raiz / ".claude-plugin/plugin.json"
    if not doc.exists():
        return ["falta .claude-plugin/plugin.json"]
    texto = doc.read_text(encoding="utf-8")
    manifiesto = json.loads(texto)
    desc = manifiesto.get("description", "")

    total = len(reglas)
    auto = sum(1 for v in reglas.values() if v["verifica"] == "auto")
    fallos = []

    m = re.search(r"(\d+)\s+reglas DS-xxx", desc)
    if not m:
        fallos.append("la descripción no dice cuántas reglas DS-xxx trae el complemento")
    elif int(m.group(1)) != total:
        fallos.append(f"la descripción anuncia {m.group(1)} reglas y hay {total}")

    m = re.search(r"de las que (\d+) se comprueban", desc)
    if not m:
        fallos.append("la descripción no dice cuántas reglas se comprueban con guiones")
    elif int(m.group(1)) != auto:
        fallos.append(f"la descripción anuncia {m.group(1)} comprobadas y hay {auto}")

    return fallos


def main():
    raiz = raiz_plugin()
    print("══ El paquete lleva lo que los guiones leen\n")

    porGuion = rutas_en_ejecucion(raiz)
    porSkill = rutas_citadas(raiz)
    if not porGuion or not porSkill:
        print(f"{ROJO}✗{FIN} no se descubrieron rutas de una de las dos clases: "
              f"algún patrón dejó de reconocerlas")
        return 1

    # Las dos clases se juntan acá: al paquete le da igual quién abra el archivo.
    rutas = {}
    for origen, mapa in (("guion", porGuion), ("skill", porSkill)):
        for r, quienes in mapa.items():
            rutas.setdefault(r, []).extend(f"{q}" for q in quienes)

    fallos = 0
    for ruta, quienes in sorted(rutas.items()):
        clase = "lo abre un guion" if ruta in porGuion else "lo manda leer una skill"
        if (raiz / ruta).exists():
            print(f"   {VERDE}✓{FIN} {ruta}")
            print(f"     {GRIS}{clase}: {' · '.join(sorted(set(quienes)))}{FIN}")
        else:
            fallos += 1
            print(f"   {ROJO}✗{FIN} {ruta} — no existe, y {clase}: "
                  f"{' · '.join(sorted(set(quienes)))}")

    fuera = ignorados(raiz, rutas)
    print()
    if fuera is None:
        print(f"   {GRIS}·{FIN} todavía no es un repositorio de git: "
              f"no se puede preguntar qué queda fuera")
    elif fuera:
        fallos += len(fuera)
        for r in fuera:
            print(f"   {ROJO}✗{FIN} {r} está en .gitignore: no viaja con el complemento")
    else:
        print(f"   {VERDE}✓{FIN} ninguna queda fuera del control de versiones")

    print("\n══ El manifiesto dice la verdad\n")
    problemas = cifras_del_manifiesto(raiz, cargar_reglas(raiz))
    if problemas:
        fallos += len(problemas)
        for p in problemas:
            print(f"   {ROJO}✗{FIN} {p}")
        print(f"     {GRIS}Se edita en .claude-plugin/plugin.json{FIN}")
    else:
        print(f"   {VERDE}✓{FIN} las cifras de plugin.json coinciden con las reglas reales")

    print()
    if fallos:
        print(f"{ROJO}{fallos} problemas de empaquetado{FIN}")
        return 1
    print(f"{VERDE}El paquete está completo.{FIN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
