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

# El historial cita a propósito nombres y cifras que ya no son los de hoy: eso es lo que
# un registro de cambios hace. Corregirlo sería reescribir la historia.
HISTORICOS = ("docs/05-registro-de-cambios.md",)


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


# ═══ Lo que el complemento anuncia de cara al usuario ═════════════════════════
#
# `plugin.json` no es la única boca del complemento. Las mismas cifras se repiten en el
# archivo de presentación, en el catálogo y en la documentación, y **la copia que nadie
# vuelve a mirar es la que miente**: el complemento anunció 83 reglas y 50 comprobadas
# durante toda la versión 1.5.0 de desarrollo, cuando ya eran 87 y 54, porque la
# comprobación existía y miraba un solo archivo.
#
# El registro de cambios y los informes fechados NO son superficie viva: sus cifras eran
# ciertas en su versión, y "corregirlas" sería reescribir la historia.
# `03-referencia-de-reglas.md` tampoco entra: lo genera `generar_referencia.py` desde la
# base de conocimiento y la etapa 4 ya comprueba que esté al día — mirarlo acá sería
# comprobar dos veces lo mismo, y sus recuentos por familia («12 reglas») no son el total.
SUPERFICIES = (
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "README.md",
    "docs/01-guia-de-uso.md",
    "docs/02-arquitectura.md",
    "docs/04-contribuir.md",
)

# Las tres formas en que hoy se anuncia una cifra. Se anclan a propósito: un `\d+ reglas`
# suelto captura los recuentos por familia y convierte la comprobación en ruido.
_CLAIMS = (
    ("total", re.compile(r"[Ll]as\s+(\d+)\s+reglas")),
    ("total", re.compile(r"(\d+)\s+reglas DS-xxx")),
    ("total", re.compile(r"reglas-(\d+)%20")),
    ("auto",  re.compile(r"(\d+)\s+comprobadas")),
    ("auto",  re.compile(r"de las que (\d+) se comprueban")),
    ("auto",  re.compile(r"%20(\d+)%20comprobadas")),
)

# Por debajo de esto, la comprobación se quedó ciega: alguien cambió la redacción y los
# patrones dejaron de reconocerla. Un cero no es un verde, es una pregunta sin hacer.
MINIMO_CLAIMS = 8


def cifras_publicadas(raiz, reglas):
    """Toda cifra anunciada en una superficie viva es la real.

    Devuelve (fallos, cuántas afirmaciones se encontraron). La segunda importa tanto como
    la primera: si no se encontró ninguna, el verde no significa que las cifras estén bien
    sino que no se leyó ninguna.
    """
    real = {"total": len(reglas),
            "auto": sum(1 for v in reglas.values() if v["verifica"] == "auto")}
    fallos, vistas = [], 0

    for rel in SUPERFICIES:
        doc = raiz / rel
        if not doc.exists():
            fallos.append(f"{rel} — la superficie no existe; si se quitó, sacala de SUPERFICIES")
            continue
        for nro, linea in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for clase, patron in _CLAIMS:
                for m in patron.finditer(linea):
                    vistas += 1
                    dice = int(m.group(1))
                    if dice != real[clase]:
                        que = "reglas" if clase == "total" else "comprobadas"
                        fallos.append(f"{rel}:{nro} anuncia {dice} {que} y hay {real[clase]}")
    return fallos, vistas


# ═══ Los nombres que el usuario escribe ══════════════════════════════════════
#
# Un comando citado en la documentación es una promesa ejecutable: quien lo escribe
# espera que pase algo. Cuando las ocho capacidades se renombraron, los seis slugs que
# la documentación citaba dejaron de existir **y todo siguió en verde**, porque no son
# enlaces de Markdown y `enlaces.py` no los ve.

# Las dos formas en que la documentación nombra un comando: la larga
# —`/design-system:audit-system`— y la abreviada de las tablas —`` `:audit-system` ``—.
# **La abreviada importa más**, porque es la que usan las dos tablas de capacidades y es
# donde los seis slugs muertos sobrevivieron a un renombrado entero. La segunda se ancla
# entre comillas invertidas: un `:palabra` suelto en prosa no es una promesa ejecutable.
_COMANDOS = (re.compile(r"design-system:([a-z0-9][a-z0-9-]*)"),
             re.compile(r"`:([a-z0-9][a-z0-9-]*)`"))
_SKILL_CITADA = re.compile(r"skill\s+`([a-z0-9][a-z0-9-]*)`")
_NOMBRE_FM = re.compile(r"^name:\s*(\S+)\s*$", re.M)

# Dónde se le enseña al usuario qué escribir. Lo mismo que arriba: el historial cita
# nombres viejos porque documenta el renombrado, y eso es correcto.
VITRINAS = ("README.md", "docs/01-guia-de-uso.md")


