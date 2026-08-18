---
name: domain
description: Define el tipo de negocio de un producto — entidades, reglas de negocio, patrones de dominio y piezas propias — para que el sistema de diseño quede agnóstico y cada pantalla pueda comprobarse contra datos reales. Úsala SIEMPRE que el usuario quiera definir el negocio, el dominio, las entidades, las tablas, las reglas de negocio, los flujos propios de un sector, o cuando vaya a maquetar pantallas de un producto nuevo y no exista aún output/domains/<tipo>.json. Produce output/domains/<tipo>.json y complementa a system-design (que hace lo visual, no lo de negocio).
---

# Dominio

**El negocio, no la marca.** `system-design` construye el sistema visual desde parámetros; `domain` define el
tipo de negocio desde parámetros. Uno no sabe de taxis ni de banca; el otro **sí, y por eso existe**: para que
el núcleo no lo sepa.

**Sin dominio no hay pantalla verificable.** Una pantalla muestra datos; un dato necesita una entidad y un campo
que lo respalde — DS-P02. Eso lo declara el dominio.

---

## 1 · Lo que no se negocia

**1 · Se entrevista, no se asume.** Nunca se inventa una entidad, una regla ni un patrón. Si el usuario no lo
sabe, se le pregunta — y si no lo sabe, **se dice** que el dominio queda incompleto, no se disfraza.

**2 · Cada campo visible responde a una columna.** El patrón declara qué entidades lee, y cada dato de la
pantalla sale de un campo de esas entidades — DS-P02. Un dato sin campo es una pantalla que no se puede
construir.

**3 · Cada patrón declara entidades, reglas y estados.** Y al menos un estado es un fallo — DS-P01, DS-P03.

**4 · Lo de otra entidad declara qué pasa si no llega.** En una base de datos por dominio, el nombre o las
estrellas pueden faltar. El patrón dice qué se muestra entonces — DS-P04.

**5 · Solo lo propio entra al inventario como no-universal.** El marcador de mapa va con `"universal": false` y
**su motivo**. Lo universal (botón, campo, tarjeta) no se redeclara: ya existe.

---

## 2 · Cuándo se usa

| El usuario pide | Qué hacer |
|---|---|
| Definir el negocio de un producto nuevo | La entrevista → §3 · El procedimiento |
| Importar un negocio que ya tiene modelo formal | §4 · Importar, sin entrevista completa |
| Agregar un patrón o una entidad a un dominio existente | §5 · Extender |
| Revisar un dominio | Cruzar contra el formato de `${CLAUDE_PLUGIN_ROOT}/domains/_plantilla.json` y reportar |

---

## 3 · El procedimiento

> **Convención de salida — `output/`.** Todo lo que se genera va a `<destino>`, que es siempre
> `<proyecto>/output/`. Las carpetas del plugin (`${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`) son de
> **solo lectura**: nunca se escribe salida dentro de ellas.
>
> **Dos carpetas se llaman `domains/` y no son la misma.** El dominio que esta skill escribe va siempre a
> `<destino>/domains/<tipo>.json`. `${CLAUDE_PLUGIN_ROOT}/domains/_plantilla.json` es la **especificación del
> formato**, es del complemento y no se toca. Cuando acá se lee `domains/<tipo>.json` a secas, es el primero.

### Paso 1 · ¿Hay modelo formal?

**Antes de preguntar nada, mira `proyecto.json` → `modelo_de_datos.tipo`.**

| `tipo` | Qué hacer |
|---|---|
| `null` | **Entrevistar.** No hay modelo: las entidades y reglas se definen desde cero |
| algo — `sql-ddl`, `csv-cabecera`, `json-esquema` | **Importar** (§4): las entidades y reglas ya existen; se declara la capa que el diseño consulta |

### Paso 2 · Entrevistar

**Lee `${CLAUDE_SKILL_DIR}/referencias/entrevista.md` y sigue sus bloques.** No inventes preguntas ni saltes bloques. Igual que la
entrevista visual de `system-design`: **una pregunta por vez cuando condiciona la siguiente**, y **todo tiene
valor por omisión**.

> **Nunca pidas criterio de diseñador ni de modelador.** No preguntes "¿cómo normalizas tus entidades?" sin
> ofrecer ejemplos concretos. El usuario describe su negocio; el dominio se declara.

**Elegir los patrones — la IA propone, el usuario elige.** Después de identificar el tipo de negocio (Paso 1),
la IA propone los patrones que su análisis del sector encuentra, **más los adicionales que podrían
complementarlo**, y el usuario elige cuáles aplican:

> *"Para un delivery encuentro: seguimiento de pedido, validación OTP, pago en línea, búsqueda con filtros,
> calificación del repartidor… y como posibles complementos: cupones, suscripción, domicilios guardados.
> ¿Cuáles usás?"*

