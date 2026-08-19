# Dibujar en el lienzo · el contrato

**`lienzo.json` no es una sugerencia: es el dibujo.** Se traduce nodo por nodo. Lo que no está en el
documento no se dibuja, y lo que está no se omite.

> **Por qué existe este archivo.** El 18-08-2026 se revisó un archivo de Figma construido con este plugin.
> El inventario declaraba para `campo` cinco variantes y **seis estados** —reposo, foco, relleno, error,
> deshabilitado, solo-lectura— con sus tokens `borde-foco` y `borde-error`. El archivo tenía **diez campos
> idénticos**: ni un foco, ni un error, ni un deshabilitado. Ningún componente tenía radio, aunque
> `forma.control` valía 8 y cada pieza lo citaba.
>
> **Nada de eso estaba mal en el JSON.** Estaba mal en el paso de traducir, porque el paso de traducir no
> estaba escrito en ninguna parte. Esto es ese paso.

---

## Índice

1. [La regla](#la-regla)
2. [El orden](#el-orden)
3. [Las páginas](#las-páginas)
4. [Los estados](#los-estados)
5. [Lo que nunca falta en un nodo](#lo-que-nunca-falta-en-un-nodo)
6. [Los iconos](#los-iconos)
7. [Antes de decir que terminaste](#antes-de-decir-que-terminaste)

---

## La regla

**No improvises el lienzo.** Si te encuentras decidiendo un tamaño, un color o una posición que el documento
no dice, pará: o el dato está en `lienzo.json` y no lo leíste, o falta en el generador y hay que arreglarlo
ahí. **Inventarlo en el lienzo lo pierde en el siguiente redibujo.**

| Síntoma | Qué significa de verdad |
|---|---|
| «lo acomodo a ojo para que se vea mejor» | El documento no trae disposición, o no la estás leyendo |
| «le pongo un gris que quede bien» | Estás escribiendo un valor en crudo — DS-T07 |
| «dibujo el componente y después los estados» | Vas a dibujar el mismo nodo N veces |

---

## El orden

**No es negociable, y es el mismo de la clase A de `puentes.md`:**

```
1 · variables          las tres colecciones, primero SIEMPRE
2 · estilos de texto   estilosDeTexto, apuntando a variables
3 · estilos de efecto  estilosDeEfecto — las sombras
4 · componentes        uno por entrada, con sus variantes y sus estados
5 · páginas            recién acá se dibuja
```

**Invertirlo deja cientos de nodos con el color escrito adentro**, y cambiar el acento deja de ser una línea.

---

## Las páginas

**Una página de Figma por página de `lienzo.json`, con su nombre exacto y en su orden.** La estructura del
archivo de sistema son **seis páginas** —`deliver.py`, DS-H01— y `lienzo.json` ya las emite en orden:

```
Para empezar · Tokens · Componentes · Patrones · Plantillas · Anotaciones
```

**No las agrupes en una sola.** Un archivo con los veintitantos componentes apilados en una página es el
mismo archivo sin estructura, y el desarrollador que lo abre no sabe dónde buscar.

---

## Los estados

**Cada instancia de `lienzo.json` trae un campo `cambia` con su delta ya resuelto.** Es lo único que
distingue un estado de otro, y es obligatorio aplicarlo.

```json
{ "tipo": "instancia", "componente": "campo",
  "propiedades": { "variante": "texto", "estado": "foco" },
  "cambia": { "anillo": { "color": "foco.color",
                          "grosor": "foco.grosor",
                          "separacion": "foco.separacion" } } }
```

| Clave de `cambia` | Cómo se dibuja en Figma |
|---|---|
| `fondo` · `borde` · `texto` · `ayuda` | El relleno o el trazo, **atado a esa variable** |
| `opacidad` | La opacidad del nodo, atada a la variable |
| `anillo` | Un trazo exterior del grosor y color dados, separado del borde |
| `indicador` | Un hijo más: el girador |
| `puntero` | No se dibuja — es para el código |

**Si `cambia` viene vacío, es `reposo`**: el estado base. **Si dos estados te salen visualmente iguales, no
aplicaste el delta.** Es exactamente el fallo que produjo los diez campos idénticos.

---

## Lo que nunca falta en un nodo

| Campo del documento | En Figma | El error si se omite |
|---|---|---|
| `disposicion` | **Auto Layout** | Figma emite coordenadas absolutas; la pieza no responde |
| `forma` | **`cornerRadius`, atado a la variable** | Todo sale a escuadra y el archivo parece sin terminar |
| `ancho: "abraza"` | **Hug contents** | El botón sale a ancho fijo y `sm`, `md` y `lg` se ven iguales |
| `fondo` · `borde` · `color` | Relleno / trazo **por variable** | El valor queda escrito adentro — DS-T07 |
| `estilo` | El **estilo de texto**, no tamaño suelto | Cambiar la escala deja de propagar — DS-X04 |
| `nombre` | El nombre de la capa | Capas «Frame 42»; nadie encuentra nada |

**El radio y el abrazo son los dos que más se caen**, y son los dos que más se notan: son la diferencia entre
un catálogo que parece terminado y uno que parece un borrador.

---

## Los iconos

**Un componente con `INSTANCE_SWAP`, nunca una lámina.** Un pliego de mil iconos sueltos ocupa más lienzo que
todo el sistema, no se puede instanciar, y obliga a copiar y pegar vectores dentro de cada pieza.

- **Uno solo** «icono», con la propiedad de intercambio.
- Los iconos **como componentes**, en su propia página, en una rejilla con nombre.
- Tamaño **atado a la variable**, alineado a la rejilla de píxel.

> Si el archivo ya tiene la lámina, **no la borres**: conviértela: cada icono a componente, y la lámina a la
> página de iconos. Borrar es destructivo y puede llevarse trabajo de otra persona.

---

## Antes de decir que terminaste

Se comprueba **mirando**, con `get_screenshot`, no solo con `get_metadata`:

- [ ] **Ningún nodo suelto en el lienzo.** Todo cuelga de una página y de una sección con nombre.
- [ ] **Todo lo que tiene `forma` tiene radio.** Se ve a simple vista.
- [ ] **Dos estados del mismo componente se ven distintos.** Si no, faltó aplicar `cambia`.
- [ ] **Cada muestra tiene su etiqueta** — la variante y el estado, legibles.
- [ ] **Los tamaños se distinguen.** `sm`, `md` y `lg` no pueden medir lo mismo.
- [ ] **Ningún relleno ni trazo sin variable** — `get_variable_defs` sobre la selección lo dice.
- [ ] **Las seis páginas existen y están en orden.**

**Y lo que se reporta es lo que se vio**, no lo que se mandó dibujar. Un `use_figma` que devuelve un id no es
una pieza que se ve bien.
