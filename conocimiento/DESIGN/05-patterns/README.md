# 05 · Patterns (Patrones)

**Un patrón es una secuencia de componentes con un propósito — y con su origen de datos declarado.** Es la
sección donde el modelo de dominio entra al diseño, y la que impide dibujar pantallas que no se pueden
construir.

**Clasificación:** `[Extensión G2]` la atadura al dominio · `[Extensión G4]` los patrones de superficie continua ·
`[Libro 2, capítulos 4 y 9]` el contenido antes que la maqueta, y los estados de interacción.

> **Esta sección define un método, no un catálogo de negocio.** Los patrones concretos de un producto
> —lo que vende, lo que cobra, lo que reserva— **viven en su capa de dominio**. Acá está cómo se declaran y
> qué tiene que cumplir cualquiera de ellos.

---

## Índice

1. [Qué es un patrón](#51--qué-es-un-patrón)
2. [El vacío que esta sección llena](#52--el-vacío-que-esta-sección-llena)
3. [Cómo se declara un patrón](#53--cómo-se-declara-un-patrón)
4. [Los patrones universales](#54--los-patrones-universales)
5. [Los patrones de superficie continua](#55--los-patrones-de-superficie-continua)
6. [El camino feliz no alcanza](#56--el-camino-feliz-no-alcanza)
7. [Reglas de esta sección](#57--reglas-de-esta-sección)

---

## 5.1 · Qué es un patrón

**Está un nivel por encima del componente y uno por debajo de la pantalla** `[Libro 1, capítulo 5]`:

```
PRIMITIVOS     el color de acento, el 8 de la escala
COMPONENTES    el botón, el campo, la tarjeta
PATRONES       ← acá.  "listar y filtrar" = campo de búsqueda + filtros + lista + vacío
PLANTILLAS     "pantalla de lista" = barra arriba, lista al centro, acción flotante
```

**La diferencia con un componente:** un componente es una pieza; **un patrón es una decisión de flujo**. El
botón no sabe para qué se toca. El patrón sí.

---

## 5.2 · El vacío que esta sección llena

**Ninguno de los dos libros conecta el diseño con el origen de los datos.** Enseñan a construir una tarjeta;
nunca a decir de qué tabla sale lo que muestra.

### Y el libro 2 nombra el problema sin resolverlo

*Fuente: `[Libro 2, capítulo 4]`*

> *"Antes de saltar a los bocetos, da un paso atrás y hazte una pregunta clave: **¿sé qué contenido va a
> incluir realmente este producto?**"*
>
> *"Las interfaces no son solo disposiciones visuales, son **contenedores construidos alrededor de contenido
> específico**. Uno de los errores más comunes del diseño de interfaz es empezar por la maqueta antes de tener
> siquiera una idea aproximada de qué datos necesita mostrar el producto. Cuando eso pasa, se rellenan las
> pantallas con texto de relleno y con estructura e información que no reflejan el producto real. **Ese enfoque
> puede producir maquetas limpias y elegantes que se desarman en cuanto entran los datos de verdad.**"*

**Su recomendación se queda en pedir una muestra:** *"siempre que sea posible, intenta conseguir al menos un
conjunto de datos de ejemplo o contenido realista de los interesados"*.

### `[Extensión]` — cuando existe un modelo de dominio declarado, se puede exigir más

**Un producto con su modelo escrito** —entidades, tablas, columnas y reglas de negocio numeradas— **no
necesita conseguir una muestra: ya tiene la fuente.**

**Entonces la extensión es directa:** en vez de *"conseguir contenido realista"*, cada patrón **declara su
dominio, sus tablas y las reglas que lo condicionan**. Deja de ser una buena práctica y pasa a ser
verificable — un guion puede comprobar que cada dato en pantalla tiene una columna detrás.

> **El precio de no tenerlo se paga siempre igual.** Es habitual que las primeras pantallas de un producto
> muestren variantes, categorías o estados **que no existen en el modelo**: se ven bien y no se pueden
> construir. Es exactamente lo que el libro describe, y la única defensa es atar el patrón a las tablas
> antes de dibujar.

---

## 5.3 · Cómo se declara un patrón

**OBLIGATORIO** — todo patrón vive en `inventario/patrones.json` con estos ocho campos:

```json
"listar-y-filtrar": {
  "proposito":   "El usuario encuentra un elemento entre muchos",
  "actor":       "<actor>",
  "dominio":     "<dominio principal>",
  "tablas":      ["<entidad>", "<entidad_estado>"],
  "lee_tambien": ["<otro_dominio>.<entidad>"],
  "reglas":      ["<R-nn>", "<R-nn>"],
  "componentes": ["campo-busqueda", "chip", "tarjeta", "estado-vacio"],
  "estados":     ["cargando", "con-resultados", "sin-resultados", "error-de-consulta"]
}
```

### Qué obliga cada campo

| Campo | Qué impide |
|---|---|
| **`dominio` y `tablas`** | Inventar un dato que no existe |
| **`lee_tambien`** | Olvidar que ese nombre o esa calificación **vienen de otro servicio** y pueden tardar o faltar |
| **`reglas`** | Diseñar algo que el modelo prohíbe |
| **`estados`** | Entregar solo el camino feliz |

### El campo `lee_tambien` no es burocracia

**`[Extensión]`** — en una arquitectura de una base de datos por dominio, **lo que viene de otro servicio puede no
llegar**. Si una tarjeta muestra un dato que produce otro dominio y ese dominio no responde, la pantalla
tiene que saber qué hacer.

> **Y el caso que más se equivoca es la distinción entre «cero» y «todavía ninguno».** Un elemento recién
> creado no tiene calificaciones, ni ventas, ni historial. La pantalla **no puede mostrar cero** — no es que
> le haya ido mal, es que aún no hay dato. Muestra *"Nuevo"*, o el equivalente. **Ese comportamiento es
> parte del patrón**, no un detalle del componente que lo dibuja.

---

## 5.4 · Los patrones universales

**Casi todo producto digital tiene estos seis, cualquiera sea su negocio.** Son el punto de partida; el
detalle de cada uno se escribe en el inventario, y el dominio agrega los suyos.

| Patrón | Propósito |
|---|---|
| **Acceder** | Entrar o registrarse, y salir |
| **Listar y filtrar** | Encontrar un elemento entre muchos |
| **Ver detalle** | Todo lo de un elemento, y qué se puede hacer con él |
| **Crear y editar** | Componer o corregir un elemento, con validación |
| **Confirmar una acción irreversible** | Advertir **antes**, con lo que se pierde dicho |
| **Esperar un proceso** | Lo que el sistema hace y el usuario no controla |

### Dónde termina un patrón y empieza el siguiente

**Donde el modelo cambia de estado.** No donde la pantalla cambia de aspecto.

> **La consecuencia práctica:** dos momentos que el usuario vive como uno solo son **dos patrones** si entre
> ellos la entidad avanzó de estado. Y al revés: tres pantallas seguidas que no mueven el modelo son **un
> solo patrón** repartido en pasos. Si el campo `<entidad>_status` avanza, es otro patrón.

---

## 5.5 · Los patrones de superficie continua

*Fuente: `[Extensión G4]`*

**Los libros no cubren nada de esto.** El libro 2 enseña interfaz móvil de listas, formularios y contenido;
ninguno trata una superficie continua no textual.

**Una superficie continua es la que el usuario lee mirando, no leyendo:** un mapa, un lienzo de dibujo, la
vista de una cámara, un visor 3D, una línea de tiempo, una partitura. **Cuando el producto tiene una, suele
ser la mitad de la aplicación** — y hay cuatro piezas que hay que definir desde cero:

| Pieza | Qué resuelve |
|---|---|
| **Hoja sobre la superficie** | La proporción entre superficie y contenido, y qué pasa al desplazar |
| **Marcador** | El punto de interés sobre la superficie. Su forma **no es la de un control** — ver `DS-F07` |
| **Trazo o recorrido** | La relación entre dos puntos, y cómo se distingue lo hecho de lo pendiente |
| **Actualización en vivo** | Lo que se mueve solo, y **qué se muestra cuando deja de actualizarse** |

> **Estas cuatro son estructura, no negocio.** La instancia concreta —qué representa el marcador, qué mide
> el trazo— **vive en el dominio del producto**, declarada con `"universal": false` y con su motivo escrito.
> Así el sistema se lleva a otro producto sin arrastrar lo que allá no sirve.

### La regla que las gobierna

**OBLIGATORIO `[Extensión]`** — **ninguna superficie continua no textual es el único portador de una información
necesaria.** Todo lo que la superficie comunica —dónde está algo, cuánto falta, por dónde va— **tiene además
una forma textual**.

> **Dos razones:** el lector de pantalla no puede leer una superficie continua `[Libro 1, capítulo 7]`, y esa
> superficie **es lo primero que falla** cuando la conexión es mala o el dispositivo es lento.

---

## 5.6 · El camino feliz no alcanza

**`[Libro 1, capítulo 8]` lo pone en su lista de calidad** — *"¿están implementados correctamente los estados de
carga? ¿están los estados de error bien diseñados y funcionales?"* — y `[Libro 2, capítulo 9]` da el marco para
enumerarlos:

> Un flujo debe mostrar claramente: **puntos de entrada** · **puntos de decisión** · **estados de éxito** ·
> **manejo de errores** · **puntos de salida**.

### Aplicado a los patrones universales

**OBLIGATORIO** — todo patrón enumera sus estados, y **al menos uno tiene que ser un fallo**.

| Patrón | Un estado que es fácil olvidar |
|---|---|
| Acceder | **La credencial venció**, o se acabaron los intentos |
| Listar y filtrar | **El filtro no devolvió nada** — que no es lo mismo que la lista vacía de origen |
| Ver detalle | **El elemento cambió o desapareció** mientras lo estabas mirando |
| Crear y editar | **Otro usuario lo editó primero**, y guardar pisaría su cambio |
| Confirmar una acción irreversible | **La acción ya no se puede deshacer, y hay que advertirlo antes** |
| Esperar un proceso | **El proceso dejó de responder** sin haber terminado ni fallado |

> **Ninguno sale de la imaginación: salen del modelo.** Cada uno corresponde a una transición de estado o a
> una regla de dominio ya escrita. Si un estado de fallo no se puede rastrear hasta una regla, o sobra o
> falta la regla.

---

## 5.7 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-P01`** | Todo patrón declara **dominio, tablas y reglas** en el inventario | OBLIGATORIO | `[Extensión G2]` |
| **`DS-P02`** | **Ningún dato se muestra sin una columna que lo respalde** | OBLIGATORIO | `[Libro 2, capítulo 4]` · `[Extensión G2]` |
| **`DS-P03`** | Todo patrón enumera sus estados, y **al menos uno es un fallo** | OBLIGATORIO | `[Libro 1, capítulo 8]` · `[Libro 2, capítulo 9]` |
| **`DS-P04`** | Lo que viene de otro dominio declara **qué se muestra si no llega** | OBLIGATORIO | `[Extensión G2]` |
| **`DS-P05`** | **Ninguna superficie continua no textual es el único portador** de una información necesaria | OBLIGATORIO | `[Extensión G4]` · `[Libro 1, capítulo 7]` |
| **`DS-P06`** | Un patrón termina donde el modelo **cambia de estado** | RECOMENDADO | `[Extensión]` |
