# Patrones · cuando es un flujo, no una pantalla

**Un patrón es una combinación de componentes con un propósito** — el tercer nivel de la arquitectura, entre
el componente y la plantilla `[Libro 1, capítulo 5]`.

**La diferencia que importa:** un **componente** no sabe para qué se lo usa. Un **patrón sí** — y por eso el
patrón es el que declara **de dónde salen los datos**.

---

## Índice

1. [Los cinco momentos](#los-cinco-momentos)
2. [El formato](#el-formato)
3. [Dónde termina un patrón](#dónde-termina-un-patrón)
4. [La conexión con los datos · el vacío G2](#la-conexión-con-los-datos--el-vacío-g2)
5. [Universal o propio del producto](#universal-o-propio-del-producto)
6. [Antes de cerrar un patrón](#antes-de-cerrar-un-patrón)

---

## Los cinco momentos

`[Libro 2, capítulo 9]` — todo flujo tiene cinco, y hay que declararlos:

| Momento | Qué es | Se olvida |
|---|---|---|
| **Entrada** | Desde dónde se llega. Puede haber más de una | A veces |
| **Decisión** | Dónde el usuario elige, y qué pasa con cada opción | Poco |
| **Éxito** | Qué ve cuando salió bien | Nunca |
| **Error** | **Qué ve cuando salió mal, y cómo sale de ahí** | **Siempre** |
| **Salida** | Adónde queda parado al terminar | A menudo |

> **El cuarto es el que falta, y DS-P03 lo exige:** un patrón sin ningún estado de fallo está incompleto. El
> verificador lo busca por nombre — *error*, *fallo*, *rechazado*, *vencido*, *cancelado*, *sin …*

---

## El formato

`inventario/patrones.json`:

```json
"acceder": {
  "proposito": "Que una persona entre a su cuenta, o cree una si no la tiene",
  "cuando_no": "Si la acción no necesita identidad, no se pide acceder",
  "universal": true,

  "pasos": [
    { "nombre": "pedir-telefono",  "plantilla": "plana",  "componentes": ["campo", "boton", "enlace"] },
    { "nombre": "verificar-codigo","plantilla": "plana",  "componentes": ["casillas-codigo", "boton", "mensaje"] },
    { "nombre": "completar-perfil","plantilla": "plana",  "componentes": ["campo", "opcion", "boton"] }
  ],

  "estados": {
    "entrada":       "Desde el arranque, o desde cualquier acción que necesite identidad",
    "codigo-enviado":"El código viaja; la pantalla muestra a qué número",
    "exito":         "Queda en donde iba antes de que se le pidiera identificarse",
    "codigo-vencido":"Se le ofrece pedir otro, con el plazo a la vista",
    "codigo-erroneo":"Se le dice cuántos intentos le quedan",
    "sin-red":       "Se le explica y se guarda lo escrito"
  },

  "datos": {
    "dominio": "identidad",
    "entidades": ["persona", "codigo"],
    "campos": ["persona.telefono", "persona.nombre", "codigo.expira_en", "codigo.intentos"],
    "reglas": ["identidad.R04", "identidad.R09"],
    "si_no_llega": "Si el servicio de códigos no responde, se dice y se ofrece reintentar"
  }
}
```

---

## Dónde termina un patrón

**Donde el modelo cambia de estado** — DS-P06.

No donde se acaba la pantalla, ni donde el diseñador se cansó. Si el flujo de pago termina cuando la
transacción queda registrada, **ahí termina el patrón**, aunque después haya una pantalla de agradecimiento.

**Sirve para no escribir patrones eternos** que tapan tres flujos distintos en uno.

---

## La conexión con los datos · el vacío G2

**Los libros nombran el problema y no lo resuelven.** `[Libro 2, capítulo 4]` dice que empezar por la maqueta produce
maquetas que se desarman con datos reales, y **recomienda conseguir contenido de ejemplo**. Nada más.

**Acá el patrón lo declara y el verificador lo comprueba:**

| Campo | Qué comprueba el guion |
|---|---|
| `entidades` | Que existan en el modelo del producto |
| `campos` | Que **cada campo exista en su entidad** |
| `reglas` | Que la regla citada **exista de verdad** |
| `si_no_llega` | Que esté escrito. **Ninguna fuente externa sin plan B** |

**Si el proyecto no declara modelo de datos**, estas tres comprobaciones **se saltan y se reportan saltadas**.
No se disfrazan de verde.

---

## Universal o propio del producto

| | |
|---|---|
| **Universal** | Acceder, buscar, elegir de una lista, confirmar algo, ver un historial |
| **Propio** | Lo que solo tiene sentido en este producto |

**Lo propio lleva `"universal": false` y su motivo escrito.** Es lo que permite después llevarse los
universales a otro producto sin arrastrar lo que no sirve.

---

## Antes de cerrar un patrón

```
□  los cinco momentos, y el de ERROR entre ellos
□  cada paso declara plantilla y componentes, y todos existen
□  cada componente cabe en alguna zona de esa plantilla
□  entidades, campos y reglas, citados y existentes
□  si_no_llega, escrito
□  universal marcado, y si es false, su motivo
□  verificar-pantalla.py en verde
```
