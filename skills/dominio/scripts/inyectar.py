#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inyectar.py — materializa un dominio en un sistema de diseño.

    python3 inyectar.py --destino <carpeta> --dominio <dominios/<tipo>.json>

Lee el archivo de dominio y produce, dentro de <destino>:
  - inventario/patrones.json        los patrones del dominio (con sus datos y estados)
  - inventario/componentes.json     fusiona los componentes propios (universal: false)
  - inventario/plantillas.json      fusiona las plantillas propias (universal: false)
  - modelo/tables/*.csv             una tabla por entidad (csv-cabecera)
  - modelo/reglas.txt               las reglas de negocio

y actualiza proyecto.json → modelo_de_datos para que verificar.py compruebe
DS-P02 (entidades y campos citados existen) y DS-P01 (reglas citadas existen)
contra el dominio — en vez de saltarlas por 'modelo_de_datos.tipo': null.

Solo biblioteca estándar.
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from comun import tabla  # noqa: E402


def cargar(ruta):
    p = pathlib.Path(ruta)
    if not p.exists():
        sys.exit(f"no existe {p}")
    return json.loads(p.read_text(encoding="utf-8")), p


def generar_modelo(destino, dominio):
    """Una tabla CSV por entidad y un archivo de reglas, en el formato que verificar.py ya lee."""
    modelo = destino / "modelo"
    tablas = modelo / "tables"
    tablas.mkdir(parents=True, exist_ok=True)
    # `tabla()` filtra las claves con guion bajo: son notas, no entidades. Sin esto,
    # un `_lee` en «entidades» llega acá como cadena y revienta con un error que no
    # dice qué pasó. Es el mismo fallo que ya había tumbado a cuatro verificadores.
    for nombre, ent in tabla(dominio, "entidades").items():
        campos = [c["nombre"] for c in ent.get("campos", [])]
        (tablas / f"{nombre}.csv").write_text(",".join(campos) + "\n", encoding="utf-8")
    reglas = [k for k in (dominio.get("reglas") or {}) if not k.startswith("_")]
    (modelo / "reglas.txt").write_text("\n".join(reglas) + "\n", encoding="utf-8")
    return modelo


def fusionar(destino, archivo, propias):
    """Fusiona piezas propias en un inventario, marcadas universal: false, sin pisar lo existente."""
    ruta = destino / "inventario" / archivo
    clave = "componentes" if archivo.endswith("componentes.json") else "plantillas"
    inv = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    tabla = inv.setdefault(clave, {})
    for nombre, def_ in {k: v for k, v in (propias or {}).items()
                         if not k.startswith("_") and isinstance(v, dict)}.items():
        if nombre in tabla:
            continue
        entrada = {k: v for k, v in def_.items() if k != "motivo"}
        entrada["universal"] = False
        if isinstance(def_.get("motivo"), str):
            entrada["_por_que_no_universal"] = def_["motivo"]
        tabla[nombre] = entrada
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")


def convertir_patrones(dominio):
    """Del formato del dominio al que verificar.py lee en inventario/patrones.json."""
    patrones = {}
    for nombre, p in tabla(dominio, "patrones").items():
        patrones[nombre] = {
            "proposito": p.get("proposito", ""),
            "estados": p.get("estados", []),
            "plantilla": p.get("plantilla", "plana"),
            "componentes": p.get("componentes", []),
            "lee_tambien": p.get("lee_tambien", []),
            "datos": {
                "entidades": p.get("entidades", []),
                # Sin esto, la mitad de DS-P02 —«ningún dato se muestra sin una columna
                # que lo respalde», la regla que la base de conocimiento llama la más valiosa del sistema—
                # corría sin nada que mirar y quedaba saltada para siempre.
                "campos": p.get("campos", []),
                "reglas": p.get("reglas", []),
            },
        }
    return patrones


def importa_modelo_formal(dominio):
    """¿El dominio REFERENCIA un modelo que ya existe, en vez de definirlo?

    Es el camino «Importar» de la skill: el producto ya tiene tablas y reglas, y el
    dominio declara solo la capa que el diseño consulta. En ese caso **no se genera nada
    y no se toca `proyecto.json`** — generar una copia del modelo y reapuntar el proyecto
    hacia ella es justo la duplicación que la skill prohíbe: se desincroniza en la primera
    edición del modelo real, y desde ahí el verificador comprueba contra un fantasma.
    """
    return bool((dominio.get("modelo_formal") or {}).get("tipo"))


def actualizar_proyecto(destino):
    p = destino / "proyecto.json"
    cfg = json.loads(p.read_text(encoding="utf-8"))
    cfg["modelo_de_datos"] = {
        "tipo": "dominio",
        "raiz": "modelo",
        "dominios": {"descubrir": "plano"},
        "entidades": {"ruta": "tables", "extension": ".csv", "formato": "csv-cabecera"},
        "reglas": {"ruta": "reglas.txt", "patron": "^([A-Z][0-9]+[a-z]?)$", "cita": "{regla}"},
    }
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Materializa un dominio en un sistema de diseño.")
    ap.add_argument("--destino", required=True, help="carpeta del sistema (marca.json, tokens/, inventario/)")
    ap.add_argument("--dominio", required=True, help="archivo dominios/<tipo>.json")
    a = ap.parse_args()

    destino = pathlib.Path(a.destino).resolve()
    dominio, _ = cargar(a.dominio)

    importado = importa_modelo_formal(dominio)
    if not importado:
        generar_modelo(destino, dominio)

    fusionar(destino, "componentes.json", dominio.get("componentes_propios"))
    fusionar(destino, "plantillas.json", dominio.get("plantillas_propias"))
    (destino / "inventario").mkdir(exist_ok=True)
    (destino / "inventario" / "patrones.json").write_text(
        json.dumps({"patrones": convertir_patrones(dominio)}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    if not importado:
        actualizar_proyecto(destino)

    entidades = tabla(dominio, "entidades")
    propios = {k: v for k, v in (dominio.get("componentes_propios") or {}).items()
               if not k.startswith("_")}
    plantillas = {k: v for k, v in (dominio.get("plantillas_propias") or {}).items()
                  if not k.startswith("_")}
    reglas = [k for k in (dominio.get("reglas") or {}) if not k.startswith("_")]

    print(f"dominio «{dominio.get('nombre')}» inyectado:")
    if importado:
        formal = dominio["modelo_formal"]
        print(f"  modelo: IMPORTADO — {formal.get('alcance') or formal.get('raiz')}")
        print(f"          no se generó copia y no se tocó proyecto.json: el modelo real manda")
        print(f"  la capa que el diseño consulta: {len(entidades)} entidades · {len(reglas)} reglas")
    else:
        print(f"  modelo: {len(entidades)} tablas · {len(reglas)} reglas — generado desde el dominio")
    print(f"  patrones: {len(convertir_patrones(dominio))}")
    print(f"  propio: {len(propios)} componentes · {len(plantillas)} plantillas")


if __name__ == "__main__":
    main()
