#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enlaces.py — comprueba que los enlaces internos de la documentación resuelven.

    python3 pruebas/enlaces.py

Dos clases de enlace, y las dos se rompen en silencio:

  · **A un archivo** — `[texto](../otro/documento.md)`. Se rompe al mover un archivo, y
    nadie se entera hasta que alguien hace clic.
  · **A un ancla** — `[texto](#3--el-procedimiento)`. Se rompe al renumerar una sección,
    que es exactamente lo que acaba de pasar en este repositorio.

Un índice que apunta a anclas inexistentes es peor que no tener índice: promete
navegación y devuelve la misma página.

Solo biblioteca estándar.
"""

import pathlib
import re
import sys
import unicodedata

ENLACE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
TITULO = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
EXCLUIR = {"conocimiento/sources"}


def ancla(titulo):
    """El identificador que GitHub genera para un título.

    Baja a minúsculas, quita todo lo que no sea letra, número, espacio o guion, y
    cambia los espacios por guiones. Los acentos SE CONSERVAN, que es lo que hace que
    `#3--el-procedimiento` funcione y `#3--el-procedimiento` con acento también.
    """
    t = titulo.strip().lower()
    t = re.sub(r"`|\*\*|\*", "", t)
    t = "".join(c for c in t
                if c.isalnum() or c in " -_" or unicodedata.category(c).startswith("M"))
    # Cada espacio es un guion, no un grupo de espacios. `1 · Título` deja dos espacios
    # al quitar el punto medio, y GitHub produce `1--título` — con dos guiones.
    return t.strip().replace(" ", "-")


def anclas_de(texto):
    return {ancla(t) for t in TITULO.findall(texto)}


def main():
    raiz = pathlib.Path(__file__).resolve().parents[1]
    rotos, revisados = [], 0

    documentos = [f for f in sorted(raiz.rglob("*.md"))
                  if not any(x in str(f.relative_to(raiz)) for x in EXCLUIR)]
    cache = {f: f.read_text(encoding="utf-8") for f in documentos}

    for f in documentos:
        propias = anclas_de(cache[f])
        for texto, destino in ENLACE.findall(cache[f]):
            if destino.startswith(("http://", "https://", "mailto:")):
                continue
            revisados += 1
            rel = f.relative_to(raiz)

            if destino.startswith("#"):
                if destino[1:] not in propias:
                    rotos.append((rel, texto, destino, "ancla inexistente en este documento"))
                continue

            ruta, _, frag = destino.partition("#")
            objetivo = (f.parent / ruta).resolve()
            if not objetivo.exists():
                rotos.append((rel, texto, destino, "el archivo no existe"))
                continue
            if frag and objetivo.suffix == ".md":
                otras = anclas_de(cache.get(objetivo, objetivo.read_text(encoding="utf-8")))
                if frag not in otras:
                    rotos.append((rel, texto, destino, "ancla inexistente en el destino"))

    print(f"{len(documentos)} documentos · {revisados} enlaces internos revisados")
    if rotos:
        print(f"\n{len(rotos)} rotos:\n")
        for archivo, texto, destino, motivo in rotos:
            print(f"   {archivo}")
            print(f"      [{texto}]({destino})  →  {motivo}\n")
        return 1
    print("todos resuelven")
    return 0


if __name__ == "__main__":
    sys.exit(main())
