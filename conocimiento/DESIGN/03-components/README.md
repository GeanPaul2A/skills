# 03 · Components (Componentes)

**Un componente es una pieza reutilizable con una fuente única.** Esta sección define qué hay que declarar de
cada uno — y por qué decir *"existe un botón"* no alcanza.

**Clasificación:** `[Book 1, cap. 5]` arquitectura y gobierno · `[Book 2, cap. 7]` mecánica de componentes y
variantes · `[Ext G3]` el contrato legible por máquina.

---

## Índice

1. [Componente no es lo mismo que estilo](#31--componente-no-es-lo-mismo-que-estilo)
2. [La arquitectura de cuatro niveles](#32--la-arquitectura-de-cuatro-niveles)
3. [Principal e instancia](#33--principal-e-instancia)
4. [La declaración de un componente](#34--la-declaración-de-un-componente)
5. [Los estados](#35--los-estados)
6. [Las propiedades](#36--las-propiedades)
7. [Cuándo agrupar como variantes, y cuándo no](#37--cuándo-agrupar-como-variantes-y-cuándo-no)
8. [Organizar la biblioteca](#38--organizar-la-biblioteca)
9. [Una biblioteca o varias](#39--una-biblioteca-o-varias)
10. [Reglas de esta sección](#310--reglas-de-esta-sección)

---

## 3.1 · Componente no es lo mismo que estilo `[Book 2, cap. 7]`

> *"A diferencia de los estilos, que aplican propiedades consistentes —color, tipografía, efectos— a elementos
> individuales, **los componentes incluyen los objetos mismos**: su estructura, jerarquía, contenido y
> disposición."*

| | Aplica | Ejemplo |
|---|---|---|
| **Estilo** | Una propiedad visual | *"este texto usa `Body/Regular`"* |
| **Token** | Un valor con nombre | *"este relleno es `spacing.3`"* |
| **Componente** | **Una estructura completa** | *"esto es una tarjeta de oferta"* |

---

## 3.2 · La arquitectura de cuatro niveles `[Book 1, cap. 5]`

**El libro presenta dos arquitecturas y prefiere la segunda.** Esta KB toma esa.

| Atomic Design (Brad Frost) | La alternativa del autor ← **esta** |
|---|---|
| Atoms | **PRIMITIVOS** — tokens, fundamentos |
| Molecules | **COMPONENTES** — elementos de interfaz sueltos |
| Organisms | **PATRONES** — combinaciones de componentes |
| Templates | **PLANTILLAS** — estructura de pantalla |
| Pages | *(no se usa)* |

> *"Este enfoque **elimina parte de la confusión** en torno a la terminología átomos/moléculas y crea
> distinciones más claras entre niveles de complejidad."*

### Y la advertencia que ordena todo el trabajo

> *"Lo más importante al construir bibliotecas de componentes es **tener fundamentos perfectos** — tokens,
> nomenclatura de color, semántica y toda la estructura subyacente. Nuestro diseñador dedicó **mucho más tiempo
> a crear la estructura de fundamentos y los tokens que a crear los componentes**."*

---

## 3.3 · Principal e instancia `[Book 2, cap. 7]`

```
COMPONENTE PRINCIPAL  ◆ (rombo relleno)     la fuente única
        ↓
INSTANCIA             ◇ (rombo hueco)       una copia enlazada
```

**Al actualizar el principal, todas las instancias se actualizan solas.**

### El detalle que hay que entender del sobreescrito

> *"Cuando sobreescribes una propiedad en una instancia —cambiar su color o su texto—, **esa propiedad
> específica queda desconectada del componente principal**. Si después actualizas esa misma propiedad en el
> principal, ya no se propagará a la instancia sobreescrita. **Todas las demás propiedades sin tocar siguen
> sincronizadas.**"*

### Las tres acciones sobre una instancia

| Acción | Qué hace |
|---|---|
| **Restablecer instancia** | La devuelve a coincidir exactamente con el principal |
| **Restablecer tamaño** | Solo revierte el tamaño, conserva contenido y estilo |
| **Desvincular instancia** | **Destructiva.** Corta el enlace y la vuelve un marco normal |

**OBLIGATORIO** — desvincular es la última salida, nunca la primera. Si hace falta desvincular, **casi siempre
significa que al componente le falta una variante**.

> **Es una señal medible** `[Book 1, cap. 5]`: *"si ves un número grande de componentes desvinculados, tienes
> un problema. Quizá te falta una variante — eso debería ser una señal para repriorizar tu hoja de ruta."*

---

## 3.4 · La declaración de un componente

**`[Book 1, cap. 5]` — el libro es explícito en que no basta con decir que el botón existe.** Lo que hay que
declarar:

```
Button
  variantes:  primary · secondary · tertiary · destructive
  tamaños:    small · medium · large
  estados:    default · hover · pressed · disabled · loading
  icono:      ninguno · adelante · atrás
```

### `[Ext G3]` — y acá se declara como dato, no en prosa

**El vacío:** los libros describen las variantes como propiedades **dentro de Figma** —`◆ Variant`,
`○ Toggle`, `@ Content`—. **Un verificador no puede leer eso.**

**Por eso cada componente declara su contrato en `inventario/componentes.json`:**

```json
"boton": {
  "variantes": ["primario", "secundario", "silencioso", "destructivo"],
  "tamanos":   ["sm", "md", "lg"],
  "estados":   ["reposo", "presionado", "foco", "deshabilitado", "cargando"],
  "tokens":    ["acento", "acento_press", "space.interior", "radius.md"],
  "reglas":    ["DS-C02", "DS-C03", "DS-A02"]
}
```

**OBLIGATORIO** — ningún componente entra al sistema sin su entrada en el inventario.

---

## 3.5 · Los estados

**Es la parte que más se omite, y la que más cuesta después.**

### Los estados de interacción

| Estado | Cuándo | Obligatorio porque |
|---|---|---|
| `default` | En reposo | — |
| `hover` | Puntero encima | **Solo escritorio.** En móvil no existe `[Book 2, cap. 8]` |
| `pressed` | Mientras se mantiene | Retroalimentación táctil |
| **`focus`** | Al llegar por teclado | **`[Book 1, cap. 7]` — accesibilidad. Con contraste mínimo 3:1** |
| `disabled` | No se puede usar | Y **por qué** no se puede tiene que ser visible |
| **`loading`** | Esperando respuesta | Ver abajo |

**OBLIGATORIO** — **todo elemento interactivo declara su estado de foco.**

> `[Book 1, cap. 7]`: *"Si una acción se puede hacer con el ratón, **debe poder hacerse también con el
> teclado**, y cualquier elemento interactivo debe recibir un indicador de foco visible al navegar con
> teclado."*

### Los tres estados de contenido `[Book 1, cap. 8]`

**El libro los exige en su lista de comprobación de calidad** — *"¿están implementados correctamente los
estados de carga? ¿están los estados de error bien diseñados y funcionales?"*

| Estado | Qué muestra |
|---|---|
| **Cargando** | Que el sistema está trabajando, y **cuánto falta si se sabe** |
| **Vacío** | Que no hay nada **y qué hacer al respecto** — nunca una pantalla en blanco |
| **Error** | **Qué pasó y cómo resolverlo**, no un código |

### `[Ext]` — cuándo esto pesa más de lo normal

**Cuando la espera es parte del producto y no un contratiempo.** Hay productos donde el usuario pide algo y
la respuesta no es inmediata por diseño: un proceso que corre minutos, un resultado que llega de a poco, un
elemento que caduca solo.

```
El usuario dispara la acción
        ↓
El proceso corre — segundos o minutos, sin respuesta definitiva
        ↓
Los resultados llegan de a uno, y algunos caducan antes de que responda
```

**Un botón sin estado de carga y una lista sin estado vacío dejan al usuario sin saber si el sistema lo está
escuchando** — justo en el momento en que la aplicación todavía no puede darle una respuesta.

**OBLIGATORIO** — todo componente que dependa de una respuesta del servidor declara sus tres estados de
contenido.

---

## 3.6 · Las propiedades `[Book 1, cap. 5]`

**Figma distingue cinco tipos, y el libro recomienda reconocerlas por su símbolo:**

| Símbolo | Propiedad | Para qué |
|---|---|---|
| **◆** | Variante | Elegir entre versiones — primaria, secundaria |
| **↺** | Intercambio de instancia | Cambiar el icono sin cambiar el botón |
| **○** | Interruptor | Mostrar u ocultar una parte |
| **@** | Contenido | El texto de la etiqueta |
| **↳** | Anidada | Exponer la propiedad de un componente interno |

---

## 3.7 · Cuándo agrupar como variantes, y cuándo no `[Book 2, cap. 7]`

**El criterio del libro, textual:**

> *"Son más efectivas cuando se aplican a componentes que **difieren de formas predecibles y limitadas**. Si
> dos componentes son funcional o visualmente demasiado distintos, **agruparlos como variantes puede reducir la
> claridad y hacer el sistema más difícil de mantener**."*

| Sí agrupar | No agrupar |
|---|---|
| Botón primario / secundario / deshabilitado | Botón y campo de texto |
| Pestaña activa / inactiva | Una tarjeta de resumen y una tarjeta con acciones |
| Tarjeta chica / grande **con la misma estructura** | Dos tarjetas con estructura distinta |

**Y el error nombrado** `[Book 1, cap. 6]`: *"crear 15 variantes de botón cuando en realidad solo necesitas 3"*.

---

## 3.8 · Organizar la biblioteca `[Book 2, cap. 7]`

### La jerarquía va en páginas y marcos, no en el nombre

> *"En lugar de depender de nombres largos de componente para expresar la estructura, puedes usar **páginas y
> marcos dentro de tu archivo** para organizar los componentes principales visualmente."*

```
Página "Buttons"
   └─ Marco "Primary"     → componentes adentro
   └─ Marco "Secondary"
   └─ Marco "Tertiary"
```

**Dos beneficios que el libro señala:**

1. El panel de Recursos **refleja esa estructura sola**, en categorías plegables.
2. **Figma considera relacionados los componentes que viven en el mismo marco** — lo que hace más fácil
   intercambiar entre ellos desde una instancia.

### Los componentes auxiliares se ocultan

**OBLIGATORIO** — lo que no debe usarse suelto **se prefija con punto**:

```
.Icon          .FieldBase          .SkeletonBlock
```

> *"Figma trata como privados los componentes que empiezan con punto, así que **no aparecen en la biblioteca
> publicada**."*

**`[Book 1, cap. 5]` menciona también el guion bajo** (`_Tooltip`) con el mismo efecto. **Esta KB usa el
punto**, por consistencia con el libro 2.

### Cada componente lleva descripción `[Book 2, cap. 11]`

**OBLIGATORIO** — nombre no alcanza. La descripción dice **cuándo usarlo y cuándo no**.

> *"Un archivo listo para entrega es aquel donde **cada elemento clave incluye una descripción breve y clara**.
> Los componentes incluyen notas de uso, las variantes están etiquetadas de forma consistente, las páginas
> siguen una estructura lógica, y los estilos incluyen una explicación corta de su propósito."*

---

## 3.9 · Una biblioteca o varias `[Book 2, cap. 7]`

**Dos enfoques, y el libro no impone ninguno:**

- **una biblioteca de fundamentos** — colores, estilos de texto, rejillas y componentes básicos
- **más bibliotecas de producto** — elementos más complejos

> *"Los equipos pequeños suelen preferir tener todo en un archivo. Los grandes separan fundamentos y
> componentes para que las actualizaciones sean más manejables. **Sea cual sea el enfoque, sé consistente.**"*

### La decisión de esta KB `[Ext]`

**Separadas**, y no por tamaño de equipo sino por **`[Book 1, cap. 5]`**:

> *"Deberías planear todo el sistema para que sea modular. Esto va desde decisiones simples como **no mantener
> fundamentos y componentes en un mismo archivo**, hasta elecciones más complejas como evitar dependencias
> intrincadas entre componentes."*

**Y porque en cuanto un producto tiene más de una aplicación** —una por cada actor, más un panel de
administración— **esas aplicaciones comparten fundamentos y no componentes**. Separar las bibliotecas desde
el principio evita el trabajo de desenredarlas después.

---

## 3.10 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-C01`** | Ningún componente entra al sistema **sin su entrada en el inventario**, con variantes, tamaños y estados | OBLIGATORIO | `[Ext G3]` |
| **`DS-C02`** | **Todo elemento interactivo declara su estado de foco**, con contraste mínimo 3:1 | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-C03`** | Todo componente que dependa de una respuesta declara sus estados de **carga, vacío y error** | OBLIGATORIO | `[Book 1, cap. 8]` · `[Ext]` |
| **`DS-C04`** | Los componentes auxiliares se prefijan con **punto** y no se publican | OBLIGATORIO | `[Book 2, cap. 7]` |
| **`DS-C05`** | Cada componente lleva **descripción**: cuándo usarlo y cuándo no | OBLIGATORIO | `[Book 2, cap. 11]` |
| **`DS-C06`** | La jerarquía va en **páginas y marcos**, no en nombres largos | OBLIGATORIO | `[Book 2, cap. 7]` |
| **`DS-C07`** | **Fundamentos y componentes no comparten archivo** | OBLIGATORIO | `[Book 1, cap. 5]` |
| **`DS-C08`** | **Desvincular una instancia es la última salida.** Si hace falta, revisar si falta una variante | RECOMENDADO | `[Book 1, cap. 5]` |
| **`DS-C09`** | Se agrupa como variantes solo lo que **difiere de forma predecible y limitada** | RECOMENDADO | `[Book 2, cap. 7]` |
| **`DS-C10`** | El estado `hover` **no se declara para móvil** | RECOMENDADO | `[Book 2, cap. 8]` |
