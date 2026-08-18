---
name: system-design
description: "Construye un sistema de diseño completo y verificable para cualquier producto — tokens en tres niveles con modos, biblioteca de componentes, patrones, plantillas y accesibilidad WCAG AA — y lo publica a CSS, Swift, Android o Figma por MCP. Úsala SIEMPRE que el usuario mencione sistema de diseño, design system, design tokens, paleta de colores, tipografía, escala de espaciado, biblioteca de componentes, tema claro/oscuro, guía de estilo, identidad visual de un producto digital, o quiera llevar tokens y componentes a Figma. Úsala también antes de diseñar cualquier pantalla: sin sistema no hay pantalla que valga."
---

# Sistema de diseño

Construye el sistema **desde parámetros**, no desde valores sueltos, y **comprueba cada paso**.

**Sin contexto de proyecto.** Todo lo específico del producto entra por la entrevista y vive en su
configuración. Esta skill no sabe de taxis, de banca ni de comercio: sabe de sistemas de diseño.

---

## 1 · Lo que no se negocia

**1 · Se entrevista antes de construir.** Nunca se asume un color, una familia ni una escala. Si el usuario
no sabe qué responder, se le proponen opciones **renderizadas** y elige mirando — no describiendo conceptos.

**2 · Tres niveles de token, siempre.**

```
1 · primitivo    indigo.600 = #3A45C9        se llama por lo que ES
2 · semántico    accion.reposo → {indigo.600}    por lo que HACE · lleva un valor por modo
3 · componente   boton.primario.fondo → {accion.reposo}    por dónde se APLICA
```

**Un primitivo nunca se llama por su rol.** Llamarlo `acento` colapsa los niveles: el semántico sobra, se
salta, y entonces piezas sin relación comparten variable. Es el error más caro y el más común.

**3 · Nada se escribe a mano dos veces.** Un parámetro entra una vez; lo demás se deriva. Si un valor aparece
en dos archivos, uno de los dos va a quedar viejo.

**4 · Se verifica antes de entregar.** Y **cada comprobación se prueba rompiendo algo a propósito**. Una que
nunca falló no está probada: está sin usar.

**5 · La accesibilidad es piso, no meta.** Contraste, foco y estados no son mejoras posteriores: son
condiciones de entrada. `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/06-accessibility/README.md`.

---

## 2 · Cuándo se usa

| El usuario pide | Qué hacer |
|---|---|
| Crear el sistema | La entrevista completa → §3 · El procedimiento |
| Agregar un componente | §4 · Extender, sin repetir la entrevista |
| Agregar modo oscuro, un idioma, una plataforma | §4 · Extender |
| Publicar a Figma, CSS, Swift o Android | §5 · Publicar |
| Revisar un sistema existente | `${CLAUDE_SKILL_DIR}/scripts/verificar.py` y reportar |
| Definir el negocio — entidades, reglas, flujos | **La skill `domain`, no esta.** Esta hace lo visual |

---

## 3 · El procedimiento

> **Convención de salida — `output/`.** Todo lo que se genera va a `<destino>`, que es siempre
> `<proyecto>/output/`. Las carpetas del plugin (`${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`) son de
> **solo lectura**: nunca se escribe salida dentro de ellas.

### Paso 0 · Preparar el ambiente de trabajo

**Antes de construir, se preparan dos ambientes: el archivo de Figma y la propia IA.** Es un gate: si algo
falta, no se avanza a dibujar.

**Lo que la IA le dice al usuario:**

> Antes de construir, necesito que dejes el **ambiente de trabajo** listo. Son tres cosas, y podés decir
> «crealo vos» en cualquiera que no quieras hacer a mano.
>
> **1 · El archivo y el permiso** — abrí en Figma el archivo donde vamos a trabajar (o decime «crealo vos»).
> Confirmá que tu asiento es **Dev** o **Full** (si es **View**, no puedo escribir).
>
> **2 · Las páginas**, en este orden:
> 1 · Portada
> 2 · Para empezar
> 3 · <nombre de tu producto>
> 4 · Componentes
> 5 · Documentación
> 6 · Pruebas y exploración
> 7 · Archivo
>
> **3 · Los iconos** — decime para qué plataforma (web, Android, iOS) y te traigo el set **gratuito** (Lucide
> por defecto). No hace falta que los subas vos.
>
> Cuando esté, decime «listo».

