# design-system

A Claude Code plugin to build a **complete, verifiable design system** — and to design, test, audit,
document and **ship** screens and flows across **different business types**.

The core is business-agnostic. Each business type is a **domain file** (`dominios/<tipo>.json`) that injects its
own entities, rules, patterns and non-universal components. The system publishes to CSS, Swift, Android or Figma,
and every validation step can be viewed as HTML.

**What makes it verifiable, and not just documented:** the 76 `DS-xxx` rules live in the knowledge base, and
**39 of them are checked by a script**. The other 37 are `semi` or `manual` — the audit report lists every one
of them so a person marks them. No rule is orphaned, and that claim is itself checked (`pruebas/correr.sh`,
stage 3).

## Skills (auto-invoked by description)

| Skill | What it does | Its script |
|---|---|---|
| `sistema-diseno` | Build the visual system: tokens (3 levels), universal components, templates, modes, publication | `derivar.py` · `verificar.py` · `construir.py` |
| `dominio` | Define the business type: entities, rules, domain patterns, own components | `inyectar.py` |
| `pantalla` | Design a screen or flow: template + data + states | `verificar-pantalla.py` |
| `probar` | Test screens and flows: five moments, states, edge values, focus, 200 % zoom | `probar.py` |
| `entregar` | **Ship to development:** seven-page file structure, asset package, animation contract, versioning | `entregar.py` |
| `auditar` | Audit an existing system, compute the score, and report rule coverage | `auditar.py` |
| `documentar` | Document a component or pattern (props, accessibility, do's/don'ts, code) | uses `verificar.py` |

## Commands (explicit)

Command names are deliberately distinct from skill names: a command and a skill sharing a name occupy the
same namespace, and one shadows the other in the listing.

`/design-system:crear` · `:definir-dominio` · `:disenar-pantalla` · `:probar-pantalla` · `:entregar-sistema` ·
`:auditar-sistema` · `:documentar-pieza` · `:extender`

## Structure

```
design-system/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json    # the `geanpaul-design` marketplace
├── commands/               # slash commands (thin entry points)
├── skills/                 # the seven skills, each with its scripts
├── lib/comun.py            # shared by every verifier — and it READS the rules from the KB
├── conocimiento/DESIGN/     # this plugin's knowledge base: the 76 DS-xxx rules, checklists, contract
├── dominios/               # `_plantilla.json`: the domain spec. Business domains live in your project
├── ejemplos/base/          # the golden system the test suite runs against
└── pruebas/                # construir.sh (assemble the golden) · correr.sh (the suite)
```

> **`conocimiento/sources/` is git-ignored on purpose.** It holds the full text of the two Packt books the
> knowledge base was built from, and their copyright page forbids redistribution. The KB cites chapter numbers
> — `[Book 1, cap. 6]` — instead of pasting text, so traceability survives without them. See `.gitignore`.

## The test suite

```bash
./pruebas/correr.sh             # everything
./pruebas/correr.sh --rapido    # clean run only, no injections
```

Three stages: the golden system passes clean · **every check detects its own injected error** · no `auto` rule
in the KB is left without a check. It exists because the plugin already claimed *«a check that never failed is
not tested: it is unused»* and nothing ran that claim. See `ejemplos/README.md`.

## Install

Run these inside Claude Code. The marketplace is named `geanpaul-design` and is defined by
`.claude-plugin/marketplace.json` at the repository root — plugins install by marketplace name, not by repo.

```
# from git
/plugin marketplace add <user>/<repo>
/plugin install design-system@geanpaul-design

# local development, from the directory containing this repo
/plugin marketplace add ./design-system
/plugin install design-system@geanpaul-design
```

If the install summary reports `Run /reload-plugins to activate.`, run that command.

The pipeline order: **sistema-diseno → dominio → pantalla → (probar, documentar) → entregar → auditar**.
