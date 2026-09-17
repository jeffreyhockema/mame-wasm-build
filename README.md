# mame-wasm-build

WebAssembly builds of [MAME](https://www.mamedev.org/) **0.244**, compiled unmodified from the
[`mame0244`](https://github.com/mamedev/mame/tree/mame0244) source tag with Emscripten 3.1.8.

A full MAME is too large to load in a browser, so the drivers are split into bundles
(`bundles.json`: bundle name → driver source files). Each bundle builds to
`mame<bundle>.js` + `mame<bundle>.wasm`.

## Building

Run the **build** workflow from the Actions tab (or `gh workflow run build -f bundles=cps2,neogeo`).
Leave `bundles` blank to build everything; tick `release` to publish the files as a release.

## License

MAME is licensed under the GNU GPL version 2 or later (portions BSD-3-Clause); see the
[MAME source](https://github.com/mamedev/mame/tree/mame0244) for the complete license and source.
This repository contains build scripts only — **no ROMs or other copyrighted game data**.
