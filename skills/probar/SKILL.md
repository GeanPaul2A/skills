---
name: probar
description: Prueba una pantalla o un flujo antes de darlo por terminado — los cinco momentos, los cuatro estados de contenido, el valor más largo y más corto, foco y teclado, zoom al 200 % y gama baja — y entrega el resultado como HTML. Úsala SIEMPRE que el usuario pida probar, revisar, validar o recorrer una pantalla o un flujo, o quiera ver si una pantalla aguanta los datos reales y los casos límite.
---

# Probar

**Maquetar es la mitad; probar es la otra.** Una pantalla no está lista cuando se ve bien, sino cuando aguanta
los datos más largos, la lista vacía y el estado de error — y se recorre con teclado. `probar` recorre todo eso
y entrega un reporte **HTML**.

---

## 1 · Lo que no se negocia

**1 · Los cinco momentos del flujo** — entrada · decisión · éxito · error · salida. Si falta el cuarto, el patrón
está incompleto — DS-P03.

**2 · Cuatro estados, no uno** — lleno, cargando, vacío, error — DS-C03.

**3 · Se prueba con el valor más largo y el más corto** — DS-L06. Un nombre de dos letras y uno de cuarenta.

**4 · Se recorre con teclado, en orden lógico** — DS-A07. Lo que se hace con ratón, con teclado.

**5 · El resultado se ve, no se lee.** Reporte HTML, no un párrafo.

**6 · Se mide antes de opinar.** `${CLAUDE_SKILL_DIR}/scripts/probar.py` comprueba ocho reglas solo —momentos,
estados, extremos, tamaño fijo, titular, teclado, zoom—. **Lo que el guion detecta no se revisa a ojo, y lo que
no puede detectar se dice.** Esta skill existía como una lista que revisaba una persona, que es justo lo que el
plugin existe para reemplazar `[Extensión G1]`.

---

## 2 · El procedimiento

### Paso 1 · Correr el guion

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/probar.py --sistema <sistema> --pantallas <carpeta> \
        --html <sistema>/salidas/pruebas/index.html
```

**Comprueba solo:** los cinco momentos (DS-P03), los cuatro estados (DS-C03), los extremos (DS-L06), el tamaño
fijo en texto (DS-F02, DS-L03), un solo titular (DS-A05), el orden de tabulación y el token de foco (DS-A07) y
lo que rompe el zoom al 200 % (DS-A08).

**Lo que no puede:** ejecutar un navegador. Las comprobaciones son estáticas —sobre la declaración y lo
publicado—. **`DS-A12` («axe-core en la tubería cuando exista la aplicación») sigue siendo la mejora
pendiente**, y esto no la reemplaza: la prepara.

Al agregar una comprobación, **pruébala rompiendo algo** — `--romper DS-L06`.

### Paso 2 · Tomar lo ya declarado

La pantalla (`pantallas/<nombre>.json`) y el dominio (`dominios/<tipo>.json`). Si no existen, no hay nada que
probar: decirlo.

### Paso 3 · Los cinco momentos

Para cada flujo, recorrer **entrada → decisión → éxito → error → salida**. El detalle de cada momento, en
`${CLAUDE_PLUGIN_ROOT}/skills/pantalla/referencias/patrones.md`. Si un momento no existe, es un fallo — DS-P03.

### Paso 4 · Los estados

| Estado | Qué se comprueba |
|---|---|
| **Lleno** | El caso feliz |
| **Cargando** | Esqueleto con la forma del contenido, no un giro genérico |
| **Vacío** | Por qué está vacío y qué hacer — no una pantalla en blanco |
| **Error** | Qué pasó y cómo reintentar |

### Paso 5 · Los valores límite

El valor **más largo** y **más corto** de cada campo — DS-L06. Es donde las maquetas se rompen.

### Paso 6 · Accesibilidad

Foco visible, recorrido por teclado, zoom al 200 %, gama baja — DS-A07, DS-A08, DS-A11. El detalle, en
`${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/06-accessibility/README.md`.

### Paso 7 · Entregar

Reporte HTML: `salidas/pruebas/<nombre>.html` — cada momento y estado, con lo que pasó y lo que falta.

---

## 3 · Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Probar solo el caso feliz** | No hay vacío ni error | Los cuatro estados |
| **Texto corto de ejemplo** | «Ana» donde va un nombre completo | El valor más largo real |
| **Saltarse el teclado** | Solo se probó con ratón | DS-A07 |
| **Reporte en prosa** | Un párrafo en vez de HTML | El HTML, siempre |

---

## 4 · Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/scripts/probar.py` | **Siempre, primero.** Las ocho comprobaciones automáticas |
| `${CLAUDE_PLUGIN_ROOT}/skills/pantalla/referencias/patrones.md` | Los cinco momentos y cómo se declaran |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/06-accessibility/README.md` | Contraste, foco, orden de lectura, zoom |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/DESIGN/10-checklists/README.md` | La lista completa de comprobación manual |

---

## 5 · Al terminar

1. **Qué se probó** — qué pantalla o flujo.
2. **Qué pasó y qué no** — cada momento y estado, con su resultado.
3. **Qué falló** — y qué regla incumple (DS-xxx).
4. **El reporte HTML**, para que lo mire.
