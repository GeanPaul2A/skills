---
name: pantalla
description: "Diseña pantallas y flujos usando un sistema de diseño ya construido — declara la plantilla, ata cada dato a su origen, cubre carga, vacío y error, verifica contra las reglas del sistema y lo dibuja en el lienzo por MCP o lo entrega como HTML. Úsala SIEMPRE que el usuario pida diseñar, maquetar o prototipar una pantalla, una vista, un flujo, un formulario, una lista, un onboarding, un registro, un inicio de sesión, un panel, o quiera ver cómo se vería una función. Requiere un sistema de diseño: si no existe, primero la skill sistema-diseno."
---

# Pantalla

Una pantalla es **una plantilla, unos datos y unos estados**. Nada más, y **nunca menos**.

**Sin sistema de diseño no hay pantalla.** Si no existe, se construye primero con la skill `sistema-diseno`.
Diseñar sin sistema produce pantallas que se ven bien sueltas y no se parecen entre sí.

---

## Lo que no se negocia

**1 · Los datos primero.** Es el error número uno del oficio, y tiene nombre:

> *"Uno de los errores más comunes es **empezar por la maqueta antes de tener idea de qué datos necesita
> mostrar el producto**. Ese enfoque produce maquetas limpias y elegantes **que se desarman en cuanto entran
> los datos de verdad**."* `[B2, cap. 4]`

**2 · Ningún valor en crudo.** Todo color, espacio, tamaño y radio es un token del nivel 3 — DS-T07. Un
`#3A45C9` escrito en una pantalla es una pantalla que no se puede volver a tematizar.

**3 · Cuatro estados, no uno.** Lleno, **cargando, vacío y error**. Entregar solo el caso feliz es entregar
un cuarto del trabajo — DS-C03.

**4 · Se prueba con el valor más largo y el más corto** — DS-L06. Un nombre de dos letras y uno de cuarenta.
Es donde las maquetas se rompen.

**5 · Toda caja lleva disposición automática** — DS-L01. Sin ella la herramienta emite coordenadas absolutas
y la pantalla deja de ser responsiva `[B2, cap. 11]`.

---

## El orden

### Paso 1 · Encontrar el sistema

Busca `marca.json` y `tokens/` en el proyecto. **Si no están, para acá** y ofrece construirlo con
`sistema-diseno`. No improvises tokens.

**Y busca `dominios/<tipo>.json`: es el negocio.** Si no está, la skill `dominio` lo define antes de dibujar.

**Lee `inventario/componentes.json` y `inventario/plantillas.json`**: eso es lo que hay disponible. **No se
inventan componentes al vuelo** — si falta uno, se agrega al inventario primero, con su contrato.

### Paso 2 · Los datos, antes de dibujar

**Antes de la primera caja, responde:**

| Pregunta | Por qué |
|---|---|
| ¿Qué **entidades** aparecen en esta pantalla? | Si no se sabe, la maqueta va a inventar campos |
| ¿Qué **campos** de cada una se muestran? | Cada dato visible necesita un campo que lo respalde — DS-P02 |
| ¿Qué **reglas de negocio** la gobiernan? | Un plazo, un mínimo, una condición |
| ¿Qué viene **de otra fuente**, y qué se muestra si no llega? | DS-P04 |
| ¿Cuál es el valor **más largo** y el **más corto** de cada campo? | DS-L06 |

**Si hay un `dominios/<tipo>.json`, esto se comprueba solo**: cada dato se cruza contra una entidad y un campo
de ese dominio — DS-P02. **Si no hay dominio, la skill `dominio` lo define primero.** Sin dominio, la pantalla
se entrega marcada como no verificada contra datos, y se dice en voz alta.

> **Nunca inventes un campo para que la maqueta quede linda.** Un dato que el producto no tiene es una
> pantalla que no se puede construir.

### Paso 3 · Elegir la plantilla

De `inventario/plantillas.json`. **Cada zona dice qué componentes admite**: si el que hace falta no está en
ninguna zona, o la plantilla es la equivocada, o el componente falta en el inventario.

### Paso 4 · Declarar la pantalla

