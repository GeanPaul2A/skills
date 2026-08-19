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

  · Con `modelo_formal.tipo` declarado  →  NO se genera copia, y el proyecto apunta
                                            al modelo REAL del producto
  · Con `modelo_formal.tipo` en null    →  SÍ se genera, y el proyecto apunta a la copia

**Lo prohibido es apuntar a una copia cuando el modelo ya existe**, no reapuntar. La
primera versión de esta prueba confundía las dos cosas y prohibía las dos.

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

        # Lo que se comprueba es A DÓNDE apunta, no si quedó intacto.
        #
        # La primera versión buscaba un centinela `_marca: "no se toca"` en la plantilla
        # y exigía que sobreviviera. Dos problemas: el centinela nunca existió en
        # `plantillas/proyecto.json`, así que el caso «con modelo formal» fallaba
        # siempre; y aunque hubiera existido no serviría, porque las dos ramas de
        # `inyectar.py` reemplazan el diccionario entero y lo borrarían igual.
        #
        # Y el fondo: la prueba prohibía reapuntar. **El mal que nació para impedir era
        # duplicar el modelo y apuntar A LA COPIA**, no apuntar al modelo real. Si no se
        # reapunta, `modelo_de_datos.tipo` queda en null, `verificar.py` se salta DS-P02
        # y las tablas del producto no se comprueban contra nada — que es justo lo que
        # el camino «Importar» existe para lograr.
        md = json.loads((destino / "proyecto.json").read_text(encoding="utf-8")
                        ).get("modelo_de_datos", {})
        if espera_copia:
            esperado = ("dominio", "modelo")            # al modelo GENERADO
        else:
            esperado = (tipo_formal, "../modelo-ajeno")  # al modelo REAL del producto
        actual = (md.get("tipo"), md.get("raiz"))
        if actual != esperado:
            fallos.append(f"proyecto.json apunta a {actual} y debía apuntar a {esperado}")

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
    ok = caso("con modelo formal declarado: no copia y apunta al modelo real", "una-base-por-dominio", False)
    ok &= caso("sin modelo formal: genera el modelo y apunta a la copia", None, True)
    print()
    if ok:
        print("las dos direcciones se comportan como corresponde")
        return 0
    print("el camino «Importar» está roto")
    return 1


if __name__ == "__main__":
    sys.exit(main())
