# Doctrina · las reglas del sistema

**76 reglas con su procedencia.** Sesenta salen enteras de la bibliografía; ocho son extensión pura, y esas
llevan escrito el vacío que las justifica.

| Etiqueta | Origen |
|---|---|
| `[B1]` | *Design Beyond Limits with Figma* — Simon Jun. **El libro del sistema** |
| `[B2]` | *Designing and Prototyping Interfaces with Figma, 3.ª ed.* **El libro del oficio** |
| `[Ext]` | **Extensión.** Llena un vacío que los libros dejan. Nunca se le atribuye a un libro una regla que no contiene |

**Columna «verifica»:** `auto` la comprueba un guion · `semi` necesita renderizar o leer la herramienta de
diseño · `manual` requiere criterio · `—` es una declaración, no una comprobación.

---

## Las seis frases que gobiernan todo

**Si hay que recordar solo seis cosas, son estas.**

> **1 ·** *"Recuerda que construyes sistemas de diseño para **acelerar todo el proceso —el desarrollo en
> particular—**, no para tener archivos bonitos de Figma."* `[B1, cap. 5]`

> **2 ·** *"Nuestro diseñador dedicó **mucho más tiempo a crear la estructura de fundamentos y los tokens que
> a crear los componentes**. Puede parecer que avanzas lento al principio, pero tener una base sólida hace que
> todo lo demás sea mucho más fácil y rápido después."* `[B1, cap. 5]`

> **3 ·** *"El código más preciso se genera cuando el diseño usa **Auto Layout**, porque corresponde
> directamente al sistema Flexbox. **Si no se usa, Figma sugiere coordenadas absolutas**, lo que lleva a
> interfaces no responsivas y trabajo extra."* `[B2, cap. 11]`

> **4 ·** *"Uno de los errores más comunes es **empezar por la maqueta antes de tener idea de qué datos
> necesita mostrar el producto**. Ese enfoque produce maquetas limpias y elegantes **que se desarman en cuanto
> entran los datos de verdad**."* `[B2, cap. 4]`

> **5 ·** *"Cuando implementas los estándares WCAG **directamente en tus tokens**, resuelves los problemas de
> accesibilidad **en su origen**, y eliminas la necesidad de volver a revisarlos y arreglarlos después."*
> `[B1, cap. 7]`

> **6 ·** *"La accesibilidad **no es binaria — es una escala**. No se trata de 'la tenemos' o 'no la tenemos',
> sino de qué tan a fondo la abordamos."* `[B1, cap. 7]`

---

## Los seis vacíos que los libros dejan

**Cada extensión nace de uno de estos**, detectado leyendo — no importado de un proyecto.

| # | Vacío | Evidencia | Qué lo llena |
|---|---|---|---|
| **G1** | **No dicen cómo verificar** que un diseño respeta el sistema. Todo el control es humano | `[B1, cap. 5]` el gobierno son reuniones y métricas de desvinculación · `[B2, cap. 12]` *Design Lint* se corre a mano · `[B1, cap. 8]` su propio revisor admite que *"deberían automatizarse mediante marcos de prueba"* | `verificar.py` y las reglas numeradas |
| **G2** | **No conectan el diseño con el origen de los datos** | `[B2, cap. 4]` nombra el problema y **solo recomienda conseguir contenido de ejemplo** | Los patrones declaran dominio, entidades y reglas |
| **G3** | **No definen contrato legible por máquina** de los componentes | `[B1, cap. 5]` las propiedades son símbolos de la interfaz de Figma, no datos | El inventario en JSON |
| **G4** | **No cubren las superficies continuas no textuales** — mapa, lienzo, cámara, visor 3D, línea de tiempo | `[B2]` cubre listas, formularios y contenido; ninguna superficie continua aparece | Componentes y plantilla propios, marcados como no universales |
| **G5** | **Dan por sentada la identidad de marca** | `[B2, cap. 5]` *"es esencial tener al menos una idea de la dirección de color"* — y ahí se detiene | La entrevista, con propuestas renderizadas |
| **G6** | **No tratan el multi-idioma como estructura** | `[B1, cap. 3]` la expansión de texto se trata como problema de maqueta | Los textos como tokens con un modo por idioma |

---

