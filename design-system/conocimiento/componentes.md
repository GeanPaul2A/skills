# Componentes · el contrato

**Un componente no está listo cuando se ve bien. Está listo cuando su entrada del inventario está completa.**

`inventario/componentes.json` es **el contrato legible por máquina**: es lo que `verificar.py` comprueba y lo
que `construir.py` traduce a la herramienta de diseño. Sin entrada, el componente no existe para el sistema
— DS-C01.

---

## Los cuatro niveles

`[B1, cap. 5]` presenta dos arquitecturas y prefiere la segunda:

| Atomic Design | La alternativa ← **esta** | Qué es |
|---|---|---|
| Atoms | **PRIMITIVOS** | Tokens y fundamentos |
| Molecules | **COMPONENTES** | Elementos sueltos: botón, campo, tarjeta |
| Organisms | **PATRONES** | Combinaciones con propósito: elegir un método de pago |
| Templates | **PLANTILLAS** | La estructura de una pantalla |
| Pages | *(no se usa)* | |

> *"Elimina la confusión de la terminología átomos/moléculas y crea distinciones más claras."*

**La frontera que importa:** un **componente** no sabe para qué se lo usa. Un **patrón** sí — y por eso el
patrón es el que declara de dónde salen sus datos.

---

## La entrada, campo por campo

```json
"boton": {
  "grupo": "accion",
  "descripcion": "La acción de una pantalla. El primario cierra un trato: enviar, aceptar, confirmar",
  "cuando_no": "Si solo navega sin cambiar nada, usar 'enlace'. Si actúa sobre una fila, usar 'boton-icono'",
  "variantes": ["primario", "secundario", "silencioso", "destructivo"],
  "tamanos": ["sm", "md", "lg"],
  "estados": ["reposo", "presionado", "foco", "deshabilitado", "cargando"],
  "tokens": {
    "primario.fondo": "accion.reposo",
    "primario.texto": "texto.sobre-accion",
    "foco.anillo":    "accion.reposo",
    "relleno":        "espacio.interior",
    "forma":          "forma.control",
    "texto":          "tipo.cuerpo"
  },
  "reglas": ["DS-C02", "DS-C03", "DS-A02", "DS-A07"],
  "interactivo": true,
  "espera_datos": false
}
```

| Campo | Qué es | Regla |
|---|---|---|
| `grupo` | Familia: acción, entrada, contenido, retroalimentación, navegación | |
| `descripcion` | **Cuándo usarlo** | DS-C05 |
| `cuando_no` | **Cuándo NO usarlo, y qué usar en su lugar** | DS-C05 |
| `variantes` | Versiones que difieren de forma **predecible y limitada** | DS-C09 |
| `tamanos` | Si escala. Vacío si tiene uno solo | |
| `estados` | **`foco` es obligatorio si es interactivo** | DS-C02 |
| `tokens` | Mapeo parte → **rol semántico**. Nunca a un primitivo | DS-T02 |
| `reglas` | Las del sistema que le aplican | |
| `interactivo` | Si recibe foco de teclado | DS-C02 |
| `espera_datos` | Si depende de una respuesta | DS-C03 |
| `datos` | Qué hace ante carga, vacío y error. **Obligatorio si espera datos** | DS-C03 |
| `props` | Propiedades públicas: `nombre`, `tipo`, `default` y `que_hace` | DS-C05 |
| `accesibilidad` | `rol`, `teclado` y `lector`. **Obligatorio si es interactivo** | DS-C02 |
| `accesibilidad.etiqueta` | Dónde vive la etiqueta persistente. **Obligatorio en el grupo `entrada`** | DS-A04 |
| `accesibilidad.vivo` | Cómo se anuncia el cambio. **Obligatorio si espera datos y declara carga o error** | DS-A10 |
| `ejemplo_codigo` | Fragmento con tokens del nivel 3, nunca valores en crudo | DS-T07 |
| `privado` | Auxiliar. Su nombre empieza con punto y no se publica | DS-C04 |

> **Los tres campos nuevos** (`props`, `accesibilidad`, `ejemplo_codigo`) los agrega la skill `documentar`,
> y los valida `verificar.py`. El detalle completo, en `skills/documentar/referencias/ficha.md`.

> **`etiqueta` y `vivo` son condicionales, no opcionales.** Un control de entrada sin `etiqueta` termina
> usando el marcador como etiqueta, y el marcador **desaparece al escribir**: quien vuelve al campo ya no sabe
> qué iba ahí. Un componente que se rellena solo y no declara `vivo` **cambia en silencio**: quien usa lector
> de pantalla no se entera de que llegó el contenido. Los dos huecos son invisibles mirando la pantalla, y por
> eso van en el contrato y no en una revisión a ojo.

