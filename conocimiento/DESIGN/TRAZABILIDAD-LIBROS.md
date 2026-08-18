# Trazabilidad Libros → Knowledge Base

Este documento demuestra que la Knowledge Base **emana de los libros**. Las fuentes primarias y la columna
vertebral son *Design Beyond Limits with Figma* (Simon Jun) y *Designing and Prototyping Interfaces with Figma,
3.ª ed.* Las **extensiones profesionales existen únicamente para llenar vacíos que los propios libros dejan**
—identificados leyéndolos—, **no** por necesidades importadas de ningún producto concreto ni de pantallas ya
dibujadas. **Ninguna regla de esta KB depende de a qué se dedique el producto.**

---

## Índice

1. [Mapa de cobertura](#parte-1--mapa-de-cobertura-de-los-libros)
2. [Registro de vacíos](#parte-2--registro-de-vacíos)
3. [Las ocho reglas de extensión pura](#parte-3--las-ocho-reglas-de-extensión-pura)
4. [El reparto](#parte-4--el-reparto)

---

## Parte 1 — Mapa de cobertura de los libros

**Los dos libros están leídos completos.** Cada capítulo declara qué sección sostiene.

### Libro 1 · *Design Beyond Limits with Figma* — 9 capítulos

| Cap. | Contenido | Sección(es) KB |
|---|---|---|
| **1** | Colaboración avanzada, versionado, permisos | `07-handoff` §7.7 · vocabulario Figma ↔ código en `04-auto-layout` §4.1 |
| **2** | Ecosistema de complementos | `08-figma-bridge` §8.7 — exportadores y árbol de decisión |
| **3** | Inteligencia artificial en Figma | `04-auto-layout` §4.9 — expansión de texto · `08-figma-bridge` §8.8 — Figma Make |
| **4** | Sinergia diseñador-desarrollador | `07-handoff` §§7.2–7.4 |
| **5** | **Escalar sistemas de diseño** | `03-components` §§3.2, 3.9 · `00-ANALISIS` — **la arquitectura de cuatro niveles** |
| **6** | **Tokens de diseño** | **`02-tokens` completa** |
| **7** | **Sistemas accesibles** | **`06-accessibility` completa** |
| **8** | Entrega de precisión | `07-handoff` §§7.5, 7.6, 7.8 · `01-foundations` §1.8 — iconos |
| **9** | Involucrar a los interesados | `09-rules` §9.1 — registros de decisión |

### Libro 2 · *Designing and Prototyping Interfaces with Figma, 3.ª ed.* — 13 capítulos

| Cap. | Contenido | Sección(es) KB |
|---|---|---|
| **1** | Figma y transición desde otras herramientas | Contexto de `08-figma-bridge` |
| **2** | Moodboards, personas y flujos en FigJam | `01-foundations` §1.9 — **los insumos del método de elección** |
| **3** | El entorno de diseño | `04-auto-layout` §4.6 — marco contra grupo · `01-foundations` §1.7 — *"los efectos están limitados a propósito"* |
| **4** | Bocetado móvil | **`05-patterns` §5.2 — el contenido antes que la maqueta** |
| **5** | **Rejillas, color y tipografía** | **`01-foundations` §§1.2–1.4** |
| **6** | **Auto Layout** | **`04-auto-layout` §§4.2–4.7** |
| **7** | **Componentes y variantes** | **`03-components` §§3.1, 3.3, 3.7, 3.8** |
| **8** | Tableta, escritorio y web | `04-auto-layout` §4.8 — puntos de corte y contenedor fijo |
| **9** | Prototipado, transiciones, componentes interactivos | `05-patterns` §5.6 — los cinco momentos de un flujo |
| **10** | Pruebas y compartir | `06-accessibility` §6.9 — la rutina de comprobación |
| **11** | **Exportación y entrega** | `07-handoff` §7.4 — **Auto Layout ↔ Flexbox** y el servidor MCP |
| **12** | Recursos, complementos y IA | `09-rules` §9.1 — **Design Lint**, el pariente más cercano a un verificador |
| **13** | **Variables y prototipado condicional** | **`08-figma-bridge` §§8.2–8.6** |

**Conclusión:** los **22 capítulos** están cubiertos. Las secciones `01`, `02`, `03`, `04`, `06`, `07` y `08`
son **Book Knowledge** (columna vertebral). Las secciones `05`, `09` y `10` son mayoritariamente extensión, y
cada parte suya nace de un vacío de la Parte 2.

---

## Parte 2 — Registro de vacíos

**Cada vacío se detectó leyendo los libros** —qué promete o necesita un sistema completo y el libro no
entrega—, no mirando los dominios del proyecto.

| # | Vacío | Evidencia en el libro | Extensión que lo llena |
|---|---|---|---|
| **G1** | **No dicen cómo verificar** que un diseño respeta el sistema. Todo el control es humano | `[B1, cap. 5]` el gobierno son reuniones mensuales y métricas de inserción/desvinculación · `[B2, cap. 12]` **Design Lint** es un complemento que se corre a mano · `[B1, cap. 8]` su propio revisor técnico admite que *"deberían automatizarse mediante marcos de prueba"* | `09-rules` — la columna **Verifica** y las reglas numeradas · `10-checklists` |
| **G2** | **No conectan el diseño con el modelo de datos.** Un componente que muestra un precio nunca se ata a la columna que lo produce | `[B2, cap. 4]` nombra el problema —*"maquetas que se desarman en cuanto entran los datos de verdad"*— y **solo recomienda conseguir contenido de ejemplo**. Ningún libro menciona origen de datos por tabla | `05-patterns` §5.3 — el patrón declara dominio, tablas y reglas |
| **G3** | **No definen un contrato legible por máquina** de los componentes. Exigen declarar variantes y estados, pero como propiedades **dentro de Figma** | `[B1, cap. 5]` las propiedades son `◆ Variant`, `○ Toggle`, `@ Content` — **símbolos de la interfaz, no datos** | `03-components` §3.4 — el inventario en JSON |
| **G4** | **No cubren las superficies continuas no textuales** —mapa, lienzo, cámara, visor 3D, línea de tiempo—. Ni la hoja sobre la superficie, ni el marcador, ni el trazo, ni la actualización en vivo | `[B2]` cubre interfaz móvil de listas, formularios y contenido; **ninguna superficie continua aparece en ningún capítulo** | `05-patterns` §5.5 |
| **G5** | **Dan por sentada la identidad de marca.** Enseñan a *aplicar* color y tipografía, no a *elegirlos* | `[B2, cap. 5]` *"es esencial tener al menos una idea aproximada de la dirección de color, **o mejor aún, datos o directrices de marca**"* — **y ahí se detiene** | `01-foundations` §1.9 — el método de cinco pasos |
| **G6** | **No tratan el multi-país como dato.** El tema se plantea como marca, no como moneda, idioma y formato variables | `[B1, cap. 6]` los temas son variantes de marca · `[B1, cap. 3]` la expansión de texto se trata como **problema de maqueta**, no como estructura | `08-figma-bridge` §8.2 — la colección `Copy` · `04-auto-layout` §4.9 |

---

## Parte 3 — Las ocho reglas de extensión pura

**Son las que no tienen respaldo directo en ningún libro, y por eso van con su justificación explícita.**

| Regla | Qué exige | Vacío | Por qué el libro no alcanza |
|---|---|---|---|
| **`DS-F07`** | El radio completo se reserva a lo que no es un control | G5 | Los libros no tratan la **semántica de la forma**; enseñan a fijar radios, no a repartirlos |
| **`DS-F11`** | Un solo acento, salvo significado codificado | G5 | Ningún libro da criterio sobre **cuántos acentos** |
| **`DS-T07`** | Ningún valor en crudo en una pantalla | G1 | El libro **admite valores fijos** al empezar; acá no hay quien los revise después |
| **`DS-C01`** | Todo componente con entrada en el inventario | G3 | El libro declara variantes **dentro de Figma**, donde un guion no las lee |
| **`DS-P01`** | Todo patrón declara dominio, tablas y reglas | G2 | El libro solo pide *"contenido realista"* |
| **`DS-P04`** | Lo de otro dominio declara qué se muestra si no llega | G2 | Ningún libro contempla **una base de datos por servicio** |
| **`DS-P06`** | Un patrón termina donde el modelo cambia de estado | G2 | El libro define flujos por **intención del usuario**, no por estado del sistema |
| **`DS-X06`** | Ninguna etapa depende de que un agente escriba en el lienzo | G1 | El libro documenta el servidor MCP **sin declarar su dirección**; la cautela es del proyecto |

---

## Parte 4 — El reparto

| Origen | Reglas | Proporción |
|---|---|---|
| **Salen enteras de los libros** | **60** | 79 % |
| Mezclan libro y extensión | 8 | 10 % |
| **Extensión pura** | **8** | 11 % |
| **Total** | **76** | |

> **Es una proporción sana para esta materia.** En la KB de modelado de datos el reparto fue **55 % libro / 45 %
> extensión**, porque el libro allí era agnóstico de motor y anterior a los microservicios. Acá los libros son
> **actuales y específicos de la herramienta**, así que cubren mucho más — y lo que dejan afuera es
> **exactamente lo que un sistema verificable necesita y ellos no dan**: verificación automática, atadura al
> modelo de datos, y las superficies continuas que ningún capítulo trata.
