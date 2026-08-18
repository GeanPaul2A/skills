---
name: entregar
description: "Prepara y comprueba la entrega del sistema a desarrollo — la estructura de siete páginas del archivo, el paquete de recursos (iconos SVG normalizados, fotografías en WebP o AVIF), el contrato de animación con sus cinco datos, el modo de desarrollo y el versionado por hito. Úsala SIEMPRE que el usuario pida entregar, exportar, empaquetar o pasar a desarrollo un sistema de diseño o unas pantallas, o pregunte por handoff, dev mode, exportación de iconos, optimización de imágenes, especificación de animaciones o cómo organizar el archivo de Figma. Cierra lo que system-design construye y verificar.py comprueba."
---

# Entregar

**El producto final no es un archivo de Figma: es código de producción.**

> *"Puedes diseñar el mejor producto del planeta, pero **si no se desarrolla correctamente, se quedará solo en
> Figma** para tu próxima publicación de Dribbble."* `[Libro 1, capítulo 8]`

`system-design` construye el sistema y `verificar.py` comprueba que cumple sus reglas. **Esta skill comprueba
lo que sale de él hacia el otro lado** — y es lo que decide si el trabajo llega entero o se queda a mitad.

---

## 1 · Lo que no se negocia

**1 · La estructura del archivo es fija, y no es una preferencia.** Siete páginas en el archivo de producto,
seis en el del sistema, **en ese orden** — DS-H01. El motivo, textual:

> *"Imagina que entras a un supermercado nuevo donde todo está colocado al azar… Suena absurdo, pero **si tú
> mismo construiste esa tienda, te parecería bien**. Después de todo, tú sabes dónde está el jugo de manzana."*
>
> *"**Los desarrolladores son los compradores nuevos en tu tienda.**"* `[Libro 1, capítulo 4]`

**2 · Un icono se mide, no se mira.** Menos de 2 kilobytes, sin `<mask>`, `<filter>` ni `<clipPath>`, con los trazados
**combinados** —`Union`, `Subtract`— y no agrupados — DS-F09, DS-F10. Un `<g>` con varias formas adentro es un
grupo, y delata que el icono se exportó sin combinar.

**3 · Las fotografías van en WebP o AVIF.** No es preferencia de formato: la base de conocimiento midió **87 % de ahorro con WebP
y 93.9 % con AVIF** sobre la misma imagen, *"sin pérdida visible de calidad"* — DS-H04. Un PNG ahí son 87
puntos de peso regalados.

**4 · Toda animación se entrega con sus cinco datos** — clase, duración, curva, disparador y propiedad —
DS-H05. Sin los cinco, quien la implementa adivina, y adivinar la curva es lo que produce animaciones que se
sienten distintas de las diseñadas.

**5 · El movimiento se anima con `transform`, nunca con posición** — DS-H06.

> *"Las animaciones con `transform` usan aceleración por hardware y no disparan recálculos de disposición…
> Las basadas en posición obligan al navegador a recalcular la disposición, lo que puede causar tirones,
> **especialmente en móviles**."* `[Libro 1, capítulo 8]`

**6 · Nada se borra** — DS-H08. Lo descartado va a la página de archivo, con su motivo. *"Nunca borres trabajo
que pueda ser valioso después."*

---

## 2 · Cuándo se usa

| El usuario pide | Qué hacer |
|---|---|
| Entregar el sistema a desarrollo | El flujo completo → §3 · El procedimiento |
| Empaquetar o revisar los iconos | Paso 3, sin el resto |
| Especificar una animación | Paso 4 · los cinco datos |
| Organizar el archivo de Figma | Paso 1 · las siete páginas |
| Cerrar un ciclo y versionar | Paso 6 |
| Saber si el puente escribe en el lienzo | **`${CLAUDE_PLUGIN_ROOT}/skills/system-design/referencias/puentes.md`** |

---

## 3 · El procedimiento

### Paso 1 · Crear el esqueleto

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/entregar.py --destino <destino> --iniciar
```

Crea `entrega/estructura.json` con las **siete páginas del producto** y las **seis del sistema**, ya
nombradas y en orden, más `movimiento.json` y las carpetas de recursos. **No inventa contenido: crea los
huecos con su nombre.**

**Las dos estructuras van separadas** por `DS-C07` — fundamentos y componentes no comparten archivo con el
producto.

### Paso 2 · Llenar lo que el producto tenga

La estructura sale creada; lo que va adentro lo sabe el producto. **Lo que no exista todavía se deja vacío y
se dice** — un hueco declarado se puede llenar, uno inventado hay que descubrirlo.

### Paso 3 · El paquete de recursos

**Los iconos no se dibujan ni se buscan a mano: se instalan del catálogo.**

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/iconos.py --catalogo
python3 ${CLAUDE_SKILL_DIR}/scripts/iconos.py --destino <destino> --plataforma ios --uso barra
```

