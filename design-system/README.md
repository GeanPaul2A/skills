# design-system

A Claude Code plugin to build a **complete, verifiable design system** — and to design, test, audit and
document screens and flows across **different business types**.

The core is business-agnostic. Each business type is a **domain file** (`dominios/<tipo>.json`) that injects its
own entities, rules, patterns and non-universal components. The system publishes to CSS, Swift, Android or Figma,
and every validation step can be viewed as HTML.

## Skills (auto-invoked by description)

| Skill | What it does |
|---|---|
| `sistema-diseno` | Build the visual system: tokens (3 levels), universal components, templates, modes, publication |
| `dominio` | Define the business type: entities, rules, domain patterns, own components |
| `pantalla` | Design a screen or flow: template + data + states |
| `probar` | Test / prototype screens and flows (the five moments, states, edge values) |
| `auditar` | Audit an existing system or screens and produce an actionable report |
| `documentar` | Document a component or pattern (props, accessibility, do's/don'ts, code) |

## Commands (explicit)

Command names are deliberately distinct from skill names: a command and a skill sharing a name occupy the
same namespace, and one shadows the other in the listing.

`/design-system:crear` · `:definir-dominio` · `:disenar-pantalla` · `:probar-pantalla` · `:auditar-sistema` ·
`:documentar-pieza` · `:extender`

## Structure

```
design-system/
├── .claude-plugin/plugin.json
├── commands/            # slash commands (thin entry points)
├── skills/              # the six skills
├── conocimiento/        # single source of truth: the 76 DS-xxx rules, checklists, contract
└── dominios/            # `_plantilla.json`: the domain spec. Business domains live in your project, not here
```

## Install

Run these inside Claude Code. The marketplace is named `geanpaul-design` and is defined by
`.claude-plugin/marketplace.json` at the repository root — plugins install by marketplace name, not by repo.

```
# from git
/plugin marketplace add <user>/<repo>
/plugin install design-system@geanpaul-design

# local development, from the directory containing this repo
/plugin marketplace add ./deepseek-claude
/plugin install design-system@geanpaul-design
```

If the install summary reports `Run /reload-plugins to activate.`, run that command.

The pipeline order: **sistema-diseno → dominio → pantalla → (probar, documentar) → auditar**.
