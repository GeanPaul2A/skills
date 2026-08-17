# Puentes · llevar el sistema a una herramienta de diseño

**La fuente de verdad es el JSON. La herramienta de diseño es una salida más** — DS-X01.

Suena a detalle y no lo es. Las variables de una herramienta de diseño **no tienen control de versiones
propio**, admiten **pocos tipos** —sin tokens compuestos— y **hacen falta complementos de terceros** para
sacarlas a código `[B1, cap. 6]`.

> Y el argumento de fondo, del mismo libro: *"Cuando empecé a usar Figma escuchaba: 'todo el mundo diseña en
> Photoshop, Figma nunca va a funcionar'. Eso no envejeció bien. **Hoy es un gigante, pero esa posición puede
> cambiar.**"*
>
> **Por eso el sistema no vive dentro de ninguna herramienta.** Vive en `tokens/`, y cada herramienta recibe
> una traducción.

---

## Lo primero: averiguar qué hay, y si escribe

**No asumas que hay un puente. No asumas que el que hay escribe.**

| Paso | Qué hacer |
|---|---|
| **1** | Mira qué herramientas de diseño hay disponibles en la sesión |
| **2** | **Averigua si escriben o solo leen.** Muchos puentes de diseño solo *envían contexto al agente*: leen el lienzo, no crean nodos |
| **3** | **Dilo antes de intentarlo.** Si solo lee, no prometas dibujar |
| **4** | Si no hay ninguno, **la salida sigue sirviendo**: las variables se importan a mano y la galería se abre en un navegador |

> **El error a evitar:** anunciar *"te lo dibujo en Figma"* y descubrir a mitad de camino que el puente no crea
> nodos. **Se comprueba primero y se dice después.**

---

## Las tres clases de puente

### Clase A · escribe en un lienzo de diseño

Crea marcos, textos y componentes. **Es lo que el usuario suele imaginar.**

**Orden de creación — no es negociable:**

```
1 · las variables          primero SIEMPRE. Sin ellas, todo nodo nace con valores en crudo
2 · los estilos de texto   apuntando a las variables, nunca a valores fijos — DS-X04
3 · los componentes        uno por entrada del inventario, con sus variantes
4 · las páginas            recién acá se dibujan pantallas
```

**Si el orden se invierte**, se termina con cientos de nodos que llevan `#3A45C9` escrito adentro, y cambiar
el acento deja de ser una línea.

### Clase B · lee el lienzo y te da contexto

Devuelve la estructura de lo que ya está dibujado. **Sirve para auditar, no para construir.**

Uso legítimo: **comprobar que lo dibujado respeta el sistema** — que ningún nodo lleve un color fuera de la
paleta, que todo contenedor tenga disposición automática.

**Dile al usuario qué clase tiene**, para que sepa qué esperar.

### Clase C · sincroniza una biblioteca de archivos

Sube la biblioteca a un espacio de diseño como archivos. **Escribe, pero no en un lienzo vectorial: en HTML.**

**`--salidas galeria` produce exactamente eso**: un HTML por componente, con sus variantes y estados
renderizados y su «cuándo usarlo / cuándo no» arriba.

**Es la clase más subestimada.** Un componente que se ve en un navegador **ya se ve**, no hace falta abrir
nada. Y el mismo archivo es la prueba de que los tokens resuelven.

> **Al usar un puente de esta clase:** sincroniza **de a un componente**, nunca reemplazando todo de golpe.
> Un reemplazo total borra lo que otra persona subió.

---

## Conectar un puente real

**El plugin no trae ningún servidor MCP configurado, y es deliberado.** Un servidor de ejemplo que no responde
falla al arrancar en la máquina de quien lo instale, y un puente concreto envejece más rápido que el sistema.

Quien quiera conectar el suyo lo declara **en su propio proyecto**, no dentro del plugin — así sobrevive a las
actualizaciones. En `.mcp.json` en la raíz del proyecto:

```json
{
  "mcpServers": {
    "figma": { "type": "http", "url": "https://<tu-servidor-mcp>/api" }
  }
}
```

El envoltorio `mcpServers` no es opcional: sin él la configuración se ignora en silencio.

> **Y nada de esto es un requisito.** DS-X06: ninguna etapa del proceso depende de que un agente escriba en el
> lienzo. Sin puente, la galería y las variables siguen siendo la entrega completa.

---

