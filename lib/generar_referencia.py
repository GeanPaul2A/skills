#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_referencia.py — produce `docs/03-referencia-de-reglas.md` desde la base de conocimiento.

    python3 lib/generar_referencia.py              escribe el documento
    python3 lib/generar_referencia.py --comprobar  falla si el documento está desactualizado

**No se escribe a mano, y el motivo es el mismo que gobierna todo el complemento:** un
documento que enumera las reglas y se mantiene aparte se desincroniza en la primera
edición de la base de conocimiento. Desde ahí la referencia describe un sistema que ya
no existe, y es peor que no tenerla — porque parece autorizada.

`--comprobar` corre dentro de la suite. Si alguien agrega una regla y no regenera este
documento, la suite falla y dice cómo arreglarlo.

Solo biblioteca estándar.
"""

import argparse
import pathlib
import re
import subprocess
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comun import FAMILIAS, cargar_reglas, raiz_plugin  # noqa: E402

DESTINO = "docs/03-referencia-de-reglas.md"

# En qué sección de la base de conocimiento vive cada familia de reglas.
SECCION = {"Fundamentos": "01-foundations", "Tokens": "02-tokens",
           "Componentes": "03-components", "Disposición": "04-auto-layout",
           "Patrones": "05-patterns", "Accesibilidad": "06-accessibility",
           "Entrega": "07-handoff", "Puente con Figma": "08-figma-bridge"}

METODO = {
    "auto": ("Automática", "Un guion la comprueba sola"),
    "semi": ("Asistida", "Necesita renderizar o una herramienta externa"),
    "manual": ("Manual", "Requiere criterio de una persona"),
    "—": ("Declarativa", "Fija un objetivo; no se comprueba pieza por pieza"),
}


def guiones_por_regla(raiz):
    """Qué guion comprueba cada regla. Se lee del código, no de una lista mantenida aparte."""
    mapa = defaultdict(set)
    for archivo in sorted((raiz / "skills").rglob("*.py")):
        texto = archivo.read_text(encoding="utf-8")
        for regla in set(re.findall(r"DS-[A-Z][0-9]{2}", texto)):
            mapa[regla].add(archivo.name)
    return mapa


def rompibles(raiz):
    """Qué reglas tienen un caso de error inyectado. Se le pregunta a cada guion."""
    destino = "/tmp/referencia-reglas"
    subprocess.run([str(raiz / "pruebas/construir.sh"), destino],
                   capture_output=True, text=True)
    invocaciones = [
        ["skills/system-design/scripts/verificar.py", "--destino", destino],
        ["skills/deliver/scripts/deliver.py", "--destino", destino],
        ["skills/screen/scripts/verificar-screen.py", "--sistema", destino,
         "--screens", f"{destino}/screens"],
        ["skills/audit/scripts/audit.py", "--destino", destino,
         "--screens", f"{destino}/screens"],
        ["skills/test/scripts/test.py", "--sistema", destino,
         "--screens", f"{destino}/screens"],
    ]
    conjunto = set()
    for inv in invocaciones:
        guion = raiz / inv[0]
        if not guion.exists():
            continue
        salida = subprocess.run(["python3", str(guion)] + inv[1:] + ["--romper", "lista"],
                                capture_output=True, text=True)
        conjunto |= set(salida.stdout.split())
    return conjunto


def recuento_esperado(reglas):
    """Las cifras que §9.11 de la base de conocimiento debería declarar.

    Se calculan leyendo las ocho tablas de reglas, que son la fuente. **La sección del
    recuento está escrita a mano** —es prosa, no una salida generada— y por eso hay que
    comprobarla: es la única parte del documento que puede contradecir al resto de sí
    mismo sin que nada se note.

    Devuelve una lista de pares (qué dice ser, qué es), en el orden en que aparecen.
    """
    filas = []
    for letra, fam in FAMILIAS.items():
        dela = {k: v for k, v in reglas.items() if v["familia"] == fam}
        conteo = [len(dela)]
        conteo.append(sum(1 for v in dela.values() if v["nivel"] == "OBLIGATORIO"))
        conteo += [sum(1 for v in dela.values() if v["verifica"] == m)
                   for m in ("auto", "semi", "manual", "—")]
        filas.append((f"{fam} · `{letra}`", conteo))
    total = [sum(f[1][i] for f in filas) for i in range(6)]
    pura = sorted(k for k, v in reglas.items() if v["origen"].startswith("Extensión"))
    mezcla = sum(1 for v in reglas.values()
                 if "Extensión" in v["origen"] and not v["origen"].startswith("Extensión"))
    libro = sum(1 for v in reglas.values() if "Extensión" not in v["origen"])
    return filas, total, pura, mezcla, libro


def comprobar_recuento(reglas, raiz):
    """¿§9.11 dice la verdad? Devuelve la lista de desacuerdos, vacía si está al día."""
    doc = raiz / "conocimiento/DESIGN/09-rules/README.md"
    texto = doc.read_text(encoding="utf-8")
    filas, total, pura, mezcla, libro = recuento_esperado(reglas)
    fallos = []

    def celdas(linea):
        return [c.strip().replace("**", "").replace("`", "")
                for c in linea.strip().strip("|").split("|")]

    leidas = {}
    for linea in texto.splitlines():
        if linea.startswith("|") and linea.count("|") >= 7:
            c = celdas(linea)
            if len(c) == 7 and all(x.isdigit() or x == "—" for x in c[1:]):
                leidas[c[0]] = [0 if x == "—" else int(x) for x in c[1:]]

    for etiqueta, esperado in filas:
        clave = etiqueta.replace("`", "")
        if clave not in leidas:
            fallos.append(f"§9.11 no tiene fila para «{clave}»")
        elif leidas[clave] != esperado:
            fallos.append(f"§9.11 · fila «{clave}» dice {leidas[clave]} y las tablas dan {esperado}")
    if leidas.get("Total") != total:
        fallos.append(f"§9.11 · el total dice {leidas.get('Total')} y las tablas dan {total}")

    n = len(reglas)
    if f"**{n} reglas**" not in texto:
        fallos.append(f"§9.11 no abre con «**{n} reglas**»")
    suma = f"**{total[2]} + {total[3]} + {total[4]} + {total[5]} = {n}**"
    if suma not in texto:
        fallos.append(f"§9.11 · la marca de conteo no dice «{suma}»")

    for cifra, etiqueta in ((libro, "Salen enteras de los libros"),
                            (mezcla, "Mezclan libro y extensión"),
                            (len(pura), "Extensión pura")):
        if not re.search(rf"\|\s*\*?\*?{re.escape(etiqueta)}\*?\*?\s*\|\s*\*?\*?{cifra}\*?\*?\s*\|", texto):
            fallos.append(f"§9.11 · «{etiqueta}» debería decir {cifra}")
    if f"**Las {len(pura)} de extensión pura" not in texto:
        fallos.append(f"§9.11 · el párrafo de extensión pura no dice {len(pura)}")
    listado = " · ".join(f"`{k}`" for k in pura)
    if listado not in texto:
        fallos.append("§9.11 · la lista de reglas de extensión pura no coincide.\n"
                      f"     Debería ser:  {listado}")
    return fallos


def redactar(reglas, guiones, probadas):
    total = len(reglas)
    automaticas = [k for k, v in reglas.items() if v["verifica"] == "auto"]
    con_guion = [k for k in reglas if k in guiones]

    L = []
    A = L.append
    A("# Referencia de reglas")
    A("")
    A("> **Documento generado.** Lo produce `lib/generar_referencia.py` leyendo")
    A("> `conocimiento/DESIGN/09-rules/README.md` y los guiones de `skills/`.")
    A("> **No se edita a mano:** los cambios se hacen en la base de conocimiento y se")
    A("> regenera. La suite de pruebas falla si este documento queda desactualizado.")
    A(">")
    A(f"> **Estado.** {total} reglas · {len(automaticas)} automáticas · "
      f"{len(con_guion)} con guion que las comprueba · {len(probadas & set(reglas))} "
      f"probadas rompiéndolas a propósito.")
    A("")
    A("---")
    A("")
    A("## Índice")
    A("")
    A("1. [Cómo se lee una regla](#1--cómo-se-lee-una-regla)")
    A("2. [Resumen por familia](#2--resumen-por-familia)")
    for i, fam in enumerate(FAMILIAS.values(), start=3):
        ancla = fam.lower().replace(" ", "-").replace("ó", "ó")
        A(f"{i}. [{fam}](#{i}--{ancla})")
    A(f"{len(FAMILIAS) + 3}. [Reglas sin comprobación automática]"
      f"(#{len(FAMILIAS) + 3}--reglas-sin-comprobación-automática)")
    A("")
    A("---")
    A("")
    A("## 1 · Cómo se lee una regla")
    A("")
    A("Cada regla tiene un identificador estable, un nivel de exigencia, un método de")
    A("comprobación y un origen. **El identificador es lo que permite citarla** desde un")
    A("guion, desde una ficha de componente o desde un informe de auditoría.")
    A("")
    A("| Columna | Qué indica |")
    A("|---|---|")
    A("| **Identificador** | `DS-` más la familia y el número. Es estable: no se reutiliza |")
    A("| **Nivel** | `OBLIGATORIO` no se negocia · `RECOMENDADO` se justifica si no se cumple |")
    A("| **Método** | Cómo se comprueba. Ver la tabla siguiente |")
    A("| **Guion** | Qué archivo la comprueba, si alguno |")
    A("| **Origen** | El capítulo del libro, o la extensión que llena un vacío |")
    A("")
    A("**Los cuatro métodos de comprobación:**")
    A("")
    A("| Método | Qué significa |")
    A("|---|---|")
    for clave, (nombre, desc) in METODO.items():
        A(f"| **{nombre}** | {desc} |")
    A("")
    A("> **`Manual` no significa opcional.** Significa que ningún guion puede comprobarla,")
    A("> y por eso el informe de auditoría la lista para que la marque una persona.")
    A("")
    A("---")
    A("")
    A("## 2 · Resumen por familia")
    A("")
    A("| Familia | Prefijo | Reglas | Automáticas | Con guion | Sección de la base de conocimiento |")
    A("|---|---|---:|---:|---:|---|")
    for letra, fam in FAMILIAS.items():
        dela = [k for k, v in reglas.items() if v["familia"] == fam]
        au = [k for k in dela if reglas[k]["verifica"] == "auto"]
        cg = [k for k in dela if k in guiones]
        A(f"| {fam} | `DS-{letra}` | {len(dela)} | {len(au)} | {len(cg)} | "
          f"`{SECCION[fam]}/` |")
    A(f"| **Total** | | **{total}** | **{len(automaticas)}** | **{len(con_guion)}** | |")
    A("")
    A("---")
    A("")

    for i, (letra, fam) in enumerate(FAMILIAS.items(), start=3):
        dela = {k: v for k, v in reglas.items() if v["familia"] == fam}
        A(f"## {i} · {fam}")
        A("")
        A(f"**Prefijo `DS-{letra}` · {len(dela)} reglas · "
          f"base de conocimiento: `conocimiento/DESIGN/{SECCION[fam]}/README.md`**")
        A("")
        A("| Identificador | Enunciado | Nivel | Método | Guion | Origen |")
        A("|---|---|---|---|---|---|")
        for k, v in dela.items():
            metodo = METODO[v["verifica"]][0]
            gs = sorted(guiones.get(k, []))
            marca = " ✓" if k in probadas else ""
            gtxt = "`" + "` · `".join(gs) + "`" + marca if gs else "—"
            A(f"| **`{k}`** | {v['enunciado']} | {v['nivel']} | {metodo} | {gtxt} | "
              f"{v['origen']} |")
        A("")
        A("---")
        A("")

    n = len(FAMILIAS) + 3
    A(f"## {n} · Reglas sin comprobación automática")
    A("")
    A("**Estas reglas las marca una persona.** Aparecen en el informe de auditoría")
    A("(`audit.py --html`) para que ninguna quede sin revisar.")
    A("")
    sin = {k: v for k, v in reglas.items() if v["verifica"] != "auto"}
    A(f"Son **{len(sin)} de {total}**.")
    A("")
    A("| Identificador | Enunciado | Nivel | Método |")
    A("|---|---|---|---|")
    for k, v in sin.items():
        A(f"| **`{k}`** | {v['enunciado']} | {v['nivel']} | {METODO[v['verifica']][0]} |")
    A("")
    A("> **Varias podrían dejar de estar en esta lista.** Tres reglas que la base de")
    A("> conocimiento clasificaba como asistidas o manuales resultaron comprobables en")
    A("> cuanto la estructura se declaró en un archivo en vez de vivir dentro de una")
    A("> herramienta. **El límite no era la regla: era dónde estaba escrita la respuesta.**")
    A("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Genera la referencia de reglas.")
    ap.add_argument("--comprobar", action="store_true",
                    help="no escribe: falla si el documento está desactualizado")
    a = ap.parse_args()

    raiz = raiz_plugin()
    reglas = cargar_reglas(raiz)
    contenido = redactar(reglas, guiones_por_regla(raiz), rompibles(raiz))
    destino = raiz / DESTINO

    if a.comprobar:
        fallos = comprobar_recuento(reglas, raiz)
        actual = destino.read_text(encoding="utf-8") if destino.exists() else ""
        if actual != contenido:
            fallos.append(f"{DESTINO} quedó desactualizado.\n"
                          "     Regeneralo con:  python3 lib/generar_referencia.py")
        if not fallos:
            print(f"   {DESTINO} está al día · §9.11 cuadra con las ocho tablas")
            return 0
        for f in fallos:
            print(f"   {f}")
        return 1

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")
    print(f"escrito {DESTINO} · {len(contenido.splitlines())} líneas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