## `DS-F` · Fundamentos

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-F01** | La rejilla se guarda como estilo; nunca se configura marco por marco | OBL | semi | `[B2·5]` |
| **DS-F02** | **Ningún texto traducible usa tamaño fijo** | OBL | semi | `[B1·3]` |
| **DS-F03** | Cuerpo **≥ 16 px**, interlineado entre **1.4 y 1.6** | OBL | auto | `[B1·7]` |
| **DS-F04** | Los estilos de texto se nombran con barra, para que agrupen | OBL | auto | `[B2·5]` |
| **DS-F05** | **Ningún par texto/fondo entra sin pasar el comprobador de contraste** | OBL | auto | `[B1·7]` |
| **DS-F06** | Ningún valor de espaciado fuera de la escala | OBL | auto | `[B2·5]` `[Ext]` |
| **DS-F07** | **El radio completo se reserva a lo que no es un control** | OBL | auto | `[Ext]` |
| **DS-F08** | La elevación se expresa **solo con sombra difusa** | OBL | auto | `[B2·3]` |
| **DS-F09** | Los iconos **combinan trazados**, no agrupan formas | OBL | semi | `[B1·8]` |
| **DS-F10** | Un icono **no supera 2 KB** ni lleva `<mask>`, `<filter>` o `<clipPath>` | OBL | semi | `[B1·8]` |
| **DS-F11** | **Un solo acento**, salvo que el segundo codifique significado | REC | manual | `[Ext]` |
| **DS-F12** | Las escalas de color se construyen en HSL y se guardan en HEX | REC | manual | `[B2·5]` |

> **DS-F07 · por qué.** Un botón con radio completo y un avatar redondo **compiten por el mismo significado**. Si
> todo es redondo, la forma deja de comunicar qué es tocable.
>
> **DS-F08 · por qué** `[B2, cap. 3]`: *"Los efectos incorporados de Figma están limitados a propósito: **solo
> incluyen lo que se puede implementar de forma realista en código**."*

---

## `DS-T` · Tokens

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-T01** | Los tokens viven en **JSON versionado**; CSS y variables son **salidas generadas** | OBL | auto | `[B1·6]` `[Ext]` |
| **DS-T02** | **Tres niveles. Un componente nunca referencia un primitivo** | OBL | auto | `[B1·6]` |
| **DS-T03** | Los primitivos van **ocultos de publicación y sin alcance** | OBL | semi | `[B2·13]` |
| **DS-T04** | Un solo convenio de nombres en todo el sistema | OBL | auto | `[B1·6]` |
| **DS-T05** | Toda variable publicada declara su **sintaxis por plataforma** | OBL | semi | `[B1·8]` |
| **DS-T06** | El orden de construcción es **color → espaciado → tipografía** | OBL | manual | `[B1·6]` |
| **DS-T07** | **Ningún valor en crudo en una pantalla** | OBL | auto | `[Ext G1]` |
| **DS-T08** | Un valor merece token si aparece en **tres o más lugares** | REC | auto | `[B1·6]` |
| **DS-T09** | El peso tipográfico se guarda como **número**, no como nombre | REC | auto | `[B2·13]` |
| **DS-T10** | Los estilos apuntan a variables semánticas — **estilo como API pública, variable como lógica interna** | REC | semi | `[B2·13]` |

### La escalera que explica DS-T02 `[B1, cap. 6]`

```
#007BFF                      ¿dónde se usa esto?  Nadie lo sabe
color/blue/500               es un azul, nivel 500
color/background/default     es el fondo, en su estado normal
button/primary/background    es el fondo del botón primario
```

> *"Si los desarrolladores implementan `button/primary/background` y más adelante cambias el valor al que
> apunta, **no necesitan modificar ni una línea**. Cambiar un color en cientos de componentes requiere
> actualizar **una sola línea**."*

### Los cuatro errores que el libro nombra `[B1, cap. 6]`

| Error | Qué es |
|---|---|
| **Sobre-tokenizar** | Tokens para valores usados una sola vez |
| **Sub-tokenizar** | **Usar el primitivo directamente en vez de crear el semántico** |
| **Nomenclatura inconsistente** | Mezclar convenios dentro del mismo sistema |
| **Demasiadas variaciones** | *"Crear 15 variantes de botón cuando solo necesitas 3"* |

### El alcance, que casi nadie configura `[B2, cap. 13]`

> *"El alcance permite **ocultar completamente una variable** de la interfaz y de la publicación. **Esto evita
> que los primitivos se apliquen directamente** y garantiza que se usen exclusivamente como alias de tokens
> semánticos."*

**Es la diferencia entre un sistema que se recomienda y uno que no se puede evitar.**

---

