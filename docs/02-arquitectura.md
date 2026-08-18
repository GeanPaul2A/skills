# Arquitectura del complemento

> **Qué explica este documento.** Cómo está armado `design-system` por dentro: qué capas tiene, qué hace cada
> carpeta, cómo circula la información entre ellas y qué decisiones de diseño sostienen esa estructura.
>
> **A quién está dirigido.** A quien vaya a modificar el complemento, agregar una regla o entender por qué está
> organizado así. Para usarlo no hace falta leer esto: para eso está la [guía de uso](01-guia-de-uso.md).

---

## Índice

1. [Principio rector](#1--principio-rector)
2. [Las cuatro capas](#2--las-cuatro-capas)
3. [Mapa de carpetas](#3--mapa-de-carpetas)
4. [Flujo de información](#4--flujo-de-información)
5. [Contratos entre capas](#5--contratos-entre-capas)
6. [Decisiones de arquitectura](#6--decisiones-de-arquitectura)
7. [Cómo se ejecuta una verificación](#7--cómo-se-ejecuta-una-verificación)
8. [Documentos relacionados](#documentos-relacionados)

---

## 1 · Principio rector

**Todo lo que el complemento afirma tiene que poder comprobarse, y toda comprobación tiene que poder probarse.**

De ese principio se derivan las tres propiedades que gobiernan la arquitectura entera:

| Propiedad | Enunciado | Dónde se hace efectiva |
|---|---|---|
| **Fuente única** | Un valor se escribe una vez. Lo demás se deriva | `marca.json` → `derivar.py` → `tokens/` |
| **Verificación real** | Una regla escrita sin comprobación es una recomendación | `conocimiento/DESIGN/09-rules/` → los guiones |
| **Prueba de la prueba** | Una comprobación que nunca falló está sin usar, no probada | `--romper` → `pruebas/correr.sh` |

> **La consecuencia más visible:** ninguna carpeta guarda algo que otra pueda calcular. Un archivo derivado y
> versionado se desincroniza en la primera edición del original, y a partir de ahí el repositorio describe un
> sistema que ya nadie construye así.

---

## 2 · Las cuatro capas

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 1 · CONOCIMIENTO          conocimiento/DESIGN/            │
│  Las 87 reglas y su fundamento. No ejecuta nada.                │
│  Es la única fuente de verdad sobre qué es correcto.            │
└─────────────────────────────────────────────────────────────────┘
                              ▲  se lee, nunca se copia
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 2 · INFRAESTRUCTURA        lib/comun.py                   │
│  El resultado de una comprobación, el veredicto, el informe     │
│  y el lector de reglas. Lo comparten los cinco verificadores.   │
└─────────────────────────────────────────────────────────────────┘
                              ▲  importan
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 3 · CAPACIDADES            skills/                        │
│  Siete competencias, cada una con su documento de              │
│  instrucciones, sus referencias y sus guiones ejecutables.      │
└─────────────────────────────────────────────────────────────────┘
                              ▲  invocan
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 4 · ENTRADAS               commands/ · recursos/ ·        │
│                                  domains/                      │
│  Puntos de entrada explícitos y catálogos parametrizables.      │
└─────────────────────────────────────────────────────────────────┘
```

**La dirección de las flechas no se invierte nunca.** La capa de conocimiento no sabe que existen los guiones;
los guiones la leen. Es lo que permite editar una regla en el documento y que el verificador la respete sin
tocar código.

---

## 3 · Mapa de carpetas

### 3.1 · Estructura completa

```
design-system/
│
├── README.md                       Puerta de entrada al repositorio
├── LICENSE                         Licencia MIT
├── .gitignore                      Qué se versiona y qué no, con su motivo
│
├── .claude-plugin/
│   ├── plugin.json                 Identidad del complemento
│   └── marketplace.json            Catálogo «geanpaul-design»
│
├── docs/                           Documentación para personas
│   ├── 01-guia-de-uso.md           Cómo se usa, de cero
│   ├── 02-arquitectura.md          Este documento
│   ├── 03-referencia-de-reglas.md  Las 87 reglas, navegables
│   ├── 04-contribuir.md            Cómo se agrega una regla o comprobación
│   ├── 05-registro-de-cambios.md   Historial de versiones
│   └── 90-auditoria-2026-08.md     Informe de auditoría fechado
│
├── conocimiento/DESIGN/            CAPA 1 · el fundamento
│   ├── README.md                   Convenios de la base de conocimiento
│   ├── 00-ANALISIS-DE-CONOCIMIENTO.md  Por qué la base tiene estas secciones
│   ├── 01-foundations/ … 11-composicion/   Las once secciones temáticas
│   ├── TRAZABILIDAD-LIBROS.md      Qué capítulo sostiene cada sección
│   └── glossary.md                 Vocabulario común
│
├── lib/
│   └── comun.py                    CAPA 2 · infraestructura compartida
│
├── skills/                         CAPA 3 · las siete capacidades
│   └── <nombre>/
│       ├── SKILL.md                Instrucciones para el agente
│       ├── referencias/            Documentos que se leen bajo demanda
│       ├── esquemas/               Validación de estructura (JSON Schema)
│       ├── plantillas/             Puntos de partida copiables
│       └── scripts/                Guiones ejecutables
│
├── commands/                       CAPA 4 · entradas explícitas
├── recursos/                       CAPA 4 · catálogos parametrizables
│   ├── iconos.json                 Acción → glifo y tamaño por plataforma
│   └── nativo.json                 Lo que provee el sistema operativo
├── domains/
│   └── _plantilla.json             Especificación de un dominio de negocio
│
├── ejemplos/base/                  El sistema de referencia (fuentes)
└── pruebas/
    ├── construir.sh                Ensambla el sistema de referencia
    └── correr.sh                   La suite completa
```

### 3.2 · Qué contiene cada carpeta de una capacidad

| Carpeta | Qué guarda | Cuándo se lee |
|---|---|---|
| `SKILL.md` | Las instrucciones que el agente sigue | Siempre que la capacidad se activa |
| `referencias/` | Detalle extenso de un tema concreto | Bajo demanda, cuando la tarea lo pide |
| `esquemas/` | Validación de estructura en formato JSON Schema | Antes de aceptar un archivo de configuración |
| `plantillas/` | Archivos de partida que se copian al proyecto | Al crear algo desde cero |
| `scripts/` | Guiones ejecutables, solo con biblioteca estándar | En los pasos de verificación y publicación |

> **La separación entre `SKILL.md` y `referencias/` es económica.** El documento principal se carga entero cada
> vez que la capacidad se activa; las referencias solo cuando hacen falta. Poner en el principal lo que se
> consulta una vez cada veinte usos desperdicia contexto en las otras diecinueve.

---

## 4 · Flujo de información

### 4.1 · Construcción de un sistema

```
  ENTREVISTA
      │
      ▼
  marca.json  ·  proyecto.json          ← lo único que se escribe a mano
      │
      ▼  derivar.py
  tokens/1-primitivos.json              se llama por lo que ES
  tokens/2-semanticos.json              por lo que HACE · un valor por modo
  tokens/3-componentes.json             por dónde se APLICA
      │
      ▼  construir.py
  outputs/sistema.css                   propiedades personalizadas
  outputs/figma-variables.json          tres colecciones con modos
  outputs/lienzo.json                   documento neutral de nodos
  outputs/galeria/*.html                lo que se le muestra a la persona
```

### 4.2 · Inyección de un dominio de negocio

```
  domains/<tipo>.json
      │
      ▼  inyectar.py
  inventario/patrones.json              los flujos del negocio
  inventario/componentes.json           fusiona las piezas propias
  modelo/tables/*.csv                   contra lo que se cruza cada dato
  proyecto.json → modelo_de_datos       queda apuntando al modelo
```

### 4.3 · Verificación

```
  conocimiento/DESIGN/09-rules/README.md
      │
      ▼  lib/comun.py → cargar_reglas()
  {DS-F01: {enunciado, nivel, verifica, origen, familia}, …}
      │
      ├──▶  verificar.py             el sistema
      ├──▶  verificar-screen.py    las pantallas
      ├──▶  deliver.py              el paquete de entrega
      ├──▶  test.py                los límites y la accesibilidad
      └──▶  audit.py               el estado y la cobertura
```

> **`cargar_reglas()` lee el documento, no una copia.** Si alguien agrega una regla a la tabla y ningún guion
> la comprueba, el informe de auditoría la señala solo. Nadie tiene que acordarse de mirar.

---

## 5 · Contratos entre capas

### 5.1 · Archivos de configuración de un sistema

| Archivo | Quién lo escribe | Quién lo lee | Se versiona |
|---|---|---|---|
| `marca.json` | La persona, mediante entrevista | `derivar.py`, `deliver.py` | Sí |
| `proyecto.json` | La persona, mediante entrevista | Todos los verificadores | Sí |
| `domains/<tipo>.json` | La persona, mediante entrevista | `inyectar.py` | Sí |
| `inventario/*.json` | `inyectar.py` y la persona | Todos los verificadores | Sí |
| `screens/*.json` | La persona | `verificar-screen.py`, `test.py` | Sí |
| `delivery/*.json` · `motion.json` | La persona | `deliver.py` | Sí |
| `tokens/*.json` | `derivar.py` | Todos | **No** |
| `outputs/*` | `construir.py` | `test.py`, `deliver.py` | **No** |
| `modelo/*` | `inyectar.py` | `verificar.py` | **No** |

### 5.2 · Interfaz común de los verificadores

Los cinco guiones de verificación exponen la misma interfaz. Quien aprendió a leer uno sabe leer los otros.

| Argumento | Efecto |
|---|---|
| `--destino` o `--sistema` | Dónde está el sistema que se verifica |
| `--regla DS-XXX` | Ejecuta solo las comprobaciones de esa regla |
| `--romper DS-XXX` | Inyecta un error a propósito y juzga si se detecta |
| `--romper lista` | Enumera qué reglas sabe romper |

**Códigos de salida, y los tres son distintos a propósito:**

| Código | Significado |
|---|---|
| `0` | Sin fallos, o el error inyectado **se detectó** |
| `1` | Hay fallos, o el error inyectado **pasó sin detectarse** |
| `2` | El error inyectado **no se pudo probar**: la comprobación está saltada |

> **El código `2` es el que hace que el mecanismo sirva.** Sin él, una comprobación que nunca corrió daría el
> mismo resultado que una que corrió y funcionó.

### 5.3 · El objeto `R`, resultado de una comprobación

```python
R(regla, nombre)     # identidad: qué regla y con qué nombre legible
  .ok(cuantos=1)     # sumó tantos elementos correctos
  .mal(mensaje)      # encontró un fallo, con su explicación
  .saltar(motivo)    # no pudo correr, y dice por qué
```

**Los tres estados no son decorativos.** `saltada` existe porque una comprobación que no corrió **no es un
resultado favorable**: es una pregunta que quedó sin hacer, y callarla la convierte en una afirmación falsa.

---

## 6 · Decisiones de arquitectura

### 6.1 · Solo biblioteca estándar

**Ningún guion depende de un paquete externo.** La instalación del complemento no ejecuta `pip` ni descarga
nada. Se puede correr en cualquier máquina con Python 3 y funciona igual dentro de cinco años.

**El costo:** algunas comprobaciones son estáticas donde una biblioteca permitiría más. `test.py` no ejecuta
un navegador, y **lo declara en su propio encabezado** en vez de disimularlo.

### 6.2 · Las reglas se leen, no se copian

`lib/comun.py` analiza la tabla de `09-rules/README.md` en tiempo de ejecución. **Una copia se desincroniza en
la primera edición**, y desde ahí el guion comprueba una regla que ya no dice lo que dice el documento.

### 6.3 · El complemento es agnóstico del negocio

Ninguna capacidad sabe de transporte, banca ni comercio. **Lo propio de un negocio vive en
`domains/<tipo>.json`**, y las piezas que solo tienen sentido ahí entran al inventario marcadas
`"universal": false` **con su motivo escrito**.

> **Para qué sirve el motivo escrito:** es lo que permite llevarse los componentes universales a otro producto
> sin arrastrar lo que no sirve. Sin él, dentro de seis meses nadie sabe cuál era cuál.

### 6.4 · Lo derivado no se versiona

Ver §5.1. **La única excepción declarada** son los recursos de `ejemplos/base/`, que son fuentes del sistema de
referencia y están exceptuados explícitamente en `.gitignore`.

### 6.5 · Las claves con guion bajo son notas

En todo archivo de configuración, una clave que empieza con `_` es una nota para quien lo lea, **no una
entrada**. `lib/comun.py` → `tabla()` las filtra en un solo lugar.

> **Se aprendió rompiéndolo:** agregar una nota `_lee` a `plantillas.json` tumbó cuatro verificadores de golpe,
> porque cada uno filtraba por su cuenta y uno se olvidaba.

### 6.6 · El catálogo de iconos declara, no distribuye

`recursos/iconos.json` declara **qué glifo corresponde a cada acción en cada plataforma**; los archivos los
descarga `icons.py` al proyecto. El motivo es legal y concreto: **SF Symbols es de Apple y su licencia prohíbe
redistribuirlos**.

---

## 7 · Cómo se ejecuta una verificación

**El recorrido completo, de la invocación al código de salida.**

```
 1. El guion construye su objeto de contexto
        Sistema(destino) · Contexto(sistema, pantallas) · Entrega(destino) …
        Carga los archivos de configuración y filtra las notas.

 2. Si se pidió --romper, se inyecta el error EN MEMORIA
        romper(contexto, "DS-C03")
        Nunca se toca el disco, salvo donde la comprobación lee de él —
        y en ese caso el guion limpia lo que escribió al terminar.

 3. Se recorren los ejes de comprobación
        for eje, comprobaciones in EJES:
            reporte.eje(eje, [fn(contexto) for fn in comprobaciones])
        Cada función devuelve un objeto R.

 4. El informe decide qué es cada resultado
        · Sin fallos y sin elementos mirados  →  SALTADA, no favorable
        · Con fallos                          →  se imprimen hasta ocho
        · Sin fallos y con elementos          →  favorable

 5. Se cierra
        Sin --romper : código 1 si hubo algún fallo, 0 si no
        Con --romper : el veredicto lo da juzgar(), mirando SOLO
                       los resultados de la regla que se rompió
```

### 7.1 · Por qué el veredicto mira una sola regla

**Si mirara el total de fallos, el mecanismo mentiría en dos direcciones.**

| Situación | Qué diría mirando el total | Qué dice mirando la regla |
|---|---|---|
| La comprobación está rota, pero falló su vecina | Favorable — **falso** | «Pasó sin detectarse» |
| La comprobación está saltada y no corrió nunca | Favorable — **falso** | «No se pudo probar» |

---

## Documentos relacionados

| Documento | Qué aporta |
|---|---|
| [Guía de uso](01-guia-de-uso.md) | Cómo se usa el complemento, paso a paso |
| [Referencia de reglas](03-referencia-de-reglas.md) | Las 87 reglas, con su estado de comprobación |
| [Cómo contribuir](04-contribuir.md) | Cómo se agrega una regla, una comprobación o una capacidad |
| [Base de conocimiento](../conocimiento/DESIGN/README.md) | El fundamento completo, con su trazabilidad |
