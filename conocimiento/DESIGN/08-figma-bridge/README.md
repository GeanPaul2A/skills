# 08 · Figma Bridge (El puente con Figma)

**Cómo el sistema —que vive en el repositorio— llega a Figma y vuelve.** Esta sección define la mecánica de
variables, colecciones, modos y alcance, y qué se puede automatizar hoy.

**Clasificación:** `[Book 2, cap. 13]` variables, colecciones y modos · `[Book 1, cap. 6]` tokens contra
variables · `[Book 1, caps. 2 y 8]` los complementos de exportación y la sintaxis por plataforma.

---

## Índice

1. [La dirección del puente](#81--la-dirección-del-puente)
2. [Las colecciones](#82--las-colecciones)
3. [Los modos](#83--los-modos)
4. [El alcance](#84--el-alcance)
5. [La sintaxis de código](#85--la-sintaxis-de-código)
6. [Estilos como API, variables como lógica](#86--estilos-como-api-variables-como-lógica)
7. [Sacar los tokens de Figma](#87--sacar-los-tokens-de-figma)
8. [Qué se puede automatizar hoy](#88--qué-se-puede-automatizar-hoy)
9. [Reglas de esta sección](#89--reglas-de-esta-sección)

---

## 8.1 · La dirección del puente

**La fuente de verdad es el repositorio, no Figma.** Está decidido en `02-tokens` §2.10:

```
tokens/*.json            ←  LA FUENTE.  JSON, en git, revisable
      │
      ├── Style Dictionary ──→  CSS / Swift / XML      código
      └── importador       ──→  variables de Figma     para dibujar
```

**Por qué en esa dirección y no al revés** `[Book 1, cap. 6]`:

- las variables de Figma **no tienen control de versiones propio** — *"viven en tu archivo junto con todo lo demás"*
- **hace falta un complemento de terceros** solo para exportarlas a código
- **solo admiten cuatro tipos** — color, número, booleano y cadena — sin tokens compuestos

> **Y el argumento de fondo del libro:** *"Cuando empecé a usar Figma, escuchaba seguido: 'eso es absurdo,
> todo el mundo diseña en Photoshop o Sketch, Figma nunca va a funcionar'. Bueno… eso no envejeció bien. Hubo
> un tiempo en que Figma era el jugador chico. Hoy es un gigante, **pero esa posición puede cambiar**."*

---

## 8.2 · Las colecciones `[Book 2, cap. 13]`

**Una colección agrupa variables que comparten propósito y modos.** El libro construye seis; esta KB las
adopta:

| Colección | Contiene | Publicada |
|---|---|---|
| `Primitives` | Los valores crudos, agrupados por familia | **No — oculta** |
| `Semantic` | Los roles: superficie, texto, acción, estado | Sí |
| `Number` | Espaciado y radios | Sí |
| `Breakpoints` | Medidas y visibilidad por dispositivo | Sí |
| `Typography` | Familia, tamaño y peso | Sí |
| `Copy` | **Los textos de interfaz** | Sí |

### `Copy` es la que hace real el multi-país

**El libro la usa para dos idiomas** `[Book 2, cap. 13]` — una columna por modo, con el mismo token
resolviendo a texto distinto.

**En cuanto el producto opera en más de un país deja de ser un ejercicio:** si el modelo de datos trata
**moneda, país, zona horaria e idioma como dato y no como código**, un sistema de diseño con el texto escrito
dentro de la pantalla **contradice el modelo que ya está construido y verificado**.

### El peso tipográfico va como número

> *"Los pesos se pueden crear como cadena o como número. **El número es la opción más segura**: los pesos
> numéricos (700, 400, 300) se mantienen consistentes entre tipografías, mientras que los nombres varían mucho
> — Bold contra SemiBold contra DemiBold, Regular contra Normal."*

### La familia va como cadena, y con una trampa

> *"Los valores de cadena **deben coincidir exactamente** con el nombre de la fuente tal como está escrito en
> Figma, incluyendo mayúsculas y espacios. **Cualquier diferencia rompe el enlace.**"*

---

## 8.3 · Los modos `[Book 2, cap. 13]`

**Un modo es una columna de valores alternativos para las mismas variables.**

```
Semantic              Claro          Oscuro
  surface.background  White          Grey/900
  surface.card        Grey/100       Grey/800
  text.default        Grey/900       White
  text.secondary      Grey/600       Grey/100
```

**Cambiar el modo del marco cambia toda la pantalla.** No hay pantallas duplicadas que mantener.

### Los modos por defecto

**Este es el reparto de partida; cada producto lo ajusta a los suyos:**

| Colección | Modos |
|---|---|
| `Semantic` | **Claro · Oscuro** |
| `Breakpoints` | **Móvil · Tableta · Escritorio** |
| `Typography` | **Móvil · Escritorio** |
| `Copy` | **Un modo por idioma** |

**El límite del plan** `[Book 1, cap. 6]`: **4 modos** en Profesional, 40 en Empresarial. *"Esta limitación
artificial existe para incentivar la mejora de plan."*

> **Consecuencia práctica:** con cuatro modos por colección alcanza para claro/oscuro y tres puntos de corte.
> **A partir del cuarto idioma hace falta otra colección o cambiar de plan** — conviene registrarlo al
> empezar, para que no aparezca como sorpresa a mitad del trabajo.

### Las booleanas de visibilidad

**El libro las usa para resolver la navegación entre dispositivos** `[Book 2, cap. 13]`:

```
Breakpoints          Escritorio   Tableta   Móvil
  _showDesktop          True       False    False
  _showMobile          False        True     True
```

**El guion bajo inicial las marca como internas.** Ver `DS-C04`.

---

## 8.4 · El alcance `[Book 2, cap. 13]`

**Es el mecanismo que impide saltarse el sistema, y es la parte que casi nadie configura.**

> *"El alcance define exactamente **dónde se puede aplicar una variable** y si debe aparecer como opción
> seleccionable para otros diseñadores. En la práctica, permite restringir una variable de color a propiedades
> específicas — por ejemplo, hacerla disponible solo para trazos e impedir su uso en rellenos. Más importante,
> **el alcance permite ocultar completamente una variable de la interfaz de diseño y de la publicación**. Esto
> evita que los tokens primitivos se apliquen directamente en las maquetas y garantiza que se usen
> exclusivamente como alias de tokens semánticos de nivel superior."*

### El procedimiento

1. seleccionar **todas** las variables de `Primitives`
2. botón derecho → *Edit variables*
3. pestaña **Detail** → marcar **Hide from publishing**
4. pestaña **Scope** → **desmarcar** *Show in all supported properties*

### Y el alcance fino, por tipo

| Tipo | Se puede acotar a |
|---|---|
| **Color** | Relleno · marco · forma · texto · trazo · efectos |
| **Número** | Radio · ancho y alto · espacio de Auto Layout · trazo · opacidad · efectos · peso · tamaño · interlineado · espaciado entre letras |

**RECOMENDADO** — acotar el número también por tipo: que la escala de espaciado **no aparezca** como opción
para el radio de esquina, y viceversa.

---

## 8.5 · La sintaxis de código `[Book 1, cap. 8]`

**Una sola variable, tres nombres.** Se configura en el campo *Code syntax* de cada variable:

```
Web       →  --color-primary-500
Android   →  color_primary_500
iOS       →  colorPrimary500
```

> *"**No necesitas configurar variables específicas por plataforma**, porque eso crearía múltiples variables
> sin ninguna razón y construiría un sistema súper complejo casi para nada."*

**Y el efecto en el modo de desarrollo:** cada desarrollador ve el nombre que espera, en su lenguaje —
`background: var(--color-primary-500)` en CSS, `.background(colorPrimary500)` en SwiftUI,
`background(color = color_primary_500)` en Compose.

**El campo existe también al editar una variable suelta** `[Book 2, cap. 13]`, y sirve *"cuando tu
nomenclatura de diseño difiere de la de código, o cuando tu equipo de ingeniería ya sigue una estructura de
tokens específica"*.

---

## 8.6 · Estilos como API, variables como lógica `[Book 2, cap. 13]`

**La arquitectura final que el libro recomienda, y la razón de cada parte:**

**Cada estilo de color apunta a una variable semántica** en lugar de a un valor fijo. Resultado:

- cambiar de modo **altera todo lo que use ese estilo**
- actualizar un primitivo **se propaga por sus estilos semánticos**
- la biblioteca **exporta estilos limpios y documentados** a los archivos que la consumen
- **el desarrollador ve tokens CSS estables** en modo de desarrollo, aunque las variables evolucionen

> *"Esta es la configuración más robusta y escalable: **los estilos quedan como tu API pública**, mientras las
> **variables son la capa de lógica interna** que impulsa el cambio de tema y la consistencia semántica."*

---

## 8.7 · Sacar los tokens de Figma `[Book 1, cap. 2]`

**Figma no exporta variables a código de forma nativa.** Los complementos que el libro nombra:

| Complemento | Qué produce |
|---|---|
| **Variables to CSS** | Propiedades personalizadas — `--dds-core-color-primary-500: #8855e2;` |
| **Variables to JSON** | JSON, con opción de convenio de nombres, resolución de alias y filtro por tipo |

**Y el destino habitual del JSON** `[Book 1, cap. 6]`: *"en entornos empresariales, el JSON exportado se
procesa típicamente con **Style Dictionary**, el estándar de la industria para transformar tokens de diseño a
formatos específicos de plataforma."*

> **Cuando la fuente de verdad es el repositorio, el flujo va al revés:** el JSON se escribe a mano y **entra** a
> Figma. Los complementos de exportación quedan como **camino de verificación** — sacar las variables y
> comprobar que coinciden con el JSON.

### El criterio para adoptar un complemento `[Book 1, cap. 2]`

**El libro da un árbol de decisión, y las preguntas son:**

1. ¿soy el único usuario? → si sí, el riesgo es bajo
2. ¿es de un solo uso? → si sí, se puede ser flexible
3. ¿es de pago? → *"prioriza complementos con modelo de negocio sostenible o respaldo corporativo"*
4. ¿lo desarrolla una empresa? → mayor probabilidad de mantenimiento
5. **¿hay alternativas confiables?** → *"si es crítico para tu flujo y no tiene competidores directos, evalúa
   su sostenibilidad a largo plazo"*

**Y una señal concreta:** *"si un complemento no se ha actualizado en más de dos años, conviene ser cauteloso"*.

---

## 8.8 · Qué se puede automatizar hoy

**Se registra el estado real, no el deseado.**

| Operación | Estado | Fuente |
|---|---|---|
| **Leer** un archivo de Figma desde un agente | **Documentado** — servidor MCP, *Inspect → MCP server*, con Claude Code entre sus clientes | `[Book 2, cap. 11]` |
| **Extraer** contexto de diseño para generar código | **Documentado** — la herramienta se llama `get_design_context` | `[Book 2, cap. 11]` |
| **Escribir** en el lienzo desde un agente | **Confirmado — 17-08-2026.** `use_figma` ejecuta la Plugin API en el archivo: crea nodos, variables, componentes y variantes. `create_new_file` crea el archivo | Comprobación directa contra el servidor |
| **Atar** componente de Figma ↔ componente de código | **Confirmado.** `get_code_connect_map` y `add_code_connect_map` | Comprobación directa |
| Generar prototipo desde una indicación | **Figma Make**, en beta. Produce **HTML/CSS/JS plano**, no componentes | `[Book 1, cap. 3]` |

### Lo que el libro suponía, y lo que resultó

**El libro concluyó que el puente era de solo lectura**, leyendo la descripción del servidor —*«Send design
context to your AI agent»*— y el nombre de su herramienta de confirmación, `get_design_context`
`[Book 2, cap. 11]`. **Era una inferencia razonable y quedó desactualizada.**

> **Se registra el cambio en vez de reescribir el pasado:** la conclusión del libro era correcta para su
> fecha; el servidor creció. Es exactamente el motivo por el que esta sección se llama *«qué se puede
> automatizar hoy»* y no *«qué se puede automatizar»*.

### La consecuencia para el plan

**OBLIGATORIO — `DS-X06` no se toca, y ahora vale más que antes.** Que el puente escriba es una ganancia, no
una dependencia. **Ninguna etapa depende de que un agente escriba en el lienzo**, y el motivo se refuerza: un
asiento *View* o un plan starter deja las mismas herramientas visibles y **el permiso denegado a mitad de la
construcción**. Se comprueba el asiento antes de prometer nada.

> El sistema vive en el repositorio y Figma es una salida. **Lo que cambió es que ahora es una salida que se
> puede escribir sola** — no que el repositorio haya dejado de mandar.

---

## 8.9 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-X01`** | La fuente de verdad es el **JSON del repositorio**; Figma es una salida | OBLIGATORIO | `[Book 1, cap. 6]` · `[Ext]` |
| **`DS-X02`** | `Primitives` va **oculta de publicación y sin alcance** | OBLIGATORIO | `[Book 2, cap. 13]` |
| **`DS-X03`** | Toda variable publicada declara su **sintaxis de código** para las tres plataformas | OBLIGATORIO | `[Book 1, cap. 8]` |
| **`DS-X04`** | Los estilos apuntan a **variables semánticas**, nunca a valores fijos | OBLIGATORIO | `[Book 2, cap. 13]` |
| **`DS-X05`** | El peso tipográfico va como **número**; la familia como **cadena exacta** | OBLIGATORIO | `[Book 2, cap. 13]` |
| **`DS-X06`** | **Ninguna etapa depende de que un agente escriba en el lienzo** | OBLIGATORIO | `[Ext]` |
| **`DS-X07`** | El alcance se acota también **por tipo de propiedad** | RECOMENDADO | `[Book 2, cap. 13]` |
| **`DS-X08`** | Un complemento no se adopta sin pasar el **árbol de decisión** | RECOMENDADO | `[Book 1, cap. 2]` |
