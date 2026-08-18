# Versionado · el sistema y las entregas avanzan por separado

**Dos cosas que cambian a distinto ritmo.** El sistema cambia poco y despacio; las funcionalidades, todo el
tiempo. Meterlas en el mismo número hace que `v1.2.0` no diga si cambió un token o si alguien agregó una
pantalla — y eso es justo lo que uno necesita saber.

---

## Las dos versiones

| Qué | Dónde vive | Quién la sube |
|---|---|---|
| **Versión del sistema** | `marca.json` → `version` | Un cambio en tokens, componentes o plantillas |
| **Versión de una entrega** | `entrega/versiones.json` → cada entrega | Un cambio en las pantallas de esa funcionalidad |

**Y cada entrega declara contra qué versión del sistema se dibujó.** Es lo único que permite, cuando el
sistema salte a `v2.0.0`, saber exactamente qué pantallas hay que revisar y cuáles ya estaban al día.

---

## Dos archivos, no uno

**`DS-C07` los separa, y el versionado es la razón más clara de por qué.** El archivo del sistema y el del
producto **cambian a distinto ritmo**, así que no pueden compartir número.

```
Archivo del SISTEMA                    Archivo del PRODUCTO
(la biblioteca — lleva la versión)     (las pantallas — lleva las entregas)
─────────────────────────────────     ────────────────────────────────────
00 · Para empezar                      01 · Para empezar
01 · Tokens                            02 · <Nombre del proyecto>
02 · Componentes                            ├── E1 · Acceso
03 · Patrones                               ├── E2 · Portafolio
04 · Plantillas                             └── …          ← las secciones lógicas
05 · Anotaciones                       03 · Documentación
                                       04 · Componentes    ← los locales del producto
                                       05 · Pruebas y exploración
                                       06 · Archivo
                                       07 · Portada
```

> **Una entrega es una «sección lógica del producto»** `[B1, cap. 4]` — que es exactamente lo que la página
> `02` pide que haya adentro. No se inventa una página nueva: se le pone número y fecha a lo que ya iba ahí.

---

## Cómo se ve, momento a momento

### Momento 1 · el sistema inicial — `v1.0.0`

Solo el archivo del sistema. **Ninguna pantalla de producto todavía**, y el libro dice por qué:

> *"Nuestro diseñador dedicó mucho más tiempo a crear la estructura de fundamentos y los tokens que a crear los
> componentes. Puede parecer que avanzas lento al principio, pero **tener una base sólida hace que todo lo demás
> sea mucho más fácil y rápido después**."* `[B1, cap. 5]`

```
SISTEMA v1.0.0      tokens · 22 componentes · 4 plantillas
PRODUCTO            02 · <proyecto> vacía
```

### Momento 2 · la primera funcionalidad

El acceso no necesita ninguna pieza nueva: **el sistema no se toca, sigue en `v1.0.0`**.

```
SISTEMA v1.0.0      sin cambios
PRODUCTO  02 · <proyecto>
          └── E1 · Acceso          v1.0.0 · sistema v1.0.0 · 2026-08-20
```

### Momento 3 · una funcionalidad que sí pide una pieza nueva

El portafolio necesita un componente `grafico` que no existía. **Eso mueve el sistema a `v1.1.0`** — agrega,
no rompe.

```
SISTEMA v1.1.0      02 · Componentes  ← ahora incluye «grafico»
PRODUCTO  02 · <proyecto>
          ├── E1 · Acceso          v1.0.0 · sistema v1.0.0
          └── E2 · Portafolio      v1.0.0 · sistema v1.1.0
```

> **`E1` no se toca y no queda vieja.** Se dibujó contra `v1.0.0`, y `v1.1.0` solo agregó: nada de lo que usa
> cambió.

### Momento 4 · un cambio que rompe

Cambia el acento de azul a verde. **Toda pantalla dibujada cambia de aspecto: `v2.0.0`.**

```
SISTEMA v2.0.0      01 · Tokens  ← acento nuevo
PRODUCTO  02 · <proyecto>
          ├── E1 · Acceso          v1.0.0 · sistema v1.0.0   ⚠ sin migrar
          └── E2 · Portafolio      v1.1.0 · sistema v2.0.0   ✓ migrada
```

**Ahí se ve el valor entero del esquema:** una sola mirada dice qué falta revisar. Sin él, habría que abrir
las dos y comparar a ojo.

---

## Qué número sube, y cuándo

**Semántico, con el significado adaptado a un sistema de diseño.**

| Cambio | Sube | Por qué |
|---|---|---|
| Cambia el acento, la familia tipográfica o la escala de espaciado | **mayor** `2.0.0` | Cambia el aspecto de **todo lo ya dibujado** |
| Se elimina o se renombra un componente, un rol o un token | **mayor** | Lo que lo usaba deja de resolver |
| Cambia el significado de un rol semántico | **mayor** | Igual de caro, y más difícil de ver |
| Se agrega un componente, un patrón o una plantilla | **menor** `1.1.0` | Lo existente sigue igual |
| Se agrega un modo, un idioma o una plataforma de salida | **menor** | Agrega sin quitar |
| Se agrega una variante o un estado a algo que ya existe | **menor** | |
| Se corrige un contraste, una descripción, un `cuando_no` | **parche** `1.0.1` | No cambia el contrato |
| Se arregla un token mal apuntado | **parche** | Restituye lo que ya decía la ficha |

> **La regla que resuelve las dudas:** si alguien que ya dibujó con la versión anterior **tiene que volver a
> mirar su pantalla**, es mayor. Si puede ignorar el cambio, es menor o parche.

---

## Cómo se nombra en Figma

**Las versiones del historial de Figma llevan el nombre estructurado de `DS-H07`**, por hito:

```
Sistema_Fundamentos_v1        el momento 1
Sistema_Grafico_v1-1          el momento 3
Acceso_Entrega_v1             el cierre de E1
```

**Y la portada muestra siempre la versión vigente del sistema.** Es lo primero que ve quien abre el archivo, y
lo que evita que alguien dibuje contra una versión que ya no existe.

---

## Lo que NO se versiona así

**Las pantallas en curso.** Mientras una funcionalidad se está dibujando vive en `05 · Pruebas y exploración`,
sin número. **Recién al cerrarla pasa a `02 · <proyecto>` como sección, con su versión.**

Un número en algo que todavía se está moviendo no informa: informa cuando alguien puede confiar en que eso ya
no cambia.

**Y nada se borra** — DS-H08. Lo descartado va a `99 · Archivo` con su motivo escrito.
