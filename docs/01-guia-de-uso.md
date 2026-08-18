# Guía de uso · de cero a un sistema entregable

**Para quien nunca usó este plugin.** Cada paso dice qué escribir, qué esperar y cómo saber que salió bien.

---

## Índice

1. [Instalar](#1--instalar)
2. [El orden, y por qué es ese](#2--el-orden-y-por-qué-es-ese)
3. [Paso a paso, la primera vez](#3--paso-a-paso-la-primera-vez)
4. [Cómo se agrega algo después](#4--cómo-se-agrega-algo-después)
5. [Las siete skills, en una tabla](#5--las-siete-skills-en-una-tabla)
6. [Cuando algo falla](#6--cuando-algo-falla)

---

## 1 · Instalar

Dentro de Claude Code:

```
/plugin marketplace add GeanPaul2A/skills
/plugin install design-system@geanpaul-design
```

Si el resumen dice `Run /reload-plugins to activate.`, corré eso.

**Comprobá que quedó bien** — esto tiene que pasar entero:

```bash
./pruebas/correr.sh
```

> Si te dice `La suite pasa entera`, el plugin está sano. Si no, no sigas: lo que falle acá va a fallar en tu
> sistema también.

---

## 2 · El orden, y por qué es ese

```
system-design  →  dominio  →  pantalla  →  probar  →  entregar  →  auditar
   lo visual       el negocio   las vistas   los límites  a desarrollo  el estado
```

**No es una sugerencia.** Cada paso necesita lo que dejó el anterior:

- Una **pantalla** sin sistema inventa colores y tamaños sueltos.
- Una **pantalla** sin dominio muestra campos que el producto no tiene.
- **Probar** sin pantallas declaradas no tiene qué probar.

> **La advertencia que el libro pone al principio y que conviene leer dos veces:** *«Nuestro diseñador dedicó
> mucho más tiempo a crear la estructura de fundamentos y los tokens que a crear los componentes. Puede parecer
> que avanzas lento al principio, pero **tener una base sólida hace que todo lo demás sea mucho más fácil y
> rápido después**.»*

---

## 3 · Paso a paso, la primera vez

### Paso 1 · Construir el sistema visual

En el chat, escribí algo así:

> «Quiero armar el sistema de diseño de mi producto.»

**Qué pasa:** se activa la skill `system-design` y **te entrevista**. Una pregunta por vez cuando la respuesta
condiciona la siguiente.

**Qué te va a preguntar** — y todo tiene valor por omisión, *«usá el que recomiendes»* es una respuesta válida
a cualquiera:

| Bloque | Ejemplo |
|---|---|
| Producto | Qué es, quién lo usa, en qué condiciones |
| **Plataformas** | `ios` · `android` · `web` · `desktop` — **elegí las que vas a diseñar de verdad** |
| Color | El acento. Si ya tenés uno, se usa el tuyo y se ajusta solo lo necesario para que cumpla contraste |
| Tipografía | La familia, o una recomendada |
| Escala | Espaciado, forma, elevación |
| Modos | Claro, oscuro, alto contraste |

**Qué te deja:**

```
marca.json          los parámetros — es lo ÚNICO que se escribe a mano
proyecto.json       el producto y sus plataformas
tokens/             los tres niveles, derivados
inventario/         22 componentes y 4 plantillas universales
outputs/galeria/    ← ABRÍ ESTO
```

**Cómo sabés que salió bien:** te muestra `outputs/galeria/index.html`. **Abrilo.** Ahí está tu paleta, tus
escalas, tu tipografía y cada componente con sus variantes y estados. Si eso se ve bien, el sistema está bien.

---

### Paso 2 · Definir el negocio

> «Ahora definí el dominio: es una tienda / una clínica / un banco.»

**Por qué existe este paso.** El sistema visual no sabe de tu negocio a propósito — eso es lo que te permite
llevártelo a otro producto. Las entidades, las reglas y los patrones propios viven acá.

**Y es lo que hace que una pantalla se pueda verificar:** cada dato visible se cruza contra una columna que lo
respalda. Sin dominio, la pantalla se entrega marcada como *no verificada contra datos*, y se dice en voz alta.

**Qué te deja:** `domains/<tipo>.json` y el modelo contra el que se cruza todo.

---

### Paso 3 · Diseñar una pantalla

> «Diseñá la pantalla de inicio de sesión.»

**Qué pasa, y es lo que más sorprende la primera vez: te pregunta por los datos antes de dibujar.**

> *«Uno de los errores más comunes es empezar por la maqueta antes de tener idea de qué datos necesita mostrar
> el producto. Ese enfoque produce maquetas limpias y elegantes **que se desarman en cuanto entran los datos de
> verdad**.»*

Te va a pedir: qué entidades aparecen, qué campos, qué reglas la gobiernan, qué viene de otra fuente y qué se
muestra si no llega, y **el valor más largo y el más corto de cada campo**.

**Qué te deja:** `screens/<nombre>.json` verificado, y el HTML para mirarlo.

---

### Paso 4 · Probar

> «Probá esa pantalla.»

Comprueba los cinco momentos, los cuatro estados, los extremos, el tamaño fijo en texto, un solo titular, el
recorrido por teclado y lo que rompe el zoom al 200 %.

**Y te dice qué NO puede comprobar.** Esa lista es tan importante como los verdes: son las cosas que tenés que
mirar vos.

---

### Paso 5 · Entregar

> «Prepará la entrega a desarrollo.»

Crea la estructura de páginas, instala los iconos del catálogo con el tamaño correcto por plataforma, comprueba
el contrato de animación y cierra la versión.

**Los iconos se instalan, no se buscan:**

```bash
python3 skills/deliver/scripts/icons.py --catalogo
python3 skills/deliver/scripts/icons.py --destino <tu-proyecto> --plataforma android --uso barra
```

> Para **iOS no descarga nada y te lo dice**: SF Symbols es de Apple y su licencia prohíbe redistribuirlos. El
> guion te dice qué glifo tomar desde Xcode.

---

### Paso 6 · Auditar

> «Auditá el sistema.»

Te da un score de 100 con la fórmula escrita, las tres acciones que más destraban, y **qué reglas de la base de
conocimiento no puede comprobar ninguna máquina** — para que las marques vos.

---

## 4 · Cómo se agrega algo después

**Nunca se rehace el sistema para agregar algo.**

| Qué querés | Qué decir | Qué se mueve |
|---|---|---|
| Un componente nuevo | «Agregá un componente X» | `inventario/` · **versión MENOR** |
| Modo oscuro | «Agregá modo oscuro» | `marca.json` → `modos` · **MENOR** |
| Un idioma | «Agregá inglés» | `proyecto.json` → `idiomas` · **MENOR** |
| Otra plataforma | «Agregá web» | `proyecto.json` → `plataformas` · **MENOR** |
| Cambiar el acento | «Cambiá el acento a verde» | `marca.json` · **MAYOR — cambia todo lo dibujado** |
| Una funcionalidad nueva | «Diseñá el portafolio» | Una **entrega** nueva, con su versión |

### El versionado, en una línea

**El sistema y las funcionalidades avanzan por separado.** El sistema lleva su versión en `marca.json`; cada
entrega lleva la suya **y declara contra qué versión del sistema se dibujó**.

```
E1 · Acceso        v1.0.0 · sistema v1.0.0     ✓
E2 · Portafolio    v1.0.0 · sistema v1.1.0     ✓
```

**Para qué sirve:** cuando el sistema salte a `v2.0.0`, esa columna te dice **qué pantallas hay que revisar** —
sin abrir ninguna.

> **La regla que resuelve las dudas:** si alguien que ya dibujó con la versión anterior **tiene que volver a
> mirar su pantalla**, es MAYOR. Si puede ignorar el cambio, es MENOR o PARCHE.

El ejemplo completo, momento a momento, en `skills/deliver/referencias/versionado.md`.

---

## 5 · Las siete skills, en una tabla

**No hace falta invocarlas por nombre**: se activan solas por lo que pedís. Los comandos existen para cuando
querés ser explícito.

| Skill | Qué hace | Comando |
|---|---|---|
| `system-design` | Tokens, componentes, plantillas, modos, publicación | `/design-system:create-system` |
| `domain` | Entidades, reglas, patrones y piezas del negocio | `:define-domain` |
| `screen` | Una pantalla o un flujo: plantilla + datos + estados | `:design-screen` |
| `test` | Momentos, estados, extremos, teclado, zoom | `:test-screen` |
| `deliver` | Estructura, recursos, animación, versión | `:deliver-system` |
| `audit` | Score, cobertura y las tres acciones | `:audit-system` |
| `document` | La ficha de una pieza: props, accesibilidad, código | `:document-piece` |

**Y un octavo comando, `:extend-system`**, que no es una skill propia: entra por `system-design` §Extender para
agregar un componente o un patrón que falta en el inventario.

---

## 6 · Cuando algo falla

### «Cero fallos o no se entrega»

**Es literal.** Si un verificador falla, el paso no se da por hecho. Cada fallo dice **qué regla incumple**
(`DS-xxx`) y dónde.

### Una comprobación «saltada» no es un verde

```
Saltadas — no son verdes, son preguntas sin hacer:
   DS-P02   los campos citados existen    proyecto.json declara 'modelo_de_datos.tipo': null
```

**Significa que la comprobación no pudo correr**, casi siempre porque falta algo antes. En ese ejemplo: no hay
dominio definido, así que nadie está comprobando que tus pantallas muestren datos que existen.

### Qué hacer cuando no entendés un fallo

Cada regla está escrita, con su origen, en `conocimiento/DESIGN/09-rules/README.md`. Buscá el número y vas a
encontrar qué dice y de dónde sale.

### Comprobar el plugin entero

```bash
./pruebas/correr.sh             # todo
./pruebas/correr.sh --rapido    # solo la corrida limpia
```

**Tres etapas:** el sistema de referencia pasa limpio · **cada comprobación detecta su propio error inyectado**
· ninguna regla `auto` queda sin comprobación.

> **Por qué la segunda etapa importa:** una comprobación que nunca falló no está probada — está sin usar. La
> suite rompe algo a propósito, una regla por vez, y exige que la comprobación correspondiente lo detecte.
