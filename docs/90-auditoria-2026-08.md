# Auditoría del conjunto de skills · `design-system`

> **Pregunta:** ¿está este conjunto de skills 100 % completo y es lo bastante robusto para elaborar un sistema
> de diseño entero, cubriendo todo lo que la base de conocimiento `DESIGN` declara?
>
> **Respuesta al auditar (1.1.0): no.** 20 de las 76 reglas no las citaba ninguna skill, `07-handoff` no tenía
> dueño, y 16 referencias apuntaban a archivos inexistentes.
>
> **Respuesta después de arreglarlo (1.2.0): sí, y ahora es comprobable.** Las 76 reglas tienen dueño — **39 un
> guion, 37 el informe de auditoría** que las lista para que las marque una persona. **Ninguna de las 39 está
> sin probar:** una suite las recorre rompiendo algo a propósito y falla si alguna no lo detecta.
>
> **Fecha:** 17 de agosto de 2026 · **Auditado:** 1.1.0 · **Estado al cierre:** 1.2.0

---

## Estado al cierre, en una tabla

| Medida | 1.1.0 · al auditar | 1.2.0 · al cerrar |
|---|---:|---:|
| Referencias rotas en las skills | **16** | **0** |
| Reglas de la base de conocimiento sin dueño | **20** | **0** |
| Reglas comprobadas por un guion | 39 | **58 citadas · 39 comprobadas** |
| Reglas `auto` con comprobación | 33 / 39 | **39 / 39** |
| Reglas `auto` probadas con `--romper` | *sin medir* | **39 / 39** |
| Secciones de la base de conocimiento con skill dueña | 9 / 10 | **10 / 10** |
| Skills sin guion | **2** (`probar`, `auditar`) | **0** |
| Suite de pruebas | **no existía** | **69 en verde · 0 fallos** |
| `marketplace.json` | **ausente** | creado |

```
══ Etapa 1 · el dorado pasa limpio
   ✓ sistema     1132 comprobaciones en verde · 0 fallos · 1 saltada
   ✓ entrega       36 comprobaciones en verde · 0 fallos
   ✓ pantallas     67 comprobaciones en verde · 0 fallos
   ✓ auditoria    524 comprobaciones en verde · 0 fallos
   ✓ pruebas-ui    61 comprobaciones en verde · 0 fallos

══ Etapa 3 · ninguna regla auto de la base de conocimiento queda sin comprobación
   reglas en la base de conocimiento            76
   marcadas «auto»            39
   con comprobación           39
   probadas con --romper      39

La suite pasa entera.
```

**Lo que sigue es el informe original, con lo que se hizo con cada hueco.**

---

## Índice

