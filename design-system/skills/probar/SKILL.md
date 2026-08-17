---
name: probar
description: Prueba una pantalla o un flujo antes de darlo por terminado — los cinco momentos, los cuatro estados de contenido, el valor más largo y más corto, foco y teclado, zoom al 200 % y gama baja — y entrega el resultado como HTML. Úsala SIEMPRE que el usuario pida probar, revisar, validar o recorrer una pantalla o un flujo, o quiera ver si una pantalla aguanta los datos reales y los casos límite.
---

# Probar

**Maquetar es la mitad; probar es la otra.** Una pantalla no está lista cuando se ve bien, sino cuando aguanta
los datos más largos, la lista vacía y el estado de error — y se recorre con teclado. `probar` recorre todo eso
y entrega un reporte **HTML**.

---

## Lo que no se negocia

**1 · Los cinco momentos del flujo** — entrada · decisión · éxito · error · salida. Si falta el cuarto, el patrón
está incompleto — DS-P03.

**2 · Cuatro estados, no uno** — lleno, cargando, vacío, error — DS-C03.

**3 · Se prueba con el valor más largo y el más corto** — DS-L06. Un nombre de dos letras y uno de cuarenta.

**4 · Se recorre con teclado, en orden lógico** — DS-A07. Lo que se hace con ratón, con teclado.

**5 · El resultado se ve, no se lee.** Reporte HTML, no un párrafo.

---

## El orden

### Paso 1 · Tomar lo ya declarado

La pantalla (`pantallas/<nombre>.json`) y el dominio (`dominios/<tipo>.json`). Si no existen, no hay nada que
probar: decirlo.

### Paso 2 · Los cinco momentos

Para cada flujo, recorrer **entrada → decisión → éxito → error → salida**. El detalle de cada momento, en
`${CLAUDE_PLUGIN_ROOT}/skills/pantalla/referencias/patrones.md`. Si un momento no existe, es un fallo — DS-P03.

### Paso 3 · Los estados

| Estado | Qué se comprueba |
|---|---|
| **Lleno** | El caso feliz |
| **Cargando** | Esqueleto con la forma del contenido, no un giro genérico |
| **Vacío** | Por qué está vacío y qué hacer — no una pantalla en blanco |
| **Error** | Qué pasó y cómo reintentar |

### Paso 4 · Los valores límite

El valor **más largo** y **más corto** de cada campo — DS-L06. Es donde las maquetas se rompen.

### Paso 5 · Accesibilidad

Foco visible, recorrido por teclado, zoom al 200 %, gama baja — DS-A07, DS-A08, DS-A11. El detalle, en
`${CLAUDE_PLUGIN_ROOT}/conocimiento/accesibilidad.md`.

### Paso 6 · Entregar

Reporte HTML: `salidas/pruebas/<nombre>.html` — cada momento y estado, con lo que pasó y lo que falta.

---

## Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/skills/pantalla/referencias/patrones.md` | Los cinco momentos y cómo se declaran |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/accesibilidad.md` | Contraste, foco, orden de lectura, zoom |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/checklists.md` | La lista completa de comprobación manual |

---

## Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Probar solo el caso feliz** | No hay vacío ni error | Los cuatro estados |
| **Texto corto de ejemplo** | «Ana» donde va un nombre completo | El valor más largo real |
| **Saltarse el teclado** | Solo se probó con ratón | DS-A07 |
| **Reporte en prosa** | Un párrafo en vez de HTML | El HTML, siempre |

---

## Al terminar

1. **Qué se probó** — qué pantalla o flujo.
2. **Qué pasó y qué no** — cada momento y estado, con su resultado.
3. **Qué falló** — y qué regla incumple (DS-xxx).
4. **El reporte HTML**, para que lo mire.