**El catálogo declara por ACCIÓN, no por dibujo** — `buscar`, no `lupa`. El día que la búsqueda cambie de
glifo, cambia una línea y no cambia ninguna pantalla. Es el mismo argumento del nivel semántico de los tokens.

| Plataforma | De dónde sale | Licencia |
|---|---|---|
| `ios` | SF Symbols | **No se descarga** — Apple prohíbe redistribuirlos. El guion dice qué glifo tomar desde Xcode |
| `android` | Material Symbols | Apache-2.0 · se descarga |
| `web` · `desktop` | Lucide | ISC · se descarga |

**Y el tamaño sale de la tabla, no del gusto** — DS-C11:

| Uso | iOS | Android | Web | Desktop |
|---|---:|---:|---:|---:|
| **Barra** — navegación, pestañas | 22 | 24 | 20 | 16 |
| **Control** — botón, acción | 20 | 24 | 20 | 16 |
| **Campo** — dentro de un input | 20 | 20 | 16 | 14 |
| **Línea** — junto a texto corrido | 17 | 18 | 16 | 14 |
| **Grande** — estado vacío | 28 | 32 | 24 | 20 |

> **Un icono de 24 dentro de un campo de 44 de alto se ve gigante; el mismo icono en una barra se ve bien.**
> No es el icono: es la relación con lo que lo rodea.

El guion además normaliza cada SVG: **`currentColor`** —un icono con el color escrito adentro no responde al
modo oscuro— y el grosor según el tamaño (1.5 por debajo de 24, 2 de ahí para arriba).

```
recursos/iconos/      solo .svg, del catálogo
recursos/imagenes/    solo .webp o .avif
```

**Y los nombres siguen el convenio de los tokens** — minúsculas, guiones, barras para agrupar — DS-H02.

> *"Si quieres que los desarrolladores exporten fácilmente los recursos, **necesitan saber qué exportar**. La
> nomenclatura unificada es la clave del éxito."* `[Libro 1, capítulo 8]`

Un recurso llamado `Icon Copy 2.svg` obliga a alguien a abrirlo para saber qué es. **El nombre del componente
que lo usa deriva de la tabla que lo alimenta** — DS-H03, y el recurso hereda ese nombre.

### Paso 4 · El contrato de animación

En `movimiento.json`, una entrada por animación con **los cinco datos**:

| Dato | Qué responde | Valores |
|---|---|---|
| `clase` | ¿se puede simplificar si es difícil? | `esencial` · `adorno` |
| `duracion` | ¿cuánto dura? ¿tiene fases? | `200ms` |
| `curva` | | `linear` · `ease-in` · `ease-out` · `ease-in-out` · Bézier propia |
| `disparador` | ¿qué la activa? **¿y si se dispara dos veces rápido?** | prosa |
| `propiedad` | ¿qué se anima? | `transform` · `opacity` — **nunca `left`, `top`, `width`** |

> **El disparador es el que más se escribe a medias.** «Al abrir» no es un contrato; «al abrir, y si se
> dispara dos veces seguidas la segunda reemplaza a la primera» sí lo es.

**Y la advertencia de peso** `[Libro 1, capítulo 8]`: más de 100 kilobytes de biblioteca solo para transiciones simples
perjudica el rendimiento. Para lo básico, CSS.