## `DS-C` · Componentes

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-C01** | Ningún componente entra **sin su entrada en el inventario** | OBL | auto | `[Ext G3]` |
| **DS-C02** | **Todo elemento interactivo declara su estado de foco**, con 3:1 | OBL | auto | `[B1·7]` |
| **DS-C03** | Lo que depende de una respuesta declara **carga, vacío y error** | OBL | auto | `[B1·8]` `[Ext]` |
| **DS-C04** | Los auxiliares se prefijan con **punto** y no se publican | OBL | auto | `[B2·7]` |
| **DS-C05** | Cada componente lleva **descripción: cuándo usarlo y cuándo no** | OBL | auto | `[B2·11]` |
| **DS-C06** | La jerarquía va en **páginas y marcos**, no en nombres largos | OBL | semi | `[B2·7]` |
| **DS-C07** | **Fundamentos y componentes no comparten archivo** | OBL | semi | `[B1·5]` |
| **DS-C08** | **Desvincular una instancia es la última salida** | REC | semi | `[B1·5]` |
| **DS-C09** | Se agrupa como variantes solo lo que **difiere de forma predecible y limitada** | REC | manual | `[B2·7]` |
| **DS-C10** | El estado `hover` **no se declara para móvil** | REC | auto | `[B2·8]` |

### La arquitectura de cuatro niveles `[B1, cap. 5]`

**El libro presenta dos y prefiere la segunda:**

| Atomic Design | La alternativa ← **esta** |
|---|---|
| Atoms | **PRIMITIVOS** — tokens y fundamentos |
| Molecules | **COMPONENTES** — elementos sueltos |
| Organisms | **PATRONES** — combinaciones con propósito |
| Templates | **PLANTILLAS** — estructura de pantalla |
| Pages | *(no se usa)* |

> *"Elimina la confusión de la terminología átomos/moléculas y crea distinciones más claras."*

### DS-C08 es una señal medible `[B1, cap. 5]`

> *"Si ves un número grande de componentes desvinculados, **tienes un problema**. Quizá te falta una variante
> — eso debería ser una señal para repriorizar tu hoja de ruta."*

---

## `DS-L` · Disposición

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-L01** | **Todo contenedor usa Auto Layout** | OBL | semi | `[B2·11]` |
| **DS-L02** | Espacio y relleno **salen de la escala** | OBL | auto | `[B2·6]` |
| **DS-L03** | **Ningún contenedor de texto usa tamaño fijo** en el eje del texto | OBL | semi | `[B1·3]` |
| **DS-L04** | La estructura se construye con **marcos**, no con grupos | OBL | semi | `[B2·3]` |
| **DS-L05** | Se diseña **móvil primero** y se escala hacia arriba | OBL | manual | `[B2·8]` |
| **DS-L06** | Toda pantalla se prueba con los **valores más largos y más cortos** | OBL | auto | `[B2·4]` `[Ext G2]` |
| **DS-L07** | Se construye **de adentro hacia afuera** | REC | manual | `[B2·6]` |
| **DS-L08** | La restricción **Escala** se reserva a lo decorativo | REC | semi | `[B2·6]` |
| **DS-L09** | Los elementos que llenan declaran **mínimo y máximo** | REC | semi | `[B2·13]` |
| **DS-L10** | Las diferencias entre dispositivos se resuelven con **variables booleanas**, no con archivos paralelos | REC | semi | `[B2·13]` |

### El vocabulario compartido `[B1, cap. 1]`

| Figma | Código |
|---|---|
| **Auto Layout** | **Flexbox** |
| Corner radius | `border-radius` |
| Frames | `div` |
| Variables / tokens | Variables CSS |

### La expansión del texto `[B1, cap. 3]`

| Español | Alemán | Húngaro |
|---|---|---|
| Login | Anmelden | Bejelentkezés |
| Aceptar todo | Alle akzeptieren | Összes elfogadása |

**Y la magnitud** `[B1, cap. 8]`: el alemán puede ser **un 30 % más largo**; el chino, mucho más corto.

> **Un contenedor de tamaño fijo revienta al cambiar de idioma. Uno que abraza su contenido, no.**

---

## `DS-P` · Patrones

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-P01** | Todo patrón declara **dominio, entidades y reglas** | OBL | auto | `[Ext G2]` |
| **DS-P02** | **Ningún dato se muestra sin un campo que lo respalde** | OBL | auto | `[B2·4]` `[Ext G2]` |
| **DS-P03** | Todo patrón enumera sus estados, y **al menos uno es un fallo** | OBL | auto | `[B1·8]` `[B2·9]` |
| **DS-P04** | Lo que viene de otra fuente declara **qué se muestra si no llega** | OBL | auto | `[Ext G2]` |
| **DS-P05** | **Ninguna superficie continua no textual es el único portador** de información necesaria | OBL | manual | `[Ext G4]` `[B1·7]` |
| **DS-P06** | Un patrón termina donde el modelo **cambia de estado** | REC | manual | `[Ext]` |

