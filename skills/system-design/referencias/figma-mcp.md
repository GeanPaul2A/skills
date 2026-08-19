# Figma MCP · herramientas y skills

**Qué instalar y qué usar para escribir en Figma.** Nombres exactos verificados contra la documentación
oficial (developers.figma.com → Figma MCP Server → Tools and Prompts).

---

## 1 · Instalación

Si las herramientas no están disponibles, instalar el plugin:

```bash
claude plugin install figma@claude-plugins-official
```

O el servidor MCP a mano:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Y autenticar con `/mcp` → **figma** → *Authenticate* → *Allow Access*.

---

## 2 · Herramientas MCP (nombres exactos)

### Lectura / inspección

| Herramienta | Qué hace |
|---|---|
| `whoami` | Identidad del usuario autenticado: plan y **asiento** (`seat`) |
| `get_metadata` | Esquema XML de la selección. **Sin `nodeId` NO es de fiar para listar páginas** — ver abajo |
| `get_design_context` | Contexto de diseño de un nodo |
| `get_screenshot` | Captura PNG de la selección |
| `get_variable_defs` | Variables y estilos usados en la selección |
| `get_motion_context` | Datos de animación por keyframes |
| `get_libraries` | Bibliotecas suscritas / disponibles |
| `search_design_system` | Busca en bibliotecas de diseño conectadas |
| `download_assets` | Descarga exports e imágenes originales |
| `get_figjam` | Convierte diagramas FigJam a XML |
| `get_code_connect_map` | Mapeo nodo → componente de código |
| `get_code_connect_suggestions` | Sugerencias de Code Connect |
| `get_context_for_code_connect` | Metadatos para plantillas Code Connect |
| `get_shader_effect` · `get_shader_fill` | Lee un efecto / relleno de shader por ID |
| `list_shader_effects` · `list_shader_fills` | Lista los shaders de la cuenta |

### Escritura / creación

| Herramienta | Qué hace |
|---|---|
| `use_figma` | Crea, edita o inspecciona nodos / variables / componentes (Plugin API) |
| `create_new_file` | Crea un archivo Design / FigJam / Slides en blanco |
| `upload_assets` | Sube PNG, JPG, GIF, WebP |
| `generate_diagram` | Genera diagramas FigJam desde Mermaid |
| `generate_figma_design` | Captura UI en vivo como capas de diseño |
| `add_code_connect_map` | Agrega mapeo nodo → componente |
| `send_code_connect_mappings` | Confirma mapeos tras las sugerencias |

### Weave (aparte)

`weave_list_tools` · `weave_get_tool_inputs` · `weave_upload_asset` · `weave_run_tool` ·
`weave_get_tool_run_output` · `weave_cancel_tool_run`

---

## 3 · Skills de Figma y cuándo cargarlas

| Skill | Cargarla antes de… |
|---|---|
| `figma-use` | **cada `use_figma`, siempre** |
| `figma-create-new-file` | **cada `create_new_file`** |
| `figma-generate-library` | construir tokens y componentes |
| `figma-generate-design` | llevar una pantalla completa |
| `figma-design-to-code` | implementar un diseño como código |
| `figma-generate-diagram` | cada `generate_diagram` |
| `figma-code-connect` | mapear componentes ↔ código |
| `figma-implement-motion` | implementar animación |
| `figma-use-motion` | animar nodos con `use_figma` |
| `figma-use-figjam` · `figma-use-slides` | FigJam / Slides |
| `figma-swiftui` | traducir a / desde SwiftUI |

---

## 4 · El inventario de páginas se pide con `use_figma`, no con `get_metadata`

**`get_metadata` sin `nodeId` devolvió UNA página de un archivo que tenía SIETE.** Las otras seis —incluida la
que guardaba 1767 iconos— eran invisibles hasta pedirlas por id.

**Lo que costó:** se concluyó que el archivo estaba vacío y que los iconos no estaban. Las dos cosas eran
falsas, y lo destapó el usuario, no la herramienta.

```js
// El listado fiable. Ve todas las páginas, siempre.
return figma.root.children.map(p => ({ id: p.id, nombre: p.name, hijos: p.children.length }));
```

> **La regla general:** ante una herramienta que devuelve *menos* de lo esperado, **no se concluye que no
> hay** — se pregunta de otra manera. *"Preguntar si está, no por dónde esperabas que estuviera."*

---

## 5 · Prompt MCP

- `create_design_system_rules` — genera un archivo de reglas para diseño-a-código.
