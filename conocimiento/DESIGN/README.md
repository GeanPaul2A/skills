# DESIGN — Knowledge Base

Estándar profesional de **diseño de interfaz y sistemas de diseño** para **cualquier producto digital**.

Esta Knowledge Base convierte el conocimiento de los dos libros fuente en un **estándar accionable** que
gobierna cómo se construye cada token, cada componente y cada pantalla — desde la elección del color hasta
la entrega a código.

> **Es agnóstica de negocio, y eso no es un detalle: es la condición para que sirva.** Nada de lo que se
> afirma acá depende de qué vende el producto. Todo vale igual para una banca, una tienda, una clínica o un
> juego. Lo propio de un negocio —sus entidades, sus reglas, sus patrones— **vive en su capa de dominio**,
> no en esta base de conocimiento. Si una afirmación de acá solo se sostiene nombrando un producto concreto, está mal escrita.

---

## Índice

1. [Propósito](#1--propósito)
2. [Alcance](#2--alcance)
3. [Fuentes y método](#3--fuentes-y-método)
4. [Cómo usar esta Knowledge Base](#4--cómo-usar-esta-knowledge-base)
5. [Niveles de obligatoriedad](#5--niveles-de-obligatoriedad)
6. [Las diez secciones](#6--las-diez-secciones)
7. [La advertencia que gobierna todo](#7--la-advertencia-que-gobierna-todo)

---

## 1 · Propósito

- Ser la **fuente de verdad** de *cómo se decide* un color, un tamaño, un componente y una pantalla.
- Permitir **generar pantallas nuevas con criterio uniforme**, y **auditar** las que ya existen.
- Estar escrita para que **la consuma un agente**: reglas explícitas, valores concretos, listas de
  comprobación y matrices de decisión — no descripciones en prosa.

> **La diferencia con los libros:** ellos enseñan a **un diseñador que mira**. Esta base de conocimiento instruye a **un agente
> que lee**. Lo que allí es criterio adquirido, acá tiene que estar escrito y ser comprobable.

## 2 · Alcance

Cubre **diseño de producto digital para móvil primero**, con extensión a tableta y escritorio.

**No** cubre: identidad de marca extendida (papelería, campañas), ilustración, movimiento complejo, ni
investigación de usuarios. La investigación se conserva como referencia en `01-foundations`, no como estándar.

## 3 · Fuentes y método

**Los libros son la fuente primaria y la columna vertebral.** La estructura **emana de ellos**: sus capítulos
forman las secciones centrales, y cada extensión profesional nace de un **vacío que los propios libros dejan**
(detectado leyéndolos). **Ningún producto concreto es insumo del diseño de esta base de conocimiento**; los productos son
únicamente el objetivo de la aplicación posterior.

Cada afirmación declara su origen:

| Etiqueta | Significa |
|---|---|
| **`[Libro 1, capítulo N]`** | Proviene de *Design Beyond Limits with Figma*, de Šimon Jůn — **el libro del sistema** |
| **`[Libro 2, capítulo N]`** | Proviene de *Designing and Prototyping Interfaces with Figma*, tercera edición — **el libro del oficio** |
| **`[Extensión]`** | **Extensión profesional.** Llena un vacío de los libros. **Nunca se le atribuye al libro una regla que no contiene** |

> - Derivación **Libros → base de conocimiento** y **registro de vacíos**: [`TRAZABILIDAD-LIBROS.md`](TRAZABILIDAD-LIBROS.md)
> - Análisis y plan que originaron la estructura: [`00-ANALISIS-DE-CONOCIMIENTO.md`](00-ANALISIS-DE-CONOCIMIENTO.md)

## 4 · Cómo usar esta Knowledge Base

| Si necesitas… | Ve a… |
|---|---|
| Entender un término | [`glossary.md`](glossary.md) |
| **Elegir** un color, una tipografía o una escala | `01-foundations/` |
| Nombrar un token o decidir si algo merece serlo | `02-tokens/` |
| Declarar un componente con sus variantes y estados | `03-components/` |
| Decidir cómo se comporta un bloque al crecer el contenido | `04-auto-layout/` |
| Diseñar un flujo completo, atado a los datos que lo alimentan | `05-patterns/` |
| Contraste, foco, lector de pantalla | `06-accessibility/` |
| Preparar la entrega a desarrollo | `07-handoff/` |
| Llevar el sistema a Figma, o traerlo de vuelta | `08-figma-bridge/` |
| Una **regla concreta y obligatoria** | [`09-rules/`](09-rules/) — reglas `DS-xxx` |
| **Auditar antes de dar por terminada una pantalla** | `10-checklists/` |

## 5 · Niveles de obligatoriedad

Toda recomendación se clasifica como:

- **OBLIGATORIO** — se cumple siempre. Una violación es un defecto, y el verificador la detecta.
- **RECOMENDADO** — se cumple salvo justificación registrada en el propio documento.
- **OPCIONAL** — criterio, sin consecuencia si se omite.

## 6 · Las diez secciones

| Sección | Origen | Qué resuelve |
|---|---|---|
| `01-foundations` | `[Libro 2, capítulo 5]` · `[Extensión G5]` | Rejilla, color, tipografía, espaciado, forma, elevación, iconografía — **y cómo se eligen** |
| `02-tokens` | `[Libro 1, capítulo 6]` | Los tres niveles, nomenclatura, alias, alcance, la regla de las tres apariciones |
| `03-components` | `[Libro 1, capítulo 5]` · `[Libro 2, capítulo 7]` | Arquitectura, propiedades, variantes, tamaños, **estados** |
| `04-auto-layout` | `[Libro 2, capítulos 6 y 8]` | Dirección, espacio, relleno, `hug`/`fill`/`fixed`, puntos de corte |
| `05-patterns` | `[Extensión G2, G4]` · `[Libro 2, capítulos 4 y 9]` | Cómo se declara un patrón — **dominio, tablas, reglas y estados** |
| `06-accessibility` | `[Libro 1, capítulo 7]` | Contraste, teclado, lector de pantalla, WCAG, criterios de aceptación |
| `07-handoff` | `[Libro 1, capítulos 4 y 8]` · `[Libro 2, capítulo 11]` | Estructura de archivo, modo de desarrollo, exportación, iconos |
| `08-figma-bridge` | `[Libro 1, capítulo 6]` · `[Libro 2, capítulo 13]` | Colecciones, modos, **alcance**, sintaxis de código por plataforma |
| `09-rules` | `[Extensión G1, G6]` | **Las reglas `DS-xxx`**, y qué comprueba cada una |
| `10-checklists` | `[Extensión G1]` | Antes de generar una pantalla · antes de publicar un componente |

## 7 · La advertencia que gobierna todo

**Del libro 1, capítulo 5**, y vale más que cualquier regla de esta base de conocimiento:

> *"Nuestro diseñador dedicó **mucho más tiempo a crear la estructura de fundamentos y los tokens que a crear
> los componentes**. Puede parecer que avanzas lento al principio, pero tener una base sólida hace que todo lo
> demás sea mucho más fácil y rápido después."*

**Y su contraparte, del mismo capítulo:**

> *"Recuerda que construyes sistemas de diseño para **acelerar todo el proceso —el desarrollo en particular—**,
> no para tener archivos bonitos de Figma."*
