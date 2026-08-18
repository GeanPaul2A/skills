# 02 · Tokens

**Un token es una decisión de diseño con nombre, que se puede transferir a código.** Es la pieza que convierte
un sistema de diseño en algo que un programa puede consumir, y es donde este proyecto se juega la consistencia.

**Clasificación:** `[Libro 1, capítulo 6]` la doctrina completa · `[Libro 2, capítulo 13]` la implementación en Figma ·
`[Extensión]` la elección de herramienta para este proyecto.

---

## Índice

1. [Qué es un token](#21--qué-es-un-token)
2. [Los tres niveles](#22--los-tres-niveles)
3. [Nomenclatura](#23--nomenclatura)
4. [El alias](#24--el-alias)
5. [Cuándo algo merece ser token](#25--cuándo-algo-merece-ser-token)
6. [El orden de construcción](#26--el-orden-de-construcción)
7. [Token, estilo y variable no son lo mismo](#27--token-estilo-y-variable-no-son-lo-mismo)
8. [El alcance](#28--el-alcance)
9. [La sintaxis por plataforma](#29--la-sintaxis-por-plataforma)
10. [Dónde viven los tokens](#210--dónde-viven-los-tokens)
11. [Reglas de esta sección](#211--reglas-de-esta-sección)

---

## 2.1 · Qué es un token

*Fuente: `[Libro 1, capítulo 6]`*

> *"Los tokens de diseño son **decisiones que tomas como diseñador**, pero a diferencia de los estilos, esas
> decisiones se pueden transferir directamente a código. ¿Qué decisiones? Cosas como colores, tipografía,
> espaciado, duración de animación, tamaños, opacidad."*

**Y el problema que resuelven, en la misma página:**

> *"Sin tokens, esas decisiones **las reescribe a mano el desarrollador** que mira tu diseño y transfiere los
> valores manualmente, introduciendo la posibilidad del error humano. Con tokens, el desarrollador trabaja con
> el token en lugar del valor."*

---

## 2.2 · Los tres niveles

*Fuente: `[Libro 1, capítulo 6]`*

**El libro lo explica con una escalera de cuatro líneas, y no hace falta más:**

```
#007BFF                      ¿dónde y cómo se usa esto?  Nadie lo sabe
color/blue/500               es un azul, nivel 500
color/background/default     es el fondo de un elemento, en su estado normal
button/primary/background    es el fondo del botón primario
```

> *"Cada nivel te da más contexto. **Empiezas con tokens primitivos** como `color/blue/500` **y construyes
> hacia tokens semánticos** como `color/background/default` **o incluso tokens de componente** como
> `button/primary/background`."*

| Nivel | Qué sabe | Ejemplo |
|---|---|---|
| **1 · Primitivo** | Solo el valor | `color.brand.500` = *(el valor sale de §1.9)* |
| **2 · Semántico** | **Para qué sirve** | `color.action.default` → `{color.brand.500}` |
| **3 · Componente** | **Dónde se aplica** | `button.primary.background` → `{color.action.default}` |

### Ejemplos de nivel 2 que el libro da como punto de partida

```
text/primary          el texto principal
text/secondary        subtítulos y texto secundario
text/error            mensajes de error
text/success          mensajes de éxito
surface/default       el fondo de la página
surface/raised        el fondo de una tarjeta o sección
border/default        el borde estándar
border/focus          el borde en estado de foco
```

### Y de nivel 3

```
button/primary/background      button/primary/text
button/secondary/background    button/secondary/border
```

---

## 2.3 · Nomenclatura

**OBLIGATORIO — un solo convenio en todo el sistema.** El libro abre con el contraejemplo:

```
// En lugar de esto:
Figma:    "Purple/500"
CSS:      "primary-color"
iOS:      "colorPurple"
Android:  "color_purple_primary"

// Usa un convenio compartido:
"color.primary.default": "#5C50E6"
```

### El convenio de esta base de conocimiento

```
<categoría>.<grupo>.<variante>[.<estado>]
```

| Ejemplo | Se lee |
|---|---|
| `color.brand.500` | Categoría color, grupo marca, paso 500 |
| `color.action.default` | Categoría color, rol acción, estado normal |
| `button.primary.background.pressed` | Componente botón, variante primaria, parte fondo, estado presionado |

**Se escribe con puntos en el JSON.** La conversión a `kebab-case`, `camelCase` o `snake_case` la hace la
herramienta de construcción, no la persona. Ver §2.9.

---

## 2.4 · El alias

*Fuente: `[Libro 1, capítulo 6]`*

**Un alias es un token que apunta a otro en lugar de a un valor.** Es lo que hace que la cadena funcione.

```
button.primary.background  →  {color.action.default}  →  {color.brand.500}  →  el valor
        nivel 3                     nivel 2                  nivel 1
```

**El libro explica el beneficio completo:**

> *"Si los desarrolladores implementan `button/primary/background` en el código, y más adelante cambias el
> valor subyacente al que ese token se conecta —digamos de `color/blue/500` a `color/green/500`—, **no
> necesitan modificar ni una línea**. Solo se actualiza el valor del token base en un solo lugar, y el cambio
> se propaga automáticamente por toda la jerarquía."*
>
> *"Esto significa que cambiar un color en cientos de componentes requiere actualizar **una sola línea** en
> lugar de cazar cada instancia a mano."*

### Y funciona en las dos direcciones

*Fuente: `[Libro 2, capítulo 13]`*

> *"También puedes **cambiar el significado de un token semántico** simplemente apuntándolo a otro
> primitivo."*

**Resuelve el caso más frecuente al madurar un sistema:** si el botón de acción y el chip seleccionado nacen
del mismo color y mañana tienen que separarse, **se reapunta `chip.selected.background` a otro primitivo** —
sin tocar ninguna pantalla.

---

## 2.5 · Cuándo algo merece ser token

*Fuente: `[Libro 1, capítulo 6]`*

### La regla de las tres apariciones

> *"Una buena regla general es que **si usas un valor —color, espaciado o tipografía— en tres o más lugares,
> probablemente merece un token**. Si solo se usa una o dos veces, quizá todavía no necesites uno."*

### Y la advertencia contraria, del mismo libro

> *"Algunos equipos son muy estrictos y exigen que todo sea un token, sin valores fijos permitidos. Aunque ese
> enfoque tiene mérito para sistemas grandes y maduros, **si estás empezando, el problema más grande al que te
> vas a enfrentar es administrar miles de tokens**, no tener algunos valores fijos."*

### Los cuatro errores de principiante, textuales

| Error | Qué es |
|---|---|
| **Sobre-tokenizar** | Crear tokens para valores que se usan una sola vez |
| **Sub-tokenizar** | **Usar el token primitivo directamente en todas partes en vez de crear el semántico** |
| **Nomenclatura inconsistente** | Mezclar convenios dentro del mismo sistema |
| **Demasiadas variaciones** | *"Crear 15 variantes de botón cuando en realidad solo necesitas 3"* |

> **El segundo es el que aparece en casi todo sistema nacido de CSS a mano.** Una variable como `--primary`
> es a la vez el valor y su significado, y no existe el tercer nivel. Por eso el botón, el chip activo y
> cualquier otro elemento acentuado **comparten variable sin compartir motivo** — y el día que uno tiene que
> cambiar, cambian todos.

### Empezar por una auditoría

**OBLIGATORIO al abrir un sistema sobre algo existente** `[Libro 1, capítulo 6]` — contar antes de decidir:

- ¿cuántos colores únicos se usan realmente?
- ¿cuántos valores de espaciado distintos aparecen?
- ¿cuántos estilos de tipografía hay?

> *"Puede sorprenderte descubrir que muchos diseñadores creen tener muchos más colores de los que realmente
> usan, cuando cuentan bien los valores únicos."*

---

## 2.6 · El orden de construcción

*Fuente: `[Libro 1, capítulo 6]`*

**OBLIGATORIO. El libro lo fija y no admite discusión:**

> *"No intentes tokenizar todo el primer día. Empieza con lo siguiente:*
> *1. **Colores primero:** son visuales y fáciles de entender.*
> *2. **Espaciado segundo:** normalmente 4-6 valores cubren la mayoría de los casos.*
> *3. **Tipografía tercero:** enfócate en los estilos de texto más comunes."*

---

## 2.7 · Token, estilo y variable no son lo mismo

**Tres palabras que se confunden todo el tiempo, y la distinción decide la arquitectura.**

| Concepto | Qué es | `[Libro]` |
|---|---|---|
| **Token** | Una decisión de diseño con nombre, **independiente de la herramienta** | `[Libro 1, capítulo 6]` |
| **Estilo de Figma** | Un **conjunto** de propiedades visuales — relleno sólido, degradado, sombra, imagen. Puede contener variables | `[Libro 2, capítulo 13]` |
| **Variable de Figma** | Un **valor único** — color, número, booleano o cadena — que se puede referenciar o **encadenar con alias** | `[Libro 2, capítulo 13]` |

### Lo que las variables de Figma **no** pueden hacer

*Fuente: `[Libro 1, capítulo 6]`*

**Solo admiten cuatro tipos: color, número, booleano y cadena.** Y falta el importante:

> *"Lo que falta de forma notable son los **tokens compuestos**. Toma la tipografía como ejemplo: en Token
> Studio, **un solo token de tipografía puede encapsular familia, tamaño, peso, interlineado y espaciado entre
> letras como una unidad cohesiva**."*

Otras limitaciones que el libro enumera: **4 modos** en el plan Profesional (40 en Empresarial), **sin control
de versiones propio**, y **hace falta un complemento de terceros para exportarlas a código**.

### La arquitectura final que el libro recomienda

*Fuente: `[Libro 2, capítulo 13]`*

**Cada estilo de color apunta a una variable semántica.** Resultado:

- cambiar de modo altera todo lo que usa ese estilo
- actualizar un primitivo se propaga por sus estilos semánticos
- la biblioteca exporta estilos limpios y documentados
- **el desarrollador ve tokens CSS estables en modo de desarrollo, aunque las variables evolucionen**

> *"Es la configuración más robusta y escalable: **los estilos quedan como tu API pública, mientras las
> variables son la capa de lógica interna** que impulsa el cambio de tema y la consistencia semántica."*

---

## 2.8 · El alcance

*Fuente: `[Libro 2, capítulo 13]`*

**Es el mecanismo que impide saltarse el sistema, y casi nadie lo usa.**

> *"El alcance define exactamente **dónde se puede aplicar una variable** y si debe aparecer como opción
> seleccionable para otros diseñadores… Más importante, el alcance permite **ocultar completamente una
> variable** de la interfaz de diseño y de la publicación. **Esto evita que los tokens primitivos se apliquen
> directamente en las maquetas** y garantiza que se usen exclusivamente como alias de tokens semánticos de
> nivel superior."*

### Cómo se hace

1. Seleccionar **todas** las variables primitivas
2. Botón derecho → *Edit variables*
3. Pestaña **Detail** → marcar **Hide from publishing**
4. Pestaña **Scope** → **desmarcar** *Show in all supported properties*

**OBLIGATORIO** — **la colección de primitivos va oculta**. Nadie puede pintar un botón con
`color.brand.500`; solo con `button.primary.background`.

> **Es la diferencia entre un sistema que se recomienda y uno que no se puede evitar.**

---

## 2.9 · La sintaxis por plataforma

*Fuente: `[Libro 1, capítulo 8]`*

**Cada plataforma tiene su convenio, y son incompatibles entre sí:**

| Plataforma | Convenio | Ejemplo |
|---|---|---|
| **Web** | `kebab-case` | `--color-primary-500` |
| **iOS** | `camelCase` | `colorPrimary500` |
| **Android** | `snake_case` | `color_primary_500` |

### La solución no es duplicar variables

> *"**No necesitas configurar variables específicas por plataforma**, porque eso crearía múltiples variables
> sin ninguna razón y construiría un sistema súper complejo casi para nada. Lo que haces en su lugar es
> preparar el nombre por plataforma mediante **Code syntax** en cada variable."*
>
> *"Esto significa que tendrás **una sola variable**, pero se nombrará distinto para web, iOS o Android, así
> que cada desarrollador verá el convenio que espera."*

**OBLIGATORIO** — toda variable publicada lleva su sintaxis de código para las tres plataformas.

---

## 2.10 · Dónde viven los tokens

*Fuente: `[Extensión]`*

**El libro da el criterio de herramienta** `[Libro 1, capítulo 6]`:

> *"Si estás construyendo un sistema pequeño solo en Figma, con modo claro y oscuro a lo sumo, **usa variables
> de Figma**. Si estás construyendo algo más grande, a prueba de futuro y no atado a Figma, **usa Token
> Studio**."*
>
> Y la pregunta previa: *"¿los tokens los van a usar solo diseñadores, o también desarrolladores? Si hay
> desarrolladores involucrados, recomendaría **Token Studio en el 99 % de los casos**."*

### La matriz de decisión

**Tres preguntas, y cada producto las responde por sí mismo:**

| Criterio | Si la respuesta es… | Empuja hacia |
|---|---|---|
| ¿Los tokens los usan también desarrolladores? | **Sí** | Token Studio |
| ¿El sistema vive solo en Figma? | **No** — hay más de un destino de código | Token Studio |
| ¿Hay presupuesto recurrente? | **No.** Token Studio necesita versión de pago para temas y carpetas | **Variables de Figma** |

> **Las dos primeras y la tercera tiran en direcciones opuestas en la mayoría de los casos.** Lo que sigue
> es cómo se resuelve el empate sin pagar.

### La decisión por defecto

**El propio libro habilita la salida:**

> *"Esta estructura se puede aplicar con Token Studio o con variables de Figma — **los principios son los
> mismos sea cual sea la herramienta que elijas**."*

**Entonces:**

```
tokens/*.json            ←  LA FUENTE DE VERDAD.  JSON, en git, revisable
      │
      ├── Style Dictionary ──→  tokens.css           pantallas y código
      └── importador       ──→  variables de Figma   para dibujar
```

**Style Dictionary es el estándar que el propio libro nombra** `[Libro 1, capítulo 6]`: *"el JSON exportado se
procesa típicamente con Style Dictionary, el estándar de la industria para transformar tokens de diseño a
formatos específicos de plataforma como variables CSS, Swift de iOS o XML de Android."*

**Lo que se pierde frente a Token Studio de pago:** la visualización de dependencias entre tokens, y los temas
ilimitados. **Con menos de doscientos tokens, ninguna de las dos hace falta.**

### Las colecciones

*Fuente: `[Libro 2, capítulo 13]`*

**El libro construye seis, y esta base de conocimiento las adopta:**

| Colección | Contiene | Modos |
|---|---|---|
| `Primitives` | Los valores crudos | — · **oculta** |
| `Semantic` | Los roles | **Claro** · *(Oscuro, después)* |
| `Number` | Espaciado y radios | — |
| `Breakpoints` | Medidas por dispositivo | **Móvil · Tableta · Escritorio** |
| `Typography` | Familia, tamaño, peso | **Móvil · Escritorio** |
| `Copy` | **Los textos de interfaz** | **es** · *(otros idiomas)* |

> **`Copy` es la que hace real el multi-país.** El texto deja de estar escrito en la pantalla y pasa a ser un
> valor con un modo por idioma — el mismo principio que rige en un modelo de datos bien hecho, donde moneda,
> país e idioma son **dato y no código**.

### El peso, como número

*Fuente: `[Libro 2, capítulo 13]`*

> *"Los pesos se pueden crear como cadena o como número. **El número es la opción más segura**: los pesos
> numéricos (700, 400, 300) se mantienen consistentes entre tipografías, mientras que los nombres varían
> mucho (Bold contra SemiBold contra DemiBold, Regular contra Normal)."*

---

## 2.11 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-T01`** | Todo token vive en **JSON versionado**; el CSS y las variables de Figma son **salidas generadas**, nunca fuentes | OBLIGATORIO | `[Libro 1, capítulo 6]` · `[Extensión]` |
| **`DS-T02`** | **Tres niveles.** Un componente **nunca** referencia un primitivo directamente | OBLIGATORIO | `[Libro 1, capítulo 6]` |
| **`DS-T03`** | La colección de primitivos va **oculta de publicación y sin alcance** | OBLIGATORIO | `[Libro 2, capítulo 13]` |
| **`DS-T04`** | Un solo convenio de nombres en todo el sistema | OBLIGATORIO | `[Libro 1, capítulo 6]` |
| **`DS-T05`** | Toda variable publicada declara su **sintaxis de código** para web, iOS y Android | OBLIGATORIO | `[Libro 1, capítulo 8]` |
| **`DS-T06`** | El orden de construcción es **color → espaciado → tipografía** | OBLIGATORIO | `[Libro 1, capítulo 6]` |
| **`DS-T07`** | **Ningún valor en crudo** en una pantalla: ni color, ni espaciado, ni tamaño de letra, ni radio | OBLIGATORIO | `[Extensión G1]` |
| **`DS-T08`** | Un valor merece token si aparece en **tres o más lugares** | RECOMENDADO | `[Libro 1, capítulo 6]` |
| **`DS-T09`** | El peso tipográfico se guarda como **número**, no como nombre | RECOMENDADO | `[Libro 2, capítulo 13]` |
| **`DS-T10`** | Los estilos de Figma apuntan a variables semánticas — **estilos como API pública, variables como lógica interna** | RECOMENDADO | `[Libro 2, capítulo 13]` |
