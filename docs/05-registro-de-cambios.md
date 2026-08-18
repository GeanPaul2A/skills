# Registro de cambios

> **Qué registra este documento.** Todo cambio relevante del complemento, en orden inverso: lo más reciente
> arriba.
>
> **Formato.** Basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Las versiones siguen
> [versionado semántico](https://semver.org/lang/es/), con el mismo criterio que el complemento aplica a los
> sistemas que construye: **si quien ya usó la versión anterior tiene que revisar su trabajo, es una versión
> mayor.**

---

## Índice

1. [1.5.0 — El paquete verificable](#150--el-paquete-verificable)
2. [1.4.0 — Documentación verificable](#140--documentación-verificable)
3. [1.3.0 — Multiplataforma, versionado y composición](#130--multiplataforma-versionado-y-composición)
4. [1.2.0 — Cobertura completa y suite de pruebas](#120--cobertura-completa-y-suite-de-pruebas)
5. [1.1.0 — Dominio de negocio](#110--dominio-de-negocio)
6. [1.0.0 — Primera versión](#100--primera-versión)

---

## 1.5.0 — El paquete verificable

**18 de agosto de 2026**

### Agregado

**`pruebas/paquete.py` y la séptima etapa de la suite.** Dejar un archivo en la carpeta correcta no es lo
mismo que empaquetarlo: un guion que abre `referencias/figma-api.json` funciona donde el archivo está al lado
y falla en la máquina de quien instale el complemento si ese archivo no viajó. La etapa comprueba que todo
archivo que un guion abre exista, que todo archivo que una skill manda leer exista, y que ninguno esté tapado
por `.gitignore`.

**Y comprueba lo que el complemento anuncia**, que es donde ya había fallado dos veces:

| Comprobación | Qué impide |
|---|---|
| Toda cifra de una **superficie viva** es la real | Que el archivo de presentación anuncie 83 reglas cuando hay 87. Antes solo se miraba `plugin.json`, y las otras cinco superficies quedaban libres |
| Todo comando citado **existe** en `commands/` | Que la documentación enseñe a escribir un comando que un renombrado borró |
| Todo comando está **en la vitrina** | Un comando que existe y que nadie encuentra porque no se cita en ningún lado |
| Todo comando **delega en una skill que existe** | Un comando huérfano tras renombrar su skill |
| El `name:` del frontmatter **es el nombre de la carpeta** | Una skill que se carga con otro nombre del que todo el mundo escribió |

El registro de cambios y los informes fechados quedan fuera a propósito: **sus cifras eran ciertas en su
versión**, y corregirlas sería reescribir la historia. Y si los patrones reconocen menos afirmaciones de las
esperadas, la etapa falla en vez de dar verde: **un cero no es un verde, es no haber leído nada.**

**`pruebas/importar.py`, con etapa propia** — el camino «Importar» no duplica el modelo ni reapunta el
proyecto. Antes corría bajo el encabezado de otra etapa y su resultado se leía como si fuera de esa.

**El contrato de la API de Figma, verificado ejecutándolo contra el servidor.**
`skills/system-design/referencias/figma-api.json` y `figma-mcp.md` reemplazan lo que antes se había escrito
leyendo el manual y nunca se había corrido.

**`skills/screen/referencias/marco-dispositivo.md`** — cada pantalla se dibuja dentro de un marco de
dispositivo, con las medidas, la barra de estado y la barra inferior de cada SO.

**Cinco reglas nuevas**, de 83 a 87 y de 50 a 54 comprobadas:

| Regla | Qué exige |
|---|---|
| `DS-P05` | Ninguna superficie continua no textual es el único portador de información necesaria |
| `DS-X09` | El nombre de toda variable publicada es importable en Figma |
| `DS-X10` | La sintaxis por plataforma nombra la variable que esa plataforma define |
| `DS-X11` | Toda referencia de una salida resuelve dentro de esa misma salida |
| `DS-X12` | Todo campo enumerado sale en el vocabulario de la herramienta, no en el propio |

### Cambiado

- **Las siete capacidades y sus guiones pasaron a nombres en inglés**, para que la carpeta y el nombre de la
  skill coincidan: `sistema-diseno` → `system-design`, `dominio` → `domain`, `pantalla` → `screen`, `probar` →
  `test`, `entregar` → `deliver`, `auditar` → `audit`, `documentar` → `document`. Los guiones acompañan:
  `auditar.py` → `audit.py`, `entregar.py` → `deliver.py`, `probar.py` → `test.py`, `iconos.py` → `icons.py`.
  Lo mismo en los datos del sistema de referencia: `dominios/` → `domains/`, `pantallas/` → `screens/`,
  `entrega/` → `delivery/`, `movimiento.json` → `motion.json`.
- **Los ocho comandos siguen la misma convención**: `:auditar-sistema` → `:audit-system`, `:crear` →
  `:create-system`, `:definir-dominio` → `:define-domain`, `:disenar-pantalla` → `:design-screen`,
  `:documentar-pieza` → `:document-piece`, `:entregar-sistema` → `:deliver-system`, `:extender` →
  `:extend-system`, `:probar-pantalla` → `:test-screen`. **Ninguno conserva su nombre anterior:** el
  renombrado se hizo entero en una sola versión a propósito, para que haya un único momento de ruptura y no
  dos.
- **Convención de salida `output/`.** Todo lo que una skill genera va a `<proyecto>/output/`. Las carpetas del
  complemento son de **solo lectura**: ninguna skill escribe dentro de ellas. Queda documentada para personas
  en el archivo de presentación (§6.1) y en arquitectura (§3.2), con el árbol de lo escrito a mano frente a lo
  derivado, y con la advertencia de que `output/domains/` y `domains/` no son la misma carpeta.
- **La suite pasó de cinco etapas a siete**, y el archivo de presentación las enumera.

### Corregido

- Un índice y un ancla de este documento que el renombrado había desincronizado.
- Las cifras del archivo de presentación y de la documentación anunciaban 83 reglas, 50 comprobadas y 1224
  comprobaciones cuando ya eran 87, 54 y 3331 — **el mismo error que la etapa 7 existe para impedir**, en los
  archivos que esa etapa todavía no miraba.
- **Los seis comandos que la documentación enseñaba a escribir ya no existían.** El renombrado se hizo en los
  archivos y no en lo que los nombra, y nada lo detectó porque un comando citado no es un enlace de Markdown.
- **`:extend-system` no se citaba en ninguna vitrina**, y era invisible desde antes del renombrado. Lo
  encontró la comprobación nueva el día que se escribió.
- La skill `domain` mezclaba dos carpetas distintas bajo el mismo nombre: el dominio que escribe
  (`<destino>/domains/`) y la especificación del formato (`${CLAUDE_PLUGIN_ROOT}/domains/_plantilla.json`). El
  ejemplo ejecutable del Paso 4 apuntaba, por eso, a una ruta relativa al directorio de trabajo.

---

## 1.4.0 — Documentación verificable

**17 de agosto de 2026**

### Agregado

**Carpeta `docs/` con documentación estructurada.**

| Documento | Qué explica |
|---|---|
| `01-guia-de-uso.md` | Cómo se usa el complemento, de cero |
| `02-arquitectura.md` | Las cuatro capas, el flujo de información y las decisiones que las sostienen |
| `03-referencia-de-reglas.md` | Las 83 reglas, con su método y qué guion las comprueba |
| `04-contribuir.md` | Cómo se agrega una regla, una comprobación o una capacidad |
| `05-registro-de-cambios.md` | Este documento |
| `90-auditoria-2026-08.md` | El informe de auditoría, fechado |

**Tres guiones que hacen verificable la propia documentación.**

- `lib/generar_referencia.py` — produce la referencia de reglas desde la base de conocimiento. Con
  `--comprobar` falla si el documento quedó desactualizado.
- `pruebas/indices.py` — regenera el índice de cada documento desde sus títulos. Un índice escrito a mano se
  desincroniza en la primera sección que se agrega, y **su fallo es silencioso**.
- `pruebas/enlaces.py` — comprueba que los 267 enlaces internos resuelven, incluidas las anclas.

**Dos etapas nuevas en la suite**, que ahora son cinco: la documentación generada está al día, y los enlaces
internos resuelven.

### Cambiado

- **Todo el repositorio está en español y sin abreviaturas.** Las citas pasaron de dos formas inconsistentes
  —`[Book 1, cap. 6]` y `[B1, cap. 6]`— a una sola: `[Libro 1, capítulo 6]`. Las tablas de reglas escriben
  `OBLIGATORIO` y `RECOMENDADO` completos.
- **Las siete capacidades tienen la misma estructura, con secciones numeradas** que se pueden citar desde otro
  documento. No llevan índice a propósito: el agente lee el archivo entero, y un índice gastaría contexto sin
  ahorrarle navegación.
- **El recuento de la base de conocimiento se calcula**, no se escribe. Estaba en 76 reglas cuando ya había 83.
- El archivo de presentación se reescribió entero: qué problema resuelve, qué lo hace distinto, y una tabla de
  dónde está cada cosa.

### Corregido

- **Cincuenta y cinco enlaces de índice apuntaban a anclas inexistentes, y lo estaban desde el principio.** La
  causa: los títulos llevaban la cita al final —`## 1.2 · La rejilla [Libro 2, capítulo 5]`—, y el
  identificador que genera GitHub incluye ese texto. Las 77 citas se movieron a una línea propia debajo del
  título.
- Las referencias entre secciones de una misma capacidad apuntaban a nombres que la numeración cambió.

---

## 1.3.0 — Multiplataforma, versionado y composición

**17 de agosto de 2026**

### Agregado

**Catálogo de iconos y componentes nativos.**

- `recursos/iconos.json` — veinticuatro acciones declaradas por **propósito**, no por dibujo, con su glifo y
  tamaño en iOS, Android, Web y Desktop, y la licencia de cada conjunto.
- `recursos/nativo.json` — teclados, los tres momentos de un permiso, componentes que provee el sistema
  operativo, zonas reservadas y objetivo táctil mínimo por plataforma.
- `skills/deliver/scripts/icons.py` — descarga los iconos al proyecto y los normaliza: `currentColor`,
  grosor según tamaño, y el tamaño que corresponde al uso.

**Versionado del sistema y de las entregas, por separado.**

- `DS-H09` — el sistema declara su versión en `marca.json`, y es semántica.
- `DS-H10` — toda entrega declara contra qué versión del sistema se dibujó.
- `skills/deliver/referencias/versionado.md` — el procedimiento, con un ejemplo momento a momento.

**Cinco reglas de composición**, en la sección nueva `conocimiento/DESIGN/11-composicion/`.

| Regla | Enunciado |
|---|---|
| `DS-C11` | El icono dentro de un componente sale de la tabla de tamaños de su plataforma |
| `DS-C12` | Ningún emoticón hace de icono de interfaz |
| `DS-C13` | Un hijo no puede ser más ancho que el espacio útil de su padre |
| `DS-C14` | Todo componente declara qué otros puede contener, y a qué profundidad |
| `DS-A13` | Toda pantalla tiene un solo foco visual primario, y se declara cuál |

### Cambiado

- **Las plataformas ahora son `ios`, `android`, `web` y `desktop`**, elegibles en `proyecto.json`. Antes eran
  `movil`, `escritorio`, `web` y `tableta`, que no permitían distinguir el tamaño de icono ni el objetivo
  táctil de cada sistema operativo.
- `DS-C10` (el estado de puntero no se declara donde no hay puntero) ahora distingue las plataformas táctiles
  de las que tienen puntero.
### Corregido

- **`lib/comun.py` → `tabla()`** filtra las claves con guion bajo en un solo lugar. Antes cada verificador lo
  hacía por su cuenta y uno se olvidaba: agregar una nota a `plantillas.json` tumbaba cuatro guiones de golpe.
- **`DS-C13` no suma los anchos de una zona.** Las piezas que una zona lista suelen ser alternativas por
  estado, no vecinas: sumarlas medía una pantalla que no existe. La suma se comprueba solo donde la pantalla
  declara explícitamente qué piezas comparten fila.
- **`DS-L06` no exige un largo mínimo.** Un valor enumerado de tres letras tiene extremos iguales con toda
  razón. Se comprueba que los dos existan y que no estén invertidos.
- **`DS-A07` y `DS-A08` miraban el archivo equivocado.** `sistema.css` es un archivo de variables, no una hoja
  con selectores: ahora comprueban que exista el token de foco, y la galería para el crecimiento del texto.

---

## 1.2.0 — Cobertura completa y suite de pruebas

**17 de agosto de 2026**

### Agregado

**La capacidad `deliver`**, que cierra la sección de entrega a desarrollo — la única de la base de
conocimiento que no tenía responsable. Cubre la estructura de páginas, el paquete de recursos, el contrato de
animación y el versionado. Nueve reglas, siete de ellas sin comprobación anterior.

**Guion para `test`** — ocho comprobaciones donde antes había una lista que revisaba una persona.

**Guion para `audit`** — calcula el resultado con la fórmula escrita, implementada una sola vez, más la
cobertura de todas las reglas leídas de la base de conocimiento.

**`lib/comun.py`** — el resultado de una comprobación, el veredicto, el informe y el lector de reglas,
compartidos por los cinco verificadores.

**`ejemplos/base/`** — el sistema de referencia, y **`pruebas/correr.sh`** — la suite en tres etapas.

**`.claude-plugin/marketplace.json`**, que el archivo de presentación documentaba y no existía.

### Corregido

- **Dieciséis referencias apuntaban a archivos inexistentes.** Las capacidades citaban cuatro documentos que no
  estaban en el repositorio. El agente no fallaba de forma visible: seguía sin las reglas.
- **La mitad de `DS-P02` corría vacía.** `inyectar.py` no arrastraba los campos del dominio a los patrones, así
  que la comprobación daba resultado favorable por no tener nada que mirar.
- **El puente con Figma estaba mal documentado.** La base de conocimiento concluía, leyendo el libro, que era
  de solo lectura. Se comprobó contra el servidor: `use_figma` ejecuta la interfaz de complementos completa.

---

## 1.1.0 — Dominio de negocio

### Agregado

- La capacidad `domain` y `domains/_plantilla.json`: entidades, reglas de negocio, patrones y piezas propias
  de un tipo de negocio, para que el núcleo quede agnóstico.
- El cruce de cada dato de cada pantalla contra una columna que lo respalde.

---

## 1.0.0 — Primera versión

### Agregado

- Las capacidades `system-design`, `screen`, `test`, `audit` y `document`.
- La base de conocimiento con sus diez secciones y las setenta y seis reglas iniciales.
- Tokens en tres niveles con modos, veintidós componentes universales y cuatro plantillas.
- Publicación a CSS, Figma, Swift, Android, documento de lienzo y galería.
- El mecanismo `--romper`: inyectar un error a propósito para probar una comprobación.
