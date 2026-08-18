# 09 · Rules (Las reglas)

**El índice único de las reglas del sistema, y cómo se comprueba cada una.** Es el documento que lee el
verificador y el que cita la skill.

**Clasificación:** consolida las ocho secciones anteriores · `[Extensión G1]` la columna de verificación.

---

## Índice

1. [Por qué las reglas llevan número](#91--por-qué-las-reglas-llevan-número)
2. [Cómo se lee la tabla](#92--cómo-se-lee-la-tabla)
3. [Fundamentos · DS-F](#93--fundamentos--ds-f)
4. [Tokens · DS-T](#94--tokens--ds-t)
5. [Componentes · DS-C](#95--componentes--ds-c)
6. [Disposición · DS-L](#96--disposición--ds-l)
7. [Patrones · DS-P](#97--patrones--ds-p)
8. [Accesibilidad · DS-A](#98--accesibilidad--ds-a)
9. [Entrega · DS-H](#99--entrega--ds-h)
10. [Puente con Figma · DS-X](#910--puente-con-figma--ds-x)
11. [El recuento](#911--el-recuento)

---

## 9.1 · Por qué las reglas llevan número

**Porque una recomendación en prosa no se puede citar ni comprobar.** Con número:

- el verificador puede reportar *"falla `DS-T07` en `02-listado.html`, línea 41"*
- la ficha de un componente puede declarar *"cumple `DS-C02` y `DS-C03`"*
- **y se puede comprobar que la regla citada existe** — igual que las 1360 citas de reglas que ya verifica
  `scripts/verificar.py` en el modelo de datos

### El vacío que esto llena

*Fuente: `[Extensión G1]`*

**Los dos libros no tienen ninguna comprobación automática.** Su control de calidad es:

| Libro | Mecanismo |
|---|---|
| `[Libro 1, capítulo 5]` | Reuniones mensuales, gobierno de tres roles, métricas de inserción y de desvinculación |
| `[Libro 1, capítulo 8]` | Listas de comprobación **que revisa una persona** |
| `[Libro 2, capítulo 12]` | **Design Lint** — el complemento que más se acerca, y **hay que abrirlo y correrlo a mano** |

**Y el propio libro admite hacia dónde debería ir** `[Libro 1, capítulo 8]`, en la nota de su revisor técnico:

> *"Muchos de estos puntos de la lista **deberían idealmente automatizarse mediante marcos de prueba** en lugar
> de comprobarse a mano por personas. La automatización garantiza consistencia, ahorra tiempo y **detecta
> problemas de forma más confiable que las revisiones manuales**."*

---

## 9.2 · Cómo se lee la tabla

| Columna | Qué dice |
|---|---|
| **Nivel** | `OBLIGATORIO` no se negocia · `RECOMENDADO` se justifica si no se cumple |
| **Verifica** | **`auto`** el guion la comprueba solo · **`semi`** necesita renderizar o una herramienta externa · **`manual`** requiere criterio |
| **Origen** | `Libro 1`/`Libro 2` más capítulo, o `Extensión` con su vacío |

> **`manual` no significa opcional.** Significa que el verificador **no puede** comprobarla, y por eso va a la
> lista de `10-checklists`, donde una persona la marca.

---

## 9.3 · Fundamentos · `DS-F`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **F01** | La rejilla se guarda como estilo; nunca se configura marco por marco | OBLIGATORIO | semi | Libro 2 · 5 |
| **F02** | Ningún texto traducible usa tamaño fijo | OBLIGATORIO | auto | Libro 1 · 3 |
| **F03** | Cuerpo ≥ 16 px, interlineado entre 1.4 y 1.6 | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **F04** | Los estilos de texto se nombran con barra | OBLIGATORIO | auto | Libro 2 · 5 |
| **F05** | Ningún par texto/fondo entra sin pasar el comprobador de contraste | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **F06** | Ningún valor de espaciado fuera de la escala | OBLIGATORIO | **auto** | Libro 2 · 5 · Extensión |
| **F07** | El radio completo se reserva a lo que no es un control | OBLIGATORIO | auto | Extensión |
| **F08** | La elevación se expresa solo con sombra difusa | OBLIGATORIO | auto | Libro 2 · 3 |
| **F09** | Los iconos combinan trazados, no agrupan formas | OBLIGATORIO | **auto** | Libro 1 · 8 |
| **F10** | Un icono no supera 2 kilobytes ni lleva `<mask>`, `<filter>` o `<clipPath>` | OBLIGATORIO | **auto** | Libro 1 · 8 |
| **F11** | Un solo color de acento, salvo que el segundo codifique significado | RECOMENDADO | manual | Extensión |
| **F12** | Las escalas de color se construyen en HSL y se guardan en HEX | RECOMENDADO | manual | Libro 2 · 5 |

---

## 9.4 · Tokens · `DS-T`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **T01** | Los tokens viven en JSON versionado; CSS y variables son salidas generadas | OBLIGATORIO | **auto** | Libro 1 · 6 · Extensión |
| **T02** | Tres niveles. Un componente nunca referencia un primitivo | OBLIGATORIO | **auto** | Libro 1 · 6 |
| **T03** | `Primitives` va oculta de publicación y sin alcance | OBLIGATORIO | semi | Libro 2 · 13 |
| **T04** | Un solo convenio de nombres en todo el sistema | OBLIGATORIO | **auto** | Libro 1 · 6 |
| **T05** | Toda variable publicada declara su sintaxis para web, iOS y Android | OBLIGATORIO | semi | Libro 1 · 8 |
| **T06** | El orden de construcción es color → espaciado → tipografía | OBLIGATORIO | manual | Libro 1 · 6 |
| **T07** | **Ningún valor en crudo en una pantalla** | OBLIGATORIO | **auto** | Extensión G1 |
| **T08** | Un valor merece token si aparece en tres o más lugares | RECOMENDADO | **auto** | Libro 1 · 6 |
| **T09** | El peso tipográfico se guarda como número | RECOMENDADO | auto | Libro 2 · 13 |
| **T10** | Los estilos apuntan a variables semánticas | RECOMENDADO | semi | Libro 2 · 13 |

---

## 9.5 · Componentes · `DS-C`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **C01** | Ningún componente entra sin su entrada en el inventario | OBLIGATORIO | **auto** | Extensión G3 |
| **C02** | Todo elemento interactivo declara estado de foco, con 3:1 | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **C03** | Todo componente con respuesta declara carga, vacío y error | OBLIGATORIO | **auto** | Libro 1 · 8 · Extensión |
| **C04** | Los auxiliares se prefijan con punto y no se publican | OBLIGATORIO | auto | Libro 2 · 7 |
| **C05** | Cada componente lleva descripción de cuándo usarlo y cuándo no | OBLIGATORIO | **auto** | Libro 2 · 11 |
| **C06** | La jerarquía va en páginas y marcos, no en nombres largos | OBLIGATORIO | semi | Libro 2 · 7 |
| **C07** | Fundamentos y componentes no comparten archivo | OBLIGATORIO | semi | Libro 1 · 5 |
| **C08** | Desvincular una instancia es la última salida | RECOMENDADO | semi | Libro 1 · 5 |
| **C09** | Se agrupa como variantes solo lo que difiere de forma limitada | RECOMENDADO | manual | Libro 2 · 7 |
| **C10** | El estado `hover` no se declara para móvil | RECOMENDADO | auto | Libro 2 · 8 |
| **C11** | El icono dentro de un componente sale de la tabla de tamaños de su plataforma | OBLIGATORIO | **auto** | Extensión G8 |
| **C12** | Ningún emoticón hace de icono de interfaz | OBLIGATORIO | **auto** | Extensión G8 |
| **C13** | Un hijo no puede ser más ancho que el espacio útil de su padre | OBLIGATORIO | **auto** | Extensión G9 |
| **C14** | Todo componente declara qué otros puede contener, y a qué profundidad | RECOMENDADO | **auto** | Extensión G9 |

---

## 9.6 · Disposición · `DS-L`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **L01** | **Todo contenedor usa Auto Layout** | OBLIGATORIO | semi | Libro 2 · 11 |
| **L02** | Espacio y relleno salen de la escala | OBLIGATORIO | **auto** | Libro 2 · 6 |
| **L03** | Ningún contenedor de texto usa `Fixed` en el eje del texto | OBLIGATORIO | semi | Libro 1 · 3 |
| **L04** | La estructura se construye con marcos, no con grupos | OBLIGATORIO | semi | Libro 2 · 3 |
| **L05** | Se diseña móvil primero | OBLIGATORIO | manual | Libro 2 · 8 |
| **L06** | Toda pantalla se prueba con los valores más largos y más cortos de su tabla | OBLIGATORIO | **auto** | Libro 2 · 4 · Extensión G2 |
| **L07** | Se construye de adentro hacia afuera | RECOMENDADO | manual | Libro 2 · 6 |
| **L08** | La restricción Escala se reserva a lo decorativo | RECOMENDADO | semi | Libro 2 · 6 |
| **L09** | Los elementos en `Fill` declaran mínimo y máximo | RECOMENDADO | semi | Libro 2 · 13 |
| **L10** | Las diferencias entre dispositivos se resuelven con booleanas | RECOMENDADO | semi | Libro 2 · 13 |

---

## 9.7 · Patrones · `DS-P`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **P01** | Todo patrón declara dominio, tablas y reglas en el inventario | OBLIGATORIO | **auto** | Extensión G2 |
| **P02** | **Ningún dato se muestra sin una columna que lo respalde** | OBLIGATORIO | **auto** | Libro 2 · 4 · Extensión G2 |
| **P03** | Todo patrón enumera sus estados, y al menos uno es un fallo | OBLIGATORIO | **auto** | Libro 1 · 8 · Libro 2 · 9 |
| **P04** | Lo que viene de otro dominio declara qué se muestra si no llega | OBLIGATORIO | **auto** | Extensión G2 |
| **P05** | Ninguna superficie continua no textual es el único portador de información necesaria | OBLIGATORIO | manual | Extensión G4 · Libro 1 · 7 |
| **P06** | Un patrón termina donde el modelo cambia de estado | RECOMENDADO | manual | Extensión |

> **`P02` es la regla más valiosa del sistema.** Es la que impide volver a dibujar *"Confort+"*, y **se puede
> comprobar sola**: se cruzan los datos que la pantalla muestra contra las columnas del dominio que declara.

---

## 9.8 · Accesibilidad · `DS-A`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **A01** | Nivel objetivo WCAG 2.1 AA; AAA en lo crítico | OBLIGATORIO | — | Libro 1 · 7 |
| **A02** | Texto 4.5:1, foco 3:1, comprobado al definir el token | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **A03** | Ninguna información se comunica solo con color | OBLIGATORIO | manual | Libro 1 · 7 |
| **A04** | Todo campo lleva etiqueta persistente; el marcador nunca hace de etiqueta | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **A05** | Un solo H1 por pantalla, con jerarquía descendente | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **A06** | Todo icono con significado lleva texto alternativo de función | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **A07** | Lo que se puede con ratón se puede con teclado, con foco visible | OBLIGATORIO | semi | Libro 1 · 7 |
| **A08** | Toda pantalla se revisa al 200 % de texto | OBLIGATORIO | semi | Libro 1 · 7 |
| **A09** | Todo movimiento tiene alternativa reducida | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **A10** | Los cambios dinámicos se anuncian con región en vivo | OBLIGATORIO | **auto** | Libro 1 · 7 |
| **A11** | Se revisa en un dispositivo de gama baja | RECOMENDADO | manual | Libro 1 · 7 |
| **A12** | `axe-core` en la tubería cuando exista la aplicación | RECOMENDADO | — | Libro 1 · 7 |
| **A13** | Toda pantalla tiene un solo foco visual primario, y se declara cuál | OBLIGATORIO | **auto** | Extensión G10 |

---

## 9.9 · Entrega · `DS-H`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **H01** | El archivo de producto sigue la estructura de siete páginas | OBLIGATORIO | **auto** | Libro 1 · 4 |
| **H02** | Capas y recursos siguen el convenio de los tokens | OBLIGATORIO | **auto** | Libro 1 · 8 |
| **H03** | El nombre de un componente deriva del nombre de la tabla | OBLIGATORIO | **auto** | Libro 1 · 4 · Extensión G2 |
| **H04** | Iconos en SVG; fotografías en WebP o AVIF | OBLIGATORIO | **auto** | Libro 1 · 8 |
| **H05** | Toda animación se entrega con sus cinco datos | OBLIGATORIO | **auto** | Libro 1 · 8 |
| **H06** | El movimiento se anima con `transform`, no con posición | OBLIGATORIO | **auto** | Libro 1 · 8 |
| **H07** | Versión manual al cerrar un ciclo, con nombre por hito | RECOMENDADO | **auto** | Libro 1 · 1 |
| **H08** | Nada se borra: lo descartado va a la página de archivo | RECOMENDADO | **auto** | Libro 1 · 4 |
| **H09** | El sistema declara su versión, y es semántica | OBLIGATORIO | **auto** | Extensión G7 |
| **H10** | Toda entrega declara contra qué versión del sistema se dibujó | OBLIGATORIO | **auto** | Extensión G7 |

---

## 9.10 · Puente con Figma · `DS-X`

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **X01** | La fuente de verdad es el JSON; Figma es una salida | OBLIGATORIO | **auto** | Libro 1 · 6 · Extensión |
| **X02** | `Primitives` oculta de publicación y sin alcance | OBLIGATORIO | semi | Libro 2 · 13 |
| **X03** | Toda variable publicada declara sintaxis para las tres plataformas | OBLIGATORIO | semi | Libro 1 · 8 |
| **X04** | Los estilos apuntan a variables semánticas | OBLIGATORIO | semi | Libro 2 · 13 |
| **X05** | Peso como número; familia como cadena exacta | OBLIGATORIO | **auto** | Libro 2 · 13 |
| **X06** | **Ninguna etapa depende de que un agente escriba en el lienzo** | OBLIGATORIO | manual | Extensión |
| **X07** | El alcance se acota también por tipo de propiedad | RECOMENDADO | semi | Libro 2 · 13 |
| **X08** | Un complemento no se adopta sin pasar el árbol de decisión | RECOMENDADO | manual | Libro 1 · 2 |

---

## 9.11 · El recuento

**83 reglas**, y así se reparten:

| Área | Reglas | Obligatorias | Automáticas | Asistidas | Manuales | Declarativas |
|---|---:|---:|---:|---:|---:|---:|
| Fundamentos · `F` | 12 | 10 | **9** | 1 | 2 | — |
| Tokens · `T` | 10 | 7 | **6** | 3 | 1 | — |
| Componentes · `C` | 14 | 10 | **10** | 3 | 1 | — |
| Disposición · `L` | 10 | 6 | **2** | 6 | 2 | — |
| Patrones · `P` | 6 | 5 | **4** | — | 2 | — |
| Accesibilidad · `A` | 13 | 11 | **7** | 2 | 2 | 2 |
| Entrega · `H` | 10 | 8 | **10** | — | — | — |
| Puente con Figma · `X` | 8 | 6 | **2** | 4 | 2 | — |
| **Total** | **83** | **63** | **50** | **19** | **12** | **2** |

### La marca de conteo

> **Hay una fila por regla en las ocho tablas de §9.3 a §9.10**, y las cuatro columnas de método suman
> **50 + 19 + 12 + 2 = 83**. Si una sección agrega una regla y este recuento
> no cambia, **falta registrarla acá**.
>
> **Y no hace falta recordarlo:** `lib/generar_referencia.py --comprobar` corre dentro de la suite y falla si
> el recuento y la tabla dejan de coincidir.

### Y el reparto entre libro y extensión

**Toda regla dice de dónde sale.** Es lo que permite discutirla: quien no esté de acuerdo puede ir a la fuente
en vez de discutir contra el documento.

| Origen | Reglas |
|---|---|
| **Salen enteras de los libros** | **60** |
| Mezclan libro y extensión | 8 |
| **Extensión pura** | **15** |

**Las 15 de extensión pura son las que hay que poder defender**, porque ningún libro las respalda:

`DS-A13` · `DS-C01` · `DS-C11` · `DS-C12` · `DS-C13` · `DS-C14` · `DS-F07` · `DS-F11` · `DS-H09` · `DS-H10` · `DS-P01` · `DS-P04` · `DS-P06` · `DS-T07` · `DS-X06`

Cada una nace de un vacío registrado en [`TRAZABILIDAD-LIBROS.md`](../TRAZABILIDAD-LIBROS.md) y en
[`00-ANALISIS-DE-CONOCIMIENTO.md`](../00-ANALISIS-DE-CONOCIMIENTO.md).

### Y lo que el recuento dice del alcance

**50 de 83 se comprueban solas**, y **las 50 están probadas contra un error inyectado a
propósito**. Ese es el alcance real de los verificadores, no una estimación.

Las **19 asistidas** dependen de renderizar la pantalla o de leer el archivo de Figma. Las
**12 manuales** y las **2 declarativas** las lista el informe de auditoría para que las marque
una persona — **manual no significa opcional**.

> **Ninguna regla se declara verificable antes de que su comprobación exista y se haya probado contra un error
> inyectado a propósito.** Es la lección más cara de este proyecto, y aplica igual acá.
>
> **Tres reglas cambiaron de método al construirse su comprobación** — `DS-H01`, `DS-H07` y `DS-H08` pasaron de
> asistidas a automáticas en cuanto la estructura del archivo se declaró en un documento en vez de vivir dentro
> de una herramienta. **El límite no era la regla: era dónde estaba escrita la respuesta.**