**Y la IA comprueba su propio ambiente antes de seguir** (no depende del usuario):

| Requisito | Cómo se comprueba | Si falta |
|---|---|---|
| MCP de Figma conectado | ejecutar `whoami` y leer `seat` | `claude plugin install figma@claude-plugins-official` o `claude mcp add --transport http figma https://mcp.figma.com/mcp` |
| Skills de Figma instaladas | buscar `figma-use`, `figma-generate-library`, `figma-create-new-file` entre las skills disponibles | Vienen con el mismo plugin |

**Lista completa de herramientas y skills de Figma (nombres correctos):**
`${CLAUDE_SKILL_DIR}/referencias/figma-mcp.md`.

### Paso 1 · Entrevistar

**Lee `${CLAUDE_SKILL_DIR}/referencias/entrevista.md` y sigue sus bloques.** No inventes preguntas ni saltes bloques.

Reglas de la entrevista:

- **Una pregunta por vez** cuando la respuesta condiciona la siguiente; agrupadas cuando son independientes.
- **Todo tiene valor por omisión.** *"Usa el que recomiendes"* es una respuesta válida a cualquier pregunta.
- **Nunca pidas criterio de diseñador.** No preguntes *"¿qué personalidad tiene la marca?"* sin ofrecer
  opciones concretas entre las que elegir.
- **Si el usuario ya tiene colores o tipografía, se usan los suyos** — y se ajustan solo lo necesario para
  que cumplan contraste, avisando de cada ajuste.

### Paso 2 · Escribir la configuración

Dos archivos, y solo dos:

```
<destino>/marca.json        los parámetros visuales      ← ${CLAUDE_SKILL_DIR}/plantillas/marca.json
<destino>/proyecto.json     el producto y su contexto    ← ${CLAUDE_SKILL_DIR}/plantillas/proyecto.json
```

Valida contra `${CLAUDE_SKILL_DIR}/esquemas/marca.schema.json` y `${CLAUDE_SKILL_DIR}/esquemas/proyecto.schema.json` antes de seguir.

### Paso 3 · Derivar

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/derivar.py --destino <destino>
```

Produce `tokens/1-primitivos.json`, `2-semanticos.json` y `3-componentes.json`, y **comprueba el contraste en
todos los modos** — incluidos los preparados y todavía inactivos. Si falla, **no continúes**: corrige los
parámetros y vuelve a derivar.

### Paso 4 · Poblar el inventario

Copia las dos plantillas al destino:

```
${CLAUDE_SKILL_DIR}/plantillas/componentes-base.json  →  <destino>/inventario/componentes.json    22 componentes universales
${CLAUDE_SKILL_DIR}/plantillas/plantillas-base.json   →  <destino>/inventario/plantillas.json      4 plantillas universales
```

**Existen en cualquier producto**, así que no se vuelven a inventar. **Agrega solo lo que el producto necesite
de verdad**, y lo que solo sirva acá márcalo con `"universal": false` **y su motivo** — es lo que permite
después llevarse los universales a otro producto sin arrastrar lo que no sirve.

Valida contra `${CLAUDE_SKILL_DIR}/esquemas/inventario.schema.json`. El detalle del contrato, en `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/03-components/README.md`.

**Vuelve a derivar** después de poblar: el nivel 3 sale del inventario.

### Paso 5 · Verificar

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/verificar.py --destino <destino>
```

**Cero fallos o no se entrega.** Cada fallo dice qué regla incumple.

**Y una comprobación saltada no es un verde.** El guion las reporta aparte, con su motivo — «no hay patrones»,
«el proyecto no declara modelo de datos». **Léeselas al usuario**: son las preguntas que quedaron sin hacer.

