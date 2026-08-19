# Tokens · los tres niveles

**Un token es un valor con nombre.** El sistema entero se apoya en que ese nombre diga **qué papel cumple**,
no qué valor tiene.

---

## Índice

1. [La escalera](#la-escalera)
2. [El error más caro, y por qué es tan común](#el-error-más-caro-y-por-qué-es-tan-común)
3. [Los cuatro errores que el libro nombra](#los-cuatro-errores-que-el-libro-nombra)
4. [Los modos](#los-modos)
5. [El alcance, que casi nadie configura](#el-alcance-que-casi-nadie-configura)
6. [Un nombre por plataforma](#un-nombre-por-plataforma)
7. [El orden de construcción](#el-orden-de-construcción)
8. [Qué se escribe a mano y qué se deriva](#qué-se-escribe-a-mano-y-qué-se-deriva)
9. [Cómo se derivan las escalas](#cómo-se-derivan-las-escalas)

---

## La escalera

`[Libro 1, capítulo 6]` la presenta así, y conviene leerla de arriba abajo:

```
#007BFF                      ¿dónde se usa esto?  Nadie lo sabe
color/blue/500               es un azul, nivel 500                 ← nivel 1
color/background/default     es el fondo, en su estado normal      ← nivel 2
button/primary/background    es el fondo del botón primario        ← nivel 3
```

> *"Si los desarrolladores implementan `button/primary/background` y más adelante cambias el valor al que
> apunta, **no necesitan modificar ni una línea**. Cambiar un color en cientos de componentes requiere
> actualizar **una sola línea**."*

| Nivel | Se llama por | Ejemplo | Quién lo cita |
|---|---|---|---|
| **1 · primitivo** | **lo que ES** | `indigo.600 = #3A45C9` | **Solo el nivel 2** |
| **2 · semántico** | **lo que HACE** | `accion.reposo → {indigo.600}` | El nivel 3 |
| **3 · componente** | **dónde se APLICA** | `boton.primario.fondo → {accion.reposo}` | **Las pantallas** |

---

## El error más caro, y por qué es tan común

**Llamar `acento` a un primitivo.**

Parece práctico: el color de la marca se llama «acento», que es lo que uno diría en voz alta. Y ahí el sistema
se rompe en silencio:

```
✗   acento = #3A45C9              el primitivo ya se llama por su rol
    boton.fondo → {acento}        el nivel 2 no aporta nada … y se salta
    chip.borde  → {acento}        ahora dos piezas sin relación comparten variable
```

**Cuando el nivel 2 no aporta nada, nadie lo escribe.** Y sin nivel 2 **no hay dónde poner los modos**: el
modo oscuro no cambia el primitivo, cambia **qué primitivo usa cada rol**.

```
✓   indigo.600 = #3A45C9                             qué ES
    accion.reposo   claro → {indigo.600}             qué HACE, por modo
                    oscuro → {indigo.400}
    boton.primario.fondo → {accion.reposo}           dónde se APLICA
```

> **La prueba de que el nivel 2 existe de verdad:** cambiar el acento en `marca.json`, volver a derivar, y que
> **ningún archivo de componente cambie**.

---

## Los cuatro errores que el libro nombra

`[Libro 1, capítulo 6]`, textual:

| Error | Qué es | Cómo se ve |
|---|---|---|
| **Sobre-tokenizar** | Tokens para valores usados una sola vez | Cien tokens, ochenta con un solo uso |
| **Sub-tokenizar** | **Usar el primitivo directamente en vez de crear el semántico** | Un componente cita `indigo.600` |
| **Nomenclatura inconsistente** | Mezclar convenios | `accion-reposo` junto a `accionReposo` |
| **Demasiadas variaciones** | *"Crear 15 variantes de botón cuando solo necesitas 3"* | Nadie sabe cuál usar |

**Contra el primero, el umbral de DS-T08:** un valor merece token cuando aparece **en tres o más lugares**.
Con menos, es una decisión local.

---

## Los modos

**Viven en el nivel 2, y en ningún otro lado.**

```
                      claro           oscuro
superficie.base       gris.0          gris.900
texto.principal       gris.900        gris.50
accion.reposo         indigo.800      indigo.600
texto.sobre-accion    gris.0          gris.1000     ← se DA VUELTA
```

**Esa última fila es la que enseña.** En claro, el texto sobre el botón es blanco. En oscuro **el acento se
aclara**, así que el texto encima tiene que **oscurecerse**. Un sistema que solo invierte los grises falla
justo ahí — y falla en el botón principal, que es lo primero que se mira.

**Y ninguno de esos cuatro peldaños está cableado.** `accion.reposo` y `texto.sobre-accion` **se eligen por
contraste** contra el color de marca que entró: el primer peldaño cercano a la marca que sostenga texto —4.5:1—
y se despegue de la superficie —3:1—, con tinta o blanco encima, el que gane. Cablear «600 con blanco» da por
sentado que toda marca es oscura, y con una marca amarilla deja una sola salida: pedirle al usuario que
oscurezca su marca. **Sobre amarillo va texto negro.**

> **Por eso los modos se estructuran desde el primer día**, aunque solo uno esté activo. **Agregarlos después
> obliga a rehacer el nivel 2 entero**, y hasta entonces nadie ve el fallo.

**Además del claro y el oscuro**, un modo puede ser **alto contraste**, **densidad compacta** o **un idioma**
—para textos que crecen al traducirse, DS-F02—.

---

## El alcance, que casi nadie configura

`[Libro 2, capítulo 13]`:

> *"El alcance permite **ocultar completamente una variable** de la interfaz y de la publicación. **Esto evita
> que los primitivos se apliquen directamente** y garantiza que se usen exclusivamente como alias de tokens
> semánticos."*

**Es la diferencia entre un sistema que se recomienda y uno que no se puede evitar.** Sin alcance, DS-T02 es
un acuerdo de buena voluntad; con alcance, la herramienta no ofrece el primitivo.

Y se acota también **por tipo de propiedad** —DS-X07—: `texto.principal` no debe aparecer al elegir un fondo.

---

## Un nombre por plataforma

`[Libro 1, capítulo 8]` — **una variable, tres nombres**, para que nadie los invente:

| | |
|---|---|
| web | `--accion-reposo` |
| iOS | `accionReposo` |
| Android | `accion_reposo` |

`construir.py` los emite juntos en `figma-variables.json`.

---

## El orden de construcción

**Color → espaciado → tipografía** — DS-T06.

No es capricho: la tipografía necesita saber sobre qué fondo se lee **para comprobar contraste**, y el
espaciado necesita la escala antes de que alguien elija un valor a ojo.

---

## Qué se escribe a mano y qué se deriva

| Archivo | Se escribe | Se genera |
|---|---|---|
| `marca.json` | **Sí** — es el único origen visual | |
| `proyecto.json` | **Sí** — lo único atado al producto | |
| `inventario/componentes.json` | **Sí** — el contrato | |
| `tokens/1-primitivos.json` | | **`derivar.py`** |
| `tokens/2-semanticos.json` | | **`derivar.py`** |
| `tokens/3-componentes.json` | | **`derivar.py`**, desde el inventario |
| `outputs/*` | | **`construir.py`** |

> **Todo lo generado lleva `_generado_por` adentro**, y `verificar.py` comprueba que esté — DS-T01. Es lo que
> delata un archivo editado a mano, que es un cambio que se va a perder.

---

## Cómo se derivan las escalas

**De un parámetro salen decenas de valores.** Es lo que hace que cambiar la marca sea barato.

| De | Sale |
|---|---|
| `identidad.acento` | **12 peldaños**, interpolados en claridad **percibida**, anclados en el peldaño que le toca al color por lo claro que se ve — el 800 para un indigo, el 200 para un amarillo. **El color entra tal cual y no se modifica nunca** |
| `grises.tinte` | La escala neutra, teñida con el **tono** del acento — nunca con su claridad |
| `estados.*` | Un trío por estado: texto, fondo y borde |
| `espaciado.base` + pasos | La escala de medidas |
| `tipografia.base` + `razon` | Los tamaños: `base × razón^paso` |
| `forma.*` | Los radios, comprobados **monótonos** — la tarjeta nunca menos que el botón |

**La saturación se amortigua en los extremos claros.** Sin eso, los peldaños 50 y 100 salen chillones y no
sirven de fondo.

**Y todo peldaño que participe de un par de contraste se comprueba al derivarlo**, en **todos los modos**,
incluidos los preparados y todavía inactivos. `[Libro 1, capítulo 7]`:

> *"Cuando implementas los estándares WCAG **directamente en tus tokens**, resuelves los problemas de
> accesibilidad **en su origen**, y eliminas la necesidad de volver a revisarlos y arreglarlos después."*
