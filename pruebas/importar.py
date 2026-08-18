#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
importar.py — prueba el camino «Importar» de la capacidad `domain`.

    python3 pruebas/importar.py

**Existe porque la rama no la ejercitaba nadie.** El sistema de referencia define su
modelo desde el propio archivo de dominio, así que `importa_modelo_formal()` devolvía
siempre `False` y la rama de importación no corría en ninguna prueba — el estado que la
doctrina del complemento llama «una comprobación que nunca falló está sin usar».

El camino se descubrió usando la capacidad contra un producto real con 113 tablas ya
modeladas. Ahí apareció el fallo: `inyectar.py` generaba una copia del modelo y
reapuntaba `proyecto.json` hacia ella — **la duplicación exacta que la capacidad
prohíbe**. Esta prueba fija ese comportamiento para que no vuelva.

Comprueba las dos direcciones, porque una sola no prueba nada:

  · Con `modelo_formal.tipo` declarado  →  NO se genera copia, NO se toca el proyecto
  · Con `modelo_formal.tipo` en null    →  SÍ se genera, SÍ se reapunta

Solo biblioteca estándar.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[1]

DOMINIO = {
    "nombre": "prueba-importacion",
    "sector": "genérico",
    "entidades": {
        "_lee": "Una nota. Si el guion no la filtra, revienta acá — y ese fallo ya ocurrió.",
        "externa.cosa": {"campos": [{"nombre": "cosa_id", "tipo": "entero"}]},
    },
    "reglas": {"_lee": "Otra nota.", "externa.R1": "Una regla del modelo ajeno"},
    "patrones": {
        "_lee": "Otra nota más.",
        "un-flujo": {
            "proposito": "probar la importación",
            "plantilla": "plana",
            "entidades": ["externa.cosa"],
            "campos": ["externa.cosa.cosa_id"],
            "reglas": ["externa.R1"],
            "componentes": ["boton"],
            "estados": ["entrada", "exito", "error"],
        },
    },
    "componentes_propios": {"_lee": "Y una más."},
    "modelo_formal": {"tipo": None, "raiz": "", "formato": "", "nota": ""},
}


def preparar(tmp):
    """Un sistema mínimo: lo que `inyectar.py` necesita para correr."""
    destino = tmp / "sistema"
    (destino / "inventario").mkdir(parents=True)
    plant = RAIZ / "skills/system-design/plantillas"
    for origen, nombre in ((plant / "marca.json", "marca.json"),
                           (plant / "proyecto.json", "proyecto.json")):
        shutil.copy(origen, destino / nombre)
    for origen, nombre in ((plant / "componentes-base.json", "componentes.json"),
                           (plant / "plantillas-base.json", "plantillas.json")):
        shutil.copy(origen, destino / "inventario" / nombre)

    # El proyecto apunta a un modelo AJENO, como haría un producto ya modelado.
    p = destino / "proyecto.json"
    cfg = json.loads(p.read_text(encoding="utf-8"))
    cfg["modelo_de_datos"] = {"tipo": "una-base-por-dominio", "raiz": "../modelo-ajeno",
                              "_marca": "no se toca"}
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return destino


def correr(destino, dominio, tmp):
    f = tmp / "domain.json"
    f.write_text(json.dumps(dominio, ensure_ascii=False, indent=2), encoding="utf-8")
    return subprocess.run(
        ["python3", str(RAIZ / "skills/domain/scripts/inyectar.py"),
         "--destino", str(destino), "--domain", str(f)],
        capture_output=True, text=True)


def caso(titulo, tipo_formal, espera_copia):
    with tempfile.TemporaryDirectory() as t:
        tmp = pathlib.Path(t)
        destino = preparar(tmp)
        dominio = json.loads(json.dumps(DOMINIO))
        dominio["modelo_formal"]["tipo"] = tipo_formal
        dominio["modelo_formal"]["raiz"] = "../modelo-ajeno" if tipo_formal else ""
        dominio["modelo_formal"]["alcance"] = "14 dominios" if tipo_formal else ""

        r = correr(destino, dominio, tmp)
        fallos = []
        if r.returncode != 0:
            fallos.append(f"el guion salió con código {r.returncode}: {r.stderr.strip()[:160]}")

        hay_copia = (destino / "modelo").exists()
        if hay_copia != espera_copia:
            fallos.append(f"copia del modelo: se esperaba {espera_copia} y hay {hay_copia}")

        raiz = json.loads((destino / "proyecto.json").read_text(encoding="utf-8"))
        marca = raiz.get("modelo_de_datos", {}).get("_marca")
        intacto = marca == "no se toca"
        if intacto == espera_copia:
            fallos.append("proyecto.json: se reapuntó cuando no debía, o al revés")

        # Las notas se filtran en las dos direcciones.
        pat = destino / "inventario" / "patrones.json"
        if pat.exists():
            p = json.loads(pat.read_text(encoding="utf-8"))["patrones"]
            if "_lee" in p:
                fallos.append("la nota «_lee» se coló como patrón")

        print(f"  {'✓' if not fallos else '✗'} {titulo}")
        for f in fallos:
            print(f"       {f}")
        return not fallos


def main():
    print("Camino «Importar» de la capacidad dominio\n")
    ok = caso("con modelo formal declarado: no copia y no reapunta", "una-base-por-dominio", False)
    ok &= caso("sin modelo formal: genera el modelo y reapunta", None, True)
    print()
    if ok:
        print("las dos direcciones se comportan como corresponde")
        return 0
    print("el camino «Importar» está roto")
    return 1


if __name__ == "__main__":
    sys.exit(main())
