# miryoku_zmk — my totem config

Personal [Miryoku](https://github.com/manna-harbour/miryoku) ZMK config for a
[GEIGEIST Totem](https://github.com/GEIGEIGEIST/zmk-config-totem) (38 keys) on
`xiao_ble` controllers.

## Keymap

All 7 layers. Home row shows **tap** (large) / **hold-mod** (small); thumbs show
**tap** / **hold-layer**.

![keymap](docs/keymap/totem.svg)

Regenerate after editing layers:

```sh
make -C docs/keymap img      # or: docs/keymap/build.sh
```

See [docs/keymap/](docs/keymap/) for how it's generated.

## What's customised vs upstream

- **Timeless home-row mods** — `u_mt` / `u_lt` use `flavor = "balanced"`,
  `require-prior-idle-ms = 150`, and `quick-tap-ms = 175` so fast typing rolls
  don't misfire mods. See `miryoku/miryoku_behaviors.dtsi`.
- **Layers** — GACS home-row mods (GUI/ALT/CTRL/SHFT), thumb layer-taps into
  Nav / Mouse / Media / Sym / Num / Fun. Defined in `miryoku/custom_config.h`.
- **Board** — `xiao_ble//zmk` (Zephyr 4.1 naming).

## Building

Trigger the **Build mine** GitHub Action (`.github/workflows/build-mine.yml`):
board `xiao_ble//zmk`, shields `totem_left` / `totem_right`.

Download the artifacts, then flash each half:

- **Left (central):** hold `Tab` (→ Nav layer), tap the **top-left** key
  (`BOOT`) → UF2 bootloader → drop `*_left.uf2`.
- **Right (peripheral):** double-short the XIAO **RST pads** → UF2 bootloader →
  drop `*_right.uf2`. (Keymap can't bootloader the peripheral — it doesn't run
  behaviours.)

Double reset = flash mode, single = reboot.

---

Upstream docs: [`readme.org`](readme.org) ·
[Miryoku](https://github.com/manna-harbour/miryoku) ·
[ZMK](https://zmk.dev/)