## Lo que se publica, y en qué orden

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/construir.py --destino <destino> --salidas css,figma,lienzo,galeria
```

| Archivo | Para qué | Quién lo consume |
|---|---|---|
| `sistema.css` | El sistema como propiedades personalizadas, un bloque por modo | El navegador, la galería, la aplicación web |
| `figma-variables.json` | **Las tres colecciones**, con modos, alcance y sintaxis por plataforma | El puente que importa variables |
| `lienzo.json` | **El documento neutral de nodos** | El puente que dibuja |
| `galeria/*.html` | Un componente por archivo, ya renderizado | El puente que sincroniza archivos, o un navegador |
| `Sistema.swift` · `values/*.xml` | Constantes nativas | iOS y Android |

---

## `figma-variables.json` · las tres colecciones

**Una colección por nivel.** Es lo que impide que los niveles se colapsen dentro de la herramienta.

| Colección | Modos | Publicada | Por qué |
|---|---|---|---|
| **1 · Primitivos** | uno solo | **no** | `[B2, cap. 13]`: *"El alcance permite **ocultar completamente una variable** de la interfaz y de la publicación. **Esto evita que los primitivos se apliquen directamente** y garantiza que se usen exclusivamente como alias."* |
| **2 · Semánticos** | **todos** | sí | **Los modos viven acá.** Un primitivo nunca cambia por modo |
| **3 · Componentes** | uno solo | sí | Alias al nivel 2. Es lo único que una pantalla cita |

### El alcance, variable por variable

**No es cosmético: es lo que hace que la herramienta no ofrezca lo que no corresponde.**

| Rol | Alcance | Efecto |
|---|---|---|
| `superficie.*` | relleno de forma | No aparece al elegir color de texto |
| `texto.*` | relleno de texto | No aparece al elegir un fondo |
| `borde.*` | color de trazo | Solo en bordes |
| `espacio.*` | espacio y relleno interior | No aparece como tamaño de fuente |
| `forma.*` | radio de esquina | Solo ahí |

### Un nombre por plataforma

`[B1, cap. 8]` — **una variable, tres nombres.** El desarrollador copia el de su plataforma y compila:

```
accion.reposo
  web       --accion-reposo
  ios       accionReposo
  android   accion_reposo
```

---

## `lienzo.json` · el documento neutral

**Describe qué dibujar, no con qué herramienta.** Si mañana cambia la herramienta, se cambia el traductor y
**el documento sigue siendo el mismo**.

```json
{ "tipo": "marco", "nombre": "boton/primario",
  "disposicion": { "direccion": "fila", "espacio": "{espacio.elementos}",
                   "relleno": "{espacio.interior}", "ancho": "abraza", "alto": "abraza" },
  "fondo": "{boton.primario.fondo}",
  "forma": "{forma.control}",
  "hijos": [ { "tipo": "texto", "contenido": "Continuar",
               "estilo": "{tipo.cuerpo}", "color": "{boton.primario.texto}" } ] }
```

**Tres cosas que nunca faltan:**

1. **Todo marco lleva `disposicion`.** `[B2, cap. 11]`: *"El código más preciso se genera cuando el diseño usa
   Auto Layout, porque corresponde directamente al sistema Flexbox. **Si no se usa, Figma sugiere coordenadas
   absolutas**, lo que lleva a interfaces no responsivas y trabajo extra."*
2. **Ningún valor en crudo.** Todo color, espacio y tamaño es una llave `{token}` — DS-T07.
3. **El dimensionado es `abraza`, `llena` o `fijo`.** Nunca un número suelto donde debería abrazar el
   contenido: es lo que revienta al cambiar de idioma — DS-L03.

### El vocabulario, para traducirlo

| Documento | Figma | CSS |
|---|---|---|
| `marco` | Frame | `div` |
| `disposicion` | **Auto Layout** | **Flexbox** |
| `abraza` | Hug contents | `width: fit-content` |
| `llena` | Fill container | `flex: 1` |
| `forma` | Corner radius | `border-radius` |
| `instancia` | Instance | uso del componente |

---

## Los cinco errores del puente

| Error | Qué pasa | Qué hacer |
|---|---|---|
| **Dibujar antes de importar variables** | Cada nodo nace con el color escrito adentro | Variables → estilos → componentes → páginas |
| **Publicar los primitivos** | El equipo aplica `indigo.600` directo y el nivel 2 se vuelve decorativo | Ocultos y sin alcance — DS-X02 |
| **Marcos sin disposición** | La herramienta emite coordenadas absolutas | Toda caja lleva `disposicion` — DS-L01 |
| **Estilos con valores fijos** | Cambiar el acento ya no propaga | Los estilos apuntan a variables — DS-X04 |
| **Prometer que dibuja sin comprobarlo** | Se anuncia y no se puede cumplir | Comprobar la clase del puente **antes** |

---

## Cuando no hay ningún puente

**No es un bloqueo.** El sistema está completo igual:

- **`galeria/*.html`** se abre en un navegador y **ya muestra todos los componentes** con sus estados.
- **`figma-variables.json`** se importa con un complemento de importación de variables.
- **`sistema.css`** se usa tal cual en la aplicación web.
- **`Sistema.swift`** y `values/*.xml` se copian al proyecto nativo.

> **Dilo así, sin disfrazarlo:** *"No hay un puente que dibuje en el lienzo. Te dejo las variables listas para
> importar y la galería lista para mirar. El sistema no depende de eso."*
>
> **DS-X06 lo pone por escrito: ninguna etapa depende de que un agente escriba en el lienzo.**
