# design-system

**Un complemento para Claude Code que construye sistemas de diseño verificables** — y que diseña, prueba,
audita, documenta y entrega las pantallas que salen de ellos.

[![Licencia MIT](https://img.shields.io/badge/licencia-MIT-informational)](LICENSE)
[![Versión 1.4.0](https://img.shields.io/badge/versión-1.4.0-informational)](docs/05-registro-de-cambios.md)
[![83 reglas · 50 comprobadas](https://img.shields.io/badge/reglas-83%20·%2050%20comprobadas-informational)](docs/03-referencia-de-reglas.md)

---

## Índice

1. [Qué problema resuelve](#1--qué-problema-resuelve)
2. [Qué lo hace distinto](#2--qué-lo-hace-distinto)
3. [Instalación](#3--instalación)
4. [Primeros pasos](#4--primeros-pasos)
5. [Las siete capacidades](#5--las-siete-capacidades)
6. [Estructura del repositorio](#6--estructura-del-repositorio)
7. [La base de conocimiento](#7--la-base-de-conocimiento)
8. [Suite de pruebas](#8--suite-de-pruebas)
9. [Documentación](#9--documentación)
10. [Licencia y procedencia](#10--licencia-y-procedencia)

---

## 1 · Qué problema resuelve

**Un sistema de diseño se documenta bien y se cumple mal.** Las reglas están escritas, y nada impide que una
pantalla lleve un color fuera de la paleta, un icono desproporcionado o un estado de error que nadie diseñó.
El control queda en manos de revisiones humanas: caras, lentas y desparejas.

**Este complemento convierte esas reglas en comprobaciones que se ejecutan.**

| Sin el complemento | Con el complemento |
|---|---|
| «El botón debería usar el token de acento» | `DS-T07` falla y dice en qué archivo y en qué línea |
| «Faltaría el estado de error» | `DS-C03` falla y nombra el componente |
| «Ese icono se ve grande» | `DS-C11` compara contra la tabla de tamaños de la plataforma |
| «Habría que revisar el contraste» | `DS-A02` lo mide al definir el token, no al final |
| «Creo que está todo bien» | 1224 comprobaciones, cero fallos, y la lista de lo que no se pudo comprobar |

### 1.1 · Qué produce

```
marca.json  ──▶  tokens en tres niveles  ──▶  CSS · Figma · Swift · Android · galería
   +                                              │
proyecto.json                                     ▼
   +                                     pantallas verificadas contra
dominio.json  ─────────────────────────▶  el modelo de datos real
```

---

## 2 · Qué lo hace distinto

### 2.1 · Las reglas se leen de la base de conocimiento, no se copian

Los guiones analizan la tabla de `conocimiento/DESIGN/09-rules/README.md` **en tiempo de ejecución**. Si se
agrega una regla al documento y ningún guion la comprueba, el informe de auditoría la señala solo.

### 2.2 · Una comprobación saltada no es un resultado favorable

```
Saltadas — no son verdes, son preguntas sin hacer:
   DS-P02   los campos citados existen    proyecto.json declara 'modelo_de_datos.tipo': null
```

**Callarlas convertiría el informe en una afirmación falsa.** Se reportan aparte, con su motivo.

### 2.3 · Cada comprobación se prueba rompiendo algo a propósito

```bash
python3 skills/system-design/scripts/verificar.py --destino <sistema> --romper DS-C03
```

**El veredicto es de la regla que se rompió, no del total** — y son tres estados, no dos:

| Código | Veredicto |
|---|---|
| `0` | **Lo detectó.** La comprobación sirve |
| `1` | **Pasó sin detectarse.** La comprobación no sirve |
| `2` | **No se pudo probar.** Está saltada — tampoco es favorable |

> Si el veredicto mirara el total, una comprobación rota daría resultado favorable porque falló su vecina, y
> una saltada lo daría sin haber corrido nunca.

### 2.4 · El núcleo no sabe de tu negocio

Ninguna capacidad conoce transporte, banca ni comercio. **Lo propio de un negocio vive en
`dominios/<tipo>.json`**, y las piezas que solo tienen sentido ahí entran marcadas `"universal": false`
**con su motivo escrito** — que es lo que permite llevarse el resto a otro producto.

### 2.5 · Solo biblioteca estándar

Ningún guion depende de un paquete externo. Se instala sin descargar nada y funciona igual dentro de cinco
años.

---

## 3 · Instalación

### 3.1 · Desde el repositorio

```
/plugin marketplace add GeanPaul2A/skills
/plugin install design-system@geanpaul-design
```

Si el resumen indica `Run /reload-plugins to activate.`, ejecutar ese comando.

### 3.2 · Para desarrollo local

```
/plugin marketplace add ./design-system
/plugin install design-system@geanpaul-design
```

### 3.3 · Comprobar que quedó bien

```bash
./pruebas/correr.sh
```

**Tiene que terminar con `La suite pasa entera`.** Si no, lo que falle aquí va a fallar también en el sistema
que construyas.

**Requisitos:** Python 3.8 o superior. Nada más.

---

## 4 · Primeros pasos

**El orden no es una sugerencia: cada paso necesita lo que dejó el anterior.**

```
system-design  →  dominio  →  pantalla  →  probar  →  entregar  →  auditar
  lo visual      el negocio   las vistas   los límites  a desarrollo  el estado
```

| Paso | Qué escribir en el chat | Qué obtenés |
|---|---|---|
| **1** | «Quiero armar el sistema de diseño de mi producto» | Tokens, componentes, plantillas y una galería para mirar |
| **2** | «Definí el dominio: es una tienda» | Entidades, reglas de negocio y patrones propios |
| **3** | «Diseñá la pantalla de inicio de sesión» | Una pantalla declarada y verificada contra datos reales |
| **4** | «Probá esa pantalla» | Los cinco momentos, los cuatro estados, los valores límite |
| **5** | «Prepará la entrega a desarrollo» | Estructura, iconos, animaciones y la versión cerrada |
| **6** | «Auditá el sistema» | Resultado sobre 100 y las tres acciones que más destraban |

> **La advertencia que conviene leer dos veces**, del libro que originó la base de conocimiento:
> *«Puede parecer que avanzas lento al principio, pero tener una base sólida hace que todo lo demás sea mucho
> más fácil y rápido después.»*

**El recorrido completo, con lo que pregunta cada paso, en la [guía de uso](docs/01-guia-de-uso.md).**

---

## 5 · Las siete capacidades

Se activan solas por lo que pidas. Los comandos existen para cuando quieras ser explícito.

| Capacidad | Qué hace | Comando | Guiones |
|---|---|---|---|
| `system-design` | Tokens en tres niveles, componentes, plantillas, modos y publicación | `/design-system:crear` | `derivar` · `verificar` · `construir` |
| `dominio` | Entidades, reglas de negocio, patrones y piezas propias | `:definir-dominio` | `inyectar` |
| `pantalla` | Una pantalla o un flujo: plantilla, datos y estados | `:disenar-pantalla` | `verificar-pantalla` |
| `probar` | Momentos, estados, valores límite, teclado y ampliación al 200 % | `:probar-pantalla` | `probar` |
| `entregar` | Estructura del archivo, recursos, animación y versión | `:entregar-sistema` | `entregar` · `iconos` |
| `auditar` | Resultado sobre 100, cobertura y acciones priorizadas | `:auditar-sistema` | `auditar` |
| `documentar` | La ficha de una pieza: propiedades, accesibilidad y código | `:documentar-pieza` | usa `verificar` |

### 5.1 · Plataformas admitidas

`ios` · `android` · `web` · `desktop` — se eligen en `proyecto.json`. De esa elección salen el objetivo táctil
mínimo, el tamaño de cada icono, si el estado de puntero tiene sentido y qué componentes nativos hay
disponibles.

---

## 6 · Estructura del repositorio

```
design-system/
├── docs/                    Documentación para personas
├── conocimiento/DESIGN/     Las 83 reglas y su fundamento
├── lib/                     Infraestructura compartida por los verificadores
├── skills/                  Las siete capacidades
├── commands/                Puntos de entrada explícitos
├── recursos/                Catálogo de iconos y contrato nativo
├── dominios/                Especificación de un dominio de negocio
├── ejemplos/base/           El sistema de referencia
└── pruebas/                 La suite
```

**El detalle completo, con qué contiene cada carpeta y por qué, en
[arquitectura](docs/02-arquitectura.md).**

### 6.1 · Qué no se versiona, y por qué

| Excluido | Motivo |
|---|---|
| `conocimiento/sources/` | **El texto completo de dos libros con derechos reservados.** La base de conocimiento cita capítulo y número en vez de copiar texto, así que la trazabilidad no depende de ellos |
| `tokens/` · `salidas/` · `modelo/` | Los produce un guion. Un archivo derivado y versionado se desincroniza en la primera edición del original |
| Iconos descargados | La licencia de SF Symbols prohíbe redistribuirlos |

**Cada exclusión está escrita con su motivo en [`.gitignore`](.gitignore).**

---

## 7 · La base de conocimiento

`conocimiento/DESIGN/` es la única fuente de verdad sobre qué es correcto. **No ejecuta nada**: los guiones la
leen.

| Sección | Qué gobierna |
|---|---|
| `01-foundations` | Rejilla, color, tipografía, espaciado, forma, elevación, iconografía |
| `02-tokens` | Los tres niveles, nomenclatura, alias, modos |
| `03-components` | Arquitectura, propiedades, variantes, estados |
| `04-auto-layout` | Dirección, espacio, relleno y ajuste |
| `05-patterns` | Cómo se declara un patrón con su dominio y sus datos |
| `06-accessibility` | Contraste, teclado, lector de pantalla, WCAG 2.1 AA |
| `07-handoff` | Estructura del archivo, exportación, animación, versionado |
| `08-figma-bridge` | Variables, colecciones, modos y alcance |
| `09-rules` | **Las 83 reglas.** Es la tabla que leen los guiones |
| `10-checklists` | Lo que revisa una persona |
| `11-composicion` | Tamaño de icono, desborde, foco visual y jerarquía |

### 7.1 · Origen y trazabilidad

La base de conocimiento se construyó leyendo dos libros completos y registrando **qué capítulo sostiene cada
sección**. Las extensiones existen solo para llenar vacíos que los propios libros dejan, detectados leyéndolos.

- *Design Beyond Limits with Figma*, de Šimon Jůn — el libro del sistema.
- *Designing and Prototyping Interfaces with Figma*, tercera edición — el libro del oficio.

**El registro capítulo por capítulo, en [`TRAZABILIDAD-LIBROS.md`](conocimiento/DESIGN/TRAZABILIDAD-LIBROS.md).**

---

## 8 · Suite de pruebas

```bash
./pruebas/correr.sh             # todo
./pruebas/correr.sh --rapido    # solo la corrida limpia, sin las inyecciones
```

**Cuatro etapas:**

| Etapa | Qué comprueba |
|---|---|
| **1** | El sistema de referencia pasa limpio en los cinco verificadores |
| **2** | **Cada comprobación detecta su propio error inyectado** |
| **3** | Ninguna regla automática de la base de conocimiento queda sin comprobación |
| **4** | La documentación generada coincide con la base de conocimiento |

### 8.1 · Estado actual

```
sistema      1224 comprobaciones en verde · 0 fallos · 1 saltada
entrega        39 comprobaciones en verde · 0 fallos
pantallas      83 comprobaciones en verde · 0 fallos
auditoría     535 comprobaciones en verde · 0 fallos
pruebas        61 comprobaciones en verde · 0 fallos

reglas en la base de conocimiento    83
marcadas «auto»                      50
con comprobación                     50
probadas rompiéndolas a propósito    50
```

---

## 9 · Documentación

| Documento | Qué explica | Para quién |
|---|---|---|
| [Guía de uso](docs/01-guia-de-uso.md) | Cómo se usa, de cero a un sistema entregable | Quien va a usarlo |
| [Arquitectura](docs/02-arquitectura.md) | Cómo está armado por dentro | Quien va a modificarlo |
| [Referencia de reglas](docs/03-referencia-de-reglas.md) | Las 83 reglas y su estado de comprobación | Consulta |
| [Cómo contribuir](docs/04-contribuir.md) | Cómo se agrega una regla o una comprobación | Quien va a extenderlo |
| [Registro de cambios](docs/05-registro-de-cambios.md) | Historial de versiones | Consulta |
| [Auditoría 2026-08](docs/90-auditoria-2026-08.md) | Informe fechado del estado del complemento | Contexto |
| [Sistema de referencia](ejemplos/README.md) | Qué ejercita la suite y cómo se amplía | Quien va a extenderlo |

---

## 10 · Licencia y procedencia

**Licencia MIT.** Ver [`LICENSE`](LICENSE).

### 10.1 · Sobre los conjuntos de iconos

El complemento **declara** qué icono usar en cada plataforma y **no redistribuye ninguno**.

| Conjunto | Licencia | Se descarga |
|---|---|---|
| SF Symbols | Apple SF Symbols License | **No.** Apple prohíbe redistribuirlos; se toman desde Xcode |
| Material Symbols | Apache-2.0 | Sí |
| Lucide | ISC | Sí |

### 10.2 · Sobre los libros

Las citas identifican capítulo y obra. **El texto de los libros no forma parte del repositorio** y está
excluido en `.gitignore`.
