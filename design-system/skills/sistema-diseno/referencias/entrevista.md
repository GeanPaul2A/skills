# La entrevista

**Cinco bloques.** Se recorren en orden: cada uno condiciona al siguiente.

**Todo tiene valor por omisión.** *"Usa el que recomiendes"* es una respuesta válida en cualquier pregunta, y
hay que decírselo al usuario al empezar.

> **La regla que gobierna la entrevista:** al usuario se le pide **información sobre su producto**, nunca
> **criterio de diseñador**. Si una pregunta necesita saber de diseño para responderse, está mal formulada —
> conviértela en opciones concretas entre las que elegir.

---

## Antes de la primera pregunta

Dilo así, o parecido:

> Te voy a hacer unas preguntas sobre tu producto para construir el sistema. **En cualquiera puedes decir
> "usa lo que recomiendes"** y yo decido con un valor por omisión sensato, te digo cuál elegí, y lo cambiamos
> después si no te convence.
>
> **No te voy a pedir que diseñes nada.** Donde haga falta criterio visual, te muestro opciones y eliges
> mirando.

---

## Bloque 1 · El producto

Se pregunta todo junto: son independientes entre sí.

| # | Pregunta | Por omisión | Qué condiciona |
|---|---|---|---|
| 1.1 | **¿Qué es el producto, en una frase?** | — *(obligatoria)* | El nombre del sistema y el contexto de todo lo demás |
| 1.2 | **¿Quiénes lo usan?** Un tipo de usuario o varios | Uno solo | Si hace falta más de un objetivo táctil o más de una densidad |
| 1.3 | **¿Dónde corre?** Móvil · escritorio · web · varios | Móvil | Los puntos de corte y qué estados existen |
| 1.4 | **¿En qué idiomas?** | Uno | Si el texto va a tokens de contenido y cuánto puede crecer |

### Qué hacer con 1.2

**Si hay más de un tipo de usuario, pregunta si alguno usa el producto en una condición distinta** — de pie,
manejando, con guantes, con una mano, al sol. Cada condición sube el objetivo táctil mínimo de esa aplicación.

### Qué hacer con 1.3

**Si dice «móvil» a secas, no preguntes más.** Se diseña móvil primero y se escala; es lo correcto por
omisión y no necesita justificarse ante el usuario.

---

## Bloque 2 · La marca

**Es el único bloque donde puede hacer falta mirar.** Empieza siempre por si ya existe algo.

### 2.1 · ¿Ya hay colores?

> **¿Tu producto ya tiene colores?** Un logo, una tarjeta, algo impreso, o un color que ya vengas usando.

| Respuesta | Qué hacer |
|---|---|
| **Da uno o más códigos** | Se toman tal cual. Se ajustan **solo** si no cumplen contraste, y **cada ajuste se nombra** |
| **Da un logo o una imagen** | Se leen sus colores dominantes y se le confirma cuál es el principal |
| **No hay nada** | → 2.2 |

### 2.2 · Proponer, cuando no hay nada

**No preguntes "¿cómo debe sentirse la marca?" en abstracto.** Genera **entre diez y doce paletas
candidatas**, aplicadas al mismo componente, y muéstraselas renderizadas.

Cada candidata lleva:

- **un nombre reconocible** — Índigo, Jade, Terracota
- **una frase de qué transmite**, en términos de producto, no de diseño
- **su riesgo**, si lo tiene — *"compite con el rojo de error"*, *"muy usado en esta categoría"*

**Todas deben cumplir contraste antes de mostrarse.** Una candidata que no cumple no se ofrece.

> El usuario responde con un nombre o un número. Si ninguna convence, pregunta **qué producto le gusta cómo
> se ve** y trabaja desde ahí — es una pregunta que cualquiera puede responder.

### 2.3 · ¿Ya hay tipografía?

> **¿Hay una tipografía definida?** Si no, te propongo tres.

Cuando no la hay, proponer **tres familias**, todas:

- libres y sin costo de licencia
- disponibles en las plataformas que dijo en 1.3
- legibles a tamaño pequeño

Y mostrarlas **aplicadas al mismo componente, con los mismos tamaños**, para que la única diferencia sea la
letra.

