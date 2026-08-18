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

1. [1.4.0 — Documentación verificable](#140--documentación-verificable)
2. [1.3.0 — Multiplataforma, versionado y composición](#130--multiplataforma-versionado-y-composición)
3. [1.2.0 — Cobertura completa y suite de pruebas](#120--cobertura-completa-y-suite-de-pruebas)
4. [1.1.0 — Dominio de negocio](#110--dominio-de-negocio)
5. [1.0.0 — Primera versión](#100--primera-versión)

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
- `skills/entregar/scripts/iconos.py` — descarga los iconos al proyecto y los normaliza: `currentColor`,
  grosor según tamaño, y el tamaño que corresponde al uso.

**Versionado del sistema y de las entregas, por separado.**

- `DS-H09` — el sistema declara su versión en `marca.json`, y es semántica.
- `DS-H10` — toda entrega declara contra qué versión del sistema se dibujó.
- `skills/entregar/referencias/versionado.md` — el procedimiento, con un ejemplo momento a momento.

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

**La capacidad `entregar`**, que cierra la sección de entrega a desarrollo — la única de la base de
conocimiento que no tenía responsable. Cubre la estructura de páginas, el paquete de recursos, el contrato de
animación y el versionado. Nueve reglas, siete de ellas sin comprobación anterior.

**Guion para `probar`** — ocho comprobaciones donde antes había una lista que revisaba una persona.

**Guion para `auditar`** — calcula el resultado con la fórmula escrita, implementada una sola vez, más la
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

- La capacidad `dominio` y `dominios/_plantilla.json`: entidades, reglas de negocio, patrones y piezas propias
  de un tipo de negocio, para que el núcleo quede agnóstico.
- El cruce de cada dato de cada pantalla contra una columna que lo respalde.

---

## 1.0.0 — Primera versión

### Agregado

- Las capacidades `system-design`, `pantalla`, `probar`, `auditar` y `documentar`.
- La base de conocimiento con sus diez secciones y las setenta y seis reglas iniciales.
- Tokens en tres niveles con modos, veintidós componentes universales y cuatro plantillas.
- Publicación a CSS, Figma, Swift, Android, documento de lienzo y galería.
- El mecanismo `--romper`: inyectar un error a propósito para probar una comprobación.
