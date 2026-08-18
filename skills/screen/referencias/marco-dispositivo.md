# Marco de dispositivo · por sistema operativo

**Cada pantalla se dibuja dentro de un marco de dispositivo, no en un lienzo suelto.** El marco es un frame a
las medidas reales del device, más la barra de estado y la barra inferior, como componentes reutilizables.

> **Lo que NO se dibuja acá** es el teclado, el selector de fecha ni los diálogos del sistema: eso se declara
> (`recursos/nativo.json`). El marco sí se dibuja — es presentación.

---

## El marco

```
<marco de dispositivo>
├── barra de estado      ← componente reutilizable (arriba)
├── <la pantalla>        ← el contenido: tus componentes
└── barra inferior       ← componente reutilizable (abajo)
```

---

## Medidas por plataforma

| Plataforma | Frame base | Barra de estado | Barra inferior |
|---|---|---|---|
| **iOS** | 375 × 812 | `iPhone X (or newer)` · 44 | `HomeIndicator` · 34 |
| **Android** | 360 × 800 | 24 dp | Barra de navegación · 48 (o gesto) |

- iOS más nuevos: 390 × 844 (iPhone 14/15/16).
- Android más nuevos: 412 × 915 (Pixel 7/8).

---

## Cómo se dibuja

1. La IA crea el frame a las medidas de la plataforma (`use_figma`).
2. Inserta la **barra de estado** (componente) arriba y la **barra inferior** (componente) abajo.
3. Dibuja el contenido de la pantalla entre ambas, con los componentes del sistema.

**La barra de estado y la barra inferior son componentes** — se crean una vez y se reusan en cada pantalla,
igual que el ejemplo de Coinbase (`iPhone X (or newer)` · `HomeIndicator`). No se redibujan por pantalla.

---

## Organización de pantallas multi-plataforma

**Se agrupa por sección del producto, no por plataforma.** Dentro de cada sección, las versiones móviles (iOS,
Android) van lado a lado para compararlas de un vistazo; desktop/web va aparte, por su form factor.

```
<Nombre del producto>
├── Sección · Onboarding
│   ├── 01-login        [iOS 375×812]  [Android 360×800]
│   ├── 02-registro     [iOS]          [Android]
├── Sección · Home
│   └── ...
└── Sección · Checkout
    └── ...
```

**Reglas:**
- **Por sección de producto** (función), no por plataforma: una función se ve completa junta.
- **Móvil lado a lado**: iOS y Android comparten sección porque comparten form factor.
- **Desktop/web aparte**: otro form factor (1440×1024), va en sección propia o página propia.
- Escalar a otra plataforma es **agregar un frame más**, no crear una página nueva.

---

## Por qué marco, y no un asset de teléfono

Un teléfono físico con bisel (opción "asset de device mockup") es decoración: suma ruido visual y depende de un
kit externo. El marco a medidas del device, con su barra de estado y su barra inferior como componentes, es lo
que usan los sistemas de diseño reales — y es lo que la IA puede dibujar sola, determinista, sin depender de
ningún asset.
