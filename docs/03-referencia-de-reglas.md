# Referencia de reglas

> **Documento generado.** Lo produce `lib/generar_referencia.py` leyendo
> `conocimiento/DESIGN/09-rules/README.md` y los guiones de `skills/`.
> **No se edita a mano:** los cambios se hacen en la base de conocimiento y se
> regenera. La suite de pruebas falla si este documento queda desactualizado.
>
> **Estado.** 87 reglas · 54 automáticas · 70 con guion que las comprueba · 58 probadas rompiéndolas a propósito.

---

## Índice

1. [Cómo se lee una regla](#1--cómo-se-lee-una-regla)
2. [Resumen por familia](#2--resumen-por-familia)
3. [Fundamentos](#3--fundamentos)
4. [Tokens](#4--tokens)
5. [Componentes](#5--componentes)
6. [Disposición](#6--disposición)
7. [Patrones](#7--patrones)
8. [Accesibilidad](#8--accesibilidad)
9. [Entrega](#9--entrega)
10. [Puente con Figma](#10--puente-con-figma)
11. [Reglas sin comprobación automática](#11--reglas-sin-comprobación-automática)

---

## 1 · Cómo se lee una regla

Cada regla tiene un identificador estable, un nivel de exigencia, un método de
comprobación y un origen. **El identificador es lo que permite citarla** desde un
guion, desde una ficha de componente o desde un informe de auditoría.

| Columna | Qué indica |
|---|---|
| **Identificador** | `DS-` más la familia y el número. Es estable: no se reutiliza |
| **Nivel** | `OBLIGATORIO` no se negocia · `RECOMENDADO` se justifica si no se cumple |
| **Método** | Cómo se comprueba. Ver la tabla siguiente |
| **Guion** | Qué archivo la comprueba, si alguno |
| **Origen** | El capítulo del libro, o la extensión que llena un vacío |

**Los cuatro métodos de comprobación:**

| Método | Qué significa |
|---|---|
| **Automática** | Un guion la comprueba sola |
| **Asistida** | Necesita renderizar o una herramienta externa |
| **Manual** | Requiere criterio de una persona |
| **Declarativa** | Fija un objetivo; no se comprueba pieza por pieza |

> **`Manual` no significa opcional.** Significa que ningún guion puede comprobarla,
> y por eso el informe de auditoría la lista para que la marque una persona.

---

## 2 · Resumen por familia

| Familia | Prefijo | Reglas | Automáticas | Con guion | Sección de la base de conocimiento |
|---|---|---:|---:|---:|---|
| Fundamentos | `DS-F` | 12 | 9 | 9 | `01-foundations/` |
| Tokens | `DS-T` | 10 | 6 | 8 | `02-tokens/` |
| Componentes | `DS-C` | 14 | 10 | 11 | `03-components/` |
| Disposición | `DS-L` | 10 | 2 | 5 | `04-auto-layout/` |
| Patrones | `DS-P` | 6 | 4 | 5 | `05-patterns/` |
| Accesibilidad | `DS-A` | 13 | 7 | 13 | `06-accessibility/` |
| Entrega | `DS-H` | 10 | 10 | 10 | `07-handoff/` |
| Puente con Figma | `DS-X` | 12 | 6 | 9 | `08-figma-bridge/` |
| **Total** | | **87** | **54** | **70** | |

---

## 3 · Fundamentos

**Prefijo `DS-F` · 12 reglas · base de conocimiento: `conocimiento/DESIGN/01-foundations/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-F01`** | La rejilla se guarda como estilo; nunca se configura marco por marco | OBLIGATORIO | Asistida | — | Libro 2 · 5 |
| **`DS-F02`** | Ningún texto traducible usa tamaño fijo | OBLIGATORIO | Automática | `probar.py` ✓ | Libro 1 · 3 |
| **`DS-F03`** | Cuerpo ≥ 16 px, interlineado entre 1.4 y 1.6 | OBLIGATORIO | Automática | `verificar-pantalla.py` · `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-F04`** | Los estilos de texto se nombran con barra | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 2 · 5 |
| **`DS-F05`** | Ningún par texto/fondo entra sin pasar el comprobador de contraste | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-F06`** | Ningún valor de espaciado fuera de la escala | OBLIGATORIO | Automática | `derivar.py` · `verificar.py` ✓ | Libro 2 · 5 · Extensión |
| **`DS-F07`** | El radio completo se reserva a lo que no es un control | OBLIGATORIO | Automática | `verificar.py` ✓ | Extensión |
| **`DS-F08`** | La elevación se expresa solo con sombra difusa | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 2 · 3 |
| **`DS-F09`** | Los iconos combinan trazados, no agrupan formas | OBLIGATORIO | Automática | `entregar.py` · `iconos.py` ✓ | Libro 1 · 8 |
| **`DS-F10`** | Un icono no supera 2 kilobytes ni lleva `<mask>`, `<filter>` o `<clipPath>` | OBLIGATORIO | Automática | `entregar.py` · `iconos.py` ✓ | Libro 1 · 8 |
| **`DS-F11`** | Un solo color de acento, salvo que el segundo codifique significado | RECOMENDADO | Manual | — | Extensión |
| **`DS-F12`** | Las escalas de color se construyen en HSL y se guardan en HEX | RECOMENDADO | Manual | — | Libro 2 · 5 |

---

## 4 · Tokens

**Prefijo `DS-T` · 10 reglas · base de conocimiento: `conocimiento/DESIGN/02-tokens/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-T01`** | Los tokens viven en JSON versionado; CSS y variables son salidas generadas | OBLIGATORIO | Automática | `construir.py` · `verificar.py` ✓ | Libro 1 · 6 · Extensión |
| **`DS-T02`** | Tres niveles. Un componente nunca referencia un primitivo | OBLIGATORIO | Automática | `construir.py` · `derivar.py` · `verificar.py` ✓ | Libro 1 · 6 |
| **`DS-T03`** | `Primitives` va oculta de publicación y sin alcance | OBLIGATORIO | Asistida | `construir.py` · `derivar.py` | Libro 2 · 13 |
| **`DS-T04`** | Un solo convenio de nombres en todo el sistema | OBLIGATORIO | Automática | `auditar.py` · `entregar.py` · `verificar.py` ✓ | Libro 1 · 6 |
| **`DS-T05`** | Toda variable publicada declara su sintaxis para web, iOS y Android | OBLIGATORIO | Asistida | `construir.py` | Libro 1 · 8 |
| **`DS-T06`** | El orden de construcción es color → espaciado → tipografía | OBLIGATORIO | Manual | — | Libro 1 · 6 |
| **`DS-T07`** | Ningún valor en crudo en una pantalla | OBLIGATORIO | Automática | `auditar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Extensión G1 |
| **`DS-T08`** | Un valor merece token si aparece en tres o más lugares | RECOMENDADO | Automática | `verificar.py` ✓ | Libro 1 · 6 |
| **`DS-T09`** | El peso tipográfico se guarda como número | RECOMENDADO | Automática | `verificar.py` ✓ | Libro 2 · 13 |
| **`DS-T10`** | Los estilos apuntan a variables semánticas | RECOMENDADO | Asistida | — | Libro 2 · 13 |

---

## 5 · Componentes

**Prefijo `DS-C` · 14 reglas · base de conocimiento: `conocimiento/DESIGN/03-components/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-C01`** | Ningún componente entra sin su entrada en el inventario | OBLIGATORIO | Automática | `auditar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Extensión G3 |
| **`DS-C02`** | Todo elemento interactivo declara estado de foco, con 3:1 | OBLIGATORIO | Automática | `auditar.py` · `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-C03`** | Todo componente con respuesta declara carga, vacío y error | OBLIGATORIO | Automática | `auditar.py` · `probar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Libro 1 · 8 · Extensión |
| **`DS-C04`** | Los auxiliares se prefijan con punto y no se publican | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 2 · 7 |
| **`DS-C05`** | Cada componente lleva descripción de cuándo usarlo y cuándo no | OBLIGATORIO | Automática | `auditar.py` · `verificar.py` ✓ | Libro 2 · 11 |
| **`DS-C06`** | La jerarquía va en páginas y marcos, no en nombres largos | OBLIGATORIO | Asistida | — | Libro 2 · 7 |
| **`DS-C07`** | Fundamentos y componentes no comparten archivo | OBLIGATORIO | Asistida | — | Libro 1 · 5 |
| **`DS-C08`** | Desvincular una instancia es la última salida | RECOMENDADO | Asistida | — | Libro 1 · 5 |
| **`DS-C09`** | Se agrupa como variantes solo lo que difiere de forma limitada | RECOMENDADO | Manual | `auditar.py` ✓ | Libro 2 · 7 |
| **`DS-C10`** | El estado `hover` no se declara para móvil | RECOMENDADO | Automática | `verificar.py` ✓ | Libro 2 · 8 |
| **`DS-C11`** | El icono dentro de un componente sale de la tabla de tamaños de su plataforma | OBLIGATORIO | Automática | `iconos.py` · `verificar.py` ✓ | Extensión G8 |
| **`DS-C12`** | Ningún emoticón hace de icono de interfaz | OBLIGATORIO | Automática | `verificar.py` ✓ | Extensión G8 |
| **`DS-C13`** | Un hijo no puede ser más ancho que el espacio útil de su padre | OBLIGATORIO | Automática | `verificar-pantalla.py` ✓ | Extensión G9 |
| **`DS-C14`** | Todo componente declara qué otros puede contener, y a qué profundidad | RECOMENDADO | Automática | `verificar.py` ✓ | Extensión G9 |

---

## 6 · Disposición

**Prefijo `DS-L` · 10 reglas · base de conocimiento: `conocimiento/DESIGN/04-auto-layout/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-L01`** | Todo contenedor usa Auto Layout | OBLIGATORIO | Asistida | `construir.py` | Libro 2 · 11 |
| **`DS-L02`** | Espacio y relleno salen de la escala | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 2 · 6 |
| **`DS-L03`** | Ningún contenedor de texto usa `Fixed` en el eje del texto | OBLIGATORIO | Asistida | `probar.py` ✓ | Libro 1 · 3 |
| **`DS-L04`** | La estructura se construye con marcos, no con grupos | OBLIGATORIO | Asistida | — | Libro 2 · 3 |
| **`DS-L05`** | Se diseña móvil primero | OBLIGATORIO | Manual | `probar.py` | Libro 2 · 8 |
| **`DS-L06`** | Toda pantalla se prueba con los valores más largos y más cortos de su tabla | OBLIGATORIO | Automática | `probar.py` · `verificar-pantalla.py` ✓ | Libro 2 · 4 · Extensión G2 |
| **`DS-L07`** | Se construye de adentro hacia afuera | RECOMENDADO | Manual | — | Libro 2 · 6 |
| **`DS-L08`** | La restricción Escala se reserva a lo decorativo | RECOMENDADO | Asistida | — | Libro 2 · 6 |
| **`DS-L09`** | Los elementos en `Fill` declaran mínimo y máximo | RECOMENDADO | Asistida | — | Libro 2 · 13 |
| **`DS-L10`** | Las diferencias entre dispositivos se resuelven con booleanas | RECOMENDADO | Asistida | — | Libro 2 · 13 |

---

## 7 · Patrones

**Prefijo `DS-P` · 6 reglas · base de conocimiento: `conocimiento/DESIGN/05-patterns/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-P01`** | Todo patrón declara dominio, tablas y reglas en el inventario | OBLIGATORIO | Automática | `inyectar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Extensión G2 |
| **`DS-P02`** | Ningún dato se muestra sin una columna que lo respalde | OBLIGATORIO | Automática | `inyectar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Libro 2 · 4 · Extensión G2 |
| **`DS-P03`** | Todo patrón enumera sus estados, y al menos uno es un fallo | OBLIGATORIO | Automática | `probar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Libro 1 · 8 · Libro 2 · 9 |
| **`DS-P04`** | Lo que viene de otro dominio declara qué se muestra si no llega | OBLIGATORIO | Automática | `verificar-pantalla.py` ✓ | Extensión G2 |
| **`DS-P05`** | Ninguna superficie continua no textual es el único portador de información necesaria | OBLIGATORIO | Manual | `probar.py` | Extensión G4 · Libro 1 · 7 |
| **`DS-P06`** | Un patrón termina donde el modelo cambia de estado | RECOMENDADO | Manual | — | Extensión |

---

## 8 · Accesibilidad

**Prefijo `DS-A` · 13 reglas · base de conocimiento: `conocimiento/DESIGN/06-accessibility/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-A01`** | Nivel objetivo WCAG 2.1 AA; AAA en lo crítico | OBLIGATORIO | Declarativa | `auditar.py` | Libro 1 · 7 |
| **`DS-A02`** | Texto 4.5:1, foco 3:1, comprobado al definir el token | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-A03`** | Ninguna información se comunica solo con color | OBLIGATORIO | Manual | `probar.py` | Libro 1 · 7 |
| **`DS-A04`** | Todo campo lleva etiqueta persistente; el marcador nunca hace de etiqueta | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-A05`** | Un solo H1 por pantalla, con jerarquía descendente | OBLIGATORIO | Automática | `probar.py` · `verificar-pantalla.py` ✓ | Libro 1 · 7 |
| **`DS-A06`** | Todo icono con significado lleva texto alternativo de función | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-A07`** | Lo que se puede con ratón se puede con teclado, con foco visible | OBLIGATORIO | Asistida | `probar.py` · `verificar-pantalla.py` · `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-A08`** | Toda pantalla se revisa al 200 % de texto | OBLIGATORIO | Asistida | `probar.py` ✓ | Libro 1 · 7 |
| **`DS-A09`** | Todo movimiento tiene alternativa reducida | OBLIGATORIO | Automática | `construir.py` · `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-A10`** | Los cambios dinámicos se anuncian con región en vivo | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 1 · 7 |
| **`DS-A11`** | Se revisa en un dispositivo de gama baja | RECOMENDADO | Manual | `probar.py` | Libro 1 · 7 |
| **`DS-A12`** | `axe-core` en la tubería cuando exista la aplicación | RECOMENDADO | Declarativa | `probar.py` | Libro 1 · 7 |
| **`DS-A13`** | Toda pantalla tiene un solo foco visual primario, y se declara cuál | OBLIGATORIO | Automática | `verificar-pantalla.py` ✓ | Extensión G10 |

---

## 9 · Entrega

**Prefijo `DS-H` · 10 reglas · base de conocimiento: `conocimiento/DESIGN/07-handoff/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-H01`** | El archivo de producto sigue la estructura de siete páginas | OBLIGATORIO | Automática | `entregar.py` ✓ | Libro 1 · 4 |
| **`DS-H02`** | Capas y recursos siguen el convenio de los tokens | OBLIGATORIO | Automática | `entregar.py` ✓ | Libro 1 · 8 |
| **`DS-H03`** | El nombre de un componente deriva del nombre de la tabla | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 1 · 4 · Extensión G2 |
| **`DS-H04`** | Iconos en SVG; fotografías en WebP o AVIF | OBLIGATORIO | Automática | `entregar.py` ✓ | Libro 1 · 8 |
| **`DS-H05`** | Toda animación se entrega con sus cinco datos | OBLIGATORIO | Automática | `entregar.py` ✓ | Libro 1 · 8 |
| **`DS-H06`** | El movimiento se anima con `transform`, no con posición | OBLIGATORIO | Automática | `entregar.py` ✓ | Libro 1 · 8 |
| **`DS-H07`** | Versión manual al cerrar un ciclo, con nombre por hito | RECOMENDADO | Automática | `entregar.py` ✓ | Libro 1 · 1 |
| **`DS-H08`** | Nada se borra: lo descartado va a la página de archivo | RECOMENDADO | Automática | `entregar.py` ✓ | Libro 1 · 4 |
| **`DS-H09`** | El sistema declara su versión, y es semántica | OBLIGATORIO | Automática | `entregar.py` ✓ | Extensión G7 |
| **`DS-H10`** | Toda entrega declara contra qué versión del sistema se dibujó | OBLIGATORIO | Automática | `entregar.py` ✓ | Extensión G7 |

---

## 10 · Puente con Figma

**Prefijo `DS-X` · 12 reglas · base de conocimiento: `conocimiento/DESIGN/08-figma-bridge/README.md`**

| Identificador | Enunciado | Nivel | Método | Guion | Origen |
|---|---|---|---|---|---|
| **`DS-X01`** | La fuente de verdad es el JSON; Figma es una salida | OBLIGATORIO | Automática | `construir.py` · `verificar.py` ✓ | Libro 1 · 6 · Extensión |
| **`DS-X02`** | `Primitives` oculta de publicación y sin alcance | OBLIGATORIO | Asistida | `construir.py` | Libro 2 · 13 |
| **`DS-X03`** | Toda variable publicada declara sintaxis para las tres plataformas | OBLIGATORIO | Asistida | `construir.py` · `verificar.py` | Libro 1 · 8 |
| **`DS-X04`** | Los estilos apuntan a variables semánticas | OBLIGATORIO | Asistida | `construir.py` | Libro 2 · 13 |
| **`DS-X05`** | Peso como número; familia como cadena exacta | OBLIGATORIO | Automática | `verificar.py` ✓ | Libro 2 · 13 |
| **`DS-X06`** | Ninguna etapa depende de que un agente escriba en el lienzo | OBLIGATORIO | Manual | — | Extensión |
| **`DS-X07`** | El alcance se acota también por tipo de propiedad | RECOMENDADO | Asistida | — | Libro 2 · 13 |
| **`DS-X08`** | Un complemento no se adopta sin pasar el árbol de decisión | RECOMENDADO | Manual | — | Libro 1 · 2 |
| **`DS-X09`** | El nombre de toda variable publicada es importable en Figma | OBLIGATORIO | Automática | `verificar.py` ✓ | Extensión G11 |
| **`DS-X10`** | La sintaxis por plataforma nombra la variable que esa plataforma define | OBLIGATORIO | Automática | `verificar.py` ✓ | Extensión G12 |
| **`DS-X11`** | Toda referencia de una salida resuelve dentro de esa misma salida | OBLIGATORIO | Automática | `verificar.py` ✓ | Extensión G12 |
| **`DS-X12`** | Todo campo enumerado sale en el vocabulario de la herramienta, no en el propio | OBLIGATORIO | Automática | `construir.py` · `verificar.py` ✓ | Extensión G13 |

---

## 11 · Reglas sin comprobación automática

**Estas reglas las marca una persona.** Aparecen en el informe de auditoría
(`auditar.py --html`) para que ninguna quede sin revisar.

Son **33 de 87**.

| Identificador | Enunciado | Nivel | Método |
|---|---|---|---|
| **`DS-F01`** | La rejilla se guarda como estilo; nunca se configura marco por marco | OBLIGATORIO | Asistida |
| **`DS-F11`** | Un solo color de acento, salvo que el segundo codifique significado | RECOMENDADO | Manual |
| **`DS-F12`** | Las escalas de color se construyen en HSL y se guardan en HEX | RECOMENDADO | Manual |
| **`DS-T03`** | `Primitives` va oculta de publicación y sin alcance | OBLIGATORIO | Asistida |
| **`DS-T05`** | Toda variable publicada declara su sintaxis para web, iOS y Android | OBLIGATORIO | Asistida |
| **`DS-T06`** | El orden de construcción es color → espaciado → tipografía | OBLIGATORIO | Manual |
| **`DS-T10`** | Los estilos apuntan a variables semánticas | RECOMENDADO | Asistida |
| **`DS-C06`** | La jerarquía va en páginas y marcos, no en nombres largos | OBLIGATORIO | Asistida |
| **`DS-C07`** | Fundamentos y componentes no comparten archivo | OBLIGATORIO | Asistida |
| **`DS-C08`** | Desvincular una instancia es la última salida | RECOMENDADO | Asistida |
| **`DS-C09`** | Se agrupa como variantes solo lo que difiere de forma limitada | RECOMENDADO | Manual |
| **`DS-L01`** | Todo contenedor usa Auto Layout | OBLIGATORIO | Asistida |
| **`DS-L03`** | Ningún contenedor de texto usa `Fixed` en el eje del texto | OBLIGATORIO | Asistida |
| **`DS-L04`** | La estructura se construye con marcos, no con grupos | OBLIGATORIO | Asistida |
| **`DS-L05`** | Se diseña móvil primero | OBLIGATORIO | Manual |
| **`DS-L07`** | Se construye de adentro hacia afuera | RECOMENDADO | Manual |
| **`DS-L08`** | La restricción Escala se reserva a lo decorativo | RECOMENDADO | Asistida |
| **`DS-L09`** | Los elementos en `Fill` declaran mínimo y máximo | RECOMENDADO | Asistida |
| **`DS-L10`** | Las diferencias entre dispositivos se resuelven con booleanas | RECOMENDADO | Asistida |
| **`DS-P05`** | Ninguna superficie continua no textual es el único portador de información necesaria | OBLIGATORIO | Manual |
| **`DS-P06`** | Un patrón termina donde el modelo cambia de estado | RECOMENDADO | Manual |
| **`DS-A01`** | Nivel objetivo WCAG 2.1 AA; AAA en lo crítico | OBLIGATORIO | Declarativa |
| **`DS-A03`** | Ninguna información se comunica solo con color | OBLIGATORIO | Manual |
| **`DS-A07`** | Lo que se puede con ratón se puede con teclado, con foco visible | OBLIGATORIO | Asistida |
| **`DS-A08`** | Toda pantalla se revisa al 200 % de texto | OBLIGATORIO | Asistida |
| **`DS-A11`** | Se revisa en un dispositivo de gama baja | RECOMENDADO | Manual |
| **`DS-A12`** | `axe-core` en la tubería cuando exista la aplicación | RECOMENDADO | Declarativa |
| **`DS-X02`** | `Primitives` oculta de publicación y sin alcance | OBLIGATORIO | Asistida |
| **`DS-X03`** | Toda variable publicada declara sintaxis para las tres plataformas | OBLIGATORIO | Asistida |
| **`DS-X04`** | Los estilos apuntan a variables semánticas | OBLIGATORIO | Asistida |
| **`DS-X06`** | Ninguna etapa depende de que un agente escriba en el lienzo | OBLIGATORIO | Manual |
| **`DS-X07`** | El alcance se acota también por tipo de propiedad | RECOMENDADO | Asistida |
| **`DS-X08`** | Un complemento no se adopta sin pasar el árbol de decisión | RECOMENDADO | Manual |

> **Varias podrían dejar de estar en esta lista.** Tres reglas que la base de
> conocimiento clasificaba como asistidas o manuales resultaron comprobables en
> cuanto la estructura se declaró en un archivo en vez de vivir dentro de una
> herramienta. **El límite no era la regla: era dónde estaba escrita la respuesta.**

