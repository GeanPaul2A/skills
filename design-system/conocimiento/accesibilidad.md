# Accesibilidad · el piso, no la meta

> *"La accesibilidad **no es binaria — es una escala**. No se trata de 'la tenemos' o 'no la tenemos', sino de
> qué tan a fondo la abordamos."* `[B1, cap. 7]`

**El nivel objetivo es WCAG 2.1 AA**, y AAA en lo crítico — DS-A01.

---

## La idea que cambia todo: resolverlo en el token

> *"Cuando implementas los estándares WCAG **directamente en tus tokens**, resuelves los problemas de
> accesibilidad **en su origen**, y eliminas la necesidad de volver a revisarlos y arreglarlos después."*
> `[B1, cap. 7]`

**Por eso `derivar.py` comprueba contraste al derivar y no al final.** Un color que no cumple **no llega a ser
token**: se oscurece hasta cumplir, y el ajuste se reporta.

**La alternativa —comprobar al final— siempre llega tarde:** para entonces el color ya está en cincuenta
pantallas.

---

## Contraste

| Qué | Mínimo | Dónde aplica |
|---|---|---|
| Texto normal | **4.5:1** | Todo texto bajo 24px, o bajo 19px en negrita |
| Texto grande | 3:1 | 24px o más |
| **Foco y elementos no textuales** | **3:1** | Anillos de foco, bordes que informan, iconos con significado |
| Decorativo | — | Lo que no comunica nada |

**Se mide en todos los modos, incluidos los preparados y todavía inactivos.**

> **El par que más falla, y el que nadie mira:** `texto.sobre-accion` en modo oscuro. En claro el texto sobre
> el botón es blanco; en oscuro **el acento se aclara** y ese blanco deja de cumplir. **Hay que darlo vuelta.**
>
> Un sistema que solo invierte los grises falla justo ahí — y falla en el botón principal.

### Cuando un par no llega, se declara

Un par que **no puede** cumplir se documenta con **por qué es aceptable**, y la compensación es obligatoria:

> El borde de un mensaje de aviso puede quedar bajo 3:1 **si el estado se identifica además por icono y por
> color de texto** — lo que obliga a que **todo mensaje lleve icono**, y eso pasa a ser regla, no sugerencia.

**Una excepción sin su compensación escrita no es una excepción: es un incumplimiento.**

---

## El color nunca va solo · DS-A03

**Ninguna información se comunica solo con color.** Siempre hay un segundo portador:

| Qué se comunica | Color | **Y además** |
|---|---|---|
| Error en un campo | Borde rojo | **Texto que dice qué pasó** |
| Éxito | Verde | **Icono de confirmación** |
| Estado en una lista | Punto de color | **La palabra del estado** |
| Elemento elegido | Fondo teñido | **Marca visible o borde grueso** |

**Es la regla que más se incumple sin querer**, y la que más gente deja afuera: uno de cada doce hombres no
distingue rojo de verde.

---

## Texto

| Regla | Valor |
|---|---|
| Tamaño mínimo del cuerpo | **16 px** — no se baja, ni por densidad |
| Interlineado del **texto corrido** | **1.4 – 1.6** |
| Interlineado de titulares | Más ajustado. Un titular a 1.5 se desarma |
| **Zoom** | Toda pantalla se revisa **al 200 %** — DS-A08 |
| **Idioma** | Ningún texto traducible con tamaño fijo — DS-F02 |

### La expansión al traducir · DS-F02

`[B1, cap. 3]`:

| Español | Alemán | Húngaro |
|---|---|---|
| Login | Anmelden | Bejelentkezés |
| Aceptar todo | Alle akzeptieren | Összes elfogadása |

**El alemán puede ser un 30 % más largo; el chino, mucho más corto** `[B1, cap. 8]`.

> **Un contenedor de tamaño fijo revienta al cambiar de idioma. Uno que abraza su contenido, no.**
> Por eso DS-L03 prohíbe el tamaño fijo en el eje del texto.

---

## Estructura y lectores de pantalla

| # | Regla |
|---|---|
| **DS-A04** | Todo campo lleva **etiqueta persistente**. El texto de marcador **nunca** hace de etiqueta: desaparece al escribir |
| **DS-A05** | **Un solo H1 por pantalla**, y la jerarquía baja sin saltarse niveles |
| **DS-A06** | Todo icono con significado lleva **texto alternativo de su función** — «cerrar», no «equis» |
| **DS-A10** | Los cambios que ocurren solos se anuncian con **región en vivo**: un mensaje de error, un contador, un estado que llega |