1. [Estado al cierre, en una tabla](#estado-al-cierre-en-una-tabla)
2. [El veredicto en una tabla](#1--el-veredicto-en-una-tabla)
3. [Lo que ya funciona, y por qué vale decirlo](#2--lo-que-ya-funciona-y-por-qué-vale-decirlo)
4. [Los nueve huecos](#3--los-nueve-huecos)
5. [Cobertura de las 76 reglas](#4--cobertura-de-las-76-reglas)
6. [Cobertura de las 10 secciones de la base de conocimiento](#5--cobertura-de-las-10-secciones-de-la-base-de-conocimiento)
7. [Lo que se arregló en esta pasada](#6--lo-que-se-arregló-en-esta-pasada)
8. [El plan de mejora, por impacto — EJECUTADO](#7--el-plan-de-mejora-por-impacto--ejecutado)
9. [Lo que queda por hacer](#8--lo-que-queda-por-hacer)

---

## 1 · El veredicto en una tabla

| Dimensión | Estado | Medida |
|---|---|---|
| **Arquitectura del conjunto** | **Sólida** | 6 skills, un pipeline con orden explícito, separación limpia entre lo visual y el negocio |
| **Cadena de construcción** | **Funciona de punta a punta** | `derivar → verificar` corre limpio: **1104 comprobaciones en verde, 0 fallos, 8 saltadas** |
| **Cobertura de reglas** | **Incompleta** | **56 / 76 citadas** · **39 / 76 con comprobación en un guion** |
| **Reglas `auto` implementadas** | **Casi** | **33 / 39** — faltan 6, y las 6 son OBLIGATORIAS |
| **Secciones de la base de conocimiento con skill dueña** | **9 / 10** | `07-handoff` no tiene ninguna |
| **Integridad de referencias** | **Estaba rota · ya arreglada** | 16 enlaces apuntaban a 4 archivos inexistentes |
| **Instalable** | **Estaba roto · ya arreglado** | El `marketplace.json` que documenta el README no existía |
| **Suite de pruebas** | **No existe** | El mecanismo `--romper` está construido y **nadie lo corre en conjunto** |

> **La conclusión honesta:** el conjunto no está al 100 %. Está en torno al **74 % de cobertura de reglas** y
> al **85 % de cobertura de secciones**, con la cadena principal —tokens, componentes, patrones, pantallas—
> completa y verificada, y **la entrega a desarrollo prácticamente sin cubrir**.

---

## 2 · Lo que ya funciona, y por qué vale decirlo

**Una auditoría que solo lista fallos no dice si vale la pena arreglarlos.** Acá sí vale, y estas cuatro
decisiones son la razón:

**1 · La verificación es real, no decorativa.** `verificar.py` son 1218 líneas que corren 1104 comprobaciones
sobre un sistema base. No es un lint de nombres: cruza contraste medido, resolución de alias, mapeo de partes a
roles y existencia de estados. **Es exactamente el vacío `G1` que la base de conocimiento dice llenar**, y está llenado.

**2 · Los saltos no cuentan como verdes.** El guion reporta las comprobaciones saltadas aparte, con su motivo
—«no hay patrones», «`proyecto.json` declara `modelo_de_datos.tipo: null`»—. **Es la diferencia entre un
verificador y un teatro de verificación**, y casi nadie la hace.

**3 · El veredicto de `--romper` mira la regla, no el total.** Tres estados, no dos: *lo detectó*, *pasó sin
detectarse*, *no se pudo probar*. Sin eso, una comprobación rota daría verde porque falló su vecina. **Este
detalle solo lo escribe quien ya se quemó con lo contrario.**

**4 · Lo agnóstico está de verdad separado.** El núcleo no sabe de taxis ni de banca; el negocio entra por
`dominios/<tipo>.json`. Y el inventario marca lo no-universal **con su motivo escrito**, que es lo que permite
llevarse los universales a otro producto. La separación se sostiene en los seis skills, sin filtraciones.

---

## 3 · Los nueve huecos

Ordenados por severidad. Los tres primeros ya están corregidos en esta pasada; los seis siguientes quedan
propuestos.

### 🔴 H1 · Dieciséis referencias apuntaban a archivos inexistentes — **ARREGLADO**

Las seis skills citaban `${CLAUDE_PLUGIN_ROOT}/conocimiento/doctrina.md`, `componentes.md`,
`accesibilidad.md` y `checklists.md`. **Ninguno de los cuatro existe.** El conocimiento vive en
`conocimiento/DESIGN/09-rules/README.md`, `03-components/`, `06-accessibility/` y `10-checklists/`.

**Por qué es el peor de los nueve:** la skill le dice al agente *«las 76 reglas están acá»* y ahí no hay nada.
El agente no falla ruidosamente: **sigue sin las reglas**, y produce un sistema que parece verificado. Es el
único hueco que convierte al plugin en algo peor que no tener plugin.

### 🔴 H2 · El `marketplace.json` documentado no existía — **ARREGLADO**

El README instruye `/plugin install design-system@geanpaul-design` y explica que el marketplace *«está definido
por `.claude-plugin/marketplace.json` en la raíz»*. **El archivo no estaba.** Nadie podía instalarlo siguiendo
sus propias instrucciones.

### 🔴 H3 · La suposición sobre Figma quedó vieja, y en la dirección cara — **ARREGLADO**

La base de conocimiento concluyó, leyendo `[Libro 2, capítulo 11]`, que el puente de Figma **solo lee**. Comprobado hoy contra el servidor
oficial: **`use_figma` ejecuta la Plugin API completa** —crea nodos, variables, colecciones, componentes y
variantes—, `create_new_file` crea el archivo y `add_code_connect_map` ata la pieza de Figma a la del código.

**El costo de la suposición vieja no es teórico:** el plugin construía un `lienzo.json` neutral *porque asumía
que nadie lo iba a dibujar*. Con el puente confirmado, ese documento pasa de ser un consuelo a ser una entrada.
Y aparece un prerrequisito que el plugin no mencionaba: **`use_figma` exige cargar la skill `figma-use` antes
de cada llamada**, y `figma-generate-library` junto a ella al construir tokens.

> **Con un matiz que ahora importa más:** tener la herramienta no es tener permiso. Un asiento *View* en un
> plan starter —el que tiene esta cuenta hoy— **deja las herramientas de escritura visibles y falla a mitad de
> la construcción**. `DS-X06` no solo sigue vigente: gana importancia.

### 🟠 H4 · Veinte de las 76 reglas no las cita ninguna skill — **ARREGLADO**

> **Cerrado.** De 20 huérfanas a **0**. Trece se cerraron con las tres acciones; las siete restantes
> —`F01`, `F12`, `C06`, `C08`, `L04`, `L08`, `L09`, `T10`, `X08`— son `semi` o `manual`, y **`auditar.py` las
> lista en su informe leyéndolas de la base de conocimiento**. Es la parte que importa del arreglo: no se agregaron a un
> `SKILL.md` para que el grep quedara limpio, se les dio un lugar donde una persona las marca.
>
> **Y la medida se volvió automática.** `auditar.py` lee `09-rules/README.md` y cruza qué guion comprueba cada
> regla. Si alguien agrega una regla al documento y nadie la comprueba, **aparece sola en el informe** — nadie
> tiene que acordarse de mirar.

**No están en ninguna parte del plugin:** ni en un `SKILL.md`, ni en una referencia, ni en un guion. Existen
en la base de conocimiento y **nada las invoca**.

`DS-F01` `DS-F12` · `DS-T10` · `DS-C06` `DS-C07` `DS-C08` · `DS-L04` `DS-L08` `DS-L09` · `DS-P05` ·
`DS-A01` `DS-A12` · `DS-H01` `DS-H02` `DS-H04` `DS-H05` `DS-H06` `DS-H07` `DS-H08` · `DS-X08`

**Siete de las veinte son de `DS-H`** — la familia de entrega. Ver H6.

### 🟠 H5 · Seis reglas marcadas `auto` y OBLIGATORIAS no tienen comprobación — **ARREGLADO**

> **Las seis tienen guion y las seis están probadas.** `DS-F09`, `DS-F10`, `DS-H04`, `DS-H05` y `DS-H06` en
> `entregar.py`; `DS-F02` en `probar.py`. Y `DS-F10` —la que más molestaba, «diez líneas de existir»— resultó
> ser exactamente eso.

La base de conocimiento las clasifica como automatizables. **Ningún guion las implementa.**

| Regla | Enunciado | Por qué falta |
|---|---|---|
| `DS-F02` | Ningún texto traducible usa tamaño fijo | Requiere mirar la pantalla, no el token |
| `DS-F09` | Los iconos combinan trazados, no agrupan formas | **Nadie procesa los SVG**: no hay etapa de iconos |
| `DS-F10` | Un icono no supera 2 kilobytes ni lleva `<mask>`, `<filter>` o `<clipPath>` | Ídem — y esta es trivial de escribir |
| `DS-H04` | Iconos en SVG; fotografías en WebP o AVIF | No hay etapa de recursos |
| `DS-H05` | Toda animación se entrega con sus cinco datos | No hay contrato de animación en el inventario |
| `DS-H06` | El movimiento se anima con `transform`, no con posición | Ídem |

> **`DS-F10` es el caso que más molesta:** medir el tamaño de un archivo y buscar tres cadenas es la
> comprobación más barata de las 76, y es la que falta. Está a diez líneas de existir.

### 🟠 H6 · `07-handoff` es la única sección de la base de conocimiento sin skill dueña — **ARREGLADO**

> **Existe la skill `entregar`**, con `entregar.py` y el comando `/design-system:entregar-sistema`. Cubre las
> siete páginas, el paquete de recursos, el contrato de animación, el modo de desarrollo y el versionado por
> hito. **De 1 de 8 reglas `DS-H` a 8 de 8**, y `DS-H01`, `DS-H07` y `DS-H08` —que la base de conocimiento marcaba `semi` y
> `manual`— resultaron comprobables una vez que la estructura se declara en un JSON.

La sección cubre **la estructura de siete páginas del archivo, el modo de desarrollo, la exportación de
recursos, los nombres por plataforma y el contrato de animación** — 249 líneas de base de conocimiento y **8 reglas**, de las
cuales el plugin cita **una**.

**Lo que hay hoy:** `construir.py` publica CSS, Swift, Android y variables. Eso cubre *los nombres por
plataforma* y nada más. **No hay nada que entregue iconos, imágenes, animaciones ni la estructura del archivo.**

**Consecuencia práctica:** el plugin construye un sistema verificable y **lo deja a medio camino de
desarrollo**. Es el hueco más grande por superficie.

### 🟡 H7 · `probar` y `auditar` no tienen guion — solo criterio — **ARREGLADO**

> **`probar.py`** comprueba ocho reglas: los cinco momentos, los cuatro estados, los extremos, el tamaño fijo
> en texto, un solo titular, el orden de tabulación con su token de foco, y lo que rompe el zoom al 200 %.
> **`auditar.py`** calcula el score con la fórmula de `informe.md`, **implementada una sola vez**, más la
> cobertura de las 76 reglas.
>
> **Y las dos dicen qué no pueden hacer.** No ejecutan un navegador: `DS-A12` («axe-core en la tubería cuando
> exista la aplicación») sigue siendo la mejora pendiente, y los guiones la preparan en vez de disimularla.

Las seis skills se reparten así:

| Skill | Guion propio | Qué comprueba una máquina |
|---|---|---|
| `sistema-diseno` | `derivar.py` · `verificar.py` · `construir.py` | 1104 comprobaciones |
| `pantalla` | `verificar-pantalla.py` | 10 reglas |
| `dominio` | `inyectar.py` | materializa; verifica con el de `sistema-diseno` |
| `documentar` | — | usa `verificar.py` ✔ razonable |
| **`probar`** | **ninguno** | **nada** |
| **`auditar`** | **ninguno** | **nada propio** |

**El problema no es que falte un guion: es que contradicen su propia doctrina.** El plugin existe porque
`[Extensión G1]` dice que *los libros no tienen ninguna comprobación automática y su control de calidad son reuniones
y listas que revisa una persona*. **`probar` y `auditar` son, hoy, exactamente eso**: una lista que revisa una
persona. La skill `auditar` incluso define una fórmula de score numérico —cobertura de nombres, valores en
crudo, completitud— **y la deja para que el agente la calcule a mano**, que es la manera más segura de que dos
auditorías del mismo sistema den números distintos.

### 🟡 H8 · No hay suite de pruebas ni proyecto de referencia — **ARREGLADO**

> **`ejemplos/base/`** es el sistema dorado y **`pruebas/correr.sh`** la suite, en tres etapas: el dorado pasa
> limpio · cada comprobación detecta su propio error inyectado · ninguna regla `auto` queda sin comprobación.
> **69 en verde, 0 fallos.**
>
> **Y encontró cosas apenas existió.** La mitad de `DS-P02` —«ningún dato se muestra sin una columna que lo
> respalde», la regla que la base de conocimiento llama la más valiosa del sistema— **corría sin nada que mirar**, porque
> `inyectar.py` no arrastraba los campos del dominio a los patrones. Estaba en verde por vacía. Eso es
> exactamente lo que una suite existe para encontrar.
>
> **También destapó tres comprobaciones mías mal planteadas** —un umbral de longitud que la base de conocimiento nunca escribió,
> un vocabulario de dimensionado incompleto, y dos reglas que le pedían selectores CSS a un archivo de
> variables—. Las tres se corrigieron: **el sistema estaba bien y la comprobación estaba mal**, que es el
> hallazgo más incómodo y el más útil.

El mecanismo `--romper DS-xxx` está construido, documentado y es el mejor detalle del plugin. **Y no hay nada
que lo corra sobre las 39 reglas de una vez.**

**Falta:**

- un **sistema dorado** de referencia —`ejemplos/base/`— con marca, inventario, un dominio y dos pantallas;
- un guion que recorra **todas** las reglas con `--romper` y falle si alguna no se detecta;
- el registro de que ese recorrido se corrió.

> **Sin esto, la garantía es una promesa.** El `SKILL.md` dice *«una comprobación que nunca falló no está
> probada: está sin usar»* — **y no hay forma de saber cuáles nunca fallaron.**

### 🟡 H9 · El plugin arrastra 6,5 MB de bases de conocimiento ajenas — **DOCUMENTADO, sin mover archivos**

> **Decisión tomada: solo `conocimiento/DESIGN` es de este plugin**, y así quedó escrito en el README. Las
> otras cuatro KBs siguen intactas donde están y **ninguna skill las lee**. No se movió ni un archivo: el
> `marketplace.json` ya admite varias entradas, así que si algún día tienen sus propios plugins no hay nada
> que reestructurar.

`CLAUDE_PLUGIN_ROOT` es la raíz del repositorio, y ahí conviven `Domain Driven Design`, `Model DataBase`,
`Fundamentals Architecture`, `building-microservices-systems` y `sources/`. **Solo `conocimiento/DESIGN/` es de
este plugin.**

No rompe nada —y las otras KBs son valiosas—, pero quien instale el plugin se lleva las cinco. **La decisión
que falta es explícita:** o el repositorio es un monorepo de KBs con varios plugins declarados en el
marketplace, o `design-system` se empaqueta con su base de conocimiento y nada más.

---

## 4 · Cobertura de las 76 reglas

**Al auditar (1.1.0), y al cerrar (1.2.0):**

| Familia | Reglas | Citadas · antes → después | En un guion · antes → después | Siguen sin citar |
|---|---:|---|---|---|
| **Fundamentos** `DS-F` | 12 | 10 → **10** | 6 → **9** | `F01` `F12` *(semi/manual)* |
| **Tokens** `DS-T` | 10 | 9 → **9** | 8 → **8** | `T10` *(semi)* |
| **Componentes** `DS-C` | 10 | 7 → **8** | 6 → **7** | `C06` `C08` *(semi)* |
| **Disposición** `DS-L` | 10 | 7 → **7** | 3 → **5** | `L04` `L08` `L09` *(semi)* |
| **Patrones** `DS-P` | 6 | 5 → **6** | 4 → **5** | — |
| **Accesibilidad** `DS-A` | 12 | 10 → **12** | 7 → **12** | — |
| **Entrega** `DS-H` | 8 | **1 → 8** | **1 → 8** | — |
| **Puente Figma** `DS-X` | 8 | 7 → **7** | 4 → **4** | `X08` *(manual)* |
| **TOTAL** | **76** | 56 → **67** · 88 % | 39 → **58** · 76 % | **9**, todas `semi`/`manual` |

**Y el corte que más importa** — de las 39 reglas que la base de conocimiento marca como `auto`, **las 39 tienen guion, y las 39
están probadas rompiendo algo a propósito**. Antes eran 33 con guion y ninguna con prueba registrada.

> **Las 9 que siguen sin cita no están huérfanas.** Son `semi` o `manual`, y `auditar.py` las lista en su
> informe HTML leyéndolas de `09-rules/README.md`. **Manual no significa opcional:** significa que el
> verificador no puede, y por eso las marca una persona. Que estén en una tabla del informe es tener dueño;
> estar mencionadas en un `SKILL.md` no lo era.

> **Un `manual` sin citar sí es un fallo.** La base de conocimiento es explícita: *«`manual` no significa opcional; significa que
> el verificador no puede comprobarla, y por eso va a la lista de `10-checklists`»*. Una regla manual que
> ninguna skill menciona **no la comprueba ni la máquina ni la persona**.

---

## 5 · Cobertura de las 10 secciones de la base de conocimiento

| Sección | Skill dueña | Estado al cerrar |
|---|---|---|
| `01-foundations` | `sistema-diseno` + `entregar` (iconos) | ✅ Completa · `DS-F09` y `DS-F10` ahora se miden |
| `02-tokens` | `sistema-diseno` — los tres niveles, modos, alias | ✅ **La mejor cubierta** |
| `03-components` | `sistema-diseno` + `documentar` | ✅ Completa |
| `04-auto-layout` | `pantalla` + `probar` — `DS-L` | ✅ 5 de 10 con guion; las 3 sin citar son `semi` |
| `05-patterns` | `dominio` + `pantalla` | ✅ Completa · **y `DS-P02` ahora corre entera**, no vacía |
| `06-accessibility` | transversal + `probar.py` | ✅ **12 de 12 con guion** · teclado y zoom incluidos |
| `07-handoff` | **`entregar`** | ✅ **Dueña nueva** · 8 de 8 reglas |
| `08-figma-bridge` | `sistema-diseno` §Publicar + `puentes.md` | ✅ Completa · y actualizada con lo comprobado |
| `09-rules` | **todas, y `lib/comun.py` la lee** | ✅ Completa · es la fuente del índice de reglas |
| `10-checklists` | `probar.py` + `auditar.py` | ✅ Se ejecuta lo automático y **se imprime lo manual** |

---

## 6 · Lo que se arregló en esta pasada

### Primera pasada · lo que rompía el plugin hoy

| Cambio | Archivos | Efecto |
|---|---|---|
| **Reapuntadas las 16 referencias rotas** a las secciones reales de la base de conocimiento | los 6 `SKILL.md` | Las rutas del plugin resuelven; antes 16 no |
| **Creado `.claude-plugin/marketplace.json`** | nuevo | El plugin se instala siguiendo su propio README |
| **Reescrito el puente de Figma con lo comprobado** | `puentes.md` · `08-figma-bridge` · `07-handoff` · `00-ANALISIS` · `sistema-diseno/SKILL.md` | El plugin sabe que puede escribir, qué skill cargar antes, y que hay que mirar el asiento |

### Segunda pasada · los seis huecos estructurales

| Cambio | Qué se agregó |
|---|---|
| **La skill `entregar`** | `SKILL.md` · `scripts/entregar.py` · `commands/entregar-sistema.md` — 9 reglas, 7 sin dueño antes |
| **`probar.py`** | 8 comprobaciones donde había una lista para revisar a ojo |
| **`auditar.py`** | El score con la fórmula implementada una vez, más la cobertura de las 76 reglas |
| **`lib/comun.py`** | `R`, `juzgar`, `Reporte`, contraste — **y `cargar_reglas()`, que lee la base de conocimiento** |
| **`ejemplos/base/`** | El sistema dorado: dominio, dos pantallas, recursos, entrega, movimiento |
| **`pruebas/construir.sh` · `correr.sh`** | La suite en tres etapas |
| **`--romper lista`** en los tres verificadores | La suite pregunta qué se puede romper en vez de adivinarlo del código |
| **`inyectar.py` arrastra los campos** | La mitad de `DS-P02` corría vacía; ahora corre |
| **Quitada la duplicación** | `R` y `juzgar` estaban copiados en tres guiones. La regla 3 de la skill decía por qué eso no se sostiene |

**Comprobado después de todos los cambios:**

```
rutas citadas que resuelven        78 / 78
JSON válidos                       todos
python compila                     lib + 7 guiones
suite completa                     69 en verde · 0 fallos · 0 avisos
reglas auto con guion              39 / 39
reglas auto probadas               39 / 39
reglas de la base de conocimiento sin dueño          0
```

**Y una decisión de método:** el párrafo viejo de `00-ANALISIS` que concluía que Figma era de solo lectura
**se dejó en pie, tachado por el nuevo con su fecha**. Una base de conocimiento que borra su conclusión anterior pierde la única
prueba de que su método funciona — la afirmación se sostuvo en una lectura, se contrastó, y se corrigió.

---

## 7 · El plan de mejora, por impacto — **EJECUTADO**

**Tres, no diez.** En este orden. **Las tres están hechas**; lo que sigue queda como registro de qué se hizo y
por qué en ese orden.

### 1 · La skill `entregar` — cierra `07-handoff` y 7 reglas de una vez

**Es el hueco más grande y el más barato de cerrar**, porque `construir.py` ya hace la mitad.

Qué cubriría: la **estructura de siete páginas** del archivo `[Libro 1, capítulo 4]`, el **paquete de recursos**
—iconos SVG normalizados, imágenes en WebP/AVIF—, el **contrato de animación con sus cinco datos** y el
**modo de desarrollo**. Con un `entregar.py` que comprueba `DS-F09`, `DS-F10`, `DS-H04`, `DS-H05` y `DS-H06`
—cinco de las seis `auto` que faltan— sobre los archivos reales, no sobre el JSON.

> Empieza por `DS-F10`. Medir bytes y buscar tres cadenas en un SVG son diez líneas, y es una regla OBLIGATORIA
> que hoy no comprueba nadie.

### 2 · La suite de pruebas y el sistema dorado

`ejemplos/base/` con marca, inventario, un dominio y dos pantallas, más `pruebas/correr.sh` que recorre las 39
reglas con `--romper` y **falla si alguna no se detecta**.

**Convierte la garantía del plugin en un hecho comprobable.** Y es lo que hace que agregar la skill `entregar`
no rompa lo que ya funciona.

### 3 · Guion para `auditar`, y `probar` con navegador

`auditar.py` que calcule el score con la fórmula de `informe.md` —cobertura de nombres, valores en crudo,
completitud— **para que dos auditorías del mismo sistema den el mismo número**. Y `probar` apoyado en un
navegador sin cabeza para lo que hoy es criterio: foco visible, recorrido por teclado, zoom al 200 % —
`DS-A07`, `DS-A08`, `DS-A11`.

**Es lo que cierra el vacío `G1` del todo:** hoy el plugin automatizó la construcción y dejó la prueba y la
auditoría en manos de una persona, que es justo lo que la base de conocimiento critica de los libros.

---

### Lo que queda fuera del plan, a propósito

- **Las reglas `semi` y `manual` no se arreglan citándolas.** Su lugar es el informe de auditoría, donde una
  persona las marca. **Agregarlas a un `SKILL.md` sin quién las mire habría sido cosmética** — y habría hecho
  que la medida de cobertura mintiera, que es peor que la cobertura baja.
- **El monorepo (H9) quedó como decisión escrita.** Solo `conocimiento/DESIGN` es de este plugin; las otras
  cuatro KBs no las lee ninguna skill. No se movió ningún archivo.
- **`DS-A12` sigue pendiente, y se dice.** «axe-core en la tubería cuando exista la aplicación» necesita un
  navegador y una aplicación; `probar.py` es estático y **lo declara en su propio encabezado**. Prepara esa
  mejora, no la disimula.

---

## 8 · Lo que queda por hacer

**Nada de esto es un hueco: es el siguiente escalón.** Se registra para que no se confunda con lo terminado.

| Qué | Por qué todavía no | Cuándo tendría sentido |
|---|---|---|
| **`axe-core` en la tubería** — `DS-A12` | Necesita un navegador y una aplicación que exista | Cuando haya una aplicación real, no solo el sistema |
| **Dibujar de verdad en el lienzo** | El asiento de esta cuenta es *View* en plan starter: las herramientas de escritura están visibles y **el permiso no** | Con un asiento que escriba. `puentes.md` ya tiene el protocolo listo |
| **`Code Connect`** | Requiere plan Organización o Empresarial `[Libro 1, capítulo 5]` | Queda como opción, no como plan — `DS-X06` |
| **Las 21 reglas `semi`** | Necesitan renderizar o una herramienta externa | Varias podrían volverse `auto` como pasó con `DS-H01`, `H07` y `H08`: **la clasificación de la base de conocimiento era conservadora** |

> **El hallazgo que vale registrar del ejercicio entero:** tres reglas que la base de conocimiento marcaba `semi` o `manual`
> resultaron comprobables en cuanto la estructura se declaró en un JSON en vez de vivir dentro de una
> herramienta. **El límite no era la regla: era dónde estaba escrita la respuesta.**
