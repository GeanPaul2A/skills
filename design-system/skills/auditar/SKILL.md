---
name: auditar
description: Audita un sistema de diseño o un conjunto de pantallas ya existentes y produce un informe accionable — score, coherencia de nombres, cobertura de tokens, completitud de componentes y acciones priorizadas. Úsala SIEMPRE que el usuario pida auditar, revisar, evaluar o medir la salud de un sistema de diseño, unas pantallas o una biblioteca de componentes ya construida. Complementa a verificar (que comprueba reglas al construir) con una evaluación de estado.
---

# Auditar

**Verificar comprueba reglas; auditar mide estado.** `verificar.py` dice si un sistema cumple las reglas mientras
se construye. `auditar` evalúa un sistema o unas pantallas **ya existentes** y dice **qué tan sano está** y **qué
arreglar primero**.

---

## Lo que no se negocia

**1 · Se mide, no se opina.** Cada hallazgo sale de un dato: un hex en crudo, un nombre que rompe el convenio, un
componente sin estados. No de «esto se ve raro».

**2 · El score es de cobertura, no de belleza.** Un sistema con 10 componentes todos documentados saca más que
uno con 50 a medio documentar. 80 % bien cubierto vale más que 100 % de 10.

**3 · Las acciones salen priorizadas por impacto.** No una lista: las tres que más destraban, primero.

**4 · Lo que `verificar.py` ya comprueba, se reusa.** No se reimplementa. La auditoría agrega lo que el
verificador no mide: nombres, cobertura, completitud.

---

## El orden

### Paso 1 · Localizar el objetivo

`marca.json`, `tokens/`, `inventario/` y `pantallas/`. Si no hay sistema, no hay nada que auditar: decirlo.

### Paso 2 · Correr lo automático

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/sistema-diseno/scripts/verificar.py --destino <destino>
python3 ${CLAUDE_PLUGIN_ROOT}/skills/pantalla/scripts/verificar-pantalla.py --sistema <s> --pantallas <p>
```

Eso cubre las reglas `auto`. Lo que **salte**, se anota como «sin comprobar» — **no es un verde**.

### Paso 3 · Medir lo que el verificador no mide

Tres medidas (el detalle y la fórmula, en `${CLAUDE_SKILL_DIR}/referencias/informe.md`):

| Medida | Qué cuenta |
|---|---|
| **Coherencia de nombres** | Nombres que rompen el convenio del sistema — token, componente, pantalla |
| **Cobertura de tokens** | Valores en crudo — hex, px, radios — que deberían ser tokens — DS-T07 |
| **Completitud de componentes** | Por componente: ¿estados? ¿variantes? ¿docs? ¿foco? — DS-C03, DS-C09, DS-C05, DS-C02 |

### Paso 4 · Calcular el score

**De 100.** Se resta por cada hueco; la fórmula está en `${CLAUDE_SKILL_DIR}/referencias/informe.md`. El score **acompaña** al
detalle, nunca lo reemplaza.

### Paso 5 · Priorizar y entregar

**Tres acciones, por impacto.** El informe completo como **HTML**: `salidas/auditoria/index.html`.

---

## Referencias

| Archivo | Cuándo |
|---|---|
| `${CLAUDE_SKILL_DIR}/referencias/informe.md` | **Al redactar el informe.** El formato y la fórmula del score |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/doctrina.md` | Las reglas `DS-xxx` que se citan en cada hallazgo |
| `${CLAUDE_PLUGIN_ROOT}/conocimiento/checklists.md` | Lo que una persona marca a ojo, además de lo automático |

---

## Errores que se cometen siempre

| Error | Qué lo delata | Qué hacer |
|---|---|---|
| **Auditar sin verificar** | Se opina sin datos | Paso 2 primero |
| **Score sin detalle** | Un número sin tablas que lo sostengan | El score acompaña, no reemplaza |
| **Todo es prioridad** | Diez acciones sin orden | Tres, por impacto |
| **Confundir salto con verde** | «verificar.py no falló» cuando saltó | Un salto se anota y se dice |

---

## Al terminar

1. **Qué se auditó** — cuántos componentes, cuántas pantallas.
2. **El score** y qué lo baja.
3. **Las tres acciones**, por impacto.
4. **Lo que `verificar.py` no pudo comprobar** — saltado, dicho en voz alta.
5. **El informe HTML**, para que lo mire.