> **DS-A06, el matiz:** el alternativo describe **qué hace**, no qué se ve. Un icono decorativo se marca como
> decorativo, para que el lector lo salte.

---

## Teclado y foco · DS-A07

**Lo que se puede con ratón se puede con teclado.**

```
□  el orden de foco sigue al orden visual … o la divergencia está documentada
□  el foco se ve siempre, con 3:1
□  nada queda inalcanzable
□  Esc cierra lo que interrumpe
□  en una superposición, el foco queda ATRAPADO adentro
□  al cerrar, el foco vuelve al elemento que la abrió
□  lo de atrás queda oculto al lector de pantalla
```

**La divergencia legítima existe.** Una pantalla con una superficie continua de fondo —mapa, lienzo, visor—
la pone primero en el documento y última en importancia: el foco entra a la hoja de contenido y la superficie
queda al final. **Eso se escribe en la plantilla**, y el verificador exige la explicación.

---

## Movimiento · DS-A09

**Todo movimiento tiene alternativa reducida.** `construir.py` la emite sola en el CSS:

```css
@media (prefers-reduced-motion: reduce) { … }
```

Y toda animación se entrega con **sus cinco datos** — DS-H05 `[B1, cap. 8]`: **esencial o de adorno · tiempo ·
curva · disparador · rendimiento**.

> *"Prefiere siempre `transform` antes que las propiedades de posición: usa aceleración por hardware y no
> dispara recálculos de disposición. La diferencia de rendimiento es dramática, **especialmente en
> móviles**."* — DS-H06

---

## Tacto

| Contexto | Mínimo |
|---|---|
| General | **44 px** |
| **Uso en movimiento** — de pie, manejando, con guantes, al sol | **más**, y se declara por actor |

**El área táctil puede ser mayor que lo que se ve.** Un icono de 24 px vive dentro de un objetivo de 44.

---

## Criterios de aceptación, por componente

**Lo que hay que poder decir que sí antes de cerrar cada uno.**

| Componente | Criterios |
|---|---|
| **Botón** | Foco visible 3:1 · objetivo ≥ mínimo · `cargando` no deja al usuario sin saber si lo escucharon · deshabilitado **explica por qué** o no se usa |
| **Campo** | Etiqueta persistente · error **con texto**, no solo borde rojo · el error se anuncia · `autocomplete` donde corresponda |
| **Casillas de código** | Se pega el código completo de una vez · cada casilla es alcanzable · el foco avanza solo pero **se puede retroceder** |
| **Desplegable** | Se abre y se recorre con teclado · Esc cierra · la opción elegida se anuncia |
| **Segmentado** | Flechas para moverse · el elegido **no se distingue solo por color** |
| **Opción / casilla** | La etiqueta es parte del área táctil · el estado se lee, no solo se ve |
| **Tarjeta elegible** | Es un control, no un adorno: **foco, teclado y estado anunciado** |
| **Mensaje** | **Lleva icono siempre** — es la compensación de DS-A03 · el urgente se anuncia solo |
| **Diálogo / hoja** | Foco atrapado · Esc cierra · el foco vuelve al origen · el fondo se oculta al lector |
| **Barra inferior** | Objetivo ≥ mínimo · el activo se distingue **además del color** · dice qué sección es |
| **Vacío** | Explica **por qué** está vacío y **qué hacer** |
| **Esqueleto** | Se anuncia como «cargando» · respeta movimiento reducido |

---

## Lo que ninguna herramienta detecta

**Y por eso queda en revisión humana** — DS-A11:

- Si el texto alternativo **dice la función** o describe la forma.
- Si el orden de foco **tiene sentido**, no solo si existe.
- Si el mensaje de error **explica cómo salir** del problema.
- Si la pantalla se puede usar **en un teléfono de gama baja**, al sol, con una mano.

> `[B1, cap. 8]`, sobre su propio marco de gobierno: *"deberían automatizarse mediante marcos de prueba"*. **Lo
> que se puede automatizar, está automatizado. Lo que no, está escrito acá para que alguien lo mire.**
