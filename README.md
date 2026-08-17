# design-system · plugin para Claude Code

Construye un **sistema de diseño completo y verificable** —tokens en tres niveles con modos, biblioteca de
componentes, patrones, plantillas y accesibilidad WCAG AA— y diseña, prueba, audita y documenta pantallas y
flujos sobre él. Publica a **CSS, Swift, Android o Figma**.

**El núcleo es agnóstico de negocio.** El sistema visual no sabe de transporte, de banca ni de comercio: lo que
sabe de un negocio vive en un archivo de dominio (`dominios/<tipo>.json`) que se declara en *tu* proyecto, con
sus entidades, reglas, patrones y piezas propias.

---

## Instalación

Dentro de Claude Code —terminal, app de escritorio o extensión de IDE:

```
/plugin marketplace add GeanPaul2A/skills
/plugin install design-system@geanpaul-design
```

Si el resumen dice `Run /reload-plugins to activate.`, corré ese comando.

Para desarrollo local, desde la carpeta que contiene este repo:

```
/plugin marketplace add ./skills
/plugin install design-system@geanpaul-design
```

---

## Las seis skills

Se activan solas cuando describís lo que querés; no hace falta memorizar comandos.

| Skill | Qué hace |
|---|---|
| `sistema-diseno` | El sistema visual: tokens (3 niveles), componentes universales, plantillas, modos, publicación |
| `dominio` | El tipo de negocio: entidades, reglas, patrones de dominio, piezas propias |
| `pantalla` | Una pantalla o un flujo: plantilla + datos + estados |
| `probar` | Los cinco momentos, los cuatro estados, valores límite, accesibilidad |
| `auditar` | Score, coherencia de nombres, cobertura de tokens, acciones priorizadas |
| `documentar` | La ficha de una pieza: props, accesibilidad, do/don't, ejemplo de código |

El orden del pipeline: **sistema-diseno → dominio → pantalla → (probar, documentar) → auditar**.

Los comandos explícitos llevan nombres distintos a los de las skills, a propósito: un comando y una skill que
se llaman igual comparten espacio de nombres y uno tapa al otro.

```
/design-system:crear              /design-system:probar-pantalla
/design-system:definir-dominio    /design-system:auditar-sistema
/design-system:disenar-pantalla   /design-system:documentar-pieza
/design-system:extender
```

---

## Lo que no se negocia

**Tres niveles de token.** Primitivo (`indigo.600`, se llama por lo que *es*) → semántico (`accion.reposo`, por
lo que *hace*, con un valor por modo) → componente (`boton.primario.fondo`, por dónde se *aplica*). Un
componente nunca cita un primitivo.

**Cero fallos o no se entrega.** `verificar.py` corre 34 comprobaciones automáticas contra las reglas del
sistema. Una comprobación **saltada no es un verde**: se reporta aparte, con su motivo.

**Cada comprobación se prueba rompiendo algo a propósito.**

```bash
python3 <plugin>/skills/sistema-diseno/scripts/verificar.py --destino <destino> --romper DS-C03
```

Tiene que fallar. Tres veredictos: `0` lo detectó · `1` pasó sin detectarse, la comprobación no sirve · `2` no
se pudo probar, está saltada.

**La accesibilidad es piso, no meta.** Contraste, foco y estados son condiciones de entrada, no mejoras
posteriores.

---

## La doctrina

`design-system/conocimiento/doctrina.md` — **76 reglas `DS-xxx`, cada una con su procedencia.** Las que salen
de la bibliografía llevan su cita; las ocho de extensión pura llevan escrito el vacío que las justifica.

**34 están marcadas `auto`, y las 34 tienen comprobación escrita y probada.** No es coincidencia: el invariante
se mide con el `diff` documentado al final de la doctrina. Si imprime algo, una de las dos miente.

El resto son `semi` (necesitan renderizar o leer la herramienta de diseño) o `manual` (requieren criterio).

---

## Estructura

```
skills/
├── .claude-plugin/marketplace.json   el catálogo: marketplace «geanpaul-design»
├── design-system/                    el plugin
│   ├── .claude-plugin/plugin.json
│   ├── commands/                     7 comandos (puntos de entrada finos)
│   ├── skills/                       las 6 skills, con scripts y referencias
│   ├── conocimiento/                 doctrina, accesibilidad, componentes, checklists
│   └── dominios/_plantilla.json      la especificación del dominio
├── pruebas/                          suite de regresión — 3 productos de prueba
└── GUIA-DE-USO.md
```

`pruebas/` está **fuera del plugin a propósito**: son datos de prueba del repositorio, no parte de lo que se
distribuye. Correr el pipeline completo sobre uno:

```bash
python3 design-system/skills/sistema-diseno/scripts/derivar.py   --destino pruebas/movilidad
python3 design-system/skills/sistema-diseno/scripts/construir.py --destino pruebas/movilidad --salidas css,galeria
python3 design-system/skills/sistema-diseno/scripts/verificar.py --destino pruebas/movilidad
```

Solo biblioteca estándar de Python 3. Sin dependencias.

---

## Licencia

MIT. Ver `design-system/LICENSE`.

Las reglas de la doctrina citan dos libros —*Design Beyond Limits with Figma* y *Designing and Prototyping
Interfaces with Figma*— como extractos breves y atribuidos, con el capítulo de origen en cada regla.
