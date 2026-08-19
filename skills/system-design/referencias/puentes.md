# Puentes · llevar el sistema a una herramienta de diseño

**La fuente de verdad es el JSON. La herramienta de diseño es una salida más** — DS-X01.

Suena a detalle y no lo es. Las variables de una herramienta de diseño **no tienen control de versiones
propio**, admiten **pocos tipos** —sin tokens compuestos— y **hacen falta complementos de terceros** para
sacarlas a código `[Libro 1, capítulo 6]`.

> Y el argumento de fondo, del mismo libro: *"Cuando empecé a usar Figma escuchaba: 'todo el mundo diseña en
> Photoshop, Figma nunca va a funcionar'. Eso no envejeció bien. **Hoy es un gigante, pero esa posición puede
> cambiar.**"*
>
> **Por eso el sistema no vive dentro de ninguna herramienta.** Vive en `tokens/`, y cada herramienta recibe
> una traducción.

---

## Índice

1. [Lo primero: averiguar qué hay, y si escribe](#lo-primero-averiguar-qué-hay-y-si-escribe)
2. [Las tres clases de puente](#las-tres-clases-de-puente)
3. [El puente de Figma · comprobado, y es de clase A](#el-puente-de-figma--comprobado-y-es-de-clase-a)
4. [Conectar un puente real](#conectar-un-puente-real)
5. [Lo que se publica, y en qué orden](#lo-que-se-publica-y-en-qué-orden)
6. [figma-variables.json · las tres colecciones](#figma-variablesjson--las-tres-colecciones)
7. [lienzo.json · el documento neutral](#lienzojson--el-documento-neutral)
8. [El contrato, y cómo se comprobó](#el-contrato-y-cómo-se-comprobó)
9. [Los siete errores del puente](#los-siete-errores-del-puente)
10. [Cuando no hay ningún puente](#cuando-no-hay-ningún-puente)

---

## Lo primero: averiguar qué hay, y si escribe

**No asumas que hay un puente. No asumas que el que hay escribe.**

| Paso | Qué hacer |
|---|---|
| **1** | Mira qué herramientas de diseño hay disponibles en la sesión |
| **2** | **Averigua si escriben o solo leen.** Muchos puentes de diseño solo *envían contexto al agente*: leen el lienzo, no crean nodos |
| **3** | **Dilo antes de intentarlo.** Si solo lee, no prometas dibujar |
| **4** | Si no hay ninguno, **la salida sigue sirviendo**: las variables se importan a mano y la galería se abre en un navegador |

> **El error a evitar:** anunciar *"te lo dibujo en Figma"* y descubrir a mitad de camino que el puente no crea
> nodos. **Se comprueba primero y se dice después.**

---

## Las tres clases de puente

### Clase A · escribe en un lienzo de diseño

Crea marcos, textos y componentes. **Es lo que el usuario suele imaginar.**

**Orden de creación — no es negociable:**

```
1 · las variables          primero SIEMPRE. Sin ellas, todo nodo nace con valores en crudo
2 · los estilos de texto   apuntando a las variables, nunca a valores fijos — DS-X04
3 · los componentes        uno por entrada del inventario, con sus variantes
4 · las páginas            recién acá se dibujan pantallas
```

**Si el orden se invierte**, se termina con cientos de nodos que llevan `#3A45C9` escrito adentro, y cambiar
el acento deja de ser una línea.

### Clase B · lee el lienzo y te da contexto

Devuelve la estructura de lo que ya está dibujado. **Sirve para auditar, no para construir.**

Uso legítimo: **comprobar que lo dibujado respeta el sistema** — que ningún nodo lleve un color fuera de la
paleta, que todo contenedor tenga disposición automática.

**Dile al usuario qué clase tiene**, para que sepa qué esperar.

### Clase C · sincroniza una biblioteca de archivos

Sube la biblioteca a un espacio de diseño como archivos. **Escribe, pero no en un lienzo vectorial: en HTML.**

**`--salidas galeria` produce exactamente eso**: un HTML por componente, con sus variantes y estados
renderizados y su «cuándo usarlo / cuándo no» arriba.

**Es la clase más subestimada.** Un componente que se ve en un navegador **ya se ve**, no hace falta abrir
nada. Y el mismo archivo es la prueba de que los tokens resuelven.

> **Al usar un puente de esta clase:** sincroniza **de a un componente**, nunca reemplazando todo de golpe.
> Un reemplazo total borra lo que otra persona subió.

---

## El puente de Figma · comprobado, y es de clase A

**Verificado el 17-08-2026 contra el servidor MCP oficial de Figma.** El análisis original de la base de conocimiento concluyó
—leyendo `[Libro 2, capítulo 11]`— que el puente era **de solo lectura**: `get_design_context` envía contexto al
agente. **Eso ya no es cierto, y la diferencia cambia el plan.**

| Herramienta | Qué hace | Clase |
|---|---|---|
| `get_design_context` · `get_metadata` · `get_screenshot` · `get_variable_defs` | Leen el lienzo | B |
| **`use_figma`** | **Ejecuta la Plugin API en el archivo: crea nodos, variables, componentes, variantes, enlaces** | **A** |
| **`create_new_file`** | **Crea el archivo de diseño, FigJam o Slides desde cero** | **A** |
| `upload_assets` · `download_assets` | Suben y bajan recursos | A / B |
| `get_code_connect_map` · `add_code_connect_map` | Atan componente de Figma ↔ componente de código | puente de doble sentido |
| `get_libraries` · `search_design_system` | Descubren qué bibliotecas y piezas ya existen | B |

### La regla que no se salta

**`use_figma` y `create_new_file` exigen cargar antes su skill.** No es una recomendación del servidor: es
prerrequisito declarado, y saltarlo produce fallos difíciles de depurar.

| Antes de llamar a | Carga primero |
|---|---|
| `use_figma` | `figma-use` — **siempre**, sin excepción |
| `create_new_file` | `figma-create-new-file` |
| construir tokens y componentes | `figma-generate-library` **junto con** `figma-use` |
| llevar una pantalla completa | `figma-generate-design` **junto con** `figma-use` |

### Cómo encaja con este sistema

**`figma-generate-library` hace en Figma exactamente lo que este plugin hace en JSON**, y su orden de fases
coincide con el de acá — lo cual es la confirmación de que el orden es el correcto:

```
figma-generate-library        este plugin
─────────────────────────    ──────────────────────────
Fase 0 · descubrimiento       Paso 1 · entrevistar
Fase 1 · fundamentos/tokens   Pasos 2-3 · marca.json → derivar.py
Fase 2 · estructura de archivo  (siete páginas · 07-handoff)
Fase 3 · componentes          Paso 4 · poblar el inventario
Fase 4 · integración y QA     Paso 5 · verificar.py
```

**Quién manda:** el JSON — DS-X01. `figma-generate-library` construye *en* Figma; acá Figma **recibe** lo que
`derivar.py` ya decidió. El orden de creación de la clase A (variables → estilos → componentes → páginas) es
el mismo que exige esa skill, y por el mismo motivo.

**Traducción concreta de las salidas:**

| Salida de `construir.py` | Cómo entra por `use_figma` |
|---|---|
| `figma-variables.json` — colección 1 | `createVariableCollection` con un modo, `scopes = []`, `hiddenFromPublishing = true` |
| colección 2 | modos claro/oscuro, cada valor como `{ type: 'VARIABLE_ALIAS', id }` al primitivo |
| colección 3 | un modo, alias al nivel 2, con `setVariableCodeSyntax` en las tres plataformas |
| `estilosDeTexto` | **no son variables**: cada entrada ata un token a un estilo de texto — una tipografía son tres valores y una variable guarda uno |
| `lienzo.json` | marcos con `layoutMode` y todo enlazado a variables; **nunca un valor en crudo** |

**Los campos van listos para pasar tal cual:** `alcance` trae los valores de Figma,
`tipo` trae el tipo resuelto —`ALIAS` no existe—, las claves de `sintaxisPorPlataforma`
son `WEB`, `iOS` y `ANDROID` con esa caja exacta, y una referencia entre llaves nombra a
la variable de Figma con barra: `{color/gris/0}`. **Nada se traduce al leer.**

> **El nombre de web va sin envolver** —`--accion-reposo`, no `var(--accion-reposo)`—.
> La sintaxis nombra la variable; envolverla mezcla el nombre con su uso, y rompe la
> comprobación de `DS-X10`, que contrasta ese nombre contra el CSS emitido.

### Los tres choques con `figma-generate-library`, y cuál manda

**Las dos skills se contradicen en tres puntos, literalmente.** Están acá para no volver a resolverlos por
deducción en cada tanda.

| Punto | `figma-generate-library` dice | Acá manda | Por qué |
|---|---|---|---|
| **Sintaxis WEB** | `var(--x)`, **con** envoltorio | **`--x`, sin envoltorio** | La sintaxis nombra la variable; envolverla mezcla el nombre con su uso y **rompe `DS-X10`**, que contrasta ese nombre contra el CSS emitido |
| **Las páginas** | Cover · Getting Started · Foundations · Components · Utilities | **Las seis de `lienzo.json`** | El lienzo es la fuente — DS-X01. Sus nombres y su orden son el contrato |
| **Paralelizar** | *"NEVER parallelize `use_figma`"* | **Lectura en paralelo, escritura en secuencia** | `figma-use` manda abanicar las lecturas por página y tiene razón; para escribir, la regla que prohíbe es la segura |

> **Y el reparto de fondo, que resuelve casi cualquier duda nueva:** `figma-generate-library` dice **CÓMO**
> llamar a la API; **`lienzo.json` dice QUÉ dibujar.** Cuando una de las dos parece decidir algo que le toca a
> la otra, gana la otra.

### Antes de prometer nada, comprueba el asiento

**Tener las herramientas no es tener permiso.** Un asiento *View* en un plan starter **lee y no escribe**, y
el fallo aparece a mitad de la construcción, no al empezar.

```
whoami  →  mira `seat`.  View = solo lectura.  Dev/Full = escribe.
```

**Si el asiento no escribe, se dice antes** y se entrega la galería y `figma-variables.json` para importar a
mano — §Cuando no hay ningún puente. El sistema no depende de eso — DS-X06.

---

## Conectar un puente real

**El plugin no trae ningún servidor MCP configurado, y es deliberado.** Un servidor de ejemplo que no responde
falla al arrancar en la máquina de quien lo instale, y un puente concreto envejece más rápido que el sistema.

Quien quiera conectar el suyo lo declara **en su propio proyecto**, no dentro del plugin — así sobrevive a las
actualizaciones. En `.mcp.json` en la raíz del proyecto:

```json
{
  "mcpServers": {
    "figma": { "type": "http", "url": "https://<tu-servidor-mcp>/api" }
  }
}
```

El envoltorio `mcpServers` no es opcional: sin él la configuración se ignora en silencio.

> **Y nada de esto es un requisito.** DS-X06: ninguna etapa del proceso depende de que un agente escriba en el
> lienzo. Sin puente, la galería y las variables siguen siendo la entrega completa.

---

## Lo que se publica, y en qué orden

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/construir.py --destino <destino> --salidas css,figma,lienzo,galeria
```

| Archivo | Para qué | Quién lo consume |
|---|---|---|
| `sistema.css` | El sistema como propiedades personalizadas, un bloque por modo | El navegador, la galería, la aplicación web |
| `figma-variables.json` | **Las tres colecciones**, con modos, alcance y sintaxis por plataforma | El puente que importa variables |
| `lienzo.json` | **El documento neutral de nodos** | El puente que dibuja |
| `galeria/*.html` | Un componente por archivo, ya renderizado | El puente que sincroniza archivos, o un navegador |
| `Sistema.swift` · `values/*.xml` | Constantes nativas | iOS y Android |

---

## `figma-variables.json` · las tres colecciones

**Una colección por nivel.** Es lo que impide que los niveles se colapsen dentro de la herramienta.

| Colección | Modos | Publicada | Por qué |
|---|---|---|---|
| **1 · Primitivos** | uno solo | **no** | `[Libro 2, capítulo 13]`: *"El alcance permite **ocultar completamente una variable** de la interfaz y de la publicación. **Esto evita que los primitivos se apliquen directamente** y garantiza que se usen exclusivamente como alias."* |
| **2 · Semánticos** | **todos** | sí | **Los modos viven acá.** Un primitivo nunca cambia por modo |
| **3 · Componentes** | uno solo | sí | Alias al nivel 2. Es lo único que una pantalla cita |

### El alcance, variable por variable

**No es cosmético: es lo que hace que la herramienta no ofrezca lo que no corresponde.**

| Rol | Alcance, con el valor que emite el archivo | Efecto |
|---|---|---|
| `superficie.*` | `FRAME_FILL` · `SHAPE_FILL` | No aparece al elegir color de texto |
| `texto.*` | `TEXT_FILL` | No aparece al elegir un fondo |
| `borde.*` | `STROKE_COLOR` | Solo en bordes |
| `accion.*` | `FRAME_FILL` · `SHAPE_FILL` · `STROKE_COLOR` | Fondo o borde, nunca texto |
| `estado.*` | los cuatro anteriores | Un error se pinta de fondo, de borde y de texto |
| `espacio.*` | `GAP` · `WIDTH_HEIGHT` | No aparece como tamaño de fuente |
| `forma.*` | `CORNER_RADIUS` | Solo ahí |
| `tipo.*.tamaño` · `tipo.*.peso` | `FONT_SIZE` · `FONT_WEIGHT` | Solo en tipografía |
| nivel 3 | `ALL_SCOPES` | Es lo que una pantalla cita: no se le acota nada |

> **Los primitivos van con `scopes = []`**, que es como Figma escribe «no la ofrezcas en
> ningún sitio». **No existe un valor `NINGUNO`**: la lista vacía es la forma.

### Un nombre por plataforma

`[Libro 1, capítulo 8]` — **una variable, tres nombres.** El desarrollador copia el de su plataforma y compila:

```
accion.reposo
  WEB       --accion-reposo
  iOS       accionReposo
  ANDROID   accion_reposo
```

**Las claves son las de `setVariableCodeSyntax`, con su caja exacta:** `iOS` lleva la i
minúscula y las otras dos van enteras en mayúscula. Pasar `IOS` devuelve *Invalid enum
value* y **la variable queda sin sintaxis en las tres plataformas**, porque el error corta
antes de llegar a las siguientes.

> **Y el acento se translitera, no se descarta.** `tipo.cuerpo.tamaño` da
> `--tipo-cuerpo-tamano`. Tirar la eñe parte la palabra en dos y produce
> `--tipo-cuerpo-tama-o`, un nombre que ninguna salida define — el desarrollador lo copia
> del panel y no resuelve. Lo hace `sin_tildes()` en `construir.py`, y lo comprueba
> `DS-X10` contrastando ese nombre contra el CSS emitido.

---

## `lienzo.json` · el documento neutral

**Describe qué dibujar, no con qué herramienta.** Si mañana cambia la herramienta, se cambia el traductor y
**el documento sigue siendo el mismo**.

```json
{ "tipo": "marco", "nombre": "boton/primario",
  "disposicion": { "direccion": "fila", "espacio": "{espacio.elementos}",
                   "relleno": "{espacio.interior}", "ancho": "abraza", "alto": "abraza" },
  "fondo": "{boton.primario.fondo}",
  "forma": "{forma.control}",
  "hijos": [ { "tipo": "texto", "contenido": "Continuar",
               "estilo": "{tipo.cuerpo}", "color": "{boton.primario.texto}" } ] }
```

**Tres cosas que nunca faltan:**

1. **Todo marco lleva `disposicion`.** `[Libro 2, capítulo 11]`: *"El código más preciso se genera cuando el diseño usa
   Auto Layout, porque corresponde directamente al sistema Flexbox. **Si no se usa, Figma sugiere coordenadas
   absolutas**, lo que lleva a interfaces no responsivas y trabajo extra."*
2. **Ningún valor en crudo.** Todo color, espacio y tamaño es una llave `{token}` — DS-T07.
3. **El dimensionado es `abraza`, `llena` o `fijo`.** Nunca un número suelto donde debería abrazar el
   contenido: es lo que revienta al cambiar de idioma — DS-L03.

### El vocabulario, para traducirlo

| Documento | Figma | CSS |
|---|---|---|
| `marco` | Frame | `div` |
| `disposicion` | **Auto Layout** | **Flexbox** |
| `abraza` | Hug contents | `width: fit-content` |
| `llena` | Fill container | `flex: 1` |
| `forma` | Corner radius | `border-radius` |
| `instancia` | Instance | uso del componente |

---

## El contrato, y cómo se comprobó

**`referencias/figma-api.json` guarda lo que Figma acepta de verdad.** Lo leen
`construir.py` —para emitirlo— y `verificar.py` —para comprobarlo—, del mismo archivo,
para que no puedan discrepar. Es lo que impone `DS-X12`.

### Cómo se le pregunta al servidor

**No se infiere del manual: se ejecuta la llamada con un valor imposible y se lee la
respuesta.** El mensaje de validación enumera el enum completo.

```js
const tmp = figma.variables.createVariableCollection("__sonda__");
const v = figma.variables.createVariable("sonda", tmp, "COLOR");
try { v.scopes = ["__NO_EXISTE__"]; } catch (e) { return e.message; }
tmp.remove();
```

> *"Expected 'ALL_SCOPES' | 'TEXT_CONTENT' | 'CORNER_RADIUS' | … | 'PARAGRAPH_INDENT'"*
>
> Veintidós valores, en una sola llamada. **La colección temporal se borra al terminar.**

### Lo que está verificado, y lo que no

**Cada restricción del contrato declara cómo se supo.** `servidor` significa que se le
preguntó a Figma y el enunciado es su respuesta literal. `inferida` significa que sale
de la documentación y nadie la probó.

> **La distinción no es burocracia: es la causa de todo lo que salió mal acá.** El puente
> estuvo declarando restricciones de la segunda clase como si fueran de la primera, y por
> eso `figma-variables.json` pasó meses en verde siendo inimportable.

**`figma-api.json` tiene una sección `sin_verificar`** con lo que no se probó — límites de
variables por colección, modos por plan, y si Figma rechaza un alcance imposible para el
tipo. **Está escrito para que nadie lo cite como comprobado.**

---

## Los siete errores del puente

Los cinco primeros son de método. **Los dos últimos son los que costaron caro de verdad**,
y los dos son la misma equivocación vista de cerca y de lejos.

| Error | Qué pasa | Qué hacer |
|---|---|---|
| **Dibujar antes de importar variables** | Cada nodo nace con el color escrito adentro | Variables → estilos → componentes → páginas |
| **Publicar los primitivos** | El equipo aplica `indigo.600` directo y el nivel 2 se vuelve decorativo | Ocultos y sin alcance — DS-X02 |
| **Marcos sin disposición** | La herramienta emite coordenadas absolutas | Toda caja lleva `disposicion` — DS-L01 |
| **Estilos con valores fijos** | Cambiar el acento ya no propaga | Los estilos apuntan a variables — DS-X04 |
| **Prometer que dibuja sin comprobarlo** | Se anuncia y no se puede cumplir | Comprobar la clase del puente **antes** |
| **Emitir un vocabulario propio** | El archivo dice ser formato de importación y usa palabras que la herramienta no conoce | Todo campo enumerado sale del contrato — DS-X12 |
| **Comprobar solo las reglas propias** | Las comprobaciones preguntan si el archivo cumple el sistema; ninguna pregunta si la herramienta puede leerlo | Una salida se comprueba **contra su consumidor** |

### Los cuatro fallos reales, y qué tenían en común

**Verificado el 18-08-2026 escribiendo el sistema de un producto real en un archivo real.**
Hasta ese día el puente nunca se había ejecutado contra Figma: se había leído la
documentación y se había escrito el generador a partir de ella.

| Qué estaba mal | Cómo se veía | Cómo se descubrió |
|---|---|---|
| **El vocabulario entero** — `RELLENO_FORMA`, `ALIAS`, `web` | El archivo se llamaba «formato de importación» y ningún importador lo entendía | Al ir a usarlo hubo que traducir cada campo a mano |
| **El punto en el nombre** | 279 variables, ninguna creable | `createVariable("superficie.base", …)` → *invalid variable name* |
| **La eñe descartada en vez de traducida** | Figma ofrecía `--tipo-cuerpo-tama-o`; el CSS definía `--tipo-cuerpo-tamano` | Comparando las dos salidas entre sí |
| **Un rol tipográfico tratado como un valor** | `var(--tipo-cuerpo)` contra un archivo que solo define sus tres partes | Al buscar el semántico al que aliasar, no estaba |

**Los cuatro pasaban todas las comprobaciones.** Y los cuatro tienen la misma forma:
**cada salida era coherente consigo misma**. El error solo aparece al comparar una salida
contra otra, o contra el programa que va a leerla.

> **De ahí sale la regla de trabajo:** una salida no está comprobada hasta que alguien la
> ejecuta contra su consumidor real. Un generador que nunca corrió contra la herramienta
> **no está probado: está sin usar** — y eso vale para el puente igual que para un
> verificador que nunca falló.

---

## Cuando no hay ningún puente

**No es un bloqueo.** El sistema está completo igual:

- **`galeria/*.html`** se abre en un navegador y **ya muestra todos los componentes** con sus estados.
- **`figma-variables.json`** se importa con un complemento de importación de variables.
- **`sistema.css`** se usa tal cual en la aplicación web.
- **`Sistema.swift`** y `values/*.xml` se copian al proyecto nativo.

> **Dilo así, sin disfrazarlo:** *"No hay un puente que dibuje en el lienzo. Te dejo las variables listas para
> importar y la galería lista para mirar. El sistema no depende de eso."*
>
> **DS-X06 lo pone por escrito: ninguna etapa depende de que un agente escriba en el lienzo.**
