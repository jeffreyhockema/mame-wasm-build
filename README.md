# mame-wasm-build

WebAssembly builds of [MAME](https://www.mamedev.org/) **0.244**, compiled from the
[`mame0244`](https://github.com/mamedev/mame/tree/mame0244) source tag with Emscripten 3.1.8.

A full MAME is too large to load in a browser, so the drivers are split into bundles
(`bundles.json`: bundle name → driver source files). Each bundle builds to
`<bundle>.js` + `<bundle>.wasm`, linked with Emscripten's IndexedDB file system (`-lidbfs.js`)
so a page can keep MAME's settings, NVRAM and save states.

## Changes to MAME's source

The emulation is MAME 0.244's own; only the browser glue is patched (`patches/`):

- `0001-save-nvram-and-settings-on-exit.patch`: in the browser, `running_machine::run()` hands
  its loop to Emscripten and never returns, so the NVRAM and configuration it saves after the
  loop were never written. The browser main loop now saves them when the machine exits, then
  calls `Module.onMameExit()` if the page defines it.
- `0002-pointer-light-gun.patch`: 0.244's SDL input has no light gun, only a relative mouse, so a
  gun can't be aimed by pointing. Adds a `-lightgunprovider sdl` that reads the pointer's
  position in the window as the gun's aim and its buttons as the gun's (a tap on a touch
  screen arrives as the left button), after the `sdl_lightgun_device` of later MAME versions.
- `0003-state-in-memory-and-single-frames.patch`: for rollback netplay, exports
  `mame_state_size()`, `mame_state_save(buf, size)` and `mame_state_load(buf, size)` (the whole
  machine's state in memory, through MAME's own `save_manager::write_buffer`/`read_buffer`, the
  way its rewind keeps states) and `mame_run_frame()`, one step of the browser main loop, so a
  page can run frames itself.
- `0004-poll-input-every-read.patch`: the OSD polls input devices at most every 10 ms of real
  time, so frames run faster than that (a rollback replaying several in one go) took a press on
  a frame that depended on timing. In the browser build every read polls, which makes a frame's
  presses count on that frame.
- `0005-save-rtc-date-and-time.patch`: a real-time clock's date and time (`device_rtc_interface`'s
  registers) weren't in save states, though the clock chip's own registers are set from them
  every second: a loaded state kept the clock it was loaded into, and two machines running the
  same state (the Neo Geo's uPD4990A, for one) parted a second later.
- `0006-list-state-entries.patch`: `mame_state_entries()` lists what a state holds (each
  registered item's name and size, in order), so a page comparing two machines' states can say
  which part of the machine they disagree on.

The build also generates `tms57002.hxx` (and makes the folder its include path goes through) before compiling: 0.244 declares that generated header
as a dependency of the CPU's own sources only, so a partial build could compile a driver that
includes it (`konamigx.cpp`) first.

## Building

Run the **build** workflow from the Actions tab (or `gh workflow run build -f bundles=cps2,neogeo`).
Leave `bundles` blank to build everything; tick `release` to publish the files as a release.

## License

MAME is licensed under the GNU GPL version 2 or later (portions BSD-3-Clause); see the
[MAME source](https://github.com/mamedev/mame/tree/mame0244) for the complete license and source.
The patches here are under the same license. This repository contains build scripts only —
**no ROMs or other copyrighted game data**.