---

## `cuando_no` es el campo que más se salta, y el más útil

**Una descripción sola no evita nada.** Lo que evita el uso equivocado es decir **qué usar en su lugar**:

> *"Si solo navega sin cambiar nada, usar `enlace`. Si actúa sobre una fila, usar `boton-icono`."*

`[B2, cap. 11]` lo pone en la descripción del componente porque **es lo que se lee en el panel de la
herramienta**, justo cuando alguien está por elegir mal.

**El verificador exige veinte caracteres mínimos.** Un `"no"` no es una respuesta.

---

## `foco` no es opcional

**Todo lo interactivo lo declara** — DS-C02, y con **3:1 contra su fondo** — DS-A02.

`[B1, cap. 7]`: *"Lo que se puede hacer con el ratón se tiene que poder hacer con el teclado, y el foco tiene
que verse."*

**El caso que se olvida siempre:** una tarjeta que se puede elegir es interactiva. Un diálogo que atrapa el
foco, también.

---

## Los tres estados de datos

**Si `espera_datos` es cierto, hay que declarar los tres** — DS-C03:

| Estado | Qué se muestra |
|---|---|
| `cargando` | Un esqueleto con la forma del contenido, no un giro genérico |
| `vacio` | **Por qué está vacío y qué hacer**, no una pantalla en blanco |
| `error` | Qué pasó y **cómo reintentar** |

**«No aplica» vale, pero con su motivo:**

```json
"datos": {
  "cargando": "estado 'cargando' — se pinta con .esqueleto",
  "vacio":    "no aplica — el contenedor no decide si hay contenido",
  "error":    "no aplica — se reemplaza por 'mensaje'"
}
```

**Un «no aplica» pelado el verificador lo rechaza.** Es la diferencia entre una decisión y un olvido.

> **El fallo más común de todo el oficio es la lista vacía sin explicación.** Se ve como una pantalla rota, y
> el usuario no sabe si es que no hay nada o si algo falló.

---

## Los auxiliares llevan punto

`[B2, cap. 7]` — un componente que **solo existe para armar otro** se prefija con punto y **no se publica**:

```
.esqueleto      la forma que se muestra mientras carga
.icono          el envoltorio de tamaño y color de un icono
```

**El punto no es decoración: la herramienta los esconde de la biblioteca publicada.** Sin él, el equipo ve
veinte piezas donde debería ver cinco.

---

## Cuántas variantes

`[B1, cap. 5]` lo dice sin vueltas: *"Crear 15 variantes de botón cuando solo necesitas 3."*

**Se agrupa como variante lo que difiere de forma predecible y limitada** — DS-C09. Si dos supuestas variantes
**no comparten estructura**, son dos componentes.

### Y hay una señal para saber si faltan

`[B1, cap. 5]`:

> *"Si ves un número grande de componentes **desvinculados**, tienes un problema. Quizá te falta una variante
> — eso debería ser **una señal para repriorizar tu hoja de ruta**."*

**Desvincular es la última salida** — DS-C08. Cuando pasa seguido, el que está mal es el sistema, no quien
desvincula.

---

## Los 22 universales

`plantillas/componentes-base.json` los trae. **Existen en cualquier producto**, así que no se vuelven a
inventar:

| Grupo | Componentes |
|---|---|
| **acción** | `boton` · `boton-icono` · `enlace` |
| **entrada** | `campo` · `casillas-codigo` · `desplegable` · `segmentado` · `opcion` · `contador` |
| **contenido** | `tarjeta` · `avatar` · `distintivo` · `chip` · `pasos` |
| **retroalimentación** | `mensaje` · `hoja-inferior` · `dialogo` · `vacio` |
| **navegación** | `barra-inferior` · `barra-superior` |
| **auxiliares** | `.esqueleto` · `.icono` |

**Agregar solo lo que el producto necesite de verdad.** Un componente que no se usa igual hay que mantenerlo.

### Lo propio del producto se marca

Un componente que **solo tiene sentido en este producto** —una tarjeta con los campos de su entidad, un
marcador sobre una superficie continua— lleva
`"universal": false` y **su motivo**. Es lo que permite, más adelante, llevarse los universales a otro
producto sin arrastrar lo que no sirve.

---

## Antes de dar un componente por cerrado

```
□  descripcion y cuando_no, ambos con sustancia
□  todas sus variantes y todos sus estados
□  foco declarado, si es interactivo
□  carga, vacío y error, si espera datos
□  cada parte mapeada a un rol SEMÁNTICO — ningún primitivo
□  contraste comprobado en todos los modos
□  objetivo táctil ≥ el mínimo del producto
□  verificar.py en verde
```