### Los cinco momentos de un flujo `[B2, cap. 9]`

**Puntos de entrada · puntos de decisión · estados de éxito · manejo de errores · puntos de salida.**

Si falta el cuarto, el patrón está incompleto — por eso `DS-P03`.

---

## `DS-A` · Accesibilidad

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-A01** | El nivel objetivo es **WCAG 2.1 AA**; AAA en lo crítico | OBL | — | `[B1·7]` |
| **DS-A02** | Texto **4.5:1**, foco **3:1**, comprobado **al definir el token** | OBL | auto | `[B1·7]` |
| **DS-A03** | **Ninguna información se comunica solo con color** | OBL | manual | `[B1·7]` |
| **DS-A04** | Todo campo lleva **etiqueta persistente**; el marcador nunca hace de etiqueta | OBL | auto | `[B1·7]` |
| **DS-A05** | **Un solo H1 por pantalla**, con jerarquía descendente | OBL | auto | `[B1·7]` |
| **DS-A06** | Todo icono con significado lleva **texto alternativo de función** | OBL | auto | `[B1·7]` |
| **DS-A07** | Lo que se puede con ratón **se puede con teclado**, con foco visible | OBL | auto | `[B1·7]` |
| **DS-A08** | Toda pantalla se revisa **al 200 % de texto** | OBL | semi | `[B1·7]` |
| **DS-A09** | Todo movimiento tiene **alternativa reducida** | OBL | auto | `[B1·7]` |
| **DS-A10** | Los cambios dinámicos se anuncian con **región en vivo** | OBL | auto | `[B1·7]` |
| **DS-A11** | El diseño se revisa en **un dispositivo de gama baja** | REC | manual | `[B1·7]` |
| **DS-A12** | Comprobación automatizada en la tubería cuando exista la aplicación | REC | — | `[B1·7]` |

**El detalle y los criterios de aceptación por componente, en `accesibilidad.md`.**

---

## `DS-H` · Entrega

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-H01** | El archivo de producto sigue una **estructura fija de páginas** | OBL | semi | `[B1·4]` |
| **DS-H02** | Capas y recursos siguen el **convenio de los tokens** | OBL | semi | `[B1·8]` |
| **DS-H03** | El nombre de un componente **deriva del concepto que representa** | OBL | auto | `[B1·4]` `[Ext G2]` |
| **DS-H04** | Iconos en **SVG**; fotografías en **WebP o AVIF** | OBL | semi | `[B1·8]` |
| **DS-H05** | Toda animación se entrega con sus **cinco datos** | OBL | semi | `[B1·8]` |
| **DS-H06** | El movimiento se anima con **`transform`**, nunca con posición | OBL | semi | `[B1·8]` |
| **DS-H07** | Versión manual **al cerrar un ciclo** | REC | manual | `[B1·1]` |
| **DS-H08** | **Nada se borra**: lo descartado va al archivo | REC | manual | `[B1·4]` |

### La analogía que explica DS-H01 `[B1, cap. 4]`

> *"Imagina un supermercado donde todo está al azar. Al lado de la leche hay manzanas, y el jugo de manzana
> está del otro lado junto a los zapatos. **Si tú construiste esa tienda, te parecería bien.** Los
> desarrolladores son los compradores nuevos."*

### Los cinco datos de una animación `[B1, cap. 8]`

**Esencial o de adorno · tiempo · curva · disparador · rendimiento.**

> *"Prefiere siempre `transform` antes que las propiedades de posición: usa aceleración por hardware y no
> dispara recálculos de disposición. La diferencia de rendimiento es dramática, **especialmente en móviles**."*

---

## `DS-X` · Puente con la herramienta de diseño

| # | Regla | Nivel | Verifica | Origen |
|---|---|---|---|---|
| **DS-X01** | La fuente de verdad es el **JSON**; la herramienta de diseño es una salida | OBL | auto | `[B1·6]` `[Ext]` |
| **DS-X02** | Los primitivos van **ocultos y sin alcance** | OBL | semi | `[B2·13]` |
| **DS-X03** | Toda variable publicada declara **sintaxis para las tres plataformas** | OBL | semi | `[B1·8]` |
| **DS-X04** | Los estilos apuntan a **variables semánticas**, nunca a valores fijos | OBL | semi | `[B2·13]` |
| **DS-X05** | Peso como **número**; familia como **cadena exacta** | OBL | auto | `[B2·13]` |
| **DS-X06** | **Ninguna etapa depende de que un agente escriba en el lienzo** | OBL | manual | `[Ext]` |
| **DS-X07** | El alcance se acota también **por tipo de propiedad** | REC | semi | `[B2·13]` |
| **DS-X08** | Un complemento no se adopta sin pasar el **árbol de decisión** | REC | manual | `[B1·2]` |

