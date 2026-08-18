#!/usr/bin/env bash
# construir.sh — ensambla el sistema dorado en una carpeta temporal.
#
#   ./pruebas/construir.sh [<carpeta>]     por omisión, /tmp/dorado
#
# Las FUENTES viven en ejemplos/base/ y están versionadas. Los DERIVADOS —tokens,
# modelo, salidas— se generan acá y no entran al repositorio: es DS-X01, la regla que
# dice que la fuente de verdad es el JSON escrito a mano y todo lo demás es una salida.
#
# Un derivado versionado se desincroniza en la primera edición de la marca, y entonces
# la suite prueba contra un sistema que ya nadie construye así.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESTINO="${1:-/tmp/dorado}"
S="$RAIZ/skills"

rm -rf "$DESTINO"
mkdir -p "$DESTINO/inventario"

# 1 · Las fuentes escritas a mano
cp "$RAIZ/ejemplos/base/marca.json" "$RAIZ/ejemplos/base/proyecto.json" \
   "$RAIZ/ejemplos/base/movimiento.json" "$DESTINO/"
cp -R "$RAIZ/ejemplos/base/pantallas" "$RAIZ/ejemplos/base/recursos" \
      "$RAIZ/ejemplos/base/entrega" "$DESTINO/"

# 2 · El inventario universal — 22 componentes y 4 plantillas que existen en cualquier producto
cp "$S/system-design/plantillas/componentes-base.json" "$DESTINO/inventario/componentes.json"
cp "$S/system-design/plantillas/plantillas-base.json"  "$DESTINO/inventario/plantillas.json"

# 3 · Derivar los tres niveles de token
python3 "$S/system-design/scripts/derivar.py" --destino "$DESTINO" >/dev/null

# 4 · Inyectar el dominio: patrones, piezas propias y el modelo contra el que se cruza DS-P02
python3 "$S/dominio/scripts/inyectar.py" --destino "$DESTINO" \
        --dominio "$RAIZ/ejemplos/base/dominio.json" >/dev/null

# 5 · Volver a derivar: el nivel 3 sale del inventario, que acaba de crecer
python3 "$S/system-design/scripts/derivar.py" --destino "$DESTINO" >/dev/null

# 6 · Publicar. Sin esto, DS-X01 y DS-A09 quedan saltadas para siempre — y una
#     comprobación saltada no es un verde, es una prueba que no corrió.
python3 "$S/system-design/scripts/construir.py" --destino "$DESTINO" \
        --salidas css,figma,lienzo,galeria >/dev/null

echo "$DESTINO"