def nombres(raiz):
    """Los cuatro invariantes de nombre que el renombrado rompió en silencio."""
    fallos = []
    comandos = {p.stem for p in (raiz / "commands").glob("*.md")}
    skills = {p.parent.name for p in (raiz / "skills").glob("*/SKILL.md")}

    # 1 · Todo comando citado existe.
    citados = {}
    for doc in sorted(raiz.rglob("*.md")):
        rel = str(doc.relative_to(raiz))
        if EXCLUIDOS & set(doc.parts) or "conocimiento/sources" in rel:
            continue
        if rel.startswith(INFORMES) or rel in HISTORICOS:
            continue
        for nro, linea in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for patron in _COMANDOS:
                for slug in patron.findall(linea):
                    citados.setdefault(slug, []).append(f"{rel}:{nro}")
    for slug, donde in sorted(citados.items()):
        if slug not in comandos:
            fallos.append(f"se cita /design-system:{slug} y no existe commands/{slug}.md "
                          f"— {' · '.join(donde[:3])}")

    # 2 · Todo comando está en la vitrina. Uno que nadie cita es uno que nadie encuentra.
    en_vitrina = set()
    for rel in VITRINAS:
        doc = raiz / rel
        if doc.exists():
            texto = doc.read_text(encoding="utf-8")
            for patron in _COMANDOS:
                en_vitrina |= set(patron.findall(texto))
    for c in sorted(comandos - en_vitrina):
        fallos.append(f"commands/{c}.md no se cita en {' ni en '.join(VITRINAS)}: nadie lo encuentra")

    # 3 · Todo comando delega en una skill que existe.
    for p in sorted((raiz / "commands").glob("*.md")):
        citadas = set(_SKILL_CITADA.findall(p.read_text(encoding="utf-8")))
        if not citadas:
            fallos.append(f"commands/{p.name} no dice en qué skill delega")
        for s in sorted(citadas - skills):
            fallos.append(f"commands/{p.name} delega en la skill `{s}`, que no existe")

    # 4 · El `name:` del frontmatter es el nombre de la carpeta. Si no coinciden, Claude
    #     Code carga la skill con otro nombre del que todo el mundo escribió.
    for p in sorted((raiz / "skills").glob("*/SKILL.md")):
        m = _NOMBRE_FM.search(p.read_text(encoding="utf-8"))
        if not m:
            fallos.append(f"skills/{p.parent.name}/SKILL.md no declara `name:`")
        elif m.group(1) != p.parent.name:
            fallos.append(f"skills/{p.parent.name}/SKILL.md declara name: {m.group(1)}, "
                          f"y la carpeta se llama {p.parent.name}")

    return fallos, len(citados) + len(comandos) + len(skills)


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

    reglas = cargar_reglas(raiz)

    print("\n══ El manifiesto dice la verdad\n")
    problemas = cifras_del_manifiesto(raiz, reglas)
    if problemas:
        fallos += len(problemas)
        for p in problemas:
            print(f"   {ROJO}✗{FIN} {p}")
        print(f"     {GRIS}Se edita en .claude-plugin/plugin.json{FIN}")
    else:
        print(f"   {VERDE}✓{FIN} las cifras de plugin.json coinciden con las reglas reales")

    print("\n══ Y lo mismo dicen las demás superficies\n")
    problemas, vistas = cifras_publicadas(raiz, reglas)
    if problemas:
        fallos += len(problemas)
        for p in problemas:
            print(f"   {ROJO}✗{FIN} {p}")
    elif vistas < MINIMO_CLAIMS:
        fallos += 1
        print(f"   {ROJO}✗{FIN} solo se reconocieron {vistas} cifras anunciadas y se esperaban "
              f"al menos {MINIMO_CLAIMS}: la redacción cambió y los patrones quedaron ciegos")
        print(f"     {GRIS}Un cero acá no es un verde: es no haber leído nada.{FIN}")
    else:
        print(f"   {VERDE}✓{FIN} {vistas} cifras anunciadas en {len(SUPERFICIES)} superficies, "
              f"todas iguales a las reales")

    print("\n══ Los nombres que el usuario escribe existen\n")
    problemas, mirados = nombres(raiz)
    if problemas:
        fallos += len(problemas)
        for p in problemas:
            print(f"   {ROJO}✗{FIN} {p}")
    else:
        print(f"   {VERDE}✓{FIN} comandos citados, comandos en vitrina, skills delegadas y "
              f"`name:` de cada skill — {mirados} nombres cruzados")

    print()
    if fallos:
        print(f"{ROJO}{fallos} problemas de empaquetado{FIN}")
        return 1
    print(f"{VERDE}El paquete está completo.{FIN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
