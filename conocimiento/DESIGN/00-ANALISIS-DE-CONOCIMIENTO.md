# Análisis de conocimiento · DESIGN

> **Qué contienen los dos libros, qué necesita este proyecto, y de dónde sale cada sección de la Knowledge
> Base.** Este documento es el que origina la estructura: se escribe **antes** que la KB y explica por qué
> tiene las secciones que tiene.
>
> **Método:** la estructura **emana de los libros**. Las extensiones profesionales existen solo para llenar
> **vacíos que los propios libros dejan**, detectados leyéndolos — nunca por necesidades importadas de un
> producto concreto ni de pantallas ya dibujadas.
>
> **Agnóstico de negocio:** esta KB no describe ningún producto. Todo lo que aquí se afirma vale igual para
> una banca, una tienda, una clínica o un juego. Lo propio de un negocio vive en su capa de dominio, fuera
> de aquí.

## Índice

1. [Las dos fuentes](#1--las-dos-fuentes)
2. [Mapa de los libros](#2--mapa-de-los-libros)
3. [Qué es distinto en esta KB](#3--qué-es-distinto-en-esta-kb)
4. [Los vacíos que dejan los libros](#4--los-vacíos-que-dejan-los-libros)
5. [La estructura que resulta](#5--la-estructura-que-resulta)
6. [Estado de lectura](#6--estado-de-lectura)

---

## 1 · Las dos fuentes

| Libro | Qué aporta | Papel |
|---|---|---|
| **Design Beyond Limits with Figma** — Simon Jun | Sistemas de diseño, **tokens**, accesibilidad, entrega a desarrollo, colaboración | **El libro del sistema.** Columna vertebral de la KB |
| **Designing and Prototyping Interfaces with Figma, 3.ª ed.** | Rejillas, color y tipografía, **Auto Layout**, componentes y variantes, variables, prototipado | **El libro del oficio.** Cómo se construye cada pieza |

**No se solapan: se completan.** El primero dice **cómo se estructura un sistema**; el segundo, **cómo se
dibuja lo que el sistema declara**. Una KB que solo tuviera el primero produciría un sistema imposible de
dibujar; una que solo tuviera el segundo, pantallas bonitas sin sistema detrás.

---

## 2 · Mapa de los libros

### Libro 1 · Design Beyond Limits with Figma

| Cap. | Contenido | Utilidad para la KB |
|---|---|---|
| 1 | Colaboración avanzada, control de versiones, permisos | **Parcial.** Presupone equipo humano; sirve el **vocabulario Figma ↔ código** y el versionado |
| 2 | Ecosistema de complementos | **Baja.** Volátil por naturaleza; el propio autor mantiene la lista fuera del libro |
| 3 | Inteligencia artificial en Figma | **Baja hoy.** Se revisará cuando la generación en Figma esté conectada |
| 4 | Sinergia diseñador-desarrollador | **Alta.** La **estructura de siete páginas** del archivo y el modo de desarrollo |
| **5** | **Escalar sistemas de diseño** | **Máxima.** Planeación, **arquitectura de componentes**, gobierno, escalado |
| **6** | **Tokens de diseño** | **Máxima.** Es el capítulo que gobierna toda la KB |
| **7** | **Sistemas accesibles** | **Máxima.** Contraste, teclado, lector de pantalla, WCAG |
| 8 | Entrega de precisión | **Alta.** Exportación, variables por plataforma, aseguramiento de calidad |
| 9 | Involucrar a los interesados | **Baja.** No hay interesados externos todavía |

### Libro 2 · Designing and Prototyping Interfaces with Figma

| Cap. | Contenido | Utilidad para la KB |
|---|---|---|
| 1–3 | Transición desde otras herramientas, entorno | **Baja.** Es introducción a la herramienta |
| 4 | Bocetado móvil con formas vectoriales | **Media.** El método de boceto |
| **5** | **Rejillas, color y tipografía** | **Máxima.** Es la base de los fundamentos |
| **6** | **Interfaz móvil con Auto Layout** | **Máxima.** Es cómo se construye todo lo responsivo |
| **7** | **Componentes y variantes** | **Máxima.** El contrato de cada componente |
| 8 | Tableta, escritorio y web | **Media.** Para la extensión a escritorio |
| 9 | Prototipado, transiciones, Smart Animate | **Media.** Cuando haya flujos que probar |
| 11 | Exportación y entrega | **Alta.** Junto con el cap. 8 del libro 1 |
| 12 | Recursos, complementos, herramientas de IA | **Baja.** Volátil |
| **13** | **Variables y prototipado condicional** | **Alta.** Es la mitad de Figma del puente de tokens |

---

## 3 · Qué es distinto en esta KB

**Los dos libros asumen un equipo de diseño humano.** Esta KB asume un agente que lee, y eso cambia qué hay
que escribir.

| Lo que los libros asumen | Lo que asume esta KB | Consecuencia para la KB |
|---|---|---|
| Un diseñador que **mira** el sistema y lo imita | **Un agente que lo lee** | La regla tiene que estar **escrita y ser comprobable**, no implícita en un archivo de Figma |
| Reuniones, revisiones, gobierno entre personas | **Quien decide el producto, sin comité** | El gobierno se sustituye por **verificación automática** |
| Figma como sitio donde vive el sistema | **El repositorio** | Los tokens viven en JSON versionado; **Figma es una salida** |
| Adopción como problema principal | **Adopción trivial** — pocos consumidores | El esfuerzo se mueve de *convencer* a **impedir la desviación** |

> **El libro 1 lo dice sin saber que aplica acá:** *"recuerda que construyes sistemas de diseño para acelerar
> todo el proceso —el desarrollo en particular—, no para tener archivos bonitos de Figma."*

---

## 4 · Los vacíos que dejan los libros

**Cada extensión de la KB nace de uno de estos, detectado leyendo.**

| # | Vacío | Evidencia en el libro | Extensión que lo llena |
|---|---|---|---|
| **G1** | **No dice cómo verificar** que un diseño respeta el sistema. Todo el control es humano — revisiones mensuales, analíticas de *detach*, gobierno | Libro 1, cap. 5: el control son reuniones y métricas de uso, nunca una comprobación automática | `rules/` + el verificador |
| **G2** | **No conecta el sistema con el modelo de datos.** Un componente que muestra un precio nunca se ata a la columna que lo produce | Ninguno de los dos libros menciona origen de datos | `patterns/` con su dominio declarado |
| **G3** | **No define un contrato legible por máquina** de los componentes. El libro exige declarar variantes, tamaños y estados, pero como propiedades de Figma | Libro 1, cap. 5: las propiedades son `◆ Variant`, `○ Toggle`, `@ Content` — dentro de Figma | `inventario/` en JSON |
| **G4** | **No cubren las superficies continuas no textuales** — mapa, lienzo, cámara, visor 3D, línea de tiempo. Ningún libro trata la hoja sobre la superficie, el marcador, el trazo ni la actualización en vivo | Libro 2 cubre interfaz móvil de listas, formularios y contenido; **ninguna superficie continua aparece en ningún capítulo** | `patterns/` §5.5 — los patrones de superficie continua |
| **G5** | **Da por sentado que hay identidad de marca.** Ambos parten de que el color y la letra ya se decidieron | Libro 2, cap. 5 enseña a *aplicar* color y tipografía, no a *elegirlos* | `foundations/` con el método de elección |
| **G6** | **No trata el multi-país como dato.** El tema se plantea como marca (theming), no como moneda, idioma y formato variables | Libro 1, cap. 6: los temas son variantes de marca | `rules/` — formato de número, moneda y largo de texto |

---

## 5 · La estructura que resulta

**El libro 1 ofrece dos arquitecturas de componentes y la KB toma la segunda**, que es la que el propio autor
prefiere por ser más clara:

```
Atomic Design (Brad Frost)        La alternativa de Dotidot   ← ESTA
─────────────────────────        ──────────────────────────
Atoms                            PRIMITIVOS   tokens, fundamentos
Molecules                        COMPONENTES  elementos sueltos
Organisms                        PATRONES     combinaciones
Templates                        PLANTILLAS   estructura de pantalla
Pages
```

> *"Este enfoque elimina la confusión de la terminología átomos/moléculas y crea distinciones más claras
> entre niveles de complejidad."* — Libro 1, cap. 5

**Y el orden de trabajo lo fija el mismo capítulo, con una advertencia que vale por todo el plan:**

> *"Nuestro diseñador dedicó mucho más tiempo a crear la estructura de fundamentos y los tokens que a crear
> los componentes. Puede parecer que avanzas lento al principio, pero tener una base sólida hace que todo lo
> demás sea mucho más fácil y rápido después."*

### Las secciones

| Sección | Origen | Qué contiene |
|---|---|---|
| `01-foundations/` | `[Book 2, cap. 5]` · `[Ext G5]` | Rejilla, color, tipografía, espaciado, forma, elevación, iconografía — **y cómo se eligen** |
| `02-tokens/` | `[Book 1, cap. 6]` | Los **tres niveles**, nomenclatura, alias, la regla de las tres apariciones |
| `03-components/` | `[Book 1, cap. 5]` · `[Book 2, cap. 7]` | Arquitectura, propiedades, variantes, tamaños, **estados** |
| `04-auto-layout/` | `[Book 2, cap. 6]` | Lo que en código es *flexbox*: dirección, espacio, relleno, ajuste |
| `05-patterns/` | `[Ext G2, G4]` | Cómo se declara un patrón — **dominio, tablas, reglas y estados** |
| `06-accessibility/` | `[Book 1, cap. 7]` | Contraste, teclado, lector de pantalla, WCAG |
| `07-handoff/` | `[Book 1, caps. 4 y 8]` | Estructura de archivo, modo de desarrollo, exportación, variables por plataforma |
| `08-figma-bridge/` | `[Book 1, cap. 6]` · `[Book 2, cap. 13]` | Variables contra Token Studio, importación y exportación |
| `09-rules/` | `[Ext G1, G6]` | **Reglas `DS-xxx`** obligatorias, y qué verifica cada una |
| `10-checklists/` | `[Ext G1]` | Antes de generar una pantalla · antes de publicar un componente |

**Más los tres archivos de convención:** `README.md`, `TRAZABILIDAD-LIBRO.md` y `glossary.md`.

### Por qué `09-rules/` numera sus reglas

**Igual que `DB-xxx` en la KB de modelado.** Una regla con número se puede citar desde el verificador, desde
la skill y desde la ficha de un componente — **y se puede comprobar que existe**. Una recomendación en prosa,
no.

---

## 6 · Estado de lectura

**Se registra a propósito:** una KB que afirma cosas de un capítulo no leído es exactamente el hallazgo
inventado contra el que este repositorio ya se protege.

**Los dos libros están leídos completos** — los 9 capítulos del primero y los 13 del segundo. Se registra
capítulo por capítulo qué sección sostiene cada uno, para que ninguna afirmación de la KB quede sin respaldo.

| Libro | Capítulo | Sostiene |
|---|---|---|
| 1 | Prefacio · 1 — colaboración | Vocabulario **Figma ↔ código**, versionado |
| 1 | 2 — complementos | `08-figma-bridge` — *Variables to CSS/JSON*, y el **árbol de decisión** para adoptar un complemento |
| 1 | 3 — inteligencia artificial | `07-handoff` — expansión de texto entre idiomas; Figma Make |
| 1 | **4** — sinergia con desarrollo | `07-handoff` — la **estructura de siete páginas**, modo de desarrollo |
| 1 | **5** — escalar sistemas | `03-components` y **la arquitectura entera** |
| 1 | **6** — tokens | `02-tokens` — los tres niveles, alias, la regla de las tres apariciones |
| 1 | **7** — accesibilidad | `06-accessibility` — contraste, teclado, lector de pantalla, WCAG |
| 1 | **8** — entrega de precisión | `07-handoff` · `08-figma-bridge` — nombres por plataforma, iconos, animación |
| 1 | 9 — interesados | `09-rules` — **registros de decisión de diseño** |
| 2 | 1 · 2 · 3 — herramienta y FigJam | `01-foundations` — declaración de propósito, personas, flujos |
| 2 | **4** — boceto | `05-patterns` — **el contenido antes que el diseño** |
| 2 | **5** — rejillas, color, tipografía | `01-foundations` |
| 2 | **6** — Auto Layout | `04-auto-layout` |
| 2 | **7** — componentes y variantes | `03-components` |
| 2 | 8 — tableta, escritorio y web | `04-auto-layout` — puntos de corte, contenedor fijo |
| 2 | 9 · 10 — prototipado y pruebas | `05-patterns` — disparadores, estados, superposiciones |
| 2 | **11** — exportación y entrega | `07-handoff` — **Auto Layout ↔ Flexbox**, servidor MCP |
| 2 | 12 — recursos y complementos | `09-rules` — **Design Lint**, el pariente más cercano a un verificador |
| 2 | **13** — variables y prototipado condicional | `08-figma-bridge` — colecciones, modos, **alcance** |

### La frase que sostiene la sección de patrones

**Libro 2, cap. 4** — y describe el error más común al empezar una pantalla:

> *"Uno de los errores más comunes del diseño de interfaces es empezar por la maqueta antes de tener siquiera
> una idea aproximada de qué datos necesita mostrar el producto. Cuando eso pasa, se rellenan las pantallas
> con texto de relleno y con una estructura que no refleja el producto real. **Ese enfoque puede producir
> maquetas limpias y elegantes que se desarman en cuanto entran los datos de verdad.**"*

**Es la justificación, tomada del libro, de que cada patrón declare su dominio y sus tablas.**

### Un hallazgo que cambia el plan de Figma

**El libro 2 documenta el servidor MCP de Figma, y nombra a Claude Code entre sus clientes** `[Book 2, cap. 11]`.
Se activa desde el panel *Inspect*, en la sección *MCP server*.

**Pero su propia descripción dice qué hace:** *«Send design context to your AI agent»*, y la herramienta que
se usa para confirmarlo se llama **`get_design_context`**.

> **Es un puente de lectura: Figma → agente → código.** No el de escritura que haría falta para que Claude
> dibujara solo en el lienzo. Habrá que comprobarlo conectándolo, pero **el libro apunta en la dirección
> contraria a la que se había planteado**.

**Comprobado el 17-08-2026 — y el libro quedó corto.** El servidor MCP oficial hoy **también escribe**:
`use_figma` ejecuta la Plugin API completa (nodos, variables, componentes, variantes), `create_new_file` crea
el archivo, y `add_code_connect_map` ata la pieza de Figma a la del repositorio. **El puente es de doble
sentido.**

> **Lo que no cambia es quién manda.** `DS-X01` sigue diciendo que la fuente de verdad es el JSON; lo que
> cambió es que ahora Figma es una salida **que se puede escribir sola**, en vez de una que había que
> importar a mano. Y `DS-X06` —*ninguna etapa depende de que un agente escriba en el lienzo*— **gana
> importancia**: las herramientas están visibles aunque el asiento del usuario no tenga permiso de escritura,
> así que el fallo llega a mitad de la construcción si no se comprueba antes.

**Se deja el párrafo anterior en pie, tachado por este.** Una KB que borra su conclusión vieja pierde la
única prueba de que el método funciona: la afirmación se sostuvo en una lectura, se contrastó contra la
realidad, y se corrigió con fecha.

**Y hay una consecuencia práctica que sí es segura** `[Book 2, cap. 11]`:

> *"El código más preciso se genera cuando el diseño usa Auto Layout, porque corresponde directamente al
> sistema Flexbox. Si no se usa Auto Layout, Figma sugiere coordenadas absolutas, lo que lleva a interfaces
> no responsivas y trabajo extra."*

**Auto Layout no es una comodidad de dibujo: es lo que hace que el diseño se pueda convertir en código.**
