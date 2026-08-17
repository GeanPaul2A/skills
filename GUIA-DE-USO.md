# Guía de uso — plugin `design-system`

El plugin vive en `design-system/` y se instala desde el marketplace `geanpaul-design`, definido en
`.claude-plugin/marketplace.json`. Tiene **6 skills** que se activan solas cuando describís lo que querés, y
**7 comandos** de atajo para invocarlas a mano.

---

## El modelo mental: un pipeline, no skills sueltas

```
sistema-diseno  →  dominio  →  pantalla  →  probar / auditar / documentar
  (lo visual)      (el negocio)  (las pantallas)   (verificar lo hecho)
```

| Skill | Qué hace | Cuándo se activa sola |
|---|---|---|
| `sistema-diseno` | Tokens en 3 niveles, componentes universales, plantillas, modos, publicación | «genera un sistema de diseño», «necesito la paleta / la tipografía» |
| `dominio` | El tipo de negocio: entidades, reglas, patrones, piezas propias | «definí el negocio», «las entidades», «las reglas de dominio» |
| `pantalla` | Una pantalla o un flujo: plantilla + datos + estados | «diseñá la pantalla de…», «un onboarding», «un registro» |
| `probar` | Los 5 momentos, los 4 estados, valores límite, accesibilidad | «probá el flujo», «¿aguanta los datos reales?» |
| `auditar` | Score, coherencia, cobertura, prioridades | «auditá mi sistema», «qué tan sano está» |
| `documentar` | Ficha de una pieza: props, accesibilidad, do/don't, código | «documentá el componente X» |

---

## Los comandos

**Los nombres son distintos a los de las skills a propósito.** Un comando y una skill que se llaman igual
ocupan el mismo espacio de nombres y uno tapa al otro en el listado.

```
/design-system:crear              construir el sistema visual
/design-system:definir-dominio    definir el negocio
/design-system:disenar-pantalla   maquetar una pantalla o un flujo
/design-system:probar-pantalla    probar
/design-system:auditar-sistema    auditar
/design-system:documentar-pieza   documentar una pieza
/design-system:extender           diseñar un componente o patrón nuevo
```

**No hace falta memorizarlos.** Cada skill se carga sola cuando describís lo que querés.

---

## Instalación

Dentro de Claude Code (terminal, app de escritorio o extensión de IDE):

```
/plugin marketplace add GeanPaul2A/skills
/plugin install design-system@geanpaul-design
```

Para desarrollo local, desde la carpeta que contiene este repo:

```
/plugin marketplace add ./skills
/plugin install design-system@geanpaul-design
```

Si el resumen de instalación dice `Run /reload-plugins to activate.`, corré ese comando.

---

## Qué produce, y dónde

Todo lo específico de tu producto vive en **tu proyecto**, nunca dentro del plugin:

```
<tu-proyecto>/
├── marca.json              los parámetros visuales      ← plantillas/marca.json
├── proyecto.json           el producto y su contexto    ← plantillas/proyecto.json
├── dominios/<tipo>.json    tu negocio                   ← dominios/_plantilla.json
├── tokens/                 generado por derivar.py
├── inventario/             componentes, patrones, plantillas
├── modelo/                 generado por inyectar.py
├── pantallas/              una por pantalla declarada
└── salidas/                generado por construir.py — no se edita a mano
```

> **El plugin es agnóstico de negocio.** No trae dominios de ejemplo: trae `dominios/_plantilla.json`, cuya
> especificación son sus propios campos `_lee`. El negocio lo declara la skill `dominio`, en tu proyecto.

---

## El orden que conviene seguir

1. **`sistema-diseno`** — entrevista, tokens, inventario, verificación, galería. Sin sistema no hay pantalla.
2. **`dominio`** — entidades, reglas y patrones. Sin dominio, una pantalla no se puede verificar contra datos.
3. **`pantalla`** — plantilla, datos con su origen, los cuatro estados.
4. **`probar`** / **`documentar`** — antes de dar nada por terminado.
5. **`auditar`** — cuando ya hay algo construido y querés saber qué tan sano está.

---

## Las tres cosas que el sistema no negocia

**1 · Tres niveles de token.** Primitivo (`indigo.600`) → semántico (`accion.reposo`) → componente
(`boton.primario.fondo`). Un componente nunca cita un primitivo.

**2 · Cero fallos o no se entrega.** `verificar.py` corre 34 comprobaciones automáticas. Y una comprobación
saltada **no es un verde**: se reporta aparte, con su motivo.

**3 · Cada comprobación se prueba rompiendo algo a propósito.**

```bash
python3 <plugin>/skills/sistema-diseno/scripts/verificar.py --destino <destino> --romper DS-C03
```

Tiene que fallar. Los tres veredictos: `0` lo detectó · `1` pasó sin detectarse (la comprobación no sirve) ·
`2` no se pudo probar (está saltada).

---

## La doctrina

`design-system/conocimiento/doctrina.md` — **76 reglas `DS-xxx` con su procedencia bibliográfica.** 34 están
marcadas `auto` y las 34 tienen comprobación escrita y probada; el resto son `semi` o `manual` porque necesitan
renderizar, leer la herramienta de diseño, o criterio humano.

El invariante se mide con el `diff` documentado al final de esa doctrina, en «La regla sobre las reglas».
**Si imprime algo, una de las dos miente.** Corrélo antes de dar por cerrada cualquier regla nueva.

---

## La suite de regresión

`pruebas/` trae tres productos de prueba —movilidad, e-commerce y comida— con su marca, su proyecto, su
inventario y su modelo. **Están fuera del plugin a propósito**: son datos de prueba del repositorio, no parte
de lo que se distribuye.

```bash
# el pipeline completo sobre un fixture
python3 design-system/skills/sistema-diseno/scripts/derivar.py   --destino pruebas/movilidad
python3 design-system/skills/sistema-diseno/scripts/construir.py --destino pruebas/movilidad --salidas css,galeria
python3 design-system/skills/sistema-diseno/scripts/verificar.py --destino pruebas/movilidad
```

`tokens/` y `salidas/` son generados y están en `.gitignore`: se reconstruyen corriendo los guiones.
