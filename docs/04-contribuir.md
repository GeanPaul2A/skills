# Cómo contribuir

> **Qué explica este documento.** El procedimiento para agregar una regla, una comprobación o una capacidad al
> complemento, y el criterio con el que se acepta cada una.
>
> **A quién está dirigido.** A quien vaya a modificar el complemento. Para usarlo alcanza con la
> [guía de uso](01-guia-de-uso.md).

---

## Índice

1. [La regla de aceptación](#1--la-regla-de-aceptación)
2. [Agregar una regla a la base de conocimiento](#2--agregar-una-regla-a-la-base-de-conocimiento)
3. [Escribir su comprobación](#3--escribir-su-comprobación)
4. [Agregar el caso de error inyectado](#4--agregar-el-caso-de-error-inyectado)
5. [Ampliar el sistema de referencia](#5--ampliar-el-sistema-de-referencia)
6. [Agregar una capacidad nueva](#6--agregar-una-capacidad-nueva)
7. [Convenios de escritura](#7--convenios-de-escritura)
8. [Lista de comprobación antes de entregar](#8--lista-de-comprobación-antes-de-entregar)
9. [Documentos relacionados](#documentos-relacionados)

---

## 1 · La regla de aceptación

**Una sola, y de ella salen todas las demás:**

> **Nada entra si no se puede comprobar, y ninguna comprobación entra si no se puede probar.**

| Lo que se propone | Qué hace falta para que entre |
|---|---|
| Una regla nueva | Que esté escrita en la base de conocimiento, con su origen |
| Una regla clasificada `auto` | Que exista el guion que la comprueba |
| Una comprobación nueva | Que exista su caso de error inyectado en `romper()` |
| Un caso de error inyectado | Que el sistema de referencia tenga el escenario que lo activa |

### 1.1 · El error que esta regla previene

**Una comprobación que nunca falló no está probada: está sin usar.** Se ve favorable en cada corrida, no
detecta nada, y nadie se entera hasta que un fallo real pasa de largo.

**Y el caso peor:** una comprobación que corre sin nada que mirar. Devuelve cero fallos, se cuenta como
favorable, y en realidad no comprobó nada. Por eso `lib/comun.py` marca como **saltada** toda comprobación que
termine con cero elementos mirados.

---

## 2 · Agregar una regla a la base de conocimiento

### 2.1 · Elegir la familia y el número

| Prefijo | Familia | Sección |
|---|---|---|
| `DS-F` | Fundamentos | `01-foundations/` |
| `DS-T` | Tokens | `02-tokens/` |
| `DS-C` | Componentes | `03-components/` · `11-composicion/` |
| `DS-L` | Disposición | `04-auto-layout/` |
| `DS-P` | Patrones | `05-patterns/` |
| `DS-A` | Accesibilidad | `06-accessibility/` · `11-composicion/` |
| `DS-H` | Entrega | `07-handoff/` |
| `DS-X` | Puente con Figma | `08-figma-bridge/` |

**El número es el siguiente libre de esa familia, y no se reutiliza nunca.** Un identificador reciclado
convierte toda cita anterior en una mentira silenciosa.

### 2.2 · Escribirla en dos lugares

**Primero en la sección temática**, con su fundamento y su ejemplo. **Después en la tabla de
`09-rules/README.md`**, que es la que leen los guiones:

```
| **C15** | Enunciado en una línea, en presente | OBLIGATORIO | **auto** | Extensión G11 |
```

| Columna | Valores admitidos |
|---|---|
| Identificador | La letra de la familia y dos dígitos, entre asteriscos dobles |
| Enunciado | Una línea. Si no entra en una línea, son dos reglas |
| Nivel | `OBLIGATORIO` o `RECOMENDADO` |
| Verifica | `auto`, `semi`, `manual` o `—` |
| Origen | `Libro N · capítulo` o `Extensión GN` |

### 2.3 · Declarar el origen

**Toda regla dice de dónde sale.** Si viene de uno de los dos libros, se cita el capítulo. Si es una extensión,
**se declara qué vacío llena** y se documenta ese vacío en `00-ANALISIS-DE-CONOCIMIENTO.md`.

> **Una regla sin origen es una preferencia con formato de norma.** El origen es lo que permite discutirla:
> si alguien no está de acuerdo, puede ir a la fuente en vez de discutir contra el documento.

### 2.4 · Comprobar que la base de conocimiento sigue legible

```bash
python3 -c "import sys; sys.path.insert(0,'lib'); from comun import cargar_reglas; print(len(cargar_reglas()))"
```

**Si el número no subió, la fila está mal formada** y el lector la descartó en silencio.

---

## 3 · Escribir su comprobación

### 3.1 · Elegir el guion

| Qué comprueba la regla | Guion |
|---|---|
| Tokens, componentes, patrones del sistema | `skills/system-design/scripts/verificar.py` |
| Una pantalla declarada | `skills/screen/scripts/verificar-screen.py` |
| El paquete de entrega, recursos, animación, versiones | `skills/deliver/scripts/deliver.py` |
| Límites, accesibilidad estática, estados | `skills/test/scripts/test.py` |
| Estado general, nombres, cobertura | `skills/audit/scripts/audit.py` |

### 3.2 · La forma de una comprobación

```python
def c15_lo_que_sea(s):
    """DS-C15 · el enunciado, en una línea.

    Por qué existe la regla, con el caso concreto que la motiva. Si la regla previene un
    error específico, se nombra ese error: es lo que hace que quien lea el código dentro
    de un año entienda por qué no puede borrarla.
    """
    r = R("DS-C15", "un nombre legible de lo que se comprueba")
    if not s.componentes:
        return r.saltar("no hay inventario que revisar")
    for nombre, c in s.componentes.items():
        if condicion_de_fallo(c):
            r.mal(f"{nombre}: qué está mal, y qué habría que hacer")
        else:
            r.ok()
    return r
```

### 3.3 · Las tres obligaciones

**Primera: saltar en vez de fingir.** Si no hay nada que comprobar, `r.saltar(motivo)` con el motivo escrito.
Nunca devolver un resultado favorable vacío.

**Segunda: el mensaje de fallo dice qué hacer.** No `«boton: mal»`, sino
`«boton: declara 12 variantes — tres o cuatro cubren cualquier producto»`.

**Tercera: no inventar reglas.** La comprobación mide **lo que la base de conocimiento escribió**, no lo que a
quien la programa le parece razonable.

> **Se aprendió cometiéndolo tres veces.** Un umbral de longitud que la base de conocimiento nunca escribió,
> un vocabulario incompleto, y dos reglas que le pedían selectores a un archivo de variables. En los tres
> casos **el sistema estaba bien y la comprobación estaba mal** — que es el hallazgo más incómodo y el más útil.

### 3.4 · Registrarla en su eje

```python
EJES = [
    ("Composición", [b16_tamano_icono, b17_sin_emoticones, b18_anidacion, c15_lo_que_sea]),
]
```

---

## 4 · Agregar el caso de error inyectado

**Sin esto, la comprobación no está probada.** La suite lo reporta como
*«con comprobación pero sin caso de `--romper`»*.

```python
daños = {
    "DS-C15": lambda: next(iter(s.componentes.values())).__setitem__("campo", "valor malo"),
}
```

### 4.1 · Cómo se elige el daño

**El daño tiene que ser el error que de verdad se comete**, no uno inventado para que la comprobación falle.

| Buen daño | Mal daño |
|---|---|
| Poner los extremos al revés — pasa al copiar y pegar de otro campo | Poner `null` donde va un objeto |
| Doce variantes en un botón — pasa al no decidir | Borrar la clave entera |
| Un icono de 24 dentro de un campo — pasa por descuido | Poner un tamaño negativo |

### 4.2 · Cuando el daño toca el disco

Algunas comprobaciones leen archivos. En ese caso, **el guion limpia lo que escribió al terminar**: una prueba
que deja restos ensucia la corrida siguiente.

### 4.3 · Comprobarlo

```bash
python3 skills/system-design/scripts/verificar.py --destino /tmp/dorado --romper DS-C15
```

| Código | Qué significa |
|---|---|
| `0` | **Lo detectó.** La comprobación sirve |
| `1` | **Pasó sin detectarse.** La comprobación no sirve |
| `2` | **No se pudo probar.** Está saltada — no es un resultado favorable |

**Si sale `2`, el sistema de referencia no tiene el escenario que la activa.** Ir a la sección siguiente.

---

## 5 · Ampliar el sistema de referencia

`ejemplos/base/` es el sistema contra el que corre la suite. **Su trabajo no es parecerse a un producto real:
es tener un caso de cada cosa que hay que comprobar.**

| Qué falta | Dónde se agrega |
|---|---|
| Una entidad, una regla de negocio o un patrón | `ejemplos/base/domain.json` |
| Una pantalla con una situación nueva | `ejemplos/base/screens/` |
| Un recurso, una animación, una entrega | `ejemplos/base/recursos/`, `motion.json`, `delivery/` |
| Un componente con una característica nueva | `skills/system-design/plantillas/componentes-base.json` |

> **Si una comprobación no puede correr contra el sistema de referencia, le falta un caso al sistema de
> referencia — no le sobra a la comprobación.** Debilitar la comprobación para que pase es exactamente el
> movimiento que hay que evitar.

**Lo derivado no se versiona.** Las fuentes viven en `ejemplos/base/`; los tokens, el modelo y las salidas los
produce `pruebas/construir.sh` en una carpeta temporal.

---

## 6 · Agregar una capacidad nueva

### 6.1 · Estructura mínima

```
skills/<nombre>/
├── SKILL.md                obligatorio
├── referencias/            lo que se lee bajo demanda
└── scripts/<nombre>.py     si tiene algo que comprobar
```

### 6.2 · El encabezado del documento de instrucciones

```yaml
---
name: <nombre>
description: "Qué hace, en una frase. Después: «Úsala SIEMPRE que el usuario pida
  …» con las palabras concretas que la persona diría. La descripción es lo único
  que el agente ve antes de decidir si activarla."
---
```

**La descripción es el disparador, no un resumen.** Tiene que contener las palabras que una persona usaría al
pedirlo, no la explicación elegante de qué hace la capacidad.

### 6.3 · Registrarla en tres lugares

1. `commands/<verbo>-<objeto>.md` — el punto de entrada explícito.
2. `pruebas/correr.sh` → arreglo `VERIF`, si tiene verificador.
3. `README.md` y `docs/02-arquitectura.md` — la tabla de capacidades.

> **El nombre del comando no puede coincidir con el de la capacidad.** Comparten espacio de nombres, y uno
> tapa al otro en el listado.

---

## 7 · Convenios de escritura

### 7.1 · Idioma y forma

| Convenio | Aplicación |
|---|---|
| Todo en español | Documentos, comentarios, mensajes de los guiones, nombres de función |
| Sin abreviaturas | «base de conocimiento», no «KB» · «capítulo», no «cap.» |
| Identificadores en inglés solo si son técnicos | `SVG`, `CSS`, `JSON`, `WCAG` |
| Las claves con guion bajo son notas | `_lee` explica el archivo a quien lo abre |

### 7.2 · Estructura de un documento

| Elemento | Cuándo |
|---|---|
| Cita de resumen al inicio | Siempre: qué explica y a quién está dirigido |
| Índice numerado | En documentos de más de noventa líneas |
| Secciones numeradas | Siempre, para poder citarlas desde otro documento |
| Tabla en vez de lista | Cuando cada elemento tiene más de un atributo |

### 7.3 · Qué NO hacer

| Práctica | Por qué se evita |
|---|---|
| Copiar una regla a un segundo archivo | Se desincroniza en la primera edición |
| Escribir un documento que enumera lo que otro define | O se genera, o queda viejo |
| Agregar un índice a un documento de instrucciones | El agente lee el archivo entero; el índice gasta contexto |
| Suavizar una comprobación para que el ejemplo pase | Es el movimiento que vacía la garantía |

---

## 8 · Lista de comprobación antes de entregar

```bash
# 1 · La suite entera
./pruebas/correr.sh

# 2 · La documentación generada
python3 lib/generar_referencia.py

# 3 · Que los guiones compilan
python3 -m py_compile lib/*.py skills/*/scripts/*.py

# 4 · Que no quedó basura
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name ".DS_Store" -delete
```

**Y las cuatro condiciones que la suite exige:**

| Condición | Qué se comprueba |
|---|---|
| El sistema de referencia pasa limpio | Los cinco verificadores, cero fallos |
| Cada comprobación detecta su error | Ninguna devuelve `1` ni `2` |
| Ninguna regla `auto` sin comprobación | La cobertura leída de la base de conocimiento |
| La documentación generada está al día | `03-referencia-de-reglas.md` coincide |

> **Cero fallos o no se entrega.** Es literal: la suite devuelve código distinto de cero y el trabajo no está
> terminado.

---

## Documentos relacionados

| Documento | Qué aporta |
|---|---|
| [Arquitectura](02-arquitectura.md) | Cómo está armado el complemento por dentro |
| [Referencia de reglas](03-referencia-de-reglas.md) | Las 89 reglas y su estado de comprobación |
| [Sistema de referencia](../ejemplos/README.md) | Qué ejercita y cómo se amplía |
