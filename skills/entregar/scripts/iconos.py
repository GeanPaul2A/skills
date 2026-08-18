#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iconos.py — instala los iconos del catálogo en un proyecto, por plataforma.

    python3 iconos.py --destino <proyecto> --plataforma web
    python3 iconos.py --destino <proyecto> --plataforma web --solo buscar,cerrar
    python3 iconos.py --destino <proyecto> --plataforma ios --listar
    python3 iconos.py --catalogo                       qué acciones hay declaradas

**El repositorio guarda el catálogo, no los iconos.** El motivo no es de tamaño: SF
Symbols es de Apple y su licencia **prohíbe redistribuirlos** — un repositorio público
con esos archivos adentro sería una redistribución. Material Symbols (Apache-2.0) y
Lucide (ISC) sí se pueden, y son los que este guion baja.

Para iOS el guion **no descarga nada y lo dice**: imprime qué glifo de SF Symbols
corresponde a cada acción para que se tome desde Xcode o desde la app SF Symbols.

Y hace lo que un catálogo suelto no haría: **escribe el tamaño correcto de cada icono
según dónde se usa** — DS-C11. Un icono de 24 dentro de un campo se ve desproporcionado,
y esa decisión deja de ser criterio de cada quien.

Solo biblioteca estándar.
"""

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import raiz_plugin  # noqa: E402

PLATAFORMAS = ["ios", "android", "web", "desktop"]
TIEMPO = 20


def catalogo():
    f = raiz_plugin() / "recursos/iconos.json"
    if not f.exists():
        sys.exit(f"falta el catálogo: {f}")
    return json.loads(f.read_text(encoding="utf-8"))


def url_de(cat, set_, glifo, tamano):
    plantilla = cat["_licencias"][set_].get("origen", "")
    if set_ == "sf-symbols":
        return None
    if set_ == "material-symbols":
        return (plantilla.replace("{glifo}", glifo)
                .replace("{peso}", str(cat["_grosor"]["material_peso"]))
                .replace("{grado}", str(cat["_grosor"]["material_grado"]))
                .replace("{tamano}", str(24 if tamano <= 24 else 48)))
    return plantilla.replace("{glifo}", glifo)


def bajar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "design-system/1.3"})
    with urllib.request.urlopen(pedido, timeout=TIEMPO) as r:
        return r.read().decode("utf-8")


def limpiar(svg, tamano, grosor):
    """Normaliza el SVG a lo que el sistema exige — DS-F09, DS-F10, DS-C11.

    `currentColor` es la parte que más importa: un icono con el color escrito adentro no
    cambia con el modo oscuro ni con el estado del componente que lo contiene, y termina
    siendo el único elemento que no responde al tema.
    """
    svg = svg.replace('stroke="#000"', 'stroke="currentColor"')
    svg = svg.replace('stroke="#000000"', 'stroke="currentColor"')
    svg = svg.replace('fill="#000"', 'fill="currentColor"')
    svg = svg.replace('fill="#000000"', 'fill="currentColor"')
    if 'stroke-width' in svg:
        import re
        svg = re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{grosor}"', svg)
    # El tamaño va en el atributo, no en el viewBox: el viewBox es la geometría.
    import re
    svg = re.sub(r'\swidth="[^"]*"', f' width="{tamano}"', svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', f' height="{tamano}"', svg, count=1)
    return svg.strip() + "\n"


def grosor_para(cat, tamano):
    return 1.5 if tamano < 24 else 2


def main():
    ap = argparse.ArgumentParser(description="Instala los iconos del catálogo.")
    ap.add_argument("--destino", help="carpeta del proyecto donde van los iconos")
    ap.add_argument("--plataforma", choices=PLATAFORMAS)
    ap.add_argument("--uso", default="control",
                    help="barra · control · campo · linea · grande (decide el tamaño)")
    ap.add_argument("--solo", help="lista de acciones separadas por coma")
    ap.add_argument("--listar", action="store_true", help="no descarga: dice qué haría")
    ap.add_argument("--catalogo", action="store_true", help="qué acciones hay declaradas")
    a = ap.parse_args()

    cat = catalogo()
    iconos = cat["iconos"]

    if a.catalogo:
        print(f"{len(iconos)} acciones declaradas:\n")
        for n, i in iconos.items():
            print(f"  {n:18} {i['proposito']}")
        print("\nTamaños por uso y plataforma:")
        for p, t in cat["_tamanos"].items():
            if p.startswith("_"):
                continue
            print(f"  {p:9} " + " · ".join(f"{k} {v}" for k, v in t.items()))
        return 0

    if not a.plataforma:
        sys.exit("hace falta --plataforma (o usá --catalogo)")
    if not a.destino and not a.listar:
        sys.exit("hace falta --destino (o usá --listar)")

    tamano = cat["_tamanos"][a.plataforma].get(a.uso)
    if tamano is None:
        sys.exit(f"«{a.uso}» no es un uso conocido: {', '.join(cat['_tamanos']['ios'])}")
    grosor = grosor_para(cat, tamano)

    pedidos = [s.strip() for s in a.solo.split(",")] if a.solo else list(iconos)
    faltan = [p for p in pedidos if p not in iconos]
    if faltan:
        sys.exit(f"no están en el catálogo: {', '.join(faltan)}")

    print(f"{a.plataforma} · uso «{a.uso}» · {tamano} px · trazo {grosor}\n")

    salida = None
    if a.destino:
        salida = pathlib.Path(a.destino).resolve() / "recursos/iconos"
        salida.mkdir(parents=True, exist_ok=True)

    puestos = manuales = fallidos = 0
    for nombre in pedidos:
        d = iconos[nombre].get(a.plataforma)
        if not d:
            print(f"  ·  {nombre:18} sin glifo declarado para {a.plataforma}")
            continue
        set_, glifo = d["set"], d["glifo"]
        url = url_de(cat, set_, glifo, tamano)
        if url is None:
            # No es un fallo: es una licencia. Se dice qué tomar y de dónde.
            print(f"  ⌘  {nombre:18} {glifo}  →  SF Symbols, se toma desde Xcode "
                  f"(Apple no permite redistribuirlo)")
            manuales += 1
            continue
        if a.listar:
            print(f"  →  {nombre:18} {set_}/{glifo}")
            continue
        try:
            svg = limpiar(bajar(url), tamano, grosor)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  ✗  {nombre:18} no se pudo bajar {set_}/{glifo} — {e}")
            fallidos += 1
            continue
        (salida / f"{nombre}.svg").write_text(svg, encoding="utf-8")
        peso = len(svg.encode("utf-8"))
        marca = "✓" if peso <= 2048 else "⚠"
        print(f"  {marca}  {nombre:18} {peso:5} B  {set_}/{glifo}")
        puestos += 1

    print()
    if a.listar:
        print(f"{len(pedidos)} acciones · no se descargó nada (--listar)")
        return 0
    print(f"{puestos} instalados · {manuales} manuales (SF Symbols) · {fallidos} fallidos")
    if salida:
        print(f"En {salida}")
        print("\nComprobalos con:  entregar.py --destino <proyecto> --regla DS-F10")
    lic = {iconos[n][a.plataforma]["set"] for n in pedidos
           if iconos[n].get(a.plataforma)}
    print("\nLicencias de lo instalado:")
    for s in sorted(lic):
        d = cat["_licencias"][s]
        print(f"   {s:18} {d['licencia']:28} {d['quien']}")
    return 1 if fallidos else 0


if __name__ == "__main__":
    sys.exit(main())