### 2.4 · Los colores de estado

**No se preguntan.** Éxito, error y aviso son fijos y **no dependen de la marca**: si cambiaran, el usuario
tendría que volver a aprender qué significa cada color.

**Sí se informa** que existen y que no cambian.

---

## Bloque 3 · Las escalas

**Todas tienen valor por omisión y casi nunca hay que cambiarlas.** Preséntalas como confirmación, no como
pregunta abierta.

| # | Pregunta | Por omisión | Cuándo cambiarlo |
|---|---|---|---|
| 3.1 | **Base de espaciado** | **8** | Interfaces muy densas — tableros, tablas — pueden querer 4 |
| 3.2 | **Densidad** | Cómoda | Compacta si el producto muestra mucho dato por pantalla |
| 3.3 | **Forma** | Redondeo leve | A escuadra si la marca es técnica; muy redondeado si es de consumo |
| 3.4 | **Tamaño base del texto** | **16 px** | **No se baja de 16.** Es el mínimo de accesibilidad |
| 3.5 | **Razón de la escala tipográfica** | **1.2** | 1.125 si hay muchos niveles; 1.25 si hay pocos y contrastados |

### Cómo presentar 3.3

**Muéstralo, no lo describas.** Tres botones idénticos con radio 0, 8 y 16, y que elija.

---

## Bloque 4 · El alcance

| # | Pregunta | Por omisión | Consecuencia |
|---|---|---|---|
| 4.1 | **¿Modo oscuro ahora o después?** | **Preparado, inactivo** | Los modos van en la estructura **desde el día uno**. Activarlo después es cambiar una línea; agregarlo después es rehacer |
| 4.2 | **¿A qué formatos hay que publicar?** | CSS y Figma | Swift, Android, o los que la tecnología pida |
| 4.3 | **¿Hay una herramienta de diseño conectada?** | Se averigua, no se asume | Ver `figma.md` |

### 4.1 no es opcional

**Aunque el usuario diga que nunca va a tener modo oscuro**, el modo se estructura igual. No cuesta nada
tenerlo preparado y cuesta rehacer todo agregarlo después.

**Lo que sí decide el usuario es si está activo.**

---

## Bloque 5 · El negocio

**No se pregunta acá: lo define la skill `dominio`.** Esta entrevista es visual — producto, marca, escalas,
alcance. Las entidades, reglas y flujos del negocio son de `dominio`, y producen `dominios/<tipo>.json`.

**Lo que sí se hace:** al cerrar esta entrevista, avisar al usuario que el negocio se define con la skill
`dominio` — y si no lo ha hecho, ofrecer hacerlo a continuación.

> **Por qué está separado:** el sistema visual no sabe de taxis, de banca ni de comercio. El que lo sabe es el
> dominio. Mezclarlos es lo que obliga a reescribir patrones de transporte cada vez que cambia el negocio.

---

## Al cerrar la entrevista

**Antes de escribir nada, resume y confirma:**

```
Producto      <una frase>
Usuarios      <quiénes>  ·  <condiciones especiales si las hay>
Plataformas   <cuáles>
Idiomas       <cuáles>

Acento        <color>   <«elegido por ti» o «propuesto y aprobado»>
Tipografía    <familia>
Espaciado     base <n>  ·  densidad <cuál>
Forma         <radio>
Texto         base <n> px  ·  razón <n>

Modos         <activos>  ·  preparados: <cuáles>
Salidas       <formatos>
Negocio       <lo define la skill dominio, a continuación>
```

Y pregunta: **¿algo que corregir antes de construir?**

---

## Lo que NUNCA se pregunta

| No preguntar | Porque |
|---|---|
| *"¿Qué personalidad tiene tu marca?"* | Pide criterio de diseñador. Ofrece opciones renderizadas |
| *"¿Prefieres una escala modular o armónica?"* | Es jerga. Se decide con un valor por omisión |
| *"¿Qué relación de contraste quieres?"* | No es negociable: **AA es el piso** |
| *"¿Qué tamaño debe tener el cuerpo de texto?"* | Tampoco: **16 px mínimo** |
| *"¿Quieres estados de carga y error?"* | Son obligatorios. No son una opción |
