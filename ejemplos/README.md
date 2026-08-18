# El sistema dorado

**El patrón de medida contra el que corre la suite.** No es un producto de ejemplo para
copiar: es el sistema mínimo que ejercita **todas** las comprobaciones del plugin.

```bash
./pruebas/construir.sh          # lo ensambla en /tmp/dorado
./pruebas/correr.sh             # lo ensambla y prueba cada comprobación
./pruebas/correr.sh --rapido    # solo la corrida limpia, sin las inyecciones
```

---

## Qué hay acá, y qué no

**Acá viven las fuentes.** Lo derivado —`tokens/`, `modelo/`, `salidas/`— se genera en un
temporal y **no entra al repositorio**: es `DS-X01`, la regla que dice que la fuente de
verdad es el JSON escrito a mano y todo lo demás es una salida.

> Un derivado versionado se desincroniza en la primera edición de `marca.json`, y desde
> ahí la suite prueba contra un sistema que ya nadie construye así.

| Archivo | Qué aporta |
|---|---|
| `base/marca.json` | Los parámetros visuales — de la plantilla, sin tocar |
| `base/proyecto.json` | Dos plataformas, para que las reglas de puntero tengan caso |
| `base/dominio.json` | Tres entidades, cuatro reglas, dos patrones, una pieza no universal |
| `base/pantallas/*.json` | Dos pantallas: una de lista y una de confirmación |
| `base/recursos/` | Tres iconos SVG sanos y una imagen en WebP |
| `base/entrega/` | Las siete páginas, lo descartado con su motivo, dos versiones por hito |
| `base/movimiento.json` | Tres animaciones con sus cinco datos |

---

## Por qué el dominio es aburrido a propósito

**Un catálogo con pedidos.** No se parece a ningún negocio de nadie, y eso es el punto:
su trabajo no es ser realista, es **tener un caso de cada cosa que hay que comprobar**.

| Lo que ejercita | Dónde está |
|---|---|
| Un dato que viene de otra entidad y puede faltar — `DS-P04` | `cliente.nombre` en `confirmar-pedido` |
| Un patrón con estado de fallo — `DS-P03` | los dos patrones declaran `error` |
| Un flujo con los cinco momentos | `confirmar-pedido` |
| Una pieza no universal con su motivo | `precio`, porque la moneda obligatoria es de este negocio |
| Un campo que no es texto y no tiene extremos — `DS-L06` | `articulo.imagen`, con su «no aplica — motivo» |
| Un enum de ancho fijo | `articulo.moneda`: corto y largo iguales, con razón |

> **Si algún día una comprobación queda sin poder correr contra el dorado, es que al
> dorado le falta un caso.** No que la comprobación esté de más.

---

## Cómo se agrega una comprobación

1. Escribirla en el guion que le corresponda, devolviendo un `R("DS-xxx", "…")`.
2. **Agregarle su daño en `romper()`.** Sin eso, `correr.sh` la reporta como *«con
   comprobación pero sin caso de `--romper`»* — y una comprobación que nunca falló no
   está probada: está sin usar.
3. Si el dorado no tiene el caso que hace falta, **agregarlo acá**, no debilitar la
   comprobación.
4. `./pruebas/correr.sh`. Cero fallos o no entra.

---

## Los tres veredictos de una inyección

| Código | Qué significa |
|---|---|
| `0` | **✓ lo detectó.** Falló *esa* comprobación, y dice cuál |
| `1` | **✗ pasó sin detectarse.** La comprobación corrió y no vio nada: **no sirve** |
| `2` | **⚠ no se pudo probar.** Está saltada: la prueba no corrió. **No es un verde** |

**El veredicto es de la regla que se rompió, no del total.** Si mirara el total, una
comprobación rota daría verde porque falló su vecina, y una saltada daría verde sin haber
corrido nunca.
