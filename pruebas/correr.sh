#!/usr/bin/env bash
# correr.sh — la suite. Construye el sistema dorado y prueba cada comprobación
# rompiendo algo a propósito.
#
#   ./pruebas/correr.sh              todo
#   ./pruebas/correr.sh --rapido     solo la corrida limpia, sin las inyecciones
#
# Existe por una frase que el plugin ya decía y no podía respaldar:
#
#     «Una comprobación que nunca falló no está probada: está sin usar.»
#
# El mecanismo --romper estaba construido desde el principio. Lo que faltaba era algo
# que lo corriera sobre TODAS las reglas de una vez, y el registro de que se corrió.
# Sin eso, la garantía era una promesa: nadie podía saber cuáles nunca fallaron.
#
# Tres etapas:
#   1 · limpio     los cuatro verificadores sobre el dorado: cero fallos
#   2 · inyección  cada regla rompible tiene que ser detectada por SU comprobación
#   3 · cobertura  ninguna regla `auto` de la base de conocimiento puede quedar sin comprobación

set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
D=/tmp/dorado-pruebas
RAPIDO=0
[[ "${1:-}" == "--rapido" ]] && RAPIDO=1

VERDE=$'\033[32m'; ROJO=$'\033[31m'; AMBAR=$'\033[33m'; GRIS=$'\033[90m'; FIN=$'\033[0m'
bien=0; mal=0; avisos=0

fallar() { echo "   ${ROJO}✗${FIN} $1"; mal=$((mal + 1)); }
pasar()  { echo "   ${VERDE}✓${FIN} $1"; bien=$((bien + 1)); }
avisar() { echo "   ${AMBAR}⚠${FIN} $1"; avisos=$((avisos + 1)); }

# ── El dorado ────────────────────────────────────────────────────────────────

echo
echo "══ Construyendo el sistema dorado"
if ! "$RAIZ/pruebas/construir.sh" "$D" >/dev/null 2>&1; then
  echo "   ${ROJO}✗${FIN} el dorado no se pudo construir — corré construir.sh a mano para ver el error"
  exit 1
fi
pasar "el dorado se construye de punta a punta"

# Cada verificador con sus argumentos. Un solo lugar donde se declara: agregar un
# guion nuevo a la suite es agregar una línea acá.
VERIF=(
  "sistema:$RAIZ/skills/system-design/scripts/verificar.py --destino $D"
  "entrega:$RAIZ/skills/entregar/scripts/entregar.py --destino $D"
  "pantallas:$RAIZ/skills/pantalla/scripts/verificar-pantalla.py --sistema $D --pantallas $D/pantallas"
  "auditoria:$RAIZ/skills/auditar/scripts/auditar.py --destino $D --pantallas $D/pantallas"
  "pruebas-ui:$RAIZ/skills/probar/scripts/probar.py --sistema $D --pantallas $D/pantallas"
)

# ── Etapa 1 · limpio ─────────────────────────────────────────────────────────

echo
echo "══ Etapa 1 · el dorado pasa limpio"
for entrada in "${VERIF[@]}"; do
  nombre="${entrada%%:*}"; cmd="${entrada#*:}"
  guion="${cmd%% *}"
  if [[ ! -f "$guion" ]]; then
    avisar "$nombre — el guion no existe todavía: $(basename "$guion")"
    continue
  fi
  salida=$(python3 $cmd 2>&1); codigo=$?
  resumen=$(echo "$salida" | grep -oE "[0-9]+ comprobaciones en verde · [0-9]+ fallos.*" | head -1)
  if [[ $codigo -ne 0 ]]; then
    fallar "$nombre — ${resumen:-salió con código $codigo}"
    echo "$salida" | grep -E "^   ✗" | head -5 | sed 's/^/       /'
  else
    pasar "$nombre — ${resumen:-sin fallos}"
  fi
done

if [[ $RAPIDO -eq 1 ]]; then
  echo
  echo "modo rápido: las inyecciones no corrieron. ${GRIS}No es un verde completo.${FIN}"
  [[ $mal -gt 0 ]] && exit 1 || exit 0
fi

# ── Etapa 2 · inyección ──────────────────────────────────────────────────────
#
# El veredicto es de la regla que se rompió, no del total. Los tres códigos que
# devuelven los guiones: 0 lo detectó · 1 pasó sin detectarse · 2 no se pudo probar.
# El 2 NO es un verde: es una prueba que no corrió.

echo
echo "══ Etapa 2 · cada comprobación detecta su propio error"
probadas=""
for entrada in "${VERIF[@]}"; do
  nombre="${entrada%%:*}"; cmd="${entrada#*:}"
  guion="${cmd%% *}"
  [[ -f "$guion" ]] || continue
  lista=$(python3 $cmd --romper lista 2>/dev/null) || continue
  [[ -z "$lista" ]] && continue
  echo "   ${GRIS}── $nombre${FIN}"
  for regla in $lista; do
    python3 $cmd --romper "$regla" >/dev/null 2>&1; codigo=$?
    case $codigo in
      0) pasar "$regla lo detectó"; probadas="$probadas $regla" ;;
      1) fallar "$regla PASÓ SIN DETECTARSE — la comprobación no sirve" ;;
      2) avisar "$regla no se pudo probar: su comprobación está saltada" ;;
      *) fallar "$regla — el guion salió con código $codigo" ;;
    esac
  done
done

# ── Etapa 3 · cobertura ──────────────────────────────────────────────────────