### Paso 5 · Comprobar

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/entregar.py --destino <destino>
```

**Cero fallos o no se entrega.** Y **las saltadas se leen en voz alta**: son las preguntas que quedaron sin
hacer, no verdes.

Al agregar una comprobación, **pruébala rompiendo algo a propósito** — `--romper DS-F10`. El veredicto es de
la regla que se rompió, no del total: **✓ lo detectó** (`0`), **✗ pasó sin detectarse** (`1`), **⚠ no se pudo
probar** (`2`, saltada — no es un verde).

### Paso 6 · Versionar y cerrar

**Dos versiones que avanzan por separado**, y la separación es el punto — DS-H09, DS-H10.

| Versión | Dónde | Qué la mueve |
|---|---|---|
| **Del sistema** | `marca.json` → `version` | Un cambio en tokens, componentes, patrones o plantillas |
| **De cada entrega** | `entrega/versiones.json` → `entregas[]` | Un cambio en las pantallas de esa funcionalidad |

**Y toda entrega declara `sistema`: contra qué versión se dibujó.** Cuando el sistema salte a una mayor, esa
línea dice **qué hay que revisar y qué ya estaba al día** — sin abrir nada.

**Qué número sube:**

| Cambio | Sube |
|---|---|
| Cambia el acento, la familia o la escala · se elimina o renombra una pieza · cambia el significado de un rol | **mayor** `2.0.0` |
| Se agrega un componente, patrón, plantilla, modo, idioma, plataforma, variante o estado | **menor** `1.1.0` |
| Se corrige un contraste, una descripción, un `cuando_no`, un token mal apuntado | **parche** `1.0.1` |

> **La duda se resuelve así:** si alguien que ya dibujó con la versión anterior **tiene que volver a mirar su
> pantalla**, es mayor. Si puede ignorar el cambio, es menor o parche.

**Y el hito en el historial de Figma** — DS-H07, en `versiones[]`:

```
Por hito      Proyecto_Hito_vN         Onboarding_Flow_v3     ← el recomendado
Por fecha     Proyecto_AAAA-MM-DD      Onboarding_Flow_2025-01-15
```

**Lo descartado va a `descartado`, con su motivo** — DS-H08.

**El ejemplo momento a momento**, en `${CLAUDE_SKILL_DIR}/referencias/versionado.md`.

---

## 4 · Lo nativo · lo que no se dibuja

**La regla:** si el sistema operativo lo provee, **no se dibuja: se declara.** El contrato completo, en
`${CLAUDE_PLUGIN_ROOT}/recursos/nativo.json`.

**El error que evita** es caro y frecuente: dibujar a mano un teclado, un selector de fecha o un diálogo de
permiso, y quedarse con una copia que **no responde al modo oscuro, no se traduce, no escala con el tamaño de
letra del sistema y no funciona con el lector de pantalla**.

### Teclados

**Todo campo declara su tipo** — y «por omisión» también se declara: se declara que se eligió. Un teclado
equivocado en un campo de teléfono se paga en cada uso.

`texto` · `correo` · `telefono` · `numero` · `decimal` · `url` · `busqueda` · `contrasena` · `codigo-otp`

> **`codigo-otp` es el que más se olvida.** Declararlo hace que el sistema ofrezca el código del SMS solo.

### Permisos · los tres momentos

**El diálogo lo pone el sistema y no se imita.** Lo que se diseña son los otros dos:

| Momento | Qué es |
|---|---|
| **Antes** | La pre-solicitud: por qué lo necesitamos, **cuando la persona intentó hacer algo que lo requiere** — nunca al abrir |
| **Durante** | El diálogo del sistema. No se dibuja, no se decora |
| **Después** | **El plan B**, y no puede ser «no se puede usar la función» |

Cubiertos: ubicación · notificaciones · cámara · fotos · contactos · biometría.

> **La biometría siempre tiene contraseña como plan B.** Falla con guantes, con la cara mojada, a contraluz.

### Componentes del sistema

`hoja-de-accion` · `alerta` · `selector-fecha` · `compartir` · `selector-archivo` · `refrescar`

> **El selector de fecha es el que más se dibuja a mano y el que peor sale.** Cada plataforma tiene su gesto
> aprendido, y una copia obliga a reaprenderlo.

### Nada de emoticones — DS-C12

**Un emoticón no es un icono.** Se ve distinto en cada sistema operativo y versión, no hereda el color del
texto, no escala con el tamaño de letra, y el lector de pantalla lo lee con un nombre que nadie eligió.

**La única excepción es el contenido de la persona usuaria.** Si alguien escribe un emoticón en un mensaje, se
muestra tal cual: es su texto, no la interfaz.

---

## 5 · El modo de desarrollo

**Lo que resuelve, textual** `[Libro 1, capítulo 4]`:

> *"Una de las fuentes más grandes de errores de implementación viene de desarrolladores **tratando de
> adivinar o medir valores a mano**… El modo de desarrollo lo resuelve **mostrando los valores de token
> exactos**. Si usas variables para tus tokens, **los desarrolladores ven los nombres de variable
> directamente**."*

**Es la razón por la que `DS-T05` y `DS-X03` exigen sintaxis por plataforma.** Una variable sin su nombre de
web, iOS y Android obliga al desarrollador a traducir, y ahí vuelve el error que el modo de desarrollo
existía para evitar.

`construir.py --salidas css,swift,android` produce los tres nombres. **Esta skill comprueba que estén.**

### Code Connect

Enlaza el componente de código real con el de Figma: el desarrollador ve una pestaña *Code* y copia el
componente listo. **El MCP de Figma lo expone** —`get_code_connect_map`, `add_code_connect_map`—, y
**requiere plan Organización o Empresarial** `[Libro 1, capítulo 5]`. Queda como opción, no como plan — DS-X06.

---

## 6 · La lista de calidad

*Fuente: `[Libro 1, capítulo 8]`*

**Lo que se revisa de lo construido contra lo diseñado.** El guion cubre lo medible; esto es lo que queda a
ojo, y va a `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/10-checklists/README.md`.

| Bloque | Qué se mira |
|---|---|
| **Fidelidad visual** | Tipografías, tamaños y pesos · espaciado · **¿los colores coinciden exactamente?** · imágenes dimensionadas |
| **Interacción** | Estados sobre/foco/activo/deshabilitado · **carga implementada** · animaciones con su tiempo y curva · **errores funcionales** · teclado fluido |
| **Responsivo** | Distintos tamaños · objetivos táctiles en móvil · componentes que se adaptan al contenido · puntos de corte |

> **Y la nota del revisor técnico del libro, que es la razón de ser de este plugin:** *"Muchos de estos puntos
> deberían idealmente **automatizarse mediante marcos de prueba** en lugar de comprobarse a mano. La
> automatización garantiza consistencia, ahorra tiempo y **detecta problemas de forma más confiable que las
> revisiones manuales**."*

---

## 7 · Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Entregar sin estructura** | Las pantallas y los componentes en la misma página | Las siete páginas, en orden — DS-H01 |
| **Iconos sin combinar** | Un `<g>` con cinco formas adentro, 8 kilobytes | `Union`/`Subtract` antes de exportar — DS-F09 |
| **Icono del tamaño equivocado** | Un 24 dentro de un campo, y se ve gigante | La tabla de `iconos.json` — DS-C11 |
| **Un emoticón como icono** | 🚀 en un botón | Un icono del catálogo — DS-C12 |
| **Dibujar el teclado o el permiso** | Una copia que no responde al modo oscuro | Declararlo en `nativo.json` |
| **Icono con el color adentro** | `fill="#3A45C9"` en el SVG | `currentColor`, siempre |
| **PNG donde va una foto** | `recursos/imagenes/*.png` | WebP o AVIF: 87 % menos — DS-H04 |
| **Animación sin disparador** | «200ms ease-out» y nada más | Los cinco datos — DS-H05 |
| **Animar `left`** | `transition: left .2s` en el CSS | `transform` — DS-H06 |
| **Nombres de exportación libres** | `Icon Copy 2.svg` | El convenio de los tokens — DS-H02 |
| **Borrar lo descartado** | No hay página de archivo | Va a `archivo`, con su motivo — DS-H08 |
| **Versionar por fecha** | `Proyecto_2025-01-15` como esquema principal | Por hito; la fecha desempata — DS-H07 |

---

## 8 · Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/referencias/versionado.md` | **Al versionar.** El ejemplo momento a momento, y qué número sube |
| `${CLAUDE_PLUGIN_ROOT}/recursos/iconos.json` | El catálogo: qué glifo y qué tamaño por plataforma |
| `${CLAUDE_PLUGIN_ROOT}/recursos/nativo.json` | **Lo que no se dibuja.** Teclados, permisos, componentes del sistema, chrome |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/11-composicion/README.md` | Tamaño de icono, desborde, foco único |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/07-handoff/README.md` | **La sección entera.** Estructura, nombres, exportación, animación, versionado |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/01-foundations/README.md` | §1.8 — las reglas técnicas del icono |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/10-checklists/README.md` | La lista de calidad que revisa una persona |
| `${CLAUDE_PLUGIN_ROOT}/skills/system-design/referencias/puentes.md` | Al llevar el sistema a Figma, y antes de prometer que se dibuja |

---

## 9 · Al terminar

1. **Qué se entrega** — cuántos iconos, cuántas imágenes, cuántas animaciones.
2. **Qué se comprobó** y cuántos fallos.
3. **Qué saltó y por qué** — dicho en voz alta, no disfrazado de verde.
4. **Qué queda a ojo** — la lista de calidad, para que una persona la marque.
5. **La versión que se cerró**, si se cerró un ciclo.
