# 07 · Handoff (Entrega)

**El producto final no es un archivo de Figma: es código de producción.** Esta sección define cómo se organiza
y se entrega el diseño para que llegue entero al otro lado.

**Clasificación:** `[Book 1, cap. 4]` estructura de archivo y modo de desarrollo · `[Book 1, cap. 8]`
exportación, iconos y animación · `[Book 2, cap. 11]` modo de desarrollo y servidor MCP.

---

## Índice

1. [La frase que gobierna la sección](#71--la-frase-que-gobierna-la-sección)
2. [La estructura del archivo](#72--la-estructura-del-archivo)
3. [Nombrar](#73--nombrar)
4. [El modo de desarrollo](#74--el-modo-de-desarrollo)
5. [Exportar](#75--exportar)
6. [Animación](#76--animación)
7. [El control de versiones](#77--el-control-de-versiones)
8. [La lista de calidad](#78--la-lista-de-calidad)
9. [Reglas de esta sección](#79--reglas-de-esta-sección)

---

## 7.1 · La frase que gobierna la sección `[Book 1, cap. 8]`

> *"Puedes diseñar el mejor producto del planeta, pero **si no se desarrolla correctamente, se quedará solo en
> Figma** para tu próxima publicación de Dribbble."*

Y su contraparte, del capítulo 5:

> *"Recuerda: **construyes sistemas de diseño para acelerar todo el proceso —el desarrollo en particular—**, no
> para tener archivos bonitos de Figma."*

---

## 7.2 · La estructura del archivo `[Book 1, cap. 4]`

**El libro usa una estructura fija de siete páginas en todos sus proyectos**, y la razón es explícita:

> *"Esta estructura inamovible me ayuda a duplicar archivos y empezar proyectos nuevos rápido, mientras que
> **los desarrolladores saben exactamente dónde encontrar lo que necesitan**."*

| Página | Contiene |
|---|---|
| **01 · Para empezar** | Se abre sola la primera vez. Cómo usar el archivo |
| **02 · Nombre del proyecto** | Las pantallas, **organizadas por secciones lógicas del producto** |
| **03 · Documentación** | Encargo, requisitos, investigación, personas, notas |
| **04 · Componentes** | Biblioteca local y su documentación |
| **05 · Pruebas y exploración** | Alternativas, trabajo en curso, experimentos |
| **06 · Archivo** | Versiones anteriores y conceptos descartados. *"Nunca borres trabajo que pueda ser valioso después"* |
| **07 · Portada** | Nombre, estado, equipo, descripción breve |

### La analogía que explica por qué importa `[Book 1, cap. 4]`

> *"Imagina que entras a un supermercado nuevo donde todo está colocado al azar. Al lado de la leche hay
> manzanas, junto a ellas jugo de naranja, pero el jugo de manzana está del otro lado de la tienda, junto a los
> zapatos. Suena absurdo, pero **si tú mismo construiste esa tienda, te parecería bien**. Después de todo, tú
> sabes dónde está el jugo de manzana."*
>
> *"**Los desarrolladores son los compradores nuevos en tu tienda.**"*

**Y la prueba que propone:** abrir un archivo de hace tres a seis meses y ver si se entiende de inmediato de
qué trata y si tiene todo lo que un desarrollador necesita.

### La estructura de los archivos del sistema `[Book 1, cap. 5]`

**Separada de los archivos de producto**, por la regla de modularidad `DS-C07`:

```
00 · Para empezar      cómo usar el sistema
01 · Tokens            la biblioteca de tokens y estilos
02 · Componentes       la biblioteca de componentes
03 · Patrones          combinaciones
04 · Plantillas        estructuras de pantalla
05 · Anotaciones       los ayudantes de documentación
```

---

## 7.3 · Nombrar `[Book 1, cap. 8]`

**El libro vuelve al tema tres veces, y siempre por lo mismo:**

> *"Si quieres que los desarrolladores exporten fácilmente los recursos desde Figma, **necesitan saber qué
> exportar**. La nomenclatura unificada es la clave del éxito."*

**OBLIGATORIO** — capas, marcos y recursos siguen el mismo convenio que los tokens (`DS-T04`).

### Y el vocabulario compartido `[Book 1, cap. 4]`

> *"Establece convenciones de nombres compartidas… **Cuando los diseñadores hablan de 'tarjetas' y los
> desarrolladores las llaman 'contenedores', la mala comunicación es inevitable.**"*

**OBLIGATORIO** `[Ext]` — **el vocabulario compartido sale del modelo de dominio**, que ya existe y ya está
acordado: los nombres de tabla y de columna. El componente que muestra una entidad **toma su nombre de la
entidad** —`tarjeta-<entidad>` de la tabla `<entidad>`— y no al revés.

> **Por qué en esa dirección y no en la contraria:** el modelo de datos sobrevive al rediseño. Un nombre de
> componente inventado en Figma obliga a mantener un diccionario de traducción que nadie mantiene.

---

## 7.4 · El modo de desarrollo `[Book 1, cap. 4]` · `[Book 2, cap. 11]`

**Qué resuelve, textual:**

> *"Una de las fuentes más grandes de errores de implementación viene de desarrolladores **tratando de adivinar
> o medir valores a mano**. En una vista normal de Figma, un desarrollador podría ver un botón e intentar
> estimar su relleno, su radio de esquina o sus valores de color. Esto lleva a inconsistencias y a
> comunicación de ida y vuelta."*
>
> *"El modo de desarrollo lo resuelve **mostrando los valores de token exactos**. Si usas variables para tus
> tokens, **los desarrolladores ven los nombres de variable directamente**."*

**Genera fragmentos para CSS, iOS y Android** `[Book 2, cap. 11]`, y **convierte los estilos de color
compartidos en variables CSS**.

### El servidor MCP `[Book 2, cap. 11]`

**Existe, se activa desde el panel *Inspect* → sección *MCP server*, y Claude Code figura entre sus clientes.**

**El libro lo describe como puente de lectura** —*«Send design context to your AI agent»*, con
`get_design_context` como herramienta de confirmación—. **Se conectó, y hoy escribe.**

| Dirección | Herramienta | Estado |
|---|---|---|
| Figma → código | `get_design_context` · `get_metadata` · `get_screenshot` · `get_variable_defs` | Como lo describe el libro |
| **código → Figma** | **`use_figma`** (Plugin API completa) · `create_new_file` · `upload_assets` | **Confirmado el 17-08-2026** |
| ida y vuelta | `get_code_connect_map` · `add_code_connect_map` | Confirmado |

> **Se registra la fecha porque el estado cambia.** El libro no se equivocó: el servidor creció después.
> Y `DS-X06` sigue en pie — **ninguna decisión de este proyecto depende de que escriba**, entre otras cosas
> porque el permiso depende del asiento del usuario, no de que la herramienta exista.

El detalle operativo —qué skill hay que cargar antes de cada llamada y cómo entran las tres colecciones— vive
en `skills/sistema-diseno/referencias/puentes.md`.

### Code Connect `[Book 1, cap. 5]`

**Enlaza el componente de código real con el componente de Figma.** El desarrollador ve una pestaña *Code* y
copia el componente listo, con sus propiedades ya puestas.

**Requiere plan Organización o Empresarial.** Queda registrado como opción, no como plan.

---

## 7.5 · Exportar `[Book 1, cap. 8]`

### Formatos, y para qué sirve cada uno

| Formato | Cuándo |
|---|---|
| **SVG** | **Iconos, logotipos, ilustraciones simples.** Escala perfecto |
| **PNG** | Gráficos con transparencia o bordes nítidos |
| **JPG** | Fotografías |
| **WebP** | Reemplazo moderno de PNG/JPG, mejor compresión |
| **AVIF** | La mejor compresión |

**Las cifras que el libro midió** sobre una misma imagen: **WebP ahorró 87 %** y **AVIF 93.9 %**, *"con
compresión increíble y sin pérdida visible de calidad"*.

**Y sobre la calidad:** una imagen de fondo a calidad baja pesó **58.4 % menos** que a calidad alta, *"y a
primera vista no se nota la diferencia"*.

### Iconos

**Las reglas técnicas están en `01-foundations` §1.8** — combinar trazados, nada de máscaras ni degradados,
menos de 2 KB, y comprobarlo abriendo el SVG en un editor de texto.

---

## 7.6 · Animación `[Book 1, cap. 8]`

**Toda animación se entrega con cinco datos:**

| Dato | Pregunta que responde |
|---|---|
| **Esencial o de adorno** | ¿se puede simplificar si es difícil? |
| **Tiempo y duración** | ¿cuánto dura? ¿tiene fases? |
| **Curva** | `linear` · `ease-in` · `ease-out` · `ease-in-out`, o una Bézier propia |
| **Disparador** | ¿qué la activa? ¿qué pasa si se dispara dos veces rápido? |
| **Rendimiento** | ¿qué propiedad se anima? ¿hay alternativa más barata? |

### La regla técnica que el libro subraya

> *"Al animar movimiento, **prefiere siempre las propiedades `transform` de CSS antes que las de posición**
> (`left`, `top`, `right`, `bottom`). Las animaciones con `transform` usan aceleración por hardware y no
> disparan recálculos de disposición, lo que da animaciones fluidas de 60 fps. Las basadas en posición obligan
> al navegador a recalcular la disposición, lo que puede causar tirones, **especialmente en móviles**."*

### Y la advertencia de peso

> *"Agregar más de 100 KB de biblioteca solo para transiciones simples **puede perjudicar el rendimiento**.
> Para animaciones básicas, las animaciones CSS suelen dar mejor rendimiento con mínima complejidad. Reserva
> las bibliotecas pesadas para animaciones verdaderamente complejas."*

---

## 7.7 · El control de versiones `[Book 1, cap. 1]`

**Se crea una versión manual al final de un ciclo**, no cada tanto. Y con nombre estructurado:

```
Por hito         NombreProyecto_Hito_vX          →  Onboarding_Flow_v3
Por fecha        NombreProyecto_AAAA-MM-DD       →  Onboarding_Flow_2025-01-15
Por revisión     NombreProyecto_Tipo_Etapa_vX    →  Onboarding_Flow_Review_v1
```

**RECOMENDADO** — **por hito**, para que el nombre de la versión coincida con los cierres de fase que el
proyecto ya registra en otro lado. La fecha sirve como desempate, no como esquema principal.

### El sistema y las entregas llevan versiones distintas `[Ext G7]`

**El libro versiona *el archivo*.** Pero un archivo de sistema y uno de producto **cambian a distinto ritmo**:
el sistema poco y despacio, las funcionalidades todo el tiempo. Un solo número no distingue *«cambió un token»*
de *«alguien agregó una pantalla»*, que es justo lo que hay que saber.

| Versión | Dónde vive | Qué la mueve |
|---|---|---|
| **Del sistema** | `marca.json` → `version` | Un cambio en tokens, componentes, patrones o plantillas |
| **De una entrega** | `entrega/versiones.json` → `entregas[]` | Un cambio en las pantallas de esa funcionalidad |

**Y toda entrega declara contra qué versión del sistema se dibujó.** Es lo único que permite, cuando el sistema
salte a una mayor, saber **qué pantallas hay que revisar y cuáles ya estaban al día** — en vez de abrirlas todas.

**Qué número sube:**

| Cambio | Sube |
|---|---|
| Cambia el acento, la familia o la escala de espaciado · se elimina o renombra una pieza · cambia el significado de un rol | **mayor** |
| Se agrega un componente, patrón, plantilla, modo, idioma, plataforma, variante o estado | **menor** |
| Se corrige un contraste, una descripción, un `cuando_no`, un token mal apuntado | **parche** |

> **La regla que resuelve las dudas:** si alguien que ya dibujó con la versión anterior **tiene que volver a
> mirar su pantalla**, es mayor. Si puede ignorar el cambio, es menor o parche.

**El detalle operativo y el ejemplo momento a momento**, en `skills/entregar/referencias/versionado.md`.

---

## 7.8 · La lista de calidad `[Book 1, cap. 8]`

**Tres bloques, para revisar lo construido contra lo diseñado.**

### Fidelidad visual

- ¿tipografías, tamaños y pesos correctos?
- ¿espaciado consistente con la especificación?
- ¿**los colores coinciden exactamente** con el sistema?
- ¿imágenes bien dimensionadas y optimizadas?

### Interacción

- ¿funcionan los estados — sobre, foco, activo, deshabilitado?
- ¿**los estados de carga están implementados**?
- ¿las animaciones respetan tiempo y curva?
- ¿**los estados de error están bien diseñados y son funcionales**?
- ¿la navegación por teclado funciona con fluidez?

### Responsivo

- ¿funciona en distintos tamaños de pantalla?
- ¿los objetivos táctiles tienen tamaño adecuado en móvil?
- ¿los componentes se adaptan al cambiar el contenido?
- ¿los puntos de corte están implementados como se diseñaron?

> **Y la nota del revisor técnico del libro, que apunta a dónde va este proyecto:** *"Muchos de estos puntos
> deberían idealmente **automatizarse mediante marcos de prueba**… en lugar de comprobarse a mano. La
> automatización garantiza consistencia, ahorra tiempo y detecta problemas de forma más confiable que las
> revisiones manuales."*

---

## 7.9 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-H01`** | El archivo de producto sigue la **estructura de siete páginas** | OBLIGATORIO | `[Book 1, cap. 4]` |
| **`DS-H02`** | Capas, marcos y recursos siguen el **mismo convenio que los tokens** | OBLIGATORIO | `[Book 1, cap. 8]` |
| **`DS-H03`** | El nombre de un componente **deriva del nombre de la tabla** que lo alimenta | OBLIGATORIO | `[Book 1, cap. 4]` · `[Ext G2]` |
| **`DS-H04`** | Los iconos se exportan en **SVG**; las fotografías en **WebP o AVIF** | OBLIGATORIO | `[Book 1, cap. 8]` |
| **`DS-H05`** | Toda animación se entrega con sus **cinco datos** | OBLIGATORIO | `[Book 1, cap. 8]` |
| **`DS-H06`** | El movimiento se anima con **`transform`**, nunca con propiedades de posición | OBLIGATORIO | `[Book 1, cap. 8]` |
| **`DS-H07`** | Se crea versión manual **al cerrar un ciclo**, con nombre por hito | RECOMENDADO | `[Book 1, cap. 1]` |
| **`DS-H08`** | **Nada se borra**: lo descartado va a la página de archivo | RECOMENDADO | `[Book 1, cap. 4]` |
| **`DS-H09`** | El sistema **declara su versión**, y es semántica | OBLIGATORIO | `[Ext G7]` |
| **`DS-H10`** | Toda entrega declara **contra qué versión del sistema** se dibujó | OBLIGATORIO | `[Ext G7]` |
