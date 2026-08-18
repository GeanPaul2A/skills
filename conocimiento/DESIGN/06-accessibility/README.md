# 06 · Accessibility (Accesibilidad)

**No es un requisito legal ni una casilla: es una escala, y cada paso beneficia a todos los usuarios.** Esta
sección fija los mínimos verificables y los criterios de aceptación por tipo de componente.

**Clasificación:** `[Book 1, cap. 7]` la sección completa · `[Book 2, cap. 5]` el comprobador incorporado ·
`[Ext]` la aplicación a las condiciones reales de uso.

---

## Índice

1. [Accesibilidad no es binaria](#61--accesibilidad-no-es-binaria)
2. [Por qué esto pesa más de lo que parece](#62--por-qué-esto-pesa-más-de-lo-que-parece)
3. [Contraste](#63--contraste)
4. [Tipografía](#64--tipografía)
5. [Teclado y foco](#65--teclado-y-foco)
6. [Lector de pantalla](#66--lector-de-pantalla)
7. [Movimiento](#67--movimiento)
8. [Criterios de aceptación por componente](#68--criterios-de-aceptación-por-componente)
9. [Cuándo se comprueba](#69--cuándo-se-comprueba)
10. [Reglas de esta sección](#610--reglas-de-esta-sección)

---

## 6.1 · Accesibilidad no es binaria `[Book 1, cap. 7]`

> *"La accesibilidad **no es binaria — es una escala**. No se trata simplemente de 'la tenemos' o 'no la
> tenemos'. Se trata de qué tan a fondo la abordamos, y se puede construir de forma incremental."*

**Y el error de encuadre que el propio autor confiesa:**

> *"La accesibilidad **no es solo discapacidades permanentes**. También abarca condiciones temporales —un brazo
> roto— y **limitaciones situacionales**: luz solar intensa, trabajar con guantes, usar el teléfono con una
> mano mientras cargas café o las compras, o mi favorita: **ir sentado en un transporte público con
> baches**."*

**OBLIGATORIO** — el nivel objetivo es **WCAG 2.1 AA**, con AAA en lo crítico.

> `[Book 1, cap. 7]`: *"Recomendaría enfocarse en el cumplimiento AA como línea base, con AAA para componentes
> críticos."*
>
> **Sobre APCA:** predice la legibilidad con más precisión, sobre todo en colores intermedios, **pero WCAG 2.1
> AA sigue siendo la norma que las regulaciones citan**. Se diseña contra WCAG; APCA sirve para desempatar.

---

## 6.2 · Por qué esto pesa más de lo que parece `[Ext]`

**El libro cuenta una práctica que no es opcional en ningún producto móvil:**

> *"Cuando diseñaba activamente, **siempre tenía dispositivos de referencia al lado**. Para escritorio, el
> monitor Full HD más barato conectado junto a mi pantalla principal. Para aplicaciones móviles, **un Android
> económico y un iPhone SE** cerca, para comprobar siempre la 'realidad' de mis diseños — no cómo se ven en mi
> dispositivo de gama alta, donde todo se ve increíble porque costó unos miles de dólares."*

### Las cuatro condiciones reales de uso

**Valen para cualquier producto móvil, sin importar a qué se dedique:**

| Condición | Consecuencia de diseño |
|---|---|
| **En la calle, con sol** | El contraste que se ve bien en interiores **desaparece afuera** |
| **Teléfono de gama baja** | Pantalla más apagada y de menor densidad |
| **Ahorro de batería activado** | El sistema **atenúa la pantalla** |
| **Una sola mano**, cargando algo | Los controles principales van **al alcance del pulgar** |

### Y la quinta, que depende del actor

**OBLIGATORIO** — cuando un actor usa el producto **en una condición distinta a la de estar sentado y
atento** —de pie, en movimiento, con guantes, con las manos ocupadas—, su aplicación exige **objetivos
táctiles más grandes y menos densidad** que la del resto.

> **Es un parámetro, no una constante.** El objetivo táctil mínimo se declara **por actor**, y el que sube
> lo hace con su motivo escrito. Un producto con un solo actor sentado usa el mínimo de §6.5 y ya.

---

## 6.3 · Contraste

### Los mínimos

| Qué | Relación mínima | Nivel |
|---|---|---|
| **Texto normal sobre su fondo** | **4.5 : 1** | AA |
| Texto grande (≥ 24 px, o ≥ 19 px en negrita) | 3 : 1 | AA |
| **Indicador de foco contra el fondo** | **3 : 1** | AA |
| Componentes de interfaz y gráficos con significado | 3 : 1 | AA |
| Texto normal, nivel reforzado | 7 : 1 | AAA |

### Se comprueba al definir el token, no al terminar la pantalla

**`[Book 1, cap. 7]` — es el punto donde el libro es más insistente:**

> *"Cuando implementas los estándares WCAG **directamente en tus tokens**, resuelves los problemas de
> accesibilidad **en su origen**, eliminando la necesidad de volver a revisarlos y arreglarlos después."*

Y advierte contra lo contrario:

> *"Diseñábamos algo y después lo contrastábamos contra las pautas WCAG, intentando 'arreglar' los problemas
> más grandes. **Ese enfoque de remiendo no es ideal ni sostenible.** Genera más trabajo, a menudo compromete
> la visión original, y con frecuencia produce soluciones de accesibilidad que se sienten pegadas encima.**"*

**Figma trae el comprobador en el propio panel de color** `[Book 2, cap. 5]`, con la lectura AA/AAA en tiempo
real. **No hay excusa para no mirarlo.**

### El color nunca es el único portador

**OBLIGATORIO** — ninguna información se comunica **solo** con color.

> `[Book 1, cap. 7]`: *"Para los campos obligatorios, usa **múltiples indicadores**… depender solo del color
> —como un asterisco rojo— **no es suficiente**. Evita indicar campos obligatorios solo con negrita o
> diferencias de color."*

**El caso típico:** dos elementos de una lista que difieren en urgencia, disponibilidad o estado **no pueden
distinguirse solo porque uno esté en verde y el otro en rojo**. Llevan el dato en texto, y un icono si hace
falta.

---

## 6.4 · Tipografía `[Book 1, cap. 7]`

| Qué | Regla |
|---|---|
| **Tamaño del cuerpo** | **16 px mínimo**, y legible al **ampliar al 200 %** |
| **Interlineado del cuerpo** | **entre 1.4 y 1.6** |
| **Familia** | Clara en tamaños pequeños. **Nada decorativo para texto corrido** |
| **Espacio entre párrafos** | Suficiente. *"Los bloques densos son más difíciles de recorrer"* |

### La prueba del 200 % `[Book 1, cap. 7]`

**OBLIGATORIO** — toda pantalla se revisa con el texto al doble.

> *"Una de mis costumbres raras es que en el metro nunca uso el teléfono; miro cómo trabajan y juegan los
> demás. Muy a menudo ves gente mayor con configuraciones que hacen su texto mucho más grande, y **detectas los
> problemas enseguida**. Por ejemplo, en muchas aplicaciones de mensajería los nombres **empiezan a cortarse
> con '…'** cuando el texto se agranda."*

**OBLIGATORIO** — todo componente que muestre un valor de longitud variable **declara su punto de rotura**:
el nombre corto cabe al 200 %; el nombre completo, no. **El componente tiene que decir qué hace ahí** —
truncar, envolver o bajar de tamaño— y no descubrirlo en producción.

---

## 6.5 · Teclado y foco `[Book 1, cap. 7]`

### La regla que lo resume

> *"**Si una acción se puede hacer con el ratón, debe poder hacerse también con el teclado**, y cualquier
> elemento interactivo debe recibir un indicador de foco visible al navegar con teclado."*

### Las cinco preguntas de la prueba

**Se hace con la tecla Tab, y toma dos minutos:**

1. ¿se alcanzan **todos** los elementos interactivos solo con teclado?
2. ¿el orden es **lógico y sigue el flujo visual** de la pantalla?
3. ¿los indicadores de foco **se ven** en todos ellos?
4. ¿se activan botones, enlaces y campos con **Enter** o **Espacio**?
5. ¿se cierran ventanas y desplegables con **Esc**?

**OBLIGATORIO** — el orden de tabulación se documenta en las pantallas con estructura no obvia. **El caso más
común es la hoja de contenido sobre una superficie continua** —mapa, lienzo, visor—, donde el orden visual y
el orden del documento no coinciden.

---

## 6.6 · Lector de pantalla `[Book 1, cap. 7]`

> *"Los lectores de pantalla hacen exactamente lo que su nombre dice. Pero no es tan simple, porque **solo
> pueden trabajar con lo que tú les des**."*

### Texto alternativo

**OBLIGATORIO** — todo icono e imagen con significado lleva texto alternativo que **describe el significado o
la función**, no la apariencia.

| Mal | Bien |
|---|---|
| *"Icono de equis"* | *"Cerrar el panel de ajustes"* |
| *"Descripción de imagen: auto"* | *"Kia Rio blanco, placa BCD-456"* |

> **Y una advertencia concreta:** no empezar con *"Icono…"* ni *"Imagen…"*, porque **el lector ya anuncia el
> tipo de elemento antes de leer tu texto**, y se produce una redundancia.

**Las imágenes decorativas llevan texto alternativo vacío** `[Book 1, cap. 8]`.

### Estructura semántica

| Regla | Detalle |
|---|---|
| **Un solo H1 por pantalla**, seguido de H2 como encabezados de sección | *"Un error común es usar el estilo 'Encabezado 1' repetidamente solo porque se ve bien. Eso confunde a los lectores de pantalla"* |
| **Agrupar el contenido relacionado** | Etiqueta, campo y mensaje de error **juntos**, y documentado que van agrupados en el código |
| **Etiqueta persistente y visible en todo campo** | **Nunca marcador de posición como etiqueta** |

> **Sobre el marcador de posición**, el libro es tajante: *"Este enfoque falla no solo desde la accesibilidad
> sino desde los principios generales de experiencia. **Los marcadores desaparecen cuando el usuario empieza a
> escribir**, dejándolo sin contexto si se distrae."*

### ARIA, y hasta dónde llega el diseño

**Es responsabilidad del desarrollo**, pero el diseño declara qué hace falta:

| Concepto | Para qué |
|---|---|
| **Puntos de referencia** | Definen regiones — navegación, contenido principal, búsqueda |
| **Estados y propiedades** | Comunican el estado actual — expandido/plegado, marcado/sin marcar |
| **Regiones en vivo** | **Anuncian cambios dinámicos** sin que el usuario tenga que ir a buscarlos |

> **La tercera es la que más se olvida:** cuando llega un elemento nuevo a una lista que se actualiza sola,
> **el lector de pantalla tiene que anunciarlo**. Sin región en vivo, la pantalla cambia en silencio y quien
> no la ve nunca se entera.

---

## 6.7 · Movimiento `[Book 1, cap. 7]`

> *"Si usas tokens para estandarizar animaciones, crea **pautas más estrictas** para velocidad y movimiento
> complejo. Aunque las animaciones complejas puedan verse 'geniales', **son difíciles de hacer inclusivas**.
> Considera ofrecer alternativas de movimiento reducido, o **una opción para desactivar todas las animaciones
> con un solo clic**."*

**OBLIGATORIO** — todo movimiento tiene alternativa reducida. El sistema respeta la preferencia del dispositivo.

**Y la distinción que decide qué se puede simplificar** `[Book 1, cap. 8]`:

| Tipo | Ejemplo | Se puede simplificar |
|---|---|---|
| **Esencial** | El foco salta al primer campo con error y lo marca | **No.** Comunica estado del sistema |
| **De adorno** | Una transición agradable entre pantallas | **Sí** |

---

## 6.8 · Criterios de aceptación por componente `[Book 1, cap. 7]`

**El libro los entrega listos para copiar a un ticket.** Esta KB los adopta tal cual.

### Botón

- accesible por teclado — **Tab** enfoca, **Enter** o **Espacio** activa
- el estado de foco es visible con **3:1** contra el fondo
- el texto tiene **4.5:1 en todos sus estados**
- el lector anuncia **su propósito y su estado actual**
- lleva los atributos ARIA correspondientes si alterna contenido

### Formulario

- **todos los campos tienen etiqueta persistente y visible**
- los obligatorios se indican con **señal visual y textual**
- los mensajes de error **se anuncian al lector cuando aparecen**
- **se puede completar entero solo con teclado**
- la validación **no depende solo del color**

### Diálogo

- **el foco queda atrapado dentro** mientras está abierto
- **Esc** lo cierra
- **el foco vuelve al elemento que lo abrió** al cerrarse
- se anuncia al lector al abrirse
- **el contenido de fondo se oculta al lector** mientras está activo

---

## 6.9 · Cuándo se comprueba `[Book 1, cap. 7]`

**La rutina del libro, en cuatro momentos:**

| Momento | Qué se hace |
|---|---|
| **Al diseñar** | Comprobador de contraste y simulador de daltonismo |
| **Antes de entregar** | La lista de comprobación de componentes |
| **Después de desarrollar** | Prueba de teclado y de lector de pantalla sobre lo construido |
| **Periódicamente** | Revisión de todo el producto |

### En código, la herramienta es `axe-core`

> *"Lo que hace a **axe-core** particularmente valioso es que los desarrolladores pueden configurarlo para
> **comprobar automáticamente cada cambio de código** antes de que salga a producción. Piénsalo como un
> corrector ortográfico, pero de accesibilidad. Si el código tiene problemas, **el sistema puede impedir que la
> actualización se publique** hasta que se arreglen."*

**RECOMENDADO** — cuando la aplicación exista, `axe-core` entra a la tubería de integración. **Es la única
forma de que la accesibilidad no se salte cuando aprieta la fecha.**

### Y la advertencia final, que vale para todo el proyecto

> *"Un archivo de Figma preparado increíblemente, con todos los estados, la documentación, el texto alternativo
> y las consideraciones de accesibilidad, **no significa nada sin una implementación adecuada**."*

---

## 6.10 · Reglas de esta sección

| Regla | Enunciado | Nivel | Origen |
|---|---|---|---|
| **`DS-A01`** | El nivel objetivo es **WCAG 2.1 AA**; AAA en lo crítico | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A02`** | Texto **4.5:1**, foco **3:1**, comprobado **al definir el token** | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A03`** | **Ninguna información se comunica solo con color** | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A04`** | Todo campo lleva **etiqueta persistente y visible**; el marcador de posición **nunca** hace de etiqueta | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A05`** | **Un solo H1 por pantalla**, con jerarquía descendente | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A06`** | Todo icono o imagen con significado lleva **texto alternativo de función**, no de apariencia | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A07`** | Lo que se puede con ratón **se puede con teclado**, con foco visible | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A08`** | Toda pantalla se revisa **al 200 % de texto** | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A09`** | Todo movimiento tiene **alternativa reducida** | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A10`** | Los cambios dinámicos se anuncian con **región en vivo** | OBLIGATORIO | `[Book 1, cap. 7]` |
| **`DS-A11`** | El diseño se revisa en **un dispositivo de gama baja**, no solo en el de trabajo | RECOMENDADO | `[Book 1, cap. 7]` |
| **`DS-A12`** | `axe-core` en la tubería de integración cuando exista la aplicación | RECOMENDADO | `[Book 1, cap. 7]` |
