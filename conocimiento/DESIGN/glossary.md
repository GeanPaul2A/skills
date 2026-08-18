# Glosario · DESIGN

**Los términos técnicos van en inglés —como los usan los libros y la herramienta— con su glosa en español.**
Ninguna sigla se usa sin desarrollar.

---

## A

**Alcance** *(scope)* — Qué propiedades puede pintar una variable, y si aparece como opción para quien diseña.
Es lo que permite **ocultar los primitivos** para que solo se usen como alias. Ver `08-figma-bridge` §8.4.

**Alias** — Un token que apunta a otro token en lugar de a un valor. Es lo que encadena los tres niveles.

**APCA** — *Advanced Perceptual Contrast Algorithm*, algoritmo perceptual avanzado de contraste. Predice la
legibilidad con más precisión que WCAG, sobre todo en colores intermedios. **Todavía no es la norma citada por
las regulaciones.**

**ARIA** — *Accessible Rich Internet Applications*, aplicaciones de internet enriquecidas y accesibles.
Especificación del W3C que agrega semántica al código para que las tecnologías de asistencia entiendan la
interfaz. Ver `06-accessibility` §6.6.

**Atomic Design** — Metodología de Brad Frost que organiza los componentes en átomos, moléculas, organismos,
plantillas y páginas. **Esta KB no la usa**; usa la alternativa de cuatro niveles. Ver `03-components` §3.2.

**Auto Layout** *(disposición automática)* — El contenedor dinámico de Figma. **Corresponde 1 a 1 con Flexbox**
en código. Ver `04-auto-layout`.

**`axe-core`** — Biblioteca libre de pruebas de accesibilidad. Se integra en la tubería de integración continua
para bloquear publicaciones con fallos.

## C

**Code Connect** — Función de Figma que enlaza el componente de código real con el de diseño, para que quien
programa copie el componente listo. Requiere plan Organización o Empresarial.

**Colección** *(collection)* — Grupo de variables de Figma que comparten propósito y modos. Esta KB usa seis.

**Componente** — Pieza reutilizable con estructura, jerarquía, contenido y disposición. **No es lo mismo que un
estilo**, que solo aplica propiedades.

**Componente principal** *(main component)* — La fuente única, marcada con rombo relleno **◆**. Sus copias son
**instancias**, marcadas con rombo hueco **◇**.

## D

**Design Lint** — Complemento que detecta colores y textos sin estilo vinculado, y radios inconsistentes. **Es
lo más parecido a un verificador que ofrecen los libros, y se corre a mano.**

**Dev Mode** *(modo de desarrollo)* — Vista de Figma que muestra valores exactos, nombres de variable y
fragmentos de código. Requiere plan de pago.

## E

**Estado de contenido** — Carga, vacío o error. Se distingue del **estado de interacción** —reposo, sobre,
presionado, foco, deshabilitado—.

**Estilo** *(style)* — Conjunto de propiedades visuales guardado con nombre. En la arquitectura de esta KB los
estilos son **la interfaz pública** y las variables la lógica interna.

## F

**Fill** *(llenar el contenedor)* — Comportamiento de Auto Layout: la caja ocupa el espacio disponible.

**Fixed** *(fijo)* — Comportamiento de Auto Layout: tamaño invariable. **Nunca en el eje de un texto
traducible.**

**Flexbox** — El sistema de disposición de CSS al que corresponde Auto Layout.

## H

**Hug** *(abrazar el contenido)* — Comportamiento de Auto Layout: la caja se encoge a lo que contiene. **Es el
que resuelve la expansión del texto entre idiomas.**

## I

**Instancia** — Copia enlazada de un componente principal. Sobreescribir una propiedad **la desconecta solo a
ella**; el resto sigue sincronizado.

## M

**MCP** — *Model Context Protocol*, protocolo de contexto de modelo. Puente entre una herramienta y un agente.
El servidor de Figma **envía contexto de diseño al agente**; que también escriba en el lienzo está sin
confirmar.

**Modo** *(mode)* — Columna de valores alternativos dentro de una colección: claro y oscuro, móvil y
escritorio, un idioma y otro. **Límite del plan Profesional: cuatro.**

## P

**Patrón** — Secuencia de componentes con un propósito **y con su origen de datos declarado**. Está entre el
componente y la plantilla.

**Primitivo** — Token de nivel 1: el valor crudo, sin significado. **Va oculto**, para que solo se use como
alias.

**Punto de corte** *(breakpoint)* — El ancho en que la disposición cambia de forma.

## S

**Semántico** — Token de nivel 2: dice **para qué sirve** el valor. `color.action.default` es semántico;
`color.brand.500` no.

**Style Dictionary** — Herramienta estándar que convierte tokens en JSON a variables CSS, Swift de iOS o XML de
Android.

**Superficie continua** *(no textual)* — Región que el usuario lee **mirando y no leyendo**: un mapa, un
lienzo, la vista de una cámara, un visor 3D, una línea de tiempo. **Nunca puede ser el único portador de una
información necesaria** (`DS-P05`): el lector de pantalla no la lee, y es lo primero que falla con mala
conexión. Ver `05-patterns` §5.5.

## T

**Token** — Una decisión de diseño con nombre, transferible a código. **Independiente de la herramienta.**

**Token de componente** — Token de nivel 3: dice **dónde se aplica**. `button.primary.background`.

**Token compuesto** — Un token que encapsula varios valores como unidad — familia, tamaño, peso e interlineado
en uno solo. **Las variables de Figma no los soportan.**

**Token Studio** — Plataforma de gestión de tokens que sincroniza con repositorios. Su versión gratuita no
admite temas ni carpetas avanzadas.

## V

**Variable** — Valor único de Figma —color, número, booleano o cadena— que se puede referenciar y encadenar.

**Variante** *(variant)* — Versión de un componente dentro de un conjunto. Se agrupan solo cosas que **difieren
de forma predecible y limitada**.

## W

**WCAG** — *Web Content Accessibility Guidelines*, pautas de accesibilidad para el contenido web. Tres niveles:
A, AA y AAA. **El objetivo de esta KB es AA**, con AAA en lo crítico.
