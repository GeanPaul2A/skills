# 01 · Foundations (Fundamentos)

Las decisiones visuales de las que cuelga todo lo demás: **rejilla, tipografía, color, espaciado, forma,
elevación e iconografía**. Y —lo que los libros dan por resuelto— **cómo se eligen**.

**Clasificación:** `[Libro 2, capítulo 5]` rejilla, tipografía y color · `[Libro 1, capítulo 7]` los límites de
accesibilidad · `[Extensión G5]` el método de elección.

---

## Índice

1. [Qué es un fundamento](#11--qué-es-un-fundamento)
2. [La rejilla](#12--la-rejilla)
3. [Tipografía](#13--tipografía)
4. [Color](#14--color)
5. [Espaciado](#15--espaciado)
6. [Forma](#16--forma)
7. [Elevación](#17--elevación)
8. [Iconografía](#18--iconografía)
9. [El método de elección](#19--el-método-de-elección)
10. [Reglas de esta sección](#110--reglas-de-esta-sección)

---

## 1.1 · Qué es un fundamento

**Un fundamento es una decisión que se toma una vez y condiciona todas las demás.** No es un componente ni un
token: es el **criterio** del que salen los tokens.

```
FUNDAMENTO   "la escala de espaciado es de base 8"      ← se decide una vez
     ↓
TOKEN        spacing.2 = 8px  ·  spacing.3 = 16px       ← se deriva
     ↓
COMPONENTE   el botón lleva spacing.3 de relleno        ← se aplica
```

**El libro 2 lo plantea como el punto en que el diseño deja de ser intuitivo** `[Libro 2, capítulo 5]`:

> *"A partir de este capítulo, tus marcos, colores, fuentes y espaciados **ya no pueden ser arbitrarios**. Cada
> elemento necesita seguir una lógica de diseño clara, porque a medida que el proyecto crece, mantener la
> consistencia te ahorrará tiempo, reducirá errores y hará tu trabajo más fácil de mantener."*

---

## 1.2 · La rejilla

*Fuente: `[Libro 2, capítulo 5]`*

**La rejilla ordena el eje horizontal.** Es invisible para el usuario y es lo que hace que dos pantallas
distintas se sientan del mismo producto.

### Los cuatro parámetros

| Parámetro | Qué controla |
|---|---|
| **Cantidad** | Cuántas columnas |
| **Tipo** | `Stretch` se estira con el marco · `Center` se centra en un ancho fijo · `Left` / `Right` se anclan |
| **Margen** | El aire contra el borde de la pantalla |
| **Canal** *(gutter)* | El aire entre columnas |

### Lo único que el libro fija

**`[Libro 2, capítulo 8]`** — en escritorio el problema se invierte: *"puedes encontrarte con demasiado espacio y no
suficiente contenido para llenarlo"*. De ahí sale la única cifra que el libro da como valor concreto:

> **Contenedor fijo de 1200 px con tipo `Center`** para las vistas de escritorio que no necesitan ancho
> completo.

### La rejilla · la decide el producto

**No se fija acá, y no es una omisión.** Las columnas, el margen y el canal de cada punto de corte **se
deciden con el método de §1.9**, junto con el resto de la identidad, y se registran entonces.

> **Por qué se delega:** la rejilla de móvil depende de qué densidad de contenido pide el producto, y eso
> sale de las personas y del análisis de competencia — no de una cifra copiada.

> **Truco del libro:** los campos numéricos de Figma aceptan operaciones. Se puede escribir `1200/12 - 24`
> directamente en el ancho de columna.

### La rejilla se guarda como estilo

**OBLIGATORIO** — la rejilla no se configura marco por marco: se crea **una vez como estilo** y se aplica.
Cambiarla después es editar el estilo, y todos los marcos se actualizan `[Libro 2, capítulo 5]`.

---

## 1.3 · Tipografía

*Fuente: `[Libro 2, capítulo 5]` · `[Libro 1, capítulo 7]`*

**El libro 2 la llama el componente más subestimado por los principiantes**, y la razón es que no es estética:
*"es cuestión de usabilidad, jerarquía, coherencia de marca y legibilidad"*.

### Los tres comportamientos del texto

| Modo | Cómo se crea | Cuándo |
|---|---|---|
| **Ancho automático** | Un clic con la herramienta de texto | Etiquetas y botones — **crece con el contenido** |
| **Alto automático** | Arrastrar, y cambiar el alto a automático | Párrafos y contenido variable |
| **Tamaño fijo** | Arrastrar | **Casi nunca.** El texto se corta si crece |

**OBLIGATORIO** — ninguna etiqueta traducible usa tamaño fijo. Ver `04-auto-layout` y la expansión entre
idiomas `[Libro 1, capítulo 3]`.

### Los límites que impone la accesibilidad

*Fuente: `[Libro 1, capítulo 7]`*

**No son recomendaciones: son el piso.**

| Qué | Valor | Por qué |
|---|---|---|
| **Tamaño del cuerpo** | **16 px mínimo** | Y tiene que seguir legible al ampliar al 200 % |
| **Interlineado del cuerpo** | **entre 1.4 y 1.6** | *"Interlineados más apretados dificultan la lectura, sobre todo con dislexia o dificultades de procesamiento visual"* |
| **Familia** | Que se mantenga clara en tamaños pequeños | **Sin tipografías decorativas para texto corrido.** Las de palo seco suelen funcionar mejor en pantalla |
| **Espacio entre párrafos** | Suficiente | Los bloques densos son más difíciles de recorrer |

### Tipografías del sistema operativo

`[Libro 2, capítulo 5]` — si la aplicación es solo para una plataforma, conviene su tipografía nativa:

| Plataforma | Palo seco | Serif |
|---|---|---|
| **iOS** | San Francisco | New York |
| **Android** | Roboto | — |

> **No aplica si el producto es multiplataforma y comparte identidad entre plataformas.** En ese caso la
> tipografía nativa se descarta y la elección se resuelve en §1.9.

### Tipografías variables

`[Libro 2, capítulo 5]` — un solo archivo con todos los pesos, ajustables de forma continua. Ventajas: flexibilidad,
consistencia entre puntos de corte, y **soporte de accesibilidad** (poder afinar el peso mejora la legibilidad).

**RECOMENDADO, con una advertencia del propio libro:** si el proyecto usa **solo uno o dos pesos**, una
tipografía estática puede pesar menos.

### El nombre lleva la jerarquía

**OBLIGATORIO** — los estilos de texto se nombran con barra, porque **la barra crea grupos** `[Libro 2, capítulo 5]`:

```
Title/Large      Title/Medium      Title/Small
Body/Regular     Body/Bold         Body/Caption
```

---

## 1.4 · Color

*Fuente: `[Libro 2, capítulo 5]`*

> *"El color no es neutro: **cada tono carga su propio peso psicológico y sus asociaciones culturales**.
> Elegir la paleta correcta ayuda a comunicar el tono, priorizar la información y sostener la accesibilidad."*

### Los cuatro modelos, y para qué sirve cada uno

| Modelo | Cuándo se usa |
|---|---|
| **HEX** | El formato de intercambio. Es el que va al token |
| **RGB** | Cuando hace falta el canal exacto |
| **HSL** · **HSB** | **Para construir escalas.** Permiten mover luminosidad manteniendo el tono |

**RECOMENDADO** — las escalas de un mismo color (100, 200, 300…) se construyen en HSL y se guardan en HEX.

### El contraste se comprueba al definir el color, no después

`[Libro 1, capítulo 7]` — **este es el punto donde el libro es más insistente**:

> *"Cuando implementas los estándares WCAG directamente en tus tokens, **resuelves los problemas de
> accesibilidad en su origen**, y eliminas la necesidad de volver a revisarlos y arreglarlos después."*

**Figma trae el comprobador incorporado en el propio panel de color** `[Libro 2, capítulo 5]`: muestra AA o AAA en
tiempo real mientras se ajusta el color.

**OBLIGATORIO** — ningún par de color texto/fondo entra al sistema sin haber pasado por ahí. El detalle, en
`06-accessibility`.

> **Sobre el futuro:** existe **APCA**, que predice la legibilidad con más precisión que WCAG 2.1 —sobre todo
> en colores intermedios— pero **la norma que las regulaciones citan hoy sigue siendo WCAG 2.1 AA**
> `[Libro 1, capítulo 7]`. Se diseña contra WCAG; APCA sirve para desempatar.

---

## 1.5 · Espaciado

**`[Libro 2, índice]` el libro trabaja sobre un sistema de 8 puntos**, y `[Libro 1, capítulo 6]` observa que
*"normalmente 4 a 6 valores cubren la mayoría de los casos"*.

### Lo que el libro fija

**La base es 8**, y `[Libro 1, capítulo 6]` acota el tamaño de la escala: *"normalmente 4 a 6 valores cubren la
mayoría de los casos"*.

### La escala · la decide el producto

**Los pasos concretos se deciden con el método de §1.9.** Lo que ya es obligatorio es la forma:

**OBLIGATORIO** — la escala tiene **base 8**, **entre cuatro y seis pasos principales**, y **ningún valor de
espaciado queda fuera de ella**.

> **Es la regla que más se viola sin darse cuenta.** Un sistema sin escala declarada acumula decenas de
> espaciados distintos en unas pocas pantallas, cada uno elegido a ojo — y ninguno se puede tokenizar
> después sin rehacer las pantallas.

> **Por qué formalizarlo como token y no como convención** `[Libro 2, capítulo 13]`: *"Aunque este enfoque es
> efectivo, **depende mucho de la memoria**, y es fácil introducir inconsistencias con el tiempo."*

---

## 1.6 · Forma

**El radio de esquina es una decisión de fundamento, no de componente.** Debe crecer con la superficie: cuanto
mayor el elemento, mayor el radio, o la pieza grande se ve más dura que la chica.

### La escala · la decide el producto

**Los valores se deciden con el método de §1.9.** Lo que sí es regla, y no depende de la identidad:

**OBLIGATORIO** — la escala tiene **un paso por tamaño de superficie** —pieza pequeña, control, tarjeta,
contenedor— y **crece de forma monótona**. Un sistema donde la tarjeta tiene menos radio que el botón está mal
construido.

**OBLIGATORIO** `[Extensión]` — **el radio completo se reserva a lo que no es un control**: avatar, marcador de mapa,
punto de parada, indicador circular.

> **Por qué:** un botón con radio completo y un avatar redondo **compiten por el mismo significado**. Si todo
> es redondo, la forma deja de comunicar qué es tocable.

---

## 1.7 · Elevación

`[Libro 2, capítulo 3]` — y es la frase que ordena toda esta sección:

> *"Los efectos incorporados de Figma están limitados a propósito: **solo incluyen lo que se puede implementar
> de forma realista en código**."*

**OBLIGATORIO** — la elevación se expresa **solo** con sombra difusa: posición, desenfoque, expansión y color
con transparencia. Nada de desenfoques, mezclas ni filtros para separar planos.

### Cuántos niveles

**RECOMENDADO** — **tres**, uno por grado de separación: lo que apenas se despega, lo que es una tarjeta, y lo
que flota sobre el contenido. Un cuarto casi nunca se distingue del tercero.

**Los valores concretos se deciden con el método de §1.9.**

---

## 1.8 · Iconografía

*Fuente: `[Libro 1, capítulo 8]`*

**Los iconos son el único fundamento que se exporta como archivo**, y por eso tienen reglas técnicas propias.

### Cómo se construyen

| Hacer | Evitar |
|---|---|
| Rectángulos, círculos y polígonos como bloques | Ilustraciones con muchos detalles pequeños |
| Formas complejas **combinando simples** | Trazos superpuestos múltiples |
| Geometría sistemática | Elementos decorativos que no sirven al propósito |

**OBLIGATORIO — se combinan los trazados, no se agrupan.** Con `Union`, `Subtract`, `Intersect` o `Exclude`.

> **Por qué:** produce trazados únicos y limpios en lugar de capas superpuestas, **reduce drásticamente la
> complejidad del SVG exportado** y mejora el rendimiento en todos los navegadores.

### Lo que no puede llevar un icono

Sombras, desenfoques, degradados —sobre todo radiales—, máscaras y recortes. **Generan código
significativamente más complejo y problemas de compatibilidad entre navegadores.**

### La prueba de calidad

**OBLIGATORIO** — antes de dar por bueno un icono, exportarlo y abrir el SVG en un editor de texto.

| Señal de alarma | Icono sano |
|---|---|
| Más de unos pocos kilobytes para un icono simple | **Menos de 2 kilobytes** |
| Cientos de líneas para algo sencillo | Estructura legible |
| Presencia de `<mask>`, `<filter>` o `<clipPath>` | Pocos `<path>` con coordenadas simples |
| Varias secciones `<defs>` con degradados | Sin efectos |

---

## 1.9 · El método de elección

*Fuente: `[Extensión G5]`*

**Este apartado existe porque los dos libros dan por hecho que el color y la tipografía ya se decidieron.**
El libro 2 enseña a *aplicar* una paleta; ninguno enseña a *elegirla*.

> **El vacío, con su evidencia:** `[Libro 2, capítulo 5]` dice *"antes de entrar al diseño de interfaz es
> imprescindible tener al menos una idea aproximada de la dirección de color, o mejor aún, **datos o
> directrices de marca** que informen tus decisiones"*. **Y ahí se detiene.** Da los insumos, no el
> procedimiento.

### Los insumos, que sí vienen del libro

`[Libro 2, capítulo 2]` — se producen antes de abrir un archivo de diseño:

| Insumo | Qué es |
|---|---|
| **Declaración de propósito** | Una descripción corta y afirmativa de para qué existe el producto |
| **Análisis de competencia** | Qué hacen los productos parecidos, qué funciona y **qué hueco dejan** |
| **Personas** | Nombre, demografía, hábitos, necesidades y frustraciones |
| **Moodboard** | Materiales reales: fotografía, señales de marca, patrones de interfaz |

### El procedimiento

*Fuente: `[Extensión]`*

**Cinco pasos, del encargo a la paleta.**

**1 · Traducir el propósito a tres adjetivos.** No más de tres, y que se puedan contradecir entre sí. Son la
vara con la que después se descarta.

**2 · Elegir el número de acentos.** Y la respuesta por omisión es **uno**.

> **La regla:** si el acento aparece dos veces en la misma pantalla, **una de las dos no era la acción
> principal**. Un segundo color solo se justifica cuando codifica un significado que el usuario debe
> aprender —origen contra destino, por ejemplo—, no para dar variedad.

**3 · Fijar el acento contra la competencia, no contra el gusto.** El análisis de competencia dice qué colores
ya están ocupados en esa categoría y en ese mercado. Copiarlos gana reconocimiento inmediato y pierde
distinción; alejarse hace lo contrario. **Es una decisión de negocio y se registra como tal.**

**4 · Derivar el resto del acento, no elegirlo aparte.**

| Rol | Cómo sale |
|---|---|
| **Presionado** | El acento, más oscuro |
| **Tenue** | El acento, muy desaturado — fondos de opción elegida |
| **Grises** | **Neutros, sin tinte**, salvo decisión explícita de teñirlos hacia el acento |
| **Confirmación, error, aviso** | Del convenio cultural del mercado, **no del acento** |

**5 · Comprobar el contraste antes de guardar nada.** Cada par texto/fondo, en el comprobador de Figma. **El
que no pasa AA no entra al sistema** — se ajusta la luminosidad hasta que pase.

### La comprobación final: los tres adjetivos

**Se vuelve al paso 1 y se pregunta si la paleta los sostiene.** Si los adjetivos eran *sobrio, confiable,
rápido* y la paleta tiene cinco colores saturados, **la paleta está mal, no los adjetivos**.

---

## 1.10 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-F01`** | La rejilla se guarda como estilo y se aplica; **nunca se configura marco por marco** | OBLIGATORIO | `[Libro 2, capítulo 5]` |
| **`DS-F02`** | **Ningún texto traducible usa tamaño fijo** | OBLIGATORIO | `[Libro 1, capítulo 3]` |
| **`DS-F03`** | El cuerpo de texto **no baja de 16 px**, con interlineado entre **1.4 y 1.6** | OBLIGATORIO | `[Libro 1, capítulo 7]` |
| **`DS-F04`** | Los estilos de texto se nombran con barra, para que agrupen | OBLIGATORIO | `[Libro 2, capítulo 5]` |
| **`DS-F05`** | **Ningún par texto/fondo entra al sistema sin pasar el comprobador de contraste** | OBLIGATORIO | `[Libro 1, capítulo 7]` |
| **`DS-F06`** | **Ningún valor de espaciado fuera de la escala** de base 4 | OBLIGATORIO | `[Libro 2, capítulo 5]` · `[Extensión]` |
| **`DS-F07`** | El radio completo se reserva a lo que **no es un control** | OBLIGATORIO | `[Extensión]` |
| **`DS-F08`** | La elevación se expresa **solo con sombra difusa**; nada de desenfoques ni mezclas | OBLIGATORIO | `[Libro 2, capítulo 3]` |
| **`DS-F09`** | Los iconos **combinan trazados**, no agrupan formas | OBLIGATORIO | `[Libro 1, capítulo 8]` |
| **`DS-F10`** | Un icono exportado **no supera 2 kilobytes** ni contiene `<mask>`, `<filter>` o `<clipPath>` | OBLIGATORIO | `[Libro 1, capítulo 8]` |
| **`DS-F11`** | **Un solo color de acento**, salvo que el segundo codifique un significado que el usuario deba aprender | RECOMENDADO | `[Extensión]` |
| **`DS-F12`** | Las escalas de color se construyen en HSL y se guardan en HEX | RECOMENDADO | `[Libro 2, capítulo 5]` |
