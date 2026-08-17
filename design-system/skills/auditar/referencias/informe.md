# El informe de auditoría

**Formato del informe y fórmula del score.** Cada hallazgo cita la regla que incumple — igual que `verificar.py`
cita `DS-xxx`.

---

## El informe

```markdown
## Auditoría del sistema · <nombre>

### Resumen
Componentes revisados: [X] · Incidencias: [X] · Score: [X/100]

### Coherencia de nombres
| Incidencia | Dónde | Estándar a adoptar |
|---|---|---|
| [nombre inconsistente] | [componente/pantalla] | [convenio] |

### Cobertura de tokens
| Categoría | Definidos | Valores en crudo encontrados |
|---|---|---|
| Colores | [X] | [X] instancias de hex en crudo |
| Espaciado | [X] | [X] instancias de valores arbitrarios |
| Tipografía | [X] | [X] instancias de fuentes/tamaños sueltos |

### Completitud de componentes
| Componente | Estados | Variantes | Docs | Foco | Nota |
|---|---|---|---|---|---|
| boton | ✅ | ✅ | ⚠️ | ✅ | falta `cuando_no` con sustancia |

### Acciones priorizadas
1. [la que más destraba]
2. [segunda]
3. [tercera]
```

---

## La fórmula del score

**Arranca en 100 y se resta.** Tres bloques, cada uno con su tope:

| Bloque | Resta | Tope |
|---|---|---|
| Cada nombre inconsistente | −2 | −20 |
| Cada valor en crudo (hex, px, radio) | −3 | −30 |
| Cada hueco de completitud (falta un estado, una variante, doc o foco) | −1 | −40 |

**Reglas:**

- Un mismo valor en crudo repetido cuenta **una vez** por aparición.
- Un componente sin su entrada en el inventario es **incidencia grave**, no un −1: se lista aparte y baja 5.
- El score **no puede bajar de 0** y **no se redondea hacia arriba**.

> **El score no es el objetivo; es el pulso.** Lo que importa son las tablas. Un score alto con una tabla de
> nombres rotos es un sistema que va a doler después.

---

## Qué es «sano» y qué no

| Score | Lectura |
|---|---|
| 90–100 | Sano. El verificador es el guardián; la auditoría confirma |
| 70–89 | Usable, con deuda. Las tres acciones la bajan |
| 50–69 | Con deuda seria. Nombres o cobertura se le escaparon al verificador |
| < 50 | En riesgo. La cobertura de tokens está rota (DS-T07 violada a escala) |
