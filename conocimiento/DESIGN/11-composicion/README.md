# 11 · Composición (Lo que hace que se vea profesional)

**Por qué existe esta sección.** Las diez anteriores dicen cómo se construye un sistema correcto. Esta dice por
qué un sistema correcto puede verse igual amateur — y qué se comprueba para que no.

**Clasificación:** `[Ext G8, G9, G10]`. **No sale de los libros**: sale de inspeccionar un archivo de referencia
real y de comparar qué hacía distinto.

---

## Índice

1. [De dónde sale esta sección](#111--de-dónde-sale-esta-sección)
2. [El tamaño del icono no es libre](#112--el-tamaño-del-icono-no-es-libre--ds-c11)
3. [Ningún emoticón hace de icono](#113--ningún-emoticón-hace-de-icono--ds-c12)
4. [El hijo no desborda al padre](#114--el-hijo-no-desborda-al-padre--ds-c13-ds-c14)
5. [Una pantalla tiene un solo foco](#115--una-pantalla-tiene-un-solo-foco--ds-a13)
6. [Reglas de esta sección](#116--reglas-de-esta-sección)

---

## 11.1 · De dónde sale esta sección

**Se inspeccionó un archivo de referencia** —un clon de la aplicación de Coinbase, ~60 pantallas— buscando qué
lo hacía verse profesional. **El hallazgo principal fue el contrario del esperado**, y vale registrarlo:

| Lo que se buscaba | Lo que había |
|---|---|
| Una biblioteca de componentes ejemplar | **Cero conjuntos de componentes.** Ninguno |
| Tokens o variables | **Ninguna variable** |
| Nombres que nombran el concepto | `Frame 154`, `Group 5214`, `Rectangle 4069` |
| Una estructura de páginas | **Una sola página**, con todo adentro |

> **El archivo de referencia viola casi todas las reglas de este sistema** — `DS-H03` (el nombre nombra el
> concepto), `DS-C06` (la jerarquía va en páginas), `DS-L04` (marcos, no grupos), `DS-C01` (contrato en el
> inventario). **Y aun así se ve muy bien.**

**Esa contradicción es exactamente el aporte de esta sección.** Lo que hace que algo se vea profesional y lo
que hace que sea mantenible **son dos cosas distintas**, y un sistema que solo cuida la segunda produce
bibliotecas impecables que dibujan pantallas mediocres.

### Lo que sí hacía bien, medido sobre el lienzo

| Qué | Cuánto | Por qué importa |
|---|---|---|
| **Un solo acento** | Un azul. Todo lo demás, escala de grises | Cuando todo puede destacar, nada destaca |
| **Márgenes generosos** | 24 px a los lados, sostenidos en las 60 pantallas | El aire es lo que separa «denso» de «apretado» |
| **Escala tipográfica corta** | 4 tamaños en toda la aplicación | Diez tamaños es no haber decidido |
| **Etiqueta persistente sobre el campo** | Siempre, nunca el marcador de posición | Coincide con `DS-A04` |
| **Foco visible y de color** | Borde **y** etiqueta cambian al acento | Coincide con `DS-C02` |
| **Iconos coherentes por contexto** | 24 en barra, 20 dentro de campo | **Es lo que se vuelve `DS-C11`** |
| **Chrome nativo, no dibujado** | Barra de estado e indicador de inicio reales | **Es lo que se vuelve el contrato nativo** |
| **Nada de emoticones** | Ni uno en 60 pantallas | **Es lo que se vuelve `DS-C12`** |

**Las cuatro reglas de esta sección son las cuatro de esa tabla que todavía no estaban escritas en ningún lado.**

---

## 11.2 · El tamaño del icono no es libre · `DS-C11`

**El error más frecuente y el más visible.** Un icono de 24 px dentro de un campo de 44 px de alto se ve
gigante; el mismo icono en una barra de navegación se ve correcto. **No es el icono: es la relación con lo que
lo rodea.**

### La tabla, por plataforma y por uso

| Uso | iOS | Android | Web | Desktop |
|---|---:|---:|---:|---:|
| **Barra** — navegación, pestañas | 22 | 24 | 20 | 16 |
| **Control** — botón, acción | 20 | 24 | 20 | 16 |
| **Campo** — dentro de un input | 20 | 20 | 16 | 14 |
| **Línea** — junto a texto corrido | 17 | 18 | 16 | 14 |
| **Grande** — estado vacío, ilustración | 28 | 32 | 24 | 20 |

**OBLIGATORIO** — un componente que lleva icono declara su `uso`, y el tamaño sale de la tabla. Vive en
`recursos/iconos.json` → `_tamanos`.

### Y el grosor acompaña al tamaño

**Un icono de trazo 2 junto a texto regular pesa más que el texto**, y eso desequilibra la línea sin que se
sepa por qué.

```
1.5   para 16–20 px
2     para 24 px y más
nunca menos de 1.25 — se rompe al exportar
```

### El color se hereda, no se escribe

**OBLIGATORIO** — `currentColor`. Un icono con el color escrito adentro **no cambia con el modo oscuro ni con
el estado del componente que lo contiene**, y termina siendo el único elemento que no responde al tema. Es el
mismo argumento de `DS-T07` aplicado a un archivo.

---

## 11.3 · Ningún emoticón hace de icono · `DS-C12`

**Un emoticón no es un icono.** Se parece a uno y falla en las cuatro cosas que un icono tiene que hacer:

| Un icono | Un emoticón |
|---|---|
| Hereda el color del texto | Trae su propio color, siempre |
| Escala con el tamaño de letra | Escala, pero cambia de forma entre versiones |
| Se ve igual en todas partes | **Distinto en cada sistema operativo y cada versión** |
| Lleva el texto alternativo que se le escribió | El lector de pantalla lee un nombre que nadie eligió |

> **El caso que lo deja claro:** el emoticón de la cara sonriente se lee *«cara sonriente con ojos de
> corazón»*. Si se usó para marcar «favorito», el lector de pantalla anuncia otra cosa — y `DS-A06` exige que
> todo icono con significado declare su función.

**La única excepción es el contenido de la persona usuaria.** Si alguien escribe un emoticón en un mensaje, se
muestra tal cual: es su texto, no la interfaz.

---

## 11.4 · El hijo no desborda al padre · `DS-C13`, `DS-C14`

**El desbordamiento no se ve en la maqueta: se ve con los datos reales.** Por eso `DS-L06` exige probar con el
valor más largo — y por eso hace falta además una regla sobre el ancho.

### La cuenta que hay que poder hacer

```
espacio útil del padre  =  ancho del padre
                         − relleno izquierdo − relleno derecho
                         − espacio entre hijos × (cantidad de hijos − 1)
```

**OBLIGATORIO** — la suma de los anchos mínimos de los hijos **no puede superar el espacio útil**. Si lo
supera, hay tres salidas, en este orden:

1. **Uno de los hijos abraza y otro llena.** Un icono abraza; el texto llena. Es lo correcto casi siempre.
2. **El texto se corta con puntos suspensivos** — y se declara *cuál* se corta, no «el que toque».
3. **El contenedor cambia de dirección.** De fila a columna.

> **Lo que nunca es una salida: achicar la letra.** Es la reacción automática y rompe `DS-F03` —cuerpo ≥ 16 px—
> y `DS-F02` —ningún texto traducible usa tamaño fijo—. El texto crece un 30 % al traducir del inglés; achicar
> hoy es garantizar el desborde mañana.

### Y qué puede contener qué · `DS-C14`

**RECOMENDADO** — todo componente declara `admite`: qué otros componentes pueden ir adentro, y hasta qué
profundidad.

```
tarjeta      admite: avatar, distintivo, chip, boton, .icono     profundidad: 2
boton        admite: .icono                                       profundidad: 1
campo        admite: .icono, boton-icono                          profundidad: 1
```

**Por qué la profundidad tiene tope.** Un botón dentro de un chip dentro de una tarjeta dentro de una lista es
**cuatro niveles de relleno acumulado**: el contenido queda a 64 px del borde y nadie decidió eso — se sumó
solo. La profundidad declarada es lo que impide que la anidación crezca sin que nadie la mire.

---

## 11.5 · Una pantalla tiene un solo foco · `DS-A13`

**El error que produce pantallas «prolijas pero que no dicen nada».** Todo está bien alineado, todo tiene el
mismo peso, y no se sabe qué hay que hacer.

**OBLIGATORIO** — toda pantalla declara `foco`: **cuál es la acción o el dato primario**, y ese es el único que
lleva el acento en su versión llena.

### Los tres niveles, y no más

| Nivel | Cuántos por pantalla | Cómo se distingue |
|---|---|---|
| **Primario** | **Exactamente uno** | Acento lleno · el tamaño mayor · sobre el pliegue |
| **Secundario** | Los que hagan falta | Contorno o acento tenue · tamaño de cuerpo |
| **Terciario** | Los que hagan falta | Solo texto · color secundario |

> **Dos botones primarios en una pantalla es no haber decidido cuál es la tarea.** Y si de verdad hay dos
> caminos igual de válidos —«Aceptar» y «Rechazar» en una solicitud—, entonces la pantalla tiene **una decisión**
> y ese es el foco: los dos botones juntos son el elemento primario, y nada más compite con ellos.

### Y el foco va sobre el pliegue

**Ya está en `05-patterns` y se repite acá porque es la mitad de la misma regla:** lo que distingue al producto
tiene que verse **sin desplazar**. Un foco primario debajo del pliegue no es un foco: es un elemento que la
persona encuentra si tiene ganas.

---

## 11.6 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-C11`** | El icono dentro de un componente **sale de la tabla de tamaños** de su plataforma | OBLIGATORIO | `[Ext G8]` |
| **`DS-C12`** | **Ningún emoticón** hace de icono de interfaz | OBLIGATORIO | `[Ext G8]` |
| **`DS-C13`** | Un hijo **no puede ser más ancho** que el espacio útil de su padre | OBLIGATORIO | `[Ext G9]` |
| **`DS-C14`** | Todo componente declara **qué otros puede contener**, y a qué profundidad | RECOMENDADO | `[Ext G9]` |
| **`DS-A13`** | Toda pantalla tiene **un solo foco visual primario**, y se declara cuál | OBLIGATORIO | `[Ext G10]` |