Al agregar una comprobación nueva, **pruébala rompiendo algo a propósito**:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/verificar.py --destino <destino> --romper DS-C03
```

Tiene que fallar. **Una comprobación que nunca falló no está probada: está sin usar.**

**El veredicto es de la regla que se rompió, no del total** — y son tres, no dos:

| Veredicto | Qué significa | Código |
|---|---|---|
| **✓ lo detectó** | Falló **esa** comprobación, y dice cuál | `0` |
| **✗ pasó sin detectarse** | La comprobación corrió y no vio nada: **no sirve** | `1` |
| **⚠ no se pudo probar** | Está **saltada**: la prueba no corrió. **No es un verde** | `2` |

> **Un fallo ajeno no prueba nada.** Si el veredicto mirara el total de fallos, una comprobación rota daría
> verde porque falló su vecina — y una saltada daría verde sin haber corrido nunca.

### Paso 6 · Publicar

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/construir.py --destino <destino> --salidas css,figma
```

**Regla de oro — no re-traducir nombres.** La IA lee `figma-variables.json` y pasa sus campos **tal cual** a
`use_figma`: nombres con `/` (ya traducidos desde el `.` del JSON), alcances, tipos y sintaxis por plataforma.
La traducción la hace `construir.py` leyendo `referencias/figma-api.json`; **la IA nunca adivina el formato,
solo pega los valores ya correctos.** Ver §5 · Publicar para el puente con Figma.

---

## 4 · Extender

**Nunca se rehace el sistema para agregar algo.**

| Qué se agrega | Dónde | Después |
|---|---|---|
| Un componente | `inventario/componentes.json` | `verificar.py` |
| Un modo — oscuro, alto contraste | `marca.json` → `modos.activos` | `derivar.py` y `verificar.py` |
| Un idioma | `proyecto.json` → `idiomas` | `construir.py` |
| Una plataforma de salida | `proyecto.json` → `salidas` | `construir.py` |
| Un acento adicional | `marca.json` → `acentos_extra`, **con su motivo** | `derivar.py` |

**Un acento adicional exige justificación escrita.** Si el segundo color no codifica un significado que el
usuario deba aprender —origen contra destino, entrada contra salida—, no es un acento: es decoración, y se
rechaza.

### Diseñar una pieza nueva

**Cuando hay que *crear* un componente o patrón** —no solo agregar una variante— se escribe la propuesta antes
de tocar el inventario:

1. **Problema** — qué necesidad o hueco cubre.
2. **Patrones existentes** — cuál se parece, qué comparte, y **por qué no alcanza**.
3. **Diseño propuesto** — API/props, variantes, estados, tokens que usa.
4. **Accesibilidad** — rol, teclado, lector de pantalla.
5. **Preguntas abiertas** — lo que necesita revisión de diseño.

La documentación completa de una pieza la hace la skill `document`; acá se decide si existe y con qué contrato
entra al inventario.

---

## 5 · Publicar

`${CLAUDE_SKILL_DIR}/scripts/construir.py` genera desde los tokens:

| Salida | Qué produce |
|---|---|
| `css` | Propiedades personalizadas, con un bloque por modo |
| `figma` | Colecciones de variables, con modos y sintaxis por plataforma |
| `swift` · `android` | Constantes nativas |
| `lienzo` | **El documento neutral que consume un MCP de diseño** |
| `galeria` | *(Opcional, fuera del flujo por defecto.)* Un HTML por componente, para cuando no se dibuja en Figma |

### El puente con un MCP

**La skill no asume qué MCP hay.** Produce un **documento de lienzo** neutral y lo traduce a lo que la
herramienta disponible acepte.

**Antes de dibujar:**

1. Averigua qué herramientas de diseño hay disponibles en la sesión.
2. **Comprueba si escriben o solo leen.** Muchos puentes de diseño solo envían contexto al agente; no todos
   crean nodos en el lienzo.
