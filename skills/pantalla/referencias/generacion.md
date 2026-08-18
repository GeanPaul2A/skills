# Generación · cómo se declara una pantalla

**Una pantalla se declara antes de dibujarse.** El archivo es lo que se verifica; el dibujo es su salida.

---

## Índice

1. [El formato](#el-formato)
2. [Campo por campo](#campo-por-campo)
3. [Las cinco decisiones de armado](#las-cinco-decisiones-de-armado)
4. [Del archivo al dibujo](#del-archivo-al-dibujo)
5. [Lo que se revisa mirando, no verificando](#lo-que-se-revisa-mirando-no-verificando)

---

## El formato

`pantallas/<nombre>.json`:

```json
{
  "nombre": "editar-perfil",
  "proposito": "La persona corrige sus datos y confirma el cambio",
  "plantilla": "plana",
  "actor": "usuario",

  "datos": {
    "entidades": ["perfil", "cuenta"],
    "campos": ["perfil.nombre", "perfil.foto", "cuenta.correo"],
    "reglas": ["cuenta.R12"],
    "si_no_llega": "El correo se muestra vacío y deshabilitado, con un aviso de que no se pudo consultar",
    "extremos": {
      "perfil.nombre": { "corto": "Ana", "largo": "María de los Ángeles Fernández Etchegoyen" },
      "perfil.foto": "no aplica — es una imagen, no tiene largo ni corto",
      "cuenta.correo": { "corto": "a@b.co", "largo": "nombre.apellido+etiqueta@subdominio.ejemplo.org" }
    }
  },

  "zonas": {
    "encabezado": ["barra-superior"],
    "contenido":  ["avatar", "campo", "mensaje"],
    "accion":     ["boton"]
  },

  "estados": {
    "lleno":    "Los datos actuales, con el nombre enfocado al entrar",
    "cargando": "Tres .esqueleto con la forma de un campo",
    "vacio":    "No aplica — un perfil siempre tiene al menos su identificador",
    "error":    "mensaje de error con 'Reintentar'; lo ya escrito no se pierde"
  },

  "textos": {
    "titulo": "Tus datos",
    "accion": "Guardar cambios",
    "vacio": null,
    "error": "No pudimos guardar los cambios. Lo que escribiste sigue acá — probá de nuevo."
  },

  "h1": "titulo",
  "orden_tabulacion": "coincide con el visual",
  "notas": []
}
```

---

## Campo por campo

| Campo | Qué es | Regla |
|---|---|---|
| `proposito` | **Qué resuelve para el usuario**, en una frase | |
| `plantilla` | Una que exista en `inventario/plantillas.json` | |
| `actor` | Quién la usa. Decide el objetivo táctil mínimo | |
| `datos.entidades` | Las que aparecen. **Tienen que existir en el modelo** | DS-P02 |
| `datos.campos` | `entidad.campo`. **Nada se muestra sin uno** | DS-P02 |
| `datos.reglas` | Las reglas de negocio que la gobiernan | DS-P01 |
| `datos.si_no_llega` | **Qué se muestra si la fuente no responde** | DS-P04 |
| `datos.extremos` | El valor **más largo y más corto** de cada campo visible. Un campo que no es texto —un icono, una imagen— lleva `"no aplica — <motivo>"`, y **el motivo no es opcional** | DS-L06 |
| `zonas` | Qué componentes van en cada zona de la plantilla | |
| `estados` | **Los cuatro.** «No aplica» vale con su motivo | DS-C03 |
| `textos` | En su versión **más larga**, no la más cómoda | DS-F02 |
| `h1` | Cuál texto es el titular. **Uno solo** | DS-A05 |
| `orden_tabulacion` | Si diverge del visual, **se explica** | DS-A07 |

---

## Las cinco decisiones de armado

### 1 · Qué va sobre el pliegue

**Lo que distingue al producto va arriba, siempre.** Si hay que desplazar para encontrarlo, **para el usuario
no existe**.

**El caso claro:** un producto cuya gracia es que el usuario controla algo que en la competencia viene fijo. Si
ese control queda bajo el pliegue, la pantalla se ve prolija y **no comunica de qué se trata el producto**.

**Cómo se resuelve:** anclarlo al pie de la zona de acción, arriba del botón. Se ve siempre y sigue estando
donde termina la tarea.

### 2 · Qué se ancla y qué se desplaza

| Se ancla | Se desplaza |
|---|---|
| La acción que cierra la tarea | El contenido que se lee |
| La navegación entre secciones | La lista |
| El estado que cambia solo | El detalle |

### 3 · Cómo se dimensiona cada caja

**`abraza`, `llena` o `fijo`. Nunca un número suelto donde debería abrazar** — DS-L03.

Y se construye **de adentro hacia afuera** — DS-L07: primero la pieza chica con su relleno, después el
contenedor que la envuelve. Al revés se termina peleando con tamaños que no cierran.

### 4 · Qué texto va, en su versión larga

**El texto de ejemplo miente.** «Ana» ocupa lo que ocupa; el nombre real puede tener cuarenta caracteres, y en
otro idioma **un 30 % más** `[Libro 1, capítulo 8]`.

**Se maqueta con el largo, no con el cómodo.**

### 5 · Qué pasa cuando algo falla

**No es un estado aparte que se agrega después: es parte de la pantalla.** Un error sin salida es una pantalla
rota.

| Estado | Lo mínimo |
|---|---|
| `cargando` | **Un esqueleto con la forma del contenido.** Un giro genérico no dice qué viene |
| `vacio` | **Por qué está vacío y qué hacer.** Nunca una pantalla en blanco |
| `error` | **Qué pasó y cómo reintentar.** Y si hay una alternativa, ofrecerla |

---

## Del archivo al dibujo

Cuando la pantalla está declarada y verificada, se produce:

| Salida | Qué es |
|---|---|
| **HTML** | La pantalla renderizada con `sistema.css`. **Se abre en un navegador y ya se ve** |
| **Nodos de lienzo** | El mismo árbol, en el formato neutral, para el puente que dibuje |

**El HTML usa solo variables del sistema.** Si hace falta un valor que no es token, **falta un token** — no se
escribe el valor a mano.

### El orden al dibujar en un lienzo

```
1 · variables       sin ellas, cada nodo nace con el color adentro
2 · estilos         apuntando a variables, nunca a valores fijos
3 · componentes     uno por entrada del inventario
4 · pantallas       recién acá
```

---

## Lo que se revisa mirando, no verificando

**Una pantalla puede pasar todas las comprobaciones y estar mal.** Lo que hay que mirar:

- **¿Se entiende qué hay que hacer** sin leer todo?
- **¿Lo importante se ve primero**, o compite con lo secundario?
- **¿Hay algo perdido** — un elemento sin relación con lo de al lado?
- **¿El ritmo del espaciado agrupa lo que va junto** y separa lo que no?
- **¿Se puede usar con una mano**, si es móvil?
- **¿Se entiende al 200 % de texto?** — DS-A08

> **El espaciado es lo que más se nota cuando está mal y menos cuando está bien.** Dos elementos relacionados
> con el mismo espacio que dos sin relación **hacen que la pantalla se lea plana**, aunque cada pieza esté
> perfecta.
