# Revisión · antes de entregar

**Dos listas.** La primera la corre un guion; la segunda **hay que mirarla**, y no hay guion que la reemplace.

---

## Lo que verifica el guion

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/verificar-pantalla.py --sistema <sistema> --pantallas <carpeta>
```

| Comprueba | Regla |
|---|---|
| La pantalla declara todo lo que la hace verificable | DS-C01 |
| La plantilla existe, y cada componente cabe en su zona | DS-C01 |
| **Los cuatro estados**, y «no aplica» solo con su motivo | DS-C03 |
| Cada campo visible declara **su valor más largo** | DS-L06 |
| **Un solo titular**, y apunta a un texto que existe | DS-A05 |
| El orden de foco, declarado — y explicado si diverge | DS-A07 |
| **Ningún color ni medida en crudo** | DS-T07 |
| Toda fuente externa tiene **plan B** | DS-P04 |
| Entidades, campos y reglas **existen en el modelo** | DS-P02 · DS-P01 |
| Todo patrón contempla el fallo | DS-P03 |

**Cero fallos o no se entrega.**

> **Y las saltadas se leen en voz alta.** «No hay modelo de datos» no es un verde: es una comprobación que no
> se pudo hacer, y el usuario tiene que saber cuál.

---

## Lo que hay que mirar

**Una pantalla puede pasar todo y estar mal.**

### Sentido

```
□  ¿se entiende qué hay que hacer sin leer todo?
□  ¿lo que distingue al producto se ve SIN desplazar?
□  ¿hay un solo camino claro hacia adelante?
□  ¿la acción principal se distingue de las demás?
□  ¿algún elemento quedó suelto, sin relación con lo de al lado?
```

> **El del pliegue es el más caro.** Una pantalla prolija donde lo característico del producto quedó abajo
> **no comunica de qué se trata**. Pasa todas las comprobaciones y falla en lo único que importaba.

### Ritmo y espacio

```
□  ¿lo relacionado está más junto que lo que no lo está?
□  ¿todos los espacios salen de la escala?
□  ¿el margen exterior es consistente entre pantallas del mismo flujo?
□  ¿hay respiro donde el usuario tiene que decidir?
```

> **El espaciado es lo que más se nota cuando está mal y menos cuando está bien.** Dos elementos relacionados
> con la misma separación que dos sin relación **hacen que la pantalla se lea plana**, aunque cada pieza esté
> perfecta.

### Tipografía

```
□  ¿cada estilo cumple un papel distinto, o hay dos que compiten?
□  ¿el cuerpo se lee cómodo a distancia de brazo?
□  ¿ningún estilo se usa fuera de su propósito?
```

> **El error que se cuela solo:** usar el estilo de dato —el de ancho fijo, el de etiqueta— para **una frase
> que se lee corrida**. Se ve «de diseño» y **es exactamente para lo que ese estilo no sirve**.

### Datos de verdad

```
□  ¿probaste con el nombre más largo, y con el más corto?
□  ¿con cero elementos? ¿con cien?
□  ¿con el número más grande que el negocio admite?
□  ¿con el idioma que más se expande?
□  ¿qué se ve si la fuente no responde?
```

> `[B2, cap. 4]`: la maqueta limpia **se desarma en cuanto entran los datos de verdad**. Esta lista es lo que
> evita descubrirlo en producción.

### Accesibilidad

```
□  ¿todo contraste cumple, en todos los modos?
□  ¿el foco se ve, con 3:1?
□  ¿ninguna información depende solo del color?
□  ¿todo campo tiene etiqueta persistente?
□  ¿se entiende al 200 % de texto?
□  ¿los objetivos táctiles llegan al mínimo del actor?
```

### Implementable

```
□  ¿toda caja tiene disposición automática?
□  ¿nada usa tamaño fijo en el eje de un texto traducible?
□  ¿todo componente sale del inventario, ninguno inventado al vuelo?
□  ¿toda animación viene con sus cinco datos?
```

> `[B2, cap. 11]`: *"**Si no se usa Auto Layout, Figma sugiere coordenadas absolutas**, lo que lleva a
> interfaces no responsivas y trabajo extra."* Es la diferencia entre entregar un diseño y entregar un
> problema.

---

## Cómo reportar

**En este orden, y sin adornar:**

1. **Qué pantallas** y de qué plantilla sale cada una.
2. **Qué datos usan y de dónde salen** — o **que no se pudo comprobar**, si no hay modelo.
3. **Qué estados se cubrieron**, y **cuál quedó afuera** si alguno quedó.
4. **El resultado del guion**: cuántas en verde, cuántos fallos, **cuáles se saltaron y por qué**.
5. **Lo que hay que mirar a ojo** — la segunda lista, sin marcar por el usuario.
6. **La pantalla**, para que la vea.

> **Lo que no se hizo, se dice.** Una pantalla entregada como terminada con el estado de error sin resolver
> **es peor que una entregada a medias y declarada**: la primera se descubre tarde.