3. **Y comprueba el permiso, no solo la herramienta.** Un asiento de solo lectura deja las herramientas de
   escritura visibles y **falla a mitad de la construcción**.
4. **Dilo antes de intentarlo.** Si solo lee, no prometas dibujar: entrega el documento de lienzo y las
   variables, que sí se pueden importar.

**Si el puente es el MCP de Figma —comprobado, escribe—** hay un prerrequisito que no se salta: **cargar
`figma-use` antes de cada `use_figma`**, y `figma-generate-library` junto a ella al construir tokens y
componentes. El detalle, en `${CLAUDE_SKILL_DIR}/referencias/puentes.md` §El puente de Figma.

El detalle del contrato y el orden de creación, en `${CLAUDE_SKILL_DIR}/referencias/puentes.md`.

---

## 6 · Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Primitivos con nombre de rol** | Existe un token llamado `acento` o `primario` | Renombrar a su escala: `indigo.600` |
| **Saltarse el nivel semántico** | Un componente cita un primitivo | Crear el rol y apuntar ahí |
| **Modos agregados después** | La estructura de tokens es plana | Los modos van en el nivel 2 **desde el primer día**, aunque solo uno esté activo |
| **Estados olvidados** | Un componente sin `foco`, sin `cargando` | Ver `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/03-components/README.md` |
| **Contraste comprobado al final** | La paleta se eligió mirando, sin medir | Se mide **al definir el token** |
| **Demasiadas variantes** | Doce variantes de botón | Tres o cuatro cubren cualquier producto |
| **Valores fuera de escala** | Un `13px` suelto entre múltiplos de 8 | Solo pasos de la escala |

---

## 7 · Referencias

Léelas cuando la tarea lo pida, no antes:

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/referencias/entrevista.md` | **Siempre al crear.** Las preguntas y sus valores por omisión |
| `${CLAUDE_SKILL_DIR}/referencias/tokens.md` | Al derivar, o cuando algo del encadenamiento no cuadre |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/03-components/README.md` | Al declarar o revisar un componente |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/06-accessibility/README.md` | Al elegir color, al declarar estados, antes de entregar |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/09-rules/README.md` | **Todas las reglas `DS-xxx` con su origen.** Consulta puntual: cuando haya que justificar algo, o al agregar una regla |
| `${CLAUDE_SKILL_DIR}/referencias/figma-mcp.md` | **Al preparar el ambiente y antes de escribir contra Figma.** Las herramientas MCP y las skills de Figma, con sus nombres correctos y cuándo cargar cada una |
| `${CLAUDE_SKILL_DIR}/referencias/puentes.md` | **Al publicar, y antes de prometer que se dibuja en un lienzo** |
| `${CLAUDE_SKILL_DIR}/referencias/figma-api.json` | **Antes de escribir una sola línea contra la API de Figma.** Los alcances, tipos, plataformas y reglas de nombre que acepta de verdad, cada uno con si se verificó contra el servidor o solo se leyó |

> **Sobre `figma-api.json`:** lo leen `construir.py` y `verificar.py` del mismo archivo,
> así que no hace falta traducir nada al consumir `figma-variables.json` — sus campos ya
> vienen en el vocabulario de Figma. Se consulta **cuando haya que escribir código nuevo
> contra la API**, para no volver a descubrir a golpes que la plataforma es `iOS` y no
> `IOS`, o que un alcance válido puede ser imposible para el tipo de la variable.

---

## 8 · Al terminar

Reporta al usuario, en este orden:

1. **Qué se construyó** — cuántos tokens por nivel, cuántos componentes, qué modos.
2. **Qué se verificó** — cuántas comprobaciones y cuántos fallos.
3. **Qué se ajustó solo y por qué** — todo color que se oscureció para cumplir contraste va nombrado.
4. **Qué quedó pendiente** — lo que el usuario dejó para después, sin disfrazarlo de terminado.
5. **Dónde mirarlo** — el resultado quedó dibujado en Figma, en el archivo del usuario.
