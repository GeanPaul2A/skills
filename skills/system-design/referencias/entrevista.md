# La entrevista

**Cinco bloques.** Se recorren en orden: cada uno condiciona al siguiente.

**Todo tiene valor por omisión.** *"Usa el que recomiendes"* es una respuesta válida en cualquier pregunta, y
hay que decírselo al usuario al empezar.

> **La regla que gobierna la entrevista:** al usuario se le pide **información sobre su producto**, nunca
> **criterio de diseñador**. Si una pregunta necesita saber de diseño para responderse, está mal formulada —
> conviértela en opciones concretas entre las que elegir.

---

## Índice

1. [Antes de la primera pregunta](#antes-de-la-primera-pregunta)
2. [Bloque 1 · El producto](#bloque-1--el-producto)
3. [Bloque 2 · La marca](#bloque-2--la-marca)
4. [Bloque 3 · Las escalas](#bloque-3--las-escalas)
5. [Bloque 4 · El alcance](#bloque-4--el-alcance)
6. [Bloque 5 · El negocio](#bloque-5--el-negocio)
7. [Al cerrar la entrevista](#al-cerrar-la-entrevista)
8. [Dónde aterriza cada respuesta](#dónde-aterriza-cada-respuesta)
9. [Lo que NUNCA se pregunta](#lo-que-nunca-se-pregunta)

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

### 1.0 · La pregunta cero — ¿ya existe?

**Antes de la tabla, una sola pregunta:** *«¿el producto ya existe — hay pantallas hechas, una app
publicada, un sistema anterior?»*

| Respuesta | Qué hacer |
|---|---|
| **Hay pantallas o un sistema construido** | **Primero la skill `audit`**: se mide lo que hay antes de proponer nada. Los colores y la tipografía vigentes entran por 2.1 y 2.3 como «ya hay» |
| **Hay marca pero no producto** | Seguir normal: 2.1 y 2.3 recogen lo que exista |
| **No hay nada** | Seguir normal — es el caso que el resto de la entrevista asume |

**Proponer una paleta a un producto que ya tiene pantallas es rehacer, no diseñar.** La entrevista asume
producto nuevo; esta pregunta es la que lo comprueba en vez de asumirlo.

Se pregunta todo junto: son independientes entre sí.

| # | Pregunta | Por omisión | Qué condiciona |
|---|---|---|---|
| 1.1 | **¿Qué es el producto, en una frase?** | — *(obligatoria)* | El nombre del sistema y el contexto de todo lo demás |
| 1.2 | **¿Qué canales tiene, y en qué dispositivos corre cada uno?** | Móvil (iOS + Android) | Los puntos de corte, qué estados existen y si «pasar por encima» tiene sentido |
| 1.3 | **¿En qué condiciones se usa?** | Nada especial | El objetivo táctil mínimo y el piso de contraste |
| 1.4 | **¿En qué idiomas?** | Uno | Si el texto va a tokens de contenido y cuánto puede crecer |

### 1.2 · Canales, no «dónde corre»

**Se pregunta en plural desde el principio.** Un producto suele tener más de un canal —la aplicación móvil y
un panel web de administración— y la pregunta en singular obliga a elegir uno y corregir después.

**Si dice «móvil» a secas, no preguntes más.** Se diseña móvil primero y se escala; es lo correcto por
omisión y no necesita justificarse ante el usuario.

### 1.3 · Condiciones, NUNCA roles

> **No preguntes quiénes son los usuarios.** Pasajero, conductor, administrador, comercio son **roles de
> negocio**, y el sistema de diseño es agnóstico al negocio: los define la skill `domain`.

**Lo único que lo visual necesita saber del uso es la condición física**, porque es lo que mueve un número:

| Condición | Qué cambia |
|---|---|
| **Manejando** o en movimiento | Objetivo táctil a 56 px |
| **Con una sola mano** | Objetivo táctil a 52 px, y las acciones principales a la zona baja |
| **Al sol, a la intemperie** | El piso de contraste sube por encima del mínimo AA |
| **Nada especial** | Se queda en los 44 px por omisión |

**Las condiciones pueden ser distintas por canal**, y casi siempre lo son: el panel de administración se usa
sentado aunque la aplicación se use al volante. **Si el usuario marca varias, pregunta cuál es de cuál** — y
si marca todas más «nada especial», es una contradicción y hay que resolverla antes de seguir.

**El dueño del dato es `proyecto.json → contexto.condiciones`** — un mapa `{ámbito: condición}` con
vocabulario cerrado: `nada-especial` · `una-mano` · `en-movimiento` · `guantes` · `intemperie`. Y **si ya
existe un dominio (`output/domains/<tipo>.json`), sus actores traen las condiciones**: `inyectar.py` las
vuelca a ese mapa, así que acá se **confirman**, no se vuelven a preguntar. `derivar.py` cruza cada condición
contra `tacto.minimo` o `tacto.por_actor.<ámbito>` y **falla si el número no la cubre**.

> **Por qué esto estaba mal antes:** la pregunta era *«¿quiénes usan la app?»*, y filtraba el dato físico a
> través de los roles. Mezclaba los dos dominios y obligaba al usuario a corregir la pregunta.

### 1.4 · Idiomas: también la escritura, no solo la lengua

**De la lista de idiomas se derivan dos cosas sin volver a preguntar:**

- **La dirección.** Árabe o hebreo en la lista significa **RTL**: la disposición se espeja entera —
  navegación, iconos direccionales, orden de lectura— y eso se declara desde el día uno, como los modos.
  Agregarlo después es rehacer cada plantilla.
- **El alfabeto.** Cirílico, griego, CJK, árabe: **las familias tipográficas que se propongan en 2.3 tienen
  que cubrir todos los alfabetos de esta lista.** Una familia «legible y libre» que no tiene los glifos del
  idioma declarado no es candidata, por linda que se vea en español.

---

## Bloque 2 · La marca

**Es el único bloque donde puede hacer falta mirar.** Empieza siempre por si ya existe algo.

### 2.1 · ¿Ya hay colores?

> **¿Tu producto ya tiene colores?** Un logo, una tarjeta, algo impreso, o un color que ya vengas usando.

| Respuesta | Qué hacer |
|---|---|
| **Da uno o más códigos** | Se toman **tal cual y no se tocan** — ver abajo |
| **Da un logo o una imagen** | Se leen sus colores dominantes y se le confirma cuál es el principal |
| **No hay nada** | → 2.2 |

> **Nunca le pidas al usuario que oscurezca su marca.** Un color de marca claro —un amarillo, un cian, un
> verde— entra igual que uno oscuro: se ancla en el peldaño que le toca por lo claro que se ve, y lo que el
> sistema decide alrededor es **en qué peldaño se apoya el botón y qué texto va encima, tinta o blanco**. Sobre
> amarillo va texto negro, no blanco.
>
> **Si el peldaño de la marca no puede sostener el botón** —porque no se despega del fondo blanco, que es lo
> que le pasa a un amarillo— el botón se apoya en un peldaño vecino **y se dice, con el número que lo
> impidió**. El color de marca sigue entero en la paleta. `derivar.py` imprime esa línea solo; no la inventes
> ni la calles.

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
- disponibles en las plataformas que dijo en 1.2
- legibles a tamaño pequeño
- **con los glifos de todos los idiomas de 1.4** — ver §1.4: una familia sin el alfabeto declarado no es candidata

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
| 3.6 | **¿El movimiento, sobrio o expresivo?** | **Sobrio** | Expresivo solo si la marca es de consumo y lo pide; alarga las transiciones y agrega entradas coreografiadas |

### Cómo presentar 3.3

**Muéstralo, no lo describas.** Tres botones idénticos con radio 0, 8 y 16, y que elija.

### 3.6 · El movimiento tiene un piso que no se pregunta

La respuesta aterriza en `marca.json → interaccion.transicion` — sobrio se queda con los valores por omisión
(120/200 ms); expresivo los alarga y lo justifica. **Y lo que no se pregunta: `prefers-reduced-motion` se
respeta siempre.** Quien pidió menos movimiento en su sistema operativo lo recibe, con marca expresiva o sin
ella — es piso de accesibilidad, igual que el contraste. Se informa, como los colores de estado.

---

## Bloque 4 · El alcance

| # | Pregunta | Por omisión | Consecuencia |
|---|---|---|---|
| 4.1 | **¿Modo oscuro ahora o después?** | **Preparado, inactivo** | Los modos van en la estructura **desde el día uno**. Activarlo después es cambiar una línea; agregarlo después es rehacer. **Vale igual para alto contraste**: se prepara sin preguntar y el usuario decide si se activa |
| 4.2 | **¿A qué formatos hay que publicar?** | CSS y Figma | Swift, Android, o los que la tecnología pida |
| 4.3 | **¿Hay una herramienta de diseño conectada?** | Se averigua, no se asume | Ver `puentes.md` y `figma-mcp.md` |

### 4.1 no es opcional

**Aunque el usuario diga que nunca va a tener modo oscuro**, el modo se estructura igual. No cuesta nada
tenerlo preparado y cuesta rehacer todo agregarlo después.

**Lo que sí decide el usuario es si está activo.**

---

## Bloque 5 · El negocio

**No se pregunta acá: lo define la skill `domain`.** Esta entrevista es visual — producto, marca, escalas,
alcance. Las entidades, reglas y flujos del negocio son de `domain`, y producen `domains/<tipo>.json`.

**Lo que sí se hace:** al cerrar esta entrevista, avisar al usuario que el negocio se define con la skill
`domain` — y si no lo ha hecho, ofrecer hacerlo a continuación.

> **Por qué está separado:** el sistema visual no sabe de taxis, de banca ni de comercio. El que lo sabe es el
> dominio. Mezclarlos es lo que obliga a reescribir patrones de transporte cada vez que cambia el negocio.

---

## Al cerrar la entrevista

**Antes de escribir nada, resume y confirma:**

```
Producto      <una frase>
Canales       <cuáles, y en qué dispositivos>
Condiciones   <por canal, o «nada especial»>
Idiomas       <cuáles>

Acento        <color>   <«elegido por ti» o «propuesto y aprobado»>
Tipografía    <familia>
Espaciado     base <n>  ·  densidad <cuál>
Forma         <radio>
Texto         base <n> px  ·  razón <n>
Movimiento    <sobrio o expresivo>

Modos         <activos>  ·  preparados: <cuáles>
Salidas       <formatos>
Negocio       <lo define la skill domain, a continuación>
```

Y pregunta: **¿algo que corregir antes de construir?**

---

## Dónde aterriza cada respuesta

**Cada respuesta se escribe en un campo concreto de la configuración** — Paso 2 del procedimiento. Una
respuesta que no se escribe se pierde, y una entrevista que no se persiste hay que repetirla.

| Pregunta | Campo |
|---|---|
| 1.0 · ¿Ya existe? | No se persiste: decide la ruta — `audit` primero si hay pantallas |
| 1.1 · El producto | `proyecto.json → proyecto.nombre` y `proyecto.descripcion` |
| 1.2 · Canales y dispositivos | `proyecto.json → proyecto.plataformas` |
| 1.3 · Condiciones de uso | `proyecto.json → contexto.condiciones` — un mapa `{ámbito: condición}` con vocabulario cerrado. La consecuencia numérica va en `marca.json → tacto.minimo` o `tacto.por_actor.<ámbito>`, y **`derivar.py` cruza los dos y falla si se contradicen** |
| 1.4 · Idiomas | `proyecto.json → proyecto.idiomas` — y de ahí se derivan RTL y alfabetos, §1.4 |
| 2.1 / 2.2 · El color | `marca.json → identidad.acento` y `identidad.nombre_acento` |
| 2.3 · La tipografía | `marca.json → tipografia.familia` |
| 3.1 · Base de espaciado | `marca.json → espaciado.base` |
| 3.2 · Densidad | `proyecto.json → contexto.densidad` — `comoda` o `compacta`. `derivar.py` avisa si `compacta` convive con espaciado base 8 |
| 3.3 · Forma | `marca.json → forma.control`, `forma.tarjeta`, `forma.contenedor` |
| 3.4 · Tamaño base del texto | `marca.json → tipografia.base` |
| 3.5 · Razón de la escala | `marca.json → tipografia.razon` |
| 3.6 · Movimiento | `marca.json → interaccion.transicion` — sobrio deja los valores por omisión |
| 4.1 · Modo oscuro | `marca.json → modos.activos` y `modos.preparados` |
| 4.2 · Formatos de salida | `proyecto.json → outputs` |
| 4.3 · Herramienta conectada | No se persiste: se comprueba en la sesión, cada vez |

**Y el porqué va en `proyecto.json → contexto.motivo`** — «elegido por el usuario» o «propuesto y
aprobado», con la razón en una frase.

**Y se registra el origen de cada decisión** — «elegido por el usuario» o «propuesto y aprobado» — en el
resumen de cierre. Es lo que permite, meses después, saber qué se puede cambiar sin preguntar y qué no.

---

## Lo que NUNCA se pregunta

| No preguntar | Porque |
|---|---|
| *"¿Qué personalidad tiene tu marca?"* | Pide criterio de diseñador. Ofrece opciones renderizadas |
| *"¿Prefieres una escala modular o armónica?"* | Es jerga. Se decide con un valor por omisión |
| *"¿Qué relación de contraste quieres?"* | No es negociable: **AA es el piso** |
| *"¿Qué tamaño debe tener el cuerpo de texto?"* | Tampoco: **16 px mínimo** |
| *"¿Quieres estados de carga y error?"* | Son obligatorios. No son una opción |
| *"¿Respetamos `prefers-reduced-motion`?"* | Siempre se respeta: es piso de accesibilidad, como el contraste |
| *"¿Preparamos el modo alto contraste?"* | Se prepara siempre, como el oscuro. Lo que decide el usuario es si se activa |
