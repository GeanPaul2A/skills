# La ficha de documentación

**El contrato completo de una pieza para quien la usa.** Se escribe en el inventario (`componentes.json` o
`patrones.json`), no en un doc suelto — DS-C01. Los tres campos nuevos son `props`, `accesibilidad` y
`ejemplo_codigo`.

---

## La ficha completa

```json
"boton": {
  "grupo": "accion",
  "descripcion": "La acción de una pantalla. El primario cierra un trato: enviar, aceptar, confirmar.",
  "cuando_no": "Si solo navega sin cambiar nada, usar 'enlace'. Si actúa sobre una fila, usar 'boton-icono'.",
  "variantes": ["primario", "secundario", "silencioso", "destructivo"],
  "tamanos": ["sm", "md", "lg"],
  "estados": ["reposo", "presionado", "foco", "deshabilitado", "cargando"],
  "tokens": { "primario.fondo": "accion.reposo" },

  "props": [
    { "nombre": "etiqueta", "tipo": "string", "default": "", "que_hace": "El texto del botón" },
    { "nombre": "variante", "tipo": "enum", "default": "primario", "que_hace": "El peso visual de la acción" },
    { "nombre": "cargando", "tipo": "boolean", "default": false, "que_hace": "Muestra el esqueleto y deshabilita" }
  ],

  "accesibilidad": {
    "rol": "button",
    "teclado": "Enter y Espacio activan; Tab entra y sale",
    "lector": "Se anuncia como «botón, [etiqueta]»; si está cargando, «cargando»"
  },

  "ejemplo_codigo": "<button class=\"btn btn--primary\" aria-busy=\"false\">Enviar</button>",

  "reglas": ["DS-C02", "DS-C03", "DS-A02", "DS-A07"],
  "interactivo": true,
  "espera_datos": false
}
```

---

## Campo por campo de lo nuevo

| Campo | Regla | Qué exige |
|---|---|---|
| `props` | DS-C05 | Cada propiedad con `nombre`, `tipo`, `default` y `que_hace`. Sin props, la pieza es un adorno |
| `accesibilidad` | DS-C02 · DS-A07 | `rol`, `teclado` y `lector`. **Obligatorio si `interactivo` es cierto** |
| `ejemplo_codigo` | DS-T07 | Un fragmento con **tokens reales del nivel 3**, nunca valores en crudo |

---

## Lo que el verificador rechaza

- Un `cuando_no` con menos de 20 caracteres — un «no» no es una respuesta (DS-C05).
- Un componente `interactivo: true` sin `accesibilidad` (DS-C02).
- Un `ejemplo_codigo` con un hex o un px en crudo (DS-T07).
- Una `props` sin `tipo` o sin `default`.

> **La regla de oro:** si la ficha no la puede leer quien NO diseñó la pieza, no está documentada.