Un archivo por pantalla, en `pantallas/<nombre>.json`. **El formato, en `${CLAUDE_SKILL_DIR}/referencias/generacion.md`.**

Declara: plantilla · zonas con sus componentes · datos con su origen · los cuatro estados · los textos con su
versión más larga.

### Paso 5 · Verificar

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/verificar-pantalla.py --sistema <sistema> --pantallas <carpeta>
```

**Cero fallos o no se entrega.** Y **las comprobaciones saltadas se leen en voz alta**: son las preguntas que
quedaron sin hacer.

Al agregar una comprobación, **pruébala rompiendo algo a propósito** —`--romper DS-L06`—. **El veredicto es de
la regla que se rompió, no del total**, y son tres: **✓ lo detectó** (código `0`), **✗ pasó sin detectarse**
(`1`, la comprobación no sirve) y **⚠ no se pudo probar** (`2`, está saltada — **no es un verde**).

### Paso 6 · Dibujar o entregar

| Si hay | Qué hacer |
|---|---|
| **Un puente que escribe en el lienzo** | Importar variables → estilos → componentes → **y recién ahí** las pantallas |
| **Un puente que solo lee** | **Decirlo.** Entregar el HTML y el documento de lienzo |
| **Ninguno** | El HTML se abre en un navegador y ya se ve |

**Comprueba la clase de puente antes de prometer nada** — `${CLAUDE_PLUGIN_ROOT}/skills/sistema-diseno/referencias/puentes.md`.

---

## Un flujo, no una pantalla suelta

**Cuando el usuario pide «el registro» o «el pago», pide un flujo.** Un flujo se declara como **patrón**, y un
patrón tiene **cinco momentos** `[B2, cap. 9]`:

**entrada · decisión · éxito · error · salida**

**Si falta el cuarto, el patrón está incompleto** — DS-P03. Y es el que siempre falta.

El detalle, en `${CLAUDE_SKILL_DIR}/referencias/patrones.md`.

---

## Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Maqueta antes que datos** | La pantalla muestra campos que nadie confirmó | Paso 2, siempre |
| **Solo el caso feliz** | No hay estado vacío ni de error | Los cuatro estados |
| **Texto de ejemplo corto** | «Ana» donde va un nombre completo | El valor más largo real |
| **Valores en crudo** | Un `#3A45C9` o un `13px` en la pantalla | Tokens del nivel 3 |
| **Componente inventado** | Una pieza que no está en el inventario | Agregarla al inventario primero |
| **Lo importante bajo el pliegue** | Lo que distingue al producto no se ve sin desplazar | Anclarlo o subirlo |
| **Cajas sin disposición** | Coordenadas absolutas al exportar | Disposición automática en todas |
| **Dos H1** | Dos titulares del mismo peso | Uno solo — DS-A05 |

> **El del pliegue es el más caro y el menos visible.** Lo que hace único al producto tiene que verse **sin
> desplazar**. Si hay que bajar para encontrarlo, para el usuario no existe.

---

## Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/referencias/generacion.md` | **Al declarar la pantalla.** El formato y las reglas de armado |
| `${CLAUDE_SKILL_DIR}/referencias/patrones.md` | Cuando es un flujo, no una pantalla |
| `${CLAUDE_SKILL_DIR}/referencias/revision.md` | **Antes de entregar.** La lista de comprobación |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/componentes.md` | Si falta un componente |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/accesibilidad.md` | Contraste, foco, orden de lectura |
| `${CLAUDE_PLUGIN_ROOT}/skills/sistema-diseno/referencias/puentes.md` | Al dibujar en el lienzo |

---

## Al terminar

1. **Qué pantallas se hicieron**, y de qué plantilla sale cada una.
2. **Qué datos usan** y de dónde salen — o **que no se pudo comprobar**, si no hay modelo.
3. **Qué estados se cubrieron.** Si alguno quedó afuera, se dice.
4. **Qué verificó el guion**, y qué saltó.
5. **Lo que hay que mirar a ojo**: lo que ninguna comprobación detecta.
6. **La pantalla**, para que la vea.
