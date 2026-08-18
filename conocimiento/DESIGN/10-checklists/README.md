# 10 · Checklists (Listas de comprobación)

**Lo que hay que responder antes de dar algo por terminado.** Cada punto cita la regla que lo respalda, y las
listas recogen sobre todo **las reglas que el verificador no puede comprobar solo**.

**Clasificación:** `[Libro 1, capítulo 8]` la práctica de la lista y sus tres bloques · `[Libro 1, capítulo 7]` la lista
de accesibilidad · `[Extensión G1]` la separación entre lo automático y lo manual.

---

## Índice

1. [Cómo se usan](#101--cómo-se-usan)
2. [Antes de generar una pantalla](#102--antes-de-generar-una-pantalla)
3. [Antes de dar una pantalla por terminada](#103--antes-de-dar-una-pantalla-por-terminada)
4. [Antes de publicar un componente](#104--antes-de-publicar-un-componente)
5. [Antes de cerrar los fundamentos](#105--antes-de-cerrar-los-fundamentos)
6. [Al revisar lo construido](#106--al-revisar-lo-construido)

---

## 10.1 · Cómo se usan

**Primero corre el verificador; la lista es lo que queda después.**

```
verificar.py           →  las 37 reglas que se comprueban solas
lista de comprobación  →  las que necesitan criterio o una mirada
```

**OBLIGATORIO** — una pantalla no se cierra sin las dos cosas. **Y quién marcó la lista queda registrado**, por
la misma razón que el modelo de datos registra quién firmó cada aprobación.

> `[Libro 1, capítulo 8]`: *"Crea listas simples que los desarrolladores puedan usar para autoevaluar su trabajo
> antes de pedir revisión de diseño. Este enfoque **detecta los problemas obvios temprano** y hace la revisión
> más eficiente para todos."*

---

## 10.2 · Antes de generar una pantalla

**Se responde antes de dibujar nada.** Si alguna queda sin respuesta, **la pantalla todavía no se puede
generar**.

### El propósito

- [ ] ¿**a qué patrón pertenece** esta pantalla? `DS-P01`
- [ ] ¿**qué hace el usuario acá** que no pueda hacer en otra?
- [ ] ¿en qué **estado del modelo** se encuentra al llegar, y en cuál queda al salir? `DS-P06`

### Los datos

- [ ] ¿**qué tablas** alimentan lo que se muestra? `DS-P01`
- [ ] ¿**cada dato tiene una columna** que lo respalde? `DS-P02`
- [ ] ¿qué se muestra si **un dominio ajeno no responde**? `DS-P04`
- [ ] ¿cuál es el **valor más largo y el más corto** que cada campo admite? `DS-L06`

### Las reglas del dominio

- [ ] ¿**qué reglas de dominio condicionan** esta pantalla? `DS-P01`
- [ ] ¿alguna de ellas **prohíbe algo** que el diseño quiere permitir?

### Las piezas

- [ ] ¿**qué componentes existentes** resuelven esto? `DS-C01`
- [ ] ¿hace falta uno nuevo, o **basta con una variante** de uno que ya existe? `DS-C09`
- [ ] ¿qué **plantilla** le corresponde?

> **La pregunta que más ahorra:** *¿hace falta uno nuevo?* — `[Libro 1, capítulo 6]` nombra *"crear 15 variantes de
> botón cuando en realidad solo necesitas 3"* entre los errores de principiante.

---

## 10.3 · Antes de dar una pantalla por terminada

### Sistema

- [ ] ¿**cero valores en crudo** — color, espaciado, tamaño, radio? `DS-T07`
- [ ] ¿ningún componente referencia un **primitivo** directamente? `DS-T02`
- [ ] ¿todo contenedor usa **Auto Layout**? `DS-L01`
- [ ] ¿la estructura son **marcos**, no grupos? `DS-L04`

### Estados

- [ ] ¿están los estados de **carga, vacío y error**? `DS-C03`
- [ ] ¿**al menos un estado es un fallo**? `DS-P03`
- [ ] ¿todo elemento interactivo tiene **foco visible**? `DS-C02`
- [ ] ¿el estado deshabilitado **explica por qué** lo está?

### Contenido

- [ ] ¿se probó con el **texto más largo** que la tabla admite? `DS-L06`
- [ ] ¿se probó con la **lista vacía** y con la lista llena?
- [ ] ¿ningún texto de interfaz está **escrito dentro de la pantalla** en vez de venir de `Copy`?

### Accesibilidad

- [ ] ¿**contraste** 4.5:1 en texto y 3:1 en foco? `DS-A02`
- [ ] ¿**ninguna información depende solo del color**? `DS-A03`
- [ ] ¿todo campo tiene **etiqueta persistente y visible**? `DS-A04`
- [ ] ¿**un solo H1**, con jerarquía descendente? `DS-A05`
- [ ] ¿los iconos con significado llevan **texto alternativo de función**? `DS-A06`
- [ ] ¿se recorre entera **solo con teclado**, en orden lógico? `DS-A07`
- [ ] ¿se revisó al **200 % de texto** sin que nada se corte? `DS-A08`
- [ ] ¿los cambios dinámicos se **anuncian**? `DS-A10`
- [ ] ¿se miró en un **dispositivo de gama baja**? `DS-A11`

### Superficie continua `[Extensión G4]` · *solo si la pantalla tiene una*

- [ ] ¿**la superficie deja de ser el único portador** de lo necesario? `DS-P05`
- [ ] ¿qué muestra cuando **deja de actualizarse**?
- [ ] ¿los controles principales quedan **al alcance del pulgar**?

### Navegación

- [ ] ¿**cada botón lleva a alguna parte**?
- [ ] ¿hay **salida** de esta pantalla en todos sus estados?

---

## 10.4 · Antes de publicar un componente

- [ ] ¿tiene su entrada en el **inventario**, con variantes, tamaños y estados? `DS-C01`
- [ ] ¿tiene **descripción**: cuándo usarlo y cuándo no? `DS-C05`
- [ ] ¿están **todos los estados de interacción**, incluido el foco? `DS-C02`
- [ ] ¿están los **tres estados de contenido**, si depende de una respuesta? `DS-C03`
- [ ] ¿usa **solo tokens semánticos o de componente**? `DS-T02`
- [ ] ¿sus **auxiliares** están prefijados con punto? `DS-C04`
- [ ] ¿su **nombre deriva de la tabla** que lo alimenta? `DS-H03`
- [ ] ¿pasa sus **criterios de aceptación** de accesibilidad? `06-accessibility` §6.8
- [ ] ¿vive en el **marco que le corresponde** dentro de su página? `DS-C06`
- [ ] ¿**no duplica** algo que ya existe? `DS-C09`

### Y la pregunta que revela una variante faltante

- [ ] ¿**alguien tuvo que desvincular una instancia** para conseguir algo? `DS-C08`

> `[Libro 1, capítulo 5]`: *"Si ves un número grande de componentes desvinculados, tienes un problema. Intenta
> descubrir por qué los diseñadores están desvinculando tus componentes. **Quizá te falta una variante** — eso
> debería ser una señal para repriorizar tu hoja de ruta."*

---

## 10.5 · Antes de cerrar los fundamentos

**Se recorre una sola vez, al terminar la etapa 2.**

### La identidad

- [ ] ¿están escritos los **tres adjetivos** del producto? `01-foundations` §1.9
- [ ] ¿la paleta **los sostiene** al mirarla completa?
- [ ] ¿la decisión de acercarse o alejarse de la competencia **quedó registrada** como decisión de negocio?

### Las escalas

- [ ] ¿la escala de espaciado tiene **base 8 y entre cuatro y seis pasos**? `DS-F06`
- [ ] ¿la escala de radios **crece de forma monótona** con el tamaño?
- [ ] ¿el radio completo quedó **solo para lo que no es un control**? `DS-F07`
- [ ] ¿hay **tres niveles de elevación**, no más?

### El texto

- [ ] ¿el cuerpo **no baja de 16 px**? `DS-F03`
- [ ] ¿el interlineado del cuerpo está **entre 1.4 y 1.6**? `DS-F03`
- [ ] ¿los estilos se **nombran con barra**? `DS-F04`
- [ ] ¿se probó la escala **al 200 %**?

### El color

- [ ] ¿**cada par texto/fondo pasó el comprobador**? `DS-F05`
- [ ] ¿hay **un solo acento**, o el segundo codifica un significado declarado? `DS-F11`
- [ ] ¿los grises son **neutros**, salvo decisión explícita?

### Los tokens

- [ ] ¿existen **los tres niveles**? `DS-T02`
- [ ] ¿`Primitives` está **oculta y sin alcance**? `DS-T03`
- [ ] ¿cada variable publicada tiene su **sintaxis para las tres plataformas**? `DS-T05`
- [ ] ¿se siguió el orden **color → espaciado → tipografía**? `DS-T06`

---

## 10.6 · Al revisar lo construido

*Fuente: `[Libro 1, capítulo 8]`*

**Los tres bloques del libro, tal como los da**, para contrastar el código contra el diseño.

### Fidelidad visual

- [ ] ¿tipografías, tamaños y pesos correctos?
- [ ] ¿espaciado consistente con la especificación?
- [ ] ¿**los colores coinciden exactamente** con el sistema?
- [ ] ¿imágenes bien dimensionadas y optimizadas?
- [ ] ¿iconos y gráficos se muestran correctamente?

### Interacción

- [ ] ¿funcionan los estados — sobre, foco, activo, deshabilitado?
- [ ] ¿**los estados de carga están implementados** correctamente?
- [ ] ¿las animaciones respetan **tiempo y curva**?
- [ ] ¿**los estados de error están bien diseñados y son funcionales**?
- [ ] ¿la navegación por teclado funciona con fluidez?

### Responsivo

- [ ] ¿la disposición funciona en distintos tamaños?
- [ ] ¿los **objetivos táctiles** tienen tamaño adecuado en móvil?
- [ ] ¿los componentes se adaptan al cambiar el contenido?
- [ ] ¿los **puntos de corte** están implementados como se diseñaron?

### Y una pregunta que el libro insiste en hacer

> *"Si encuentras inconsistencias, **pregunta a los desarrolladores por qué lo implementaron distinto**. ¿Es un
> malentendido o una limitación técnica? Esa es una diferencia enorme en cómo abordas el problema."*

**Y cuando la respuesta es una limitación técnica, se documenta** `[Libro 1, capítulo 8]`: *"Cuando las
restricciones técnicas exigen cambios respecto del diseño original, documenta esas decisiones con claridad.
**Esta documentación evita que las mismas discusiones se repitan.**"*