### Por qué DS-X01 `[B1, cap. 6]`

Las variables de la herramienta **no tienen control de versiones propio**, **solo admiten cuatro tipos** —sin
tokens compuestos— y **hacen falta complementos de terceros** para exportarlas a código.

> Y el argumento de fondo: *"Cuando empecé a usar Figma escuchaba: 'todo el mundo diseña en Photoshop, Figma
> nunca va a funcionar'. Eso no envejeció bien. **Hoy es un gigante, pero esa posición puede cambiar.**"*

### El árbol de decisión de DS-X08 `[B1, cap. 2]`

**¿soy el único usuario? · ¿es de un solo uso? · ¿es de pago? · ¿lo hace una empresa? · ¿hay alternativas?**

Y una señal concreta: *"si no se ha actualizado en más de dos años, conviene ser cauteloso"*.

---

## El recuento

| Área | Reglas | Obligatorias | `auto` |
|---|---|---|---|
| `F` Fundamentos | 12 | 10 | 6 |
| `T` Tokens | 10 | 7 | 6 |
| `C` Componentes | 10 | 7 | 6 |
| `L` Disposición | 10 | 6 | 2 |
| `P` Patrones | 6 | 5 | 4 |
| `A` Accesibilidad | 12 | 10 | 7 |
| `H` Entrega | 8 | 6 | 1 |
| `X` Puente | 8 | 6 | 2 |
| **Total** | **76** | **57** | **34** |

**Las 34 `auto` son exactamente las 34 que tienen comprobación escrita y probada.** No es una
coincidencia: la columna se reconcilia contra el código, no al revés. Si no coinciden, una de las dos miente.

### Por qué seis dejaron de ser `auto`

`DS-F02` · `DS-F09` · `DS-F10` · `DS-H04` · `DS-H05` · `DS-H06`. Ninguna se puede comprobar desde los artefactos que la tubería
posee: **cuatro necesitan los archivos de icono o de imagen**, que el sistema no versiona, y **dos necesitan un
modelo de movimiento** que `marca.json` todavía no declara.

> **Bajarlas es la corrección honesta, no una rebaja.** Estaban marcadas `auto` sin comprobación: prometían un
> control que nadie ejercía. Vuelven a `auto` el día que exista de qué leerlas — un `movimiento` en `marca.json`
> devuelve `DS-H05` y `DS-H06`; una carpeta de iconos versionada devuelve `DS-F09`, `DS-F10` y `DS-H04`.

**Son 76 reglas, una por cada fila de las ocho tablas.** Si una sección agrega una y este recuento sigue en
76, falta registrarla.

### Las ocho de extensión pura

`DS-F07` · `DS-F11` · `DS-T07` · `DS-C01` · `DS-P01` · `DS-P04` · `DS-P06` · `DS-X06` — **las únicas que no tienen respaldo directo
en la bibliografía**, y por eso cada una lleva su vacío escrito arriba.

---

## La regla sobre las reglas

**Ninguna se declara verificable antes de que su comprobación exista y se haya probado contra un error
inyectado a propósito.**

Una comprobación que nunca falló no está probada: está sin usar.

### Y se comprueba, no se promete

La columna «verifica» es la parte de esta doctrina que **más fácil se desalinea**: agregar una regla y marcarla
`auto` cuesta un renglón; escribir su comprobación, no. Por eso el invariante se mide:

```bash
# las reglas 'auto' de la doctrina, contra las comprobaciones que existen de verdad
grep -E '^\| \*\*DS-[A-Z][0-9]{2}\*\*.*\| auto \|' conocimiento/doctrina.md \
  | sed -E 's/^\| \*\*(DS-[A-Z][0-9]{2})\*\*.*/\1/' | sort -u > /tmp/a
grep -ohE 'R\("DS-[A-Z][0-9]{2}"' skills/*/scripts/verificar*.py | grep -oE 'DS-[A-Z][0-9]{2}' | sort -u > /tmp/b
diff /tmp/a /tmp/b && echo "reconciliado"
```

**Si `diff` imprime algo, una de las dos miente.** Una regla `auto` sin comprobación promete un control que
nadie ejerce; una comprobación sin regla `auto` hace trabajo que la doctrina no reconoce.
