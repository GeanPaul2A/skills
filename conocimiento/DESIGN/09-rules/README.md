# 09 · Rules (Las reglas)

**El índice único de las reglas del sistema, y cómo se comprueba cada una.** Es el documento que lee el
verificador y el que cita la skill.

**Clasificación:** consolida las ocho secciones anteriores · `[Ext G1]` la columna de verificación.

---

## Índice

1. [Por qué las reglas llevan número](#91--por-qué-las-reglas-llevan-número)
2. [Cómo se lee la tabla](#92--cómo-se-lee-la-tabla)
3. [Fundamentos · `DS-F`](#93--fundamentos--ds-f)
4. [Tokens · `DS-T`](#94--tokens--ds-t)
5. [Componentes · `DS-C`](#95--componentes--ds-c)
6. [Disposición · `DS-L`](#96--disposición--ds-l)
7. [Patrones · `DS-P`](#97--patrones--ds-p)
8. [Accesibilidad · `DS-A`](#98--accesibilidad--ds-a)
9. [Entrega · `DS-H`](#99--entrega--ds-h)
10. [Puente con Figma · `DS-X`](#910--puente-con-figma--ds-x)
11. [El recuento](#911--el-recuento)

---

## 9.1 · Por qué las reglas llevan número

**Porque una recomendación en prosa no se puede citar ni comprobar.** Con número:

- el verificador puede reportar *"falla `DS-T07` en `02-listado.html`, línea 41"*
- la ficha de un componente puede declarar *"cumple `DS-C02` y `DS-C03`"*
- **y se puede comprobar que la regla citada existe** — igual que las 1360 citas de reglas que ya verifica
  `scripts/verificar.py` en el modelo de datos

### El vacío que esto llena `[Ext G1]`

**Los dos libros no tienen ninguna comprobación automática.** Su control de calidad es:

| Libro | Mecanismo |
|---|---|
| `[Book 1, cap. 5]` | Reuniones mensuales, gobierno de tres roles, métricas de inserción y de desvinculación |
| `[Book 1, cap. 8]` | Listas de comprobación **que revisa una persona** |
| `[Book 2, cap. 12]` | **Design Lint** — el complemento que más se acerca, y **hay que abrirlo y correrlo a mano** |

**Y el propio libro admite hacia dónde debería ir** `[Book 1, cap. 8]`, en la nota de su revisor técnico:

> *"Muchos de estos puntos de la lista **deberían idealmente automatizarse mediante marcos de prueba** en lugar
> de comprobarse a mano por personas. La automatización garantiza consistencia, ahorra tiempo y **detecta
> problemas de forma más confiable que las revisiones manuales**."*

---

## 9.2 · Cómo se lee la tabla

| Columna | Qué dice |
|---|---|
| **Nivel** | `OBL` obligatorio · `REC` recomendado |
| **Verifica** | **`auto`** el guion la comprueba solo · **`semi`** necesita renderizar o una herramienta externa · **`manual`** requiere criterio |
| **Origen** | `B1`/`B2` más capítulo, o `Ext` con su vacío |

> **`manual` no significa opcional.** Significa que el verificador **no puede** comprobarla, y por eso va a la
> lista de `10-checklists`, donde una persona la marca.

---

## 9.3 · Fundamentos · `DS-F`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **F01** | La rejilla se guarda como estilo; nunca se configura marco por marco | OBL | semi | B2·5 |
| **F02** | Ningún texto traducible usa tamaño fijo | OBL | auto | B1·3 |
| **F03** | Cuerpo ≥ 16 px, interlineado entre 1.4 y 1.6 | OBL | **auto** | B1·7 |
| **F04** | Los estilos de texto se nombran con barra | OBL | auto | B2·5 |
| **F05** | Ningún par texto/fondo entra sin pasar el comprobador de contraste | OBL | **auto** | B1·7 |
| **F06** | Ningún valor de espaciado fuera de la escala | OBL | **auto** | B2·5 · Ext |
| **F07** | El radio completo se reserva a lo que no es un control | OBL | auto | Ext |
| **F08** | La elevación se expresa solo con sombra difusa | OBL | auto | B2·3 |
| **F09** | Los iconos combinan trazados, no agrupan formas | OBL | **auto** | B1·8 |
| **F10** | Un icono no supera 2 KB ni lleva `<mask>`, `<filter>` o `<clipPath>` | OBL | **auto** | B1·8 |
| **F11** | Un solo color de acento, salvo que el segundo codifique significado | REC | manual | Ext |
| **F12** | Las escalas de color se construyen en HSL y se guardan en HEX | REC | manual | B2·5 |

---

## 9.4 · Tokens · `DS-T`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **T01** | Los tokens viven en JSON versionado; CSS y variables son salidas generadas | OBL | **auto** | B1·6 · Ext |
| **T02** | Tres niveles. Un componente nunca referencia un primitivo | OBL | **auto** | B1·6 |
| **T03** | `Primitives` va oculta de publicación y sin alcance | OBL | semi | B2·13 |
| **T04** | Un solo convenio de nombres en todo el sistema | OBL | **auto** | B1·6 |
| **T05** | Toda variable publicada declara su sintaxis para web, iOS y Android | OBL | semi | B1·8 |
| **T06** | El orden de construcción es color → espaciado → tipografía | OBL | manual | B1·6 |
| **T07** | **Ningún valor en crudo en una pantalla** | OBL | **auto** | Ext G1 |
| **T08** | Un valor merece token si aparece en tres o más lugares | REC | **auto** | B1·6 |
| **T09** | El peso tipográfico se guarda como número | REC | auto | B2·13 |
| **T10** | Los estilos apuntan a variables semánticas | REC | semi | B2·13 |

---

## 9.5 · Componentes · `DS-C`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **C01** | Ningún componente entra sin su entrada en el inventario | OBL | **auto** | Ext G3 |
| **C02** | Todo elemento interactivo declara estado de foco, con 3:1 | OBL | **auto** | B1·7 |
| **C03** | Todo componente con respuesta declara carga, vacío y error | OBL | **auto** | B1·8 · Ext |
| **C04** | Los auxiliares se prefijan con punto y no se publican | OBL | auto | B2·7 |
| **C05** | Cada componente lleva descripción de cuándo usarlo y cuándo no | OBL | **auto** | B2·11 |
| **C06** | La jerarquía va en páginas y marcos, no en nombres largos | OBL | semi | B2·7 |
| **C07** | Fundamentos y componentes no comparten archivo | OBL | semi | B1·5 |
| **C08** | Desvincular una instancia es la última salida | REC | semi | B1·5 |
| **C09** | Se agrupa como variantes solo lo que difiere de forma limitada | REC | manual | B2·7 |
| **C10** | El estado `hover` no se declara para móvil | REC | auto | B2·8 |
| **C11** | El icono dentro de un componente sale de la tabla de tamaños de su plataforma | OBL | **auto** | Ext G8 |
| **C12** | Ningún emoticón hace de icono de interfaz | OBL | **auto** | Ext G8 |
| **C13** | Un hijo no puede ser más ancho que el espacio útil de su padre | OBL | **auto** | Ext G9 |
| **C14** | Todo componente declara qué otros puede contener, y a qué profundidad | REC | **auto** | Ext G9 |

---

## 9.6 · Disposición · `DS-L`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **L01** | **Todo contenedor usa Auto Layout** | OBL | semi | B2·11 |
| **L02** | Espacio y relleno salen de la escala | OBL | **auto** | B2·6 |
| **L03** | Ningún contenedor de texto usa `Fixed` en el eje del texto | OBL | semi | B1·3 |
| **L04** | La estructura se construye con marcos, no con grupos | OBL | semi | B2·3 |
| **L05** | Se diseña móvil primero | OBL | manual | B2·8 |
| **L06** | Toda pantalla se prueba con los valores más largos y más cortos de su tabla | OBL | **auto** | B2·4 · Ext G2 |
| **L07** | Se construye de adentro hacia afuera | REC | manual | B2·6 |
| **L08** | La restricción Escala se reserva a lo decorativo | REC | semi | B2·6 |
| **L09** | Los elementos en `Fill` declaran mínimo y máximo | REC | semi | B2·13 |
| **L10** | Las diferencias entre dispositivos se resuelven con booleanas | REC | semi | B2·13 |

---

## 9.7 · Patrones · `DS-P`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **P01** | Todo patrón declara dominio, tablas y reglas en el inventario | OBL | **auto** | Ext G2 |
| **P02** | **Ningún dato se muestra sin una columna que lo respalde** | OBL | **auto** | B2·4 · Ext G2 |
| **P03** | Todo patrón enumera sus estados, y al menos uno es un fallo | OBL | **auto** | B1·8 · B2·9 |
| **P04** | Lo que viene de otro dominio declara qué se muestra si no llega | OBL | **auto** | Ext G2 |
| **P05** | Ninguna superficie continua no textual es el único portador de información necesaria | OBL | manual | Ext G4 · B1·7 |
| **P06** | Un patrón termina donde el modelo cambia de estado | REC | manual | Ext |

> **`P02` es la regla más valiosa del sistema.** Es la que impide volver a dibujar *"Confort+"*, y **se puede
> comprobar sola**: se cruzan los datos que la pantalla muestra contra las columnas del dominio que declara.

---

## 9.8 · Accesibilidad · `DS-A`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **A01** | Nivel objetivo WCAG 2.1 AA; AAA en lo crítico | OBL | — | B1·7 |
| **A02** | Texto 4.5:1, foco 3:1, comprobado al definir el token | OBL | **auto** | B1·7 |
| **A03** | Ninguna información se comunica solo con color | OBL | manual | B1·7 |
| **A04** | Todo campo lleva etiqueta persistente; el marcador nunca hace de etiqueta | OBL | **auto** | B1·7 |
| **A05** | Un solo H1 por pantalla, con jerarquía descendente | OBL | **auto** | B1·7 |
| **A06** | Todo icono con significado lleva texto alternativo de función | OBL | **auto** | B1·7 |
| **A07** | Lo que se puede con ratón se puede con teclado, con foco visible | OBL | semi | B1·7 |
| **A08** | Toda pantalla se revisa al 200 % de texto | OBL | semi | B1·7 |
| **A09** | Todo movimiento tiene alternativa reducida | OBL | **auto** | B1·7 |
| **A10** | Los cambios dinámicos se anuncian con región en vivo | OBL | **auto** | B1·7 |
| **A11** | Se revisa en un dispositivo de gama baja | REC | manual | B1·7 |
| **A12** | `axe-core` en la tubería cuando exista la aplicación | REC | — | B1·7 |
| **A13** | Toda pantalla tiene un solo foco visual primario, y se declara cuál | OBL | **auto** | Ext G10 |

---

## 9.9 · Entrega · `DS-H`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **H01** | El archivo de producto sigue la estructura de siete páginas | OBL | **auto** | B1·4 |
| **H02** | Capas y recursos siguen el convenio de los tokens | OBL | **auto** | B1·8 |
| **H03** | El nombre de un componente deriva del nombre de la tabla | OBL | **auto** | B1·4 · Ext G2 |
| **H04** | Iconos en SVG; fotografías en WebP o AVIF | OBL | **auto** | B1·8 |
| **H05** | Toda animación se entrega con sus cinco datos | OBL | **auto** | B1·8 |
| **H06** | El movimiento se anima con `transform`, no con posición | OBL | **auto** | B1·8 |
| **H07** | Versión manual al cerrar un ciclo, con nombre por hito | REC | **auto** | B1·1 |
| **H08** | Nada se borra: lo descartado va a la página de archivo | REC | **auto** | B1·4 |
| **H09** | El sistema declara su versión, y es semántica | OBL | **auto** | Ext G7 |
| **H10** | Toda entrega declara contra qué versión del sistema se dibujó | OBL | **auto** | Ext G7 |

---

## 9.10 · Puente con Figma · `DS-X`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **X01** | La fuente de verdad es el JSON; Figma es una salida | OBL | **auto** | B1·6 · Ext |
| **X02** | `Primitives` oculta de publicación y sin alcance | OBL | semi | B2·13 |
| **X03** | Toda variable publicada declara sintaxis para las tres plataformas | OBL | semi | B1·8 |
| **X04** | Los estilos apuntan a variables semánticas | OBL | semi | B2·13 |
| **X05** | Peso como número; familia como cadena exacta | OBL | **auto** | B2·13 |
| **X06** | **Ninguna etapa depende de que un agente escriba en el lienzo** | OBL | manual | Ext |
| **X07** | El alcance se acota también por tipo de propiedad | REC | semi | B2·13 |
| **X08** | Un complemento no se adopta sin pasar el árbol de decisión | REC | manual | B1·2 |

---

## 9.11 · El recuento

**Setenta y seis reglas**, y así se reparten:

| Área | Reglas | Obligatorias | `auto` | `semi` | `manual` | — |
|---|---|---|---|---|---|---|
| Fundamentos · `F` | 12 | 10 | **9** | 1 | 2 | — |
| Tokens · `T` | 10 | 7 | **6** | 3 | 1 | — |
| Componentes · `C` | 10 | 7 | **6** | 3 | 1 | — |
| Disposición · `L` | 10 | 6 | **2** | 6 | 2 | — |
| Patrones · `P` | 6 | 5 | **4** | — | 2 | — |
| Accesibilidad · `A` | 12 | 10 | **6** | 2 | 2 | 2 |
| Entrega · `H` | 8 | 6 | **4** | 2 | 2 | — |
| Puente Figma · `X` | 8 | 6 | **2** | 4 | 2 | — |
| **Total** | **76** | **57** | **39** | **21** | **14** | **2** |

### La marca de conteo

> **Son setenta y seis reglas, una por cada fila de las ocho tablas de §9.3 a §9.10**, y las cuatro columnas de
> verificación suman **39 + 21 + 14 + 2 = 76**. Si mañana una sección agrega una regla y este recuento sigue en
> setenta y seis, **falta registrarla acá**.

### Y el reparto entre libro y extensión

| Origen | Reglas |
|---|---|
| **Salen enteras de los libros** | **60** |
| Mezclan libro y extensión | 8 |
| **Extensión pura** | **8** |

**Las ocho de extensión pura son las que hay que poder defender**: `F07` · `F11` · `T07` · `C01` · `P01` ·
`P04` · `P06` · `X06`. Cada una nace de un vacío registrado en
[`TRAZABILIDAD-LIBROS.md`](../TRAZABILIDAD-LIBROS.md).

### Y lo que el recuento dice del plan

**39 de las 76 se pueden comprobar solas** — más de dos tercios de las obligatorias que no dependen de una
herramienta externa. **Ese es el alcance real del verificador de la etapa 6.**

Las **21 `semi`** dependen de renderizar la pantalla o de leer el archivo de Figma, y **entran cuando exista
cada cosa**. Las **14 `manual`** van a `10-checklists`, donde una persona las marca **y queda registrado que
las marcó**. Las **2 sin método** —`A01` y `A12`— no son reglas de comprobación sino declaraciones de nivel
objetivo y de herramienta futura.

> **Ninguna regla se declara verificable antes de que su comprobación exista y se haya probado contra un error
> inyectado a propósito.** Es la lección más cara de este proyecto, y aplica igual acá.