echo
echo "══ Etapa 3 · ninguna regla auto de la base de conocimiento queda sin comprobación"
python3 - "$RAIZ" "$probadas" <<'PY'
import sys, pathlib, subprocess
raiz = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(raiz / "lib"))
from comun import cargar_reglas

reglas = cargar_reglas(raiz)
probadas = set(sys.argv[2].split())
# Lo que un GUION comprueba, aunque su error todavía no se pueda inyectar.
# Se miran solo los scripts a propósito: una regla nombrada en un SKILL.md está citada,
# no comprobada, y contarla acá convertiría la cobertura en una medida de prosa.
citadas = set(subprocess.run(
    ["grep", "-rhoE", "--include=*.py", "DS-[A-Z][0-9]+", str(raiz / "skills")],
    capture_output=True, text=True).stdout.split())

auto = {k: v for k, v in reglas.items() if v["verifica"] == "auto"}
sin_guion = sorted(k for k in auto if k not in citadas)
sin_probar = sorted(k for k in auto if k in citadas and k not in probadas)

print(f"   reglas en la base de conocimiento            {len(reglas)}")
print(f"   marcadas «auto»            {len(auto)}")
print(f"   con comprobación           {len(auto) - len(sin_guion)}")
print(f"   probadas con --romper      {len(auto) - len(sin_guion) - len(sin_probar)}")

fallos = 0
if sin_guion:
    print(f"\n   \033[31m✗\033[0m {len(sin_guion)} reglas «auto» sin ninguna comprobación:")
    for k in sin_guion:
        print(f"       {k}  {reglas[k]['enunciado'][:66]}")
    fallos += 1
if sin_probar:
    print(f"\n   \033[33m⚠\033[0m {len(sin_probar)} con comprobación pero sin caso de --romper:")
    for k in sin_probar:
        print(f"       {k}  {reglas[k]['enunciado'][:66]}")
    print("       No están probadas: están sin usar. Agregales su daño en romper().")
sys.exit(1 if fallos else 0)
PY
cobertura=$?
[[ $cobertura -ne 0 ]] && mal=$((mal + 1))

# ── Etapa 4 · documentación generada ─────────────────────────────────────────
#
# `docs/03-referencia-de-reglas.md` se produce desde la base de conocimiento. Si alguien
# agrega una regla y no lo regenera, el documento describe un sistema que ya no existe —
# y es peor que no tenerlo, porque parece autorizado.

echo
echo "══ Etapa 4 · la documentación generada está al día"
if python3 "$RAIZ/lib/generar_referencia.py" --comprobar; then
  pasar "docs/03-referencia-de-reglas.md coincide con la base de conocimiento"
else
  fallar "docs/03-referencia-de-reglas.md quedó desactualizado"
fi

if python3 "$RAIZ/pruebas/indices.py" --comprobar; then
  pasar "los índices coinciden con los títulos de cada documento"
else
  fallar "hay índices desactualizados"
fi

# ── Etapa 5 · enlaces internos ───────────────────────────────────────────────
#
# Un enlace roto falla en silencio: lleva al principio de la página en vez de a la
# sección, y nadie lo reporta. Se rompieron 55 de golpe al renumerar las secciones.

if python3 "$RAIZ/pruebas/importar.py" >/dev/null 2>&1; then
  pasar "el camino «Importar» no duplica el modelo ni reapunta el proyecto"
else
  fallar "el camino «Importar» está roto"
  python3 "$RAIZ/pruebas/importar.py" 2>&1 | sed 's/^/       /'
fi

echo
echo "══ Etapa 5 · los enlaces internos resuelven"
salida_enlaces=$(python3 "$RAIZ/pruebas/enlaces.py" 2>&1)
if [[ $? -eq 0 ]]; then
  pasar "$(echo "$salida_enlaces" | head -1)"
else
  fallar "hay enlaces internos rotos"
  echo "$salida_enlaces" | head -12 | sed 's/^/       /'
fi

# ── Etapa 6 · el paquete ─────────────────────────────────────────────────────
#
# Las etapas anteriores comprueban que el complemento hace lo que dice. Esta comprueba
# que lo lleve consigo: un archivo que un guion abre o que una skill manda leer funciona
# perfecto acá, donde está al lado, y falta en la máquina de quien lo instale si no viajó.

echo
echo "══ Etapa 6 · el paquete lleva lo que los guiones y las skills leen"
salida_paquete=$(python3 "$RAIZ/pruebas/paquete.py" 2>&1)
if [[ $? -eq 0 ]]; then
  pasar "$(echo "$salida_paquete" | grep -c '✓') archivos en su sitio · el manifiesto cuadra"
else
  fallar "el paquete está incompleto"
  echo "$salida_paquete" | grep '✗' | head -8 | sed 's/^/       /'
fi

# ── El veredicto ─────────────────────────────────────────────────────────────

echo
echo "─────────────────────────────────────────────────────────────"
printf "%s%d en verde%s · %s%d fallos%s" "$VERDE" "$bien" "$FIN" \
       "$( [[ $mal -gt 0 ]] && echo "$ROJO" || echo "$GRIS" )" "$mal" "$FIN"
[[ $avisos -gt 0 ]] && printf " · %s%d avisos%s" "$AMBAR" "$avisos" "$FIN"
echo
if [[ $mal -gt 0 ]]; then
  echo "${ROJO}La suite falla.${FIN} No se entrega hasta que esté en cero."
  exit 1
fi
if [[ $avisos -gt 0 ]]; then
  echo "${AMBAR}Sin fallos, con avisos.${FIN} Un aviso es una prueba que no corrió — no es un verde."
  exit 0
fi
echo "${VERDE}La suite pasa entera.${FIN}"