**El usuario es quien confirma.** Nunca se declara un patrón sin su confirmación — proponer candidatos no es
inventar, es ofrecer opciones (igual que la entrevista visual propone paletas). Si el usuario describe un
patrón propio que no está en la lista, se agrega igual: la lista es punto de partida, no un límite.

### Paso 3 · Escribir el dominio

```bash
output/domains/<tipo>.json      ← copia el formato de ${CLAUDE_PLUGIN_ROOT}/domains/_plantilla.json
```

Un archivo por negocio, con el formato de `_plantilla.json` (los `_lee` de cada campo son la especificación).
Los nombres en `kebab-case`, las entidades y campos en minúsculas.

### Paso 4 · Inyectar el dominio

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/inyectar.py --destino <destino> --domain <destino>/domains/<tipo>.json
```

Materializa los patrones en `inventario/patrones.json`, fusiona las piezas propias (con `"universal": false` y
su motivo) en el inventario, y genera `modelo/` (tablas y reglas) para que el verificador cruce DS-P02 y DS-P01
contra el dominio. Después se vuelve a derivar (el inventario cambió); la verificación queda en el Paso 5.

### Paso 5 · Verificar

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/system-design/scripts/verificar.py --destino <destino>
```

**Y el cruce que define a esta skill:** cada patrón del dominio cita entidades que existen en `entidades`, y
cada regla citada por un patrón existe en `reglas`. Eso lo comprueba `screen` al maquetar — DS-P02.

---

## 4 · Importar

**Cuando el producto ya tiene modelo formal** —dominios, tablas y reglas numeradas—, no se reescribe a mano:

1. Se lee el modelo desde la ruta de `proyecto.json.modelo_de_datos`.
2. Se declara en `output/domains/<tipo>.json` la **capa que el diseño consulta**: las entidades y reglas que las
   pantallas tocan, los patrones con su dominio, y las piezas propias.
3. En `modelo_formal` se referencia el modelo completo — **no se duplica**.

> **El dominio no es el modelo de datos completo; es lo que el diseño necesita de él.** Para los 113 tablas y
> 212 reglas, el patrón cita solo las que su pantalla toca. Si hace falta modelar el dato, eso es otra base de conocimiento
> (`Model DataBase`, `Domain Driven Design`); acá se declara la interfaz del diseño con ese dato.

---

## 5 · Extender

| Qué se agrega | Dónde | Después |
|---|---|---|
| Una entidad o un campo | `output/domains/<tipo>.json` → `entidades` | `verificar.py` |
| Una regla | `output/domains/<tipo>.json` → `reglas` | — |
| Un patrón | `output/domains/<tipo>.json` → `patrones` | `verificar.py` |
| Una pieza propia | `output/domains/<tipo>.json` → `componentes_propios` + inventario | `derivar.py` y `verificar.py` |

**Nunca se rehace el dominio para agregar algo.**

---

## 6 · Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Entidad inventada** | Un dato en una pantalla que no tiene campo | Paso 2, siempre — DS-P02 |
| **Patrón sin estado de fallo** | Todos los estados son felices | Al menos uno es un fallo — DS-P03 |
| **Lo ajeno sin `lee_tambien`** | El patrón asume que todo llega siempre | Declarar qué se muestra si no llega — DS-P04 |
| **Pieza propia sin motivo** | Un componente no-universal sin `"universal": false` | Motivo escrito, o es universal y no va acá |
| **Duplicar el modelo formal** | Las 113 tablas copiadas al dominio | `modelo_formal` referencia; el dominio solo declara la capa de diseño |
| **Negocio mezclado con el núcleo** | Un patrón de transporte escrito en un skill universal | Acá, en `output/domains/<tipo>.json` |

---

## 7 · Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/referencias/entrevista.md` | **Siempre al crear.** Las preguntas del negocio y sus valores por omisión |
| `${CLAUDE_PLUGIN_ROOT}/domains/_plantilla.json` | **Al escribir el dominio.** El formato y sus `_lee` son la especificación |
| `${CLAUDE_SKILL_DIR}/scripts/inyectar.py` | **Al materializar el dominio en un sistema.** Patrones, piezas y modelo |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/09-rules/README.md` | Las reglas `DS-P01` a `DS-P06` (patrones) que gobiernan esta skill |

---

## 8 · Al terminar

1. **Qué negocio se definió** — sector, cuántas entidades, cuántas reglas, cuántos patrones.
2. **De dónde salió** — entrevista, o importado de un modelo formal.
3. **Qué se inyectó al inventario** — piezas propias con su motivo.
4. **Qué quedó sin confirmar** — entidades o reglas que el usuario no supo, dichas en voz alta.
5. **Cómo sigue** — `system-design` para lo visual, `screen` para las pantallas.
