#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
indices.py — regenera el índice de cada documento desde sus propios títulos.

    python3 pruebas/indices.py              reescribe los índices
    python3 pruebas/indices.py --comprobar  falla si alguno quedó desactualizado

**Un índice escrito a mano se desincroniza en la primera sección que se agrega, se
renumera o se renombra.** Y su fallo es silencioso: el enlace lleva al principio de la
página en vez de a la sección, así que nadie lo reporta.

Este guion lo construye desde los títulos de nivel dos, que es la única fuente que no
puede mentir sobre qué secciones tiene el documento.

**No toca los documentos de instrucciones de las capacidades** (`SKILL.md`): el agente
lee el archivo entero, así que un índice ahí gasta contexto sin ahorrarle navegación.

Solo biblioteca estándar.
"""

import argparse
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "pruebas"))
from enlaces import ancla  # noqa: E402

TITULO2 = re.compile(r"^## (.+?)\s*$", re.M)
EXCLUIR = ("conocimiento/sources", "SKILL.md", "docs/03-referencia-de-reglas.md")
MINIMO = 90  # líneas: por debajo de esto, un índice estorba más de lo que ayuda


def limpiar(titulo):
    """El texto del título, sin el número que lo precede ni el formato."""
    t = re.sub(r"^\d+(?:\.\d+)?\s*·\s*", "", titulo)
    return re.sub(r"`|\*\*|\*", "", t).strip()


def indice_de(texto):
    titulos = [t for t in TITULO2.findall(texto) if limpiar(t).lower() != "índice"]
    if not titulos:
        return None
    lineas = ["## Índice", ""]
    for i, t in enumerate(titulos, start=1):
        lineas.append(f"{i}. [{limpiar(t)}](#{ancla(t)})")
    # El separador es parte del bloque: sin él, el índice queda pegado a la primera
    # sección y el documento pierde el respiro que lo hace legible.
    lineas += ["", "---", "", ""]
    return "\n".join(lineas)


def reescribir(texto):
    """Sustituye el bloque del índice, o lo inserta tras el preámbulo si no existe."""
    nuevo = indice_de(texto)
    if nuevo is None:
        return texto

    inicio = texto.find("\n## Índice")
    if inicio != -1:
        inicio += 1
        # El bloque termina en el título siguiente.
        siguiente = texto.find("\n## ", inicio + 1)
        return texto[:inicio] + nuevo + texto[siguiente + 1:] if siguiente != -1 else \
            texto[:inicio] + nuevo

    primero = texto.find("\n## ")
    if primero == -1:
        return texto
    return texto[:primero + 1] + nuevo + texto[primero + 1:]


def main():
    ap = argparse.ArgumentParser(description="Regenera los índices de la documentación.")
    ap.add_argument("--comprobar", action="store_true",
                    help="no escribe: falla si algún índice quedó desactualizado")
    a = ap.parse_args()

    raiz = pathlib.Path(__file__).resolve().parents[1]
    tocados, desfasados = [], []

    for f in sorted(raiz.rglob("*.md")):
        rel = str(f.relative_to(raiz))
        if any(x in rel for x in EXCLUIR):
            continue
        texto = f.read_text(encoding="utf-8")
        if len(texto.split("\n")) < MINIMO and "## Índice" not in texto:
            continue
        nuevo = reescribir(texto)
        if nuevo == texto:
            continue
        if a.comprobar:
            desfasados.append(rel)
        else:
            f.write_text(nuevo, encoding="utf-8")
            tocados.append(rel)

    if a.comprobar:
        if desfasados:
            print(f"   {len(desfasados)} índices desactualizados:")
            for d in desfasados:
                print(f"      {d}")
            print("   Regeneralos con:  python3 pruebas/indices.py")
            return 1
        print("   todos los índices están al día")
        return 0

    print(f"{len(tocados)} índices regenerados")
    for t in tocados:
        print(f"   {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
