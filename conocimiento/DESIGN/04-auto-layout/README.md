# 04 · Auto Layout

**Es lo que hace que un diseño se pueda convertir en código.** No es una comodidad de dibujo: es la diferencia
entre entregar una interfaz responsiva y entregar coordenadas absolutas.

**Clasificación:** `[Book 2, cap. 6]` la mecánica · `[Book 2, cap. 8]` puntos de corte y escalado ·
`[Book 2, cap. 11]` la correspondencia con código · `[Book 1, cap. 3]` la expansión del texto.

---

## Índice

1. [Auto Layout es Flexbox](#41--auto-layout-es-flexbox)
2. [Estático contra dinámico](#42--estático-contra-dinámico)
3. [Los parámetros](#43--los-parámetros)
4. [Hug, Fill y Fixed](#44--hug-fill-y-fixed)
5. [Las restricciones](#45--las-restricciones)
6. [Marco y grupo no son lo mismo](#46--marco-y-grupo-no-son-lo-mismo)
7. [Construir de adentro hacia afuera](#47--construir-de-adentro-hacia-afuera)
8. [Puntos de corte](#48--puntos-de-corte)
9. [La expansión del texto](#49--la-expansión-del-texto)
10. [Reglas de esta sección](#410--reglas-de-esta-sección)

---

## 4.1 · Auto Layout es Flexbox `[Book 2, cap. 11]`

**La cita que convierte esto en obligatorio y no en preferencia:**

> *"El código más preciso y eficiente se genera cuando tu diseño usa Auto Layout, ya que **corresponde
> directamente al sistema Flexbox** del desarrollo web. Esta relación **1 a 1** hace mucho más fácil que los
> desarrolladores recreen disposiciones responsivas que se comporten exactamente como las prototipaste. **Si no
> se usa Auto Layout, Figma sugiere en su lugar coordenadas absolutas para cada marco**, lo que a menudo lleva
> a interfaces no responsivas y trabajo extra durante el desarrollo."*

### El vocabulario compartido `[Book 1, cap. 1]`

**El libro trae la tabla de equivalencias, y sirve para hablar con quien programa:**

| Figma | Código |
|---|---|
| **Auto Layout** | **Flexbox** |
| Corner radius | `border-radius` |
| Frames | `div` |
| Variables / tokens de diseño | Variables CSS |
| Prototipos | Maquetas clicables |

**OBLIGATORIO** — todo contenedor de toda pantalla usa Auto Layout. **Sin excepciones que no estén
registradas.**

---

## 4.2 · Estático contra dinámico `[Book 2, cap. 6]`

**La rejilla y Auto Layout parecen resolver lo mismo. No es así:**

> *"Las rejillas son **estáticas**. Dan una base sólida para la consistencia, pero **no se adaptan cuando el
> contenido cambia**… Auto Layout, en cambio, es **dinámico**. Una vez que fijas sus reglas, Figma se encarga
> del resto, ajustando automáticamente la posición y el espaciado de los elementos según haga falta."*

| | Rejilla | Auto Layout |
|---|---|---|
| Ordena | El eje horizontal de la pantalla | **El interior de un bloque** |
| Ante contenido más largo | **Se rompe** | Se reacomoda |
| Equivale en código a | Un sistema de columnas | **Flexbox** |

**Los dos se usan a la vez.** La rejilla alinea los bloques; Auto Layout gobierna lo que pasa dentro de cada uno.

---

## 4.3 · Los parámetros `[Book 2, cap. 6]`

| Parámetro | Qué controla | En CSS |
|---|---|---|
| **Dirección** | Vertical, horizontal o con salto de línea | `flex-direction` · `flex-wrap` |
| **Espacio** *(gap)* | La separación **entre** hijos | `gap` |
| **Relleno** *(padding)* | El aire **dentro** del contenedor | `padding` |
| **Alineación** | Dónde se apoyan los hijos — nueve posiciones | `justify-content` · `align-items` |

**OBLIGATORIO** — el espacio y el relleno **salen de la escala de espaciado** (`DS-F06`). Nunca un número suelto.

> **Y una consecuencia que conviene tener presente** `[Book 2, cap. 6]`: *"una vez aplicado Auto Layout, **ya no
> puedes posicionar libremente los elementos internos** como harías en un grupo o marco normal."* Eso no es una
> limitación: es lo que garantiza que el bloque se comporte igual en código.

---

## 4.4 · Hug, Fill y Fixed `[Book 2, cap. 6]`

**Tres comportamientos, y elegir mal es la causa más común de que un diseño se rompa.**

| Modo | Qué hace | Cuándo se usa |
|---|---|---|
| **Hug** *(abraza el contenido)* | La caja **se encoge a lo que tiene adentro** | Botones, chips, distintivos — **todo lo que envuelve texto** |
| **Fill** *(llena el contenedor)* | La caja **ocupa lo que le den** | Campos, filas de lista, columnas de una tarjeta |
| **Fixed** *(fijo)* | Tamaño invariable | Avatares, iconos, miniaturas |

### Mínimos y máximos

**RECOMENDADO** — un elemento en `Fill` puede declarar **ancho mínimo y máximo**. Es lo que impide que una
tarjeta se vuelva ilegible en pantalla ancha o se aplaste en una angosta.

### La regla que se deriva

**OBLIGATORIO** — **ningún contenedor de texto usa `Fixed` en el eje del texto.** Si el texto crece —por
traducción, por un nombre largo, por una dirección larga— la caja tiene que crecer con él.

---

## 4.5 · Las restricciones `[Book 2, cap. 6]`

**Las restricciones dicen a qué borde se ancla un elemento cuando su contenedor cambia de tamaño.** Funcionan
junto a Auto Layout, no en su lugar.

| Restricción | Efecto |
|---|---|
| Arriba · Abajo · Izquierda · Derecha | Se ancla a ese borde |
| Centrado | Se mantiene centrado |
| **Escala** | **Se estira proporcionalmente** — se activa desactivando todas las demás |

**RECOMENDADO** — la escala se reserva a elementos decorativos. Un control que escala **deja de tener el tamaño
mínimo táctil**.

---

## 4.6 · Marco y grupo no son lo mismo `[Book 2, cap. 3]`

**Una diferencia que parece menor y decide el comportamiento:**

> *"Redimensionar el **grupo** también escala las formas de adentro, mientras que redimensionar el **marco**
> solo cambia las dimensiones del marco: **el contenido se queda en su sitio**. Esta diferencia se vuelve
> crucial al trabajar con disposiciones responsivas."*

**OBLIGATORIO** — la estructura de una pantalla se construye con **marcos**. Los grupos quedan para agrupar
temporalmente mientras se trabaja.

---

## 4.7 · Construir de adentro hacia afuera `[Book 2, cap. 6]`

**El método que el libro enseña, y que evita rehacer:**

> *"En lugar de abordar esto de arriba hacia abajo, **empezaremos desde adentro hacia afuera**, comenzando por
> elementos simples y autocontenidos. Este enfoque modular hará tu diseño más escalable y mejor preparado para
> el siguiente capítulo, donde empezarás a trabajar con componentes."*

```
1  el botón            ← se resuelve solo, con Hug
2  el grupo de botones ← los envuelve, con espacio
3  el formulario       ← envuelve campos y grupo de botones
4  la pantalla         ← envuelve todo
```

**Cada nivel es un Auto Layout que contiene al anterior.** Es literalmente el anidado de `div` que produce el
código.

---

## 4.8 · Puntos de corte `[Book 2, cap. 8]`

### Móvil primero, y por qué

> *"La mayoría de los marcos de desarrollo modernos están construidos con una mentalidad de móvil primero…
> **Es mucho más fácil escalar hacia arriba una disposición compacta y bien estructurada que reducir y
> reorganizar después una disposición compleja de escritorio.**"*

### Fluido contra encajonado

**En escritorio el problema se invierte:** sobra espacio y falta contenido. El libro da la solución y la cifra:

| Tipo de vista | Disposición |
|---|---|
| **Formularios y flujos cortos** — acceso, registro | **Encajonada** en un contenedor fijo de **1200 px**, centrado |
| **Vistas de contenido** — listas, detalle | **Fluida**, para aprovechar el ancho |

### Las variables de punto de corte `[Book 2, cap. 13]`

**El libro las convierte en una colección con un modo por dispositivo:**

```
Breakpoints        Escritorio   Tableta   Móvil
  width               1280        744      375
  height               832       1133      812
  minWidth             340        300      200
  maxWidth             430        400      400
  _showDesktop        True       False    False     ← booleanas, controlan visibilidad
  _showMobile        False        True     True
```

> **Las booleanas resuelven la navegación:** la barra inferior de pestañas existe en móvil y **no en
> escritorio**, donde la navegación se rehace `[Book 2, cap. 8]`. Con una variable booleana **es el mismo
> archivo cambiando de modo**, no dos diseños que hay que mantener sincronizados.

---

## 4.9 · La expansión del texto `[Book 1, cap. 3]`

**Es la razón por la que `Hug` no es opcional en un producto multi-país.** El libro trae la tabla:

| Español | Alemán | Húngaro |
|---|---|---|
| Login | Anmelden | Bejelentkezés |
| Aceptar todo | Alle akzeptieren | Összes elfogadása |

**Y la magnitud** `[Book 1, cap. 8]`: *"el texto alemán puede ser un 30 % más largo que el inglés"*, mientras
que *"el chino puede ser mucho más corto"*.

> **Un botón `Fixed` revienta al cambiar de idioma. Uno `Hug` no.** Ese es todo el tema.

**Y en cuanto el producto opera en más de un país deja de ser hipotético:** si moneda, país, zona horaria e
idioma son **dato y no código** en el modelo de datos, un sistema de diseño que solo funciona en un idioma
**contradice el modelo que ya está construido**.

### Probar con contenido real, no de relleno `[Book 2, cap. 4]`

> *"Uno de los errores más comunes del diseño de interfaces es **empezar por la maqueta antes de tener siquiera
> una idea aproximada de qué datos necesita mostrar el producto**… Ese enfoque puede producir maquetas limpias
> y elegantes **que se desarman en cuanto entran los datos de verdad**."*

**OBLIGATORIO** — toda pantalla se prueba con los valores más largos y más cortos que su tabla admite.

> **El caso típico:** un campo de texto libre —`<entidad>.<campo>`— declarado en el modelo con un límite alto,
> digamos **500 caracteres**. El valor corto cabe en cualquier diseño; el de 500 no. **La pantalla tiene que
> decir qué hace con el segundo** — truncar, envolver, o abrir un detalle. El límite lo da la columna, no el
> ojo del diseñador.

---

## 4.10 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-L01`** | **Todo contenedor usa Auto Layout.** Sin él, la entrega son coordenadas absolutas | OBLIGATORIO | `[Book 2, cap. 11]` |
| **`DS-L02`** | Espacio y relleno **salen de la escala de espaciado**; nunca un número suelto | OBLIGATORIO | `[Book 2, cap. 6]` · `DS-F06` |
| **`DS-L03`** | **Ningún contenedor de texto usa `Fixed`** en el eje del texto | OBLIGATORIO | `[Book 1, cap. 3]` |
| **`DS-L04`** | La estructura se construye con **marcos**, no con grupos | OBLIGATORIO | `[Book 2, cap. 3]` |
| **`DS-L05`** | Se diseña **móvil primero** y se escala hacia arriba | OBLIGATORIO | `[Book 2, cap. 8]` |
| **`DS-L06`** | Toda pantalla se prueba con los **valores más largos y más cortos** que su tabla admite | OBLIGATORIO | `[Book 2, cap. 4]` · `[Ext G2]` |
| **`DS-L07`** | Se construye **de adentro hacia afuera** | RECOMENDADO | `[Book 2, cap. 6]` |
| **`DS-L08`** | La restricción **Escala** se reserva a elementos decorativos | RECOMENDADO | `[Book 2, cap. 6]` |
| **`DS-L09`** | Los elementos en `Fill` declaran **ancho mínimo y máximo** | RECOMENDADO | `[Book 2, cap. 13]` |
| **`DS-L10`** | Las diferencias entre dispositivos se resuelven con **variables booleanas de visibilidad**, no con archivos paralelos | RECOMENDADO | `[Book 2, cap. 13]` |
