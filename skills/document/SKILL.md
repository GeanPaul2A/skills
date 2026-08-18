---
name: document
description: Documenta un componente o patrón con su contrato completo para quien lo usa — descripción, variantes, propiedades con tipo y valor por omisión, estados, accesibilidad (rol, teclado, lector de pantalla), buenas y malas prácticas y ejemplo de código. Úsala SIEMPRE que el usuario pida documentar, especificar o escribir la ficha de un componente o patrón, o quiera que una pieza del inventario quede lista para publicarse.
---

# Documentar

**Un componente no está listo cuando se ve bien; está listo cuando su ficha está completa.** El inventario guarda
el contrato de máquina; `document` produce el contrato **para quien lo usa**: qué hace, cuándo usarlo, cuándo
no, y cómo se comporta en cada estado.

---

## 1 · Lo que no se negocia

**1 · De dónde sale.** Se documenta una pieza que **ya existe en el inventario** — DS-C01. No se documenta una
pieza que no está declarada.

**2 · Los tres campos nuevos del contrato.** `descripcion` y `cuando_no` ya existían (DS-C05); ahora se agregan
**`props`, `accesibilidad` y `ejemplo_codigo`**.

**3 · La accesibilidad es parte del contrato, no un anexo.** Rol ARIA, comportamiento de teclado y lo que anuncia
el lector de pantalla.

**4 · El `cuando_no` es el campo más valioso.** Dice qué usar en su lugar — DS-C05. Un «no» pelado no sirve.

---

## 2 · El procedimiento

> **Convención de salida — `output/`.** Todo lo que se genera va a `<destino>`, que es siempre
> `<proyecto>/output/`. Las carpetas del plugin (`${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`) son de
> **solo lectura**: nunca se escribe salida dentro de ellas.

### Paso 1 · Tomar la pieza del inventario

`output/inventario/componentes.json` o `output/inventario/patrones.json`. Si no está, primero se declara (`system-design` o
`domain`).

### Paso 2 · Completar la ficha

El formato completo y ejemplos, en `${CLAUDE_SKILL_DIR}/referencias/ficha.md`. Los campos:

| Campo | Qué es |
|---|---|
| `descripcion` · `cuando_no` | Qué es, cuándo usarlo y cuándo NO (con qué en su lugar) |
| `variantes` · `estados` · `tamanos` | Ya en el inventario |
| **`props`** | Propiedades: nombre, tipo, valor por omisión, qué hace |
| **`accesibilidad`** | Rol, teclado, lector de pantalla |
| **`ejemplo_codigo`** | Fragmento en el framework del producto |

### Paso 3 · Escribir los tres campos nuevos

**`props`, `accesibilidad` y `ejemplo_codigo` se agregan al inventario**, no se dejan en un doc suelto. El
verificador los valida — una pieza publicable tiene su ficha completa.

### Paso 4 · Verificar

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/system-design/scripts/verificar.py --destino <destino>
```

**Cero fallos o no se da por documentada.**

---

## 3 · Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Documentar lo que no existe** | Una ficha sin entrada en el inventario | Declarar primero — DS-C01 |
| **Sin `cuando_no`** | Solo dice qué es, nunca qué no es | El campo que más se salta y el más útil |
| **Accesibilidad como anexo** | Rol/teclado al final, si sobra tiempo | Parte del contrato |
| **Ejemplo inventado** | Código que no compila o no usa tokens | Con tokens reales del nivel 3 |

---

## 4 · Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/referencias/ficha.md` | **Al redactar.** El formato completo y ejemplos |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/03-components/README.md` | El contrato del inventario, campo por campo |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/06-accessibility/README.md` | Rol, teclado, lector de pantalla, contraste |

---

## 5 · Al terminar

1. **Qué se documentó** y qué campos nuevos se agregaron.
2. **El `cuando_no`** — qué usar en su lugar.
3. **La accesibilidad** declarada.
4. **El resultado de `verificar.py`.**
