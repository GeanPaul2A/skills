# La entrevista de negocio

**Cinco bloques.** Se recorren en orden: cada uno condiciona al siguiente. Es el espejo de negocio de la
entrevista visual de `sistema-diseno`.

**Todo tiene valor por omisión.** *"Usa lo que recomiendes"* vale en cualquier pregunta.

> **La regla que gobierna la entrevista:** al usuario se le pide **información sobre su negocio**, nunca
> criterio de diseñador ni de modelador de datos. Donde haga falta decidir, se ofrecen opciones concretas.

---

## Índice

1. [Antes de la primera pregunta](#antes-de-la-primera-pregunta)
2. [Bloque 1 · El negocio](#bloque-1--el-negocio)
3. [Bloque 2 · Las entidades](#bloque-2--las-entidades)
4. [Bloque 3 · Las reglas](#bloque-3--las-reglas)
5. [Bloque 4 · Los patrones (flujos)](#bloque-4--los-patrones-flujos)
6. [Bloque 5 · Lo propio](#bloque-5--lo-propio)
7. [Al cerrar la entrevista](#al-cerrar-la-entrevista)
8. [Lo que NUNCA se pregunta](#lo-que-nunca-se-pregunta)

---

## Antes de la primera pregunta

Dilo así, o parecido:

> Te voy a hacer preguntas sobre **tu negocio** — qué hace, qué información maneja y qué flujos tiene — para
> declararlo y que cada pantalla que diseñemos se compruebe contra datos que existen de verdad. En cualquier
> pregunta puedes decir **"usa lo que recomiendes"**.
>
> No te voy a pedir que diseñes ni que modelees. Si algo no lo sabes, me lo dices y lo dejamos anotado como
> pendiente.

---

## Bloque 1 · El negocio

| # | Pregunta | Por omisión | Qué condiciona |
|---|---|---|---|
| 1.1 | **¿Qué es el negocio, en una frase?** | — *(obligatoria)* | El `nombre` y `sector` del dominio |
| 1.2 | **¿En qué sector?** transporte, comercio, banca, salud… | Se infiere de 1.1 | El vocabulario de los patrones |
| 1.3 | **¿Quiénes lo usan?** Y si alguno lo usa en una condición distinta — de pie, manejando, con guantes | Un solo actor | Los `actores` y el objetivo táctil |

## Bloque 2 · Las entidades

**Es el bloque central.** No se pide el modelo completo; se pide **lo que las pantallas van a mostrar**.

| # | Pregunta | Por omisión | Qué condiciona |
|---|---|---|---|
| 2.1 | **¿Qué "cosas" maneja el negocio?** (un viaje, un producto, una cuenta) | — *(obligatoria)* | Las claves de `entidades` |
| 2.2 | **De cada una, ¿qué campos se muestran o se capturan?** | Se listan juntos | Los campos de cada entidad — DS-P02 |
| 2.3 | **¿Qué campo tiene solo un conjunto de valores?** (estado: solicitado, aceptado…) | Se pregunta por entidad | Los `enum` y sus `valores` |

**Si el usuario no sabe listar campos, pide una pantalla concreta y extráelos de ahí:** *"¿qué muestra la
pantalla principal?"* es una pregunta que cualquiera responde.

> **Nunca inventes un campo para que la entidad quede completa.** Un campo que el producto no tiene es una
> pantalla que no se puede construir.

## Bloque 3 · Las reglas

| # | Pregunta | Por omisión | Qué condiciona |
|---|---|---|---|
| 3.1 | **¿Qué reglas gobiernan el negocio?** (un plazo, un mínimo, una condición) | Se pregunta por patrón | Las entradas de `reglas` |
| 3.2 | **¿Alguna regla prohíbe algo que el diseño querría permitir?** | — | Los estados de fallo de los patrones |

**La pregunta que revela el estado de fallo:** *"¿qué puede salir mal en este flujo?"* — cada respuesta es un
estado del patrón (DS-P03).

## Bloque 4 · Los patrones (flujos)

**Para cada flujo clave del negocio** — registrarse, pedir, pagar, cancelar — se pregunta:

| # | Pregunta | Por omisión |
|---|---|---|
| 4.1 | **¿Qué hace el usuario en este flujo?** (en una frase) | — |
| 4.2 | **¿Qué entidades toca?** | De las ya declaradas |
| 4.3 | **¿Qué lee de otra entidad que puede no llegar?** (nombre, estrellas) | Se marca `lee_tambien` |
| 4.4 | **¿Qué puede salir mal?** | Un estado de fallo al menos |

> **Un patrón termina donde el modelo cambia de estado.** *"Pedir un viaje"* y *"elegir conductor"* son dos
> porque la solicitud existe en el primero y la subasta corre en el segundo — DS-P06.

## Bloque 5 · Lo propio

| # | Pregunta | Por omisión | Qué condiciona |
|---|---|---|---|
| 5.1 | **¿Hay algo que solo exista en este negocio?** (un mapa, una tarjeta de oferta) | Nada | `componentes_propios` y `plantillas_propias` |
| 5.2 | **¿Por qué no sirve algo universal?** | — | El `motivo` (obligatorio) |

---

## Al cerrar la entrevista

**Antes de escribir nada, resume y confirma:**

```
Negocio      <una frase>  ·  sector <cuál>
Actores      <quiénes>  ·  <condiciones si las hay>

Entidades    <n>  ·  campos totales <m>
Reglas       <n>
Patrones     <n>  ·  cada uno con su estado de fallo
Propio       <piezas, o "nada">

Modelo formal  <dónde, o "sin modelo formal">
```

Y pregunta: **¿algo que corregir antes de escribir el dominio?**

---

## Lo que NUNCA se pregunta

| No preguntar | Porque |
|---|---|
| *"¿Cómo normalizas tus entidades?"* | Pide criterio de modelador. Se extrae de lo que muestra cada pantalla |
| *"¿Qué patrón de arquitectura usas?"* | No es de diseño. Si hay modelo formal, se importa |
| *"¿Necesitas un estado de error?"* | Es obligatorio — DS-P03. No es una opción |
| *"¿Qué datos muestro?"* en abstracto | Se responde pantalla por pantalla, con una pantalla concreta delante |
