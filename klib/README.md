# klib tools

Small utilities around Kotlin/Native **`.klib`** metadata, focused on comparing what two compiler snapshots expose on a platform (for example `ohos_arm64`).

## Mapping (`mapping.py`)

**Purpose.** Build a CSV that relates **source klib exports** to **target klib exports** when migrating or diffing Kotlin/Native versions.

**Pipeline.**

1. **Collect signatures** — For each immediate child directory under `SOURCE_KLIBS` and under `TARGET_KLIBS`, run the `klib` binary with `dump-metadata-signatures` (see `declarations.collect_from_klibs` in `declarations.py`).
2. **Normalize** — Parser keeps `(package, declaration)` pairs and skips synthetic accessors (`.<get-…>`, `.<set-…>`, `.<init>`).
3. **Index target** — For every target klib, map each `declaration` path to the Kotlin **packages** that define it in that version, remembering which target klib directory each package came from.
4. **Join source → target** — For each `(source_klib, source_package, declaration)` from the source scan, look up `declaration` in the target index. All packages that define that same declaration path become candidate **target FQ names** `package.declaration`.
5. **Disambiguation (optional)** — If a row is `ambiguous`, `generate_mapping()` may reclassify it as `mapped`. It reads the **source** klib’s `default/manifest` `includedHeaders`, resolves existing headers under `SOURCE_SYSROOT`, runs **Universal Ctags** (JSON) to find which single header defines the C symbol (declaration must not contain `.`; dotted Kotlin paths are skipped). It then keeps only target candidates whose manifest `includedHeaders` contains that same path token. Klib **folder name** (disk) and Kotlin **package** from the dump are independent; manifests also carry `package=` / `unique_name=` separately from the directory name.

**Row status.**

| Status | Meaning |
|--------|---------|
| `mapped` | Exactly one target FQ name for this declaration path (across target packages/klibs), or resolved by disambiguation. |
| `ambiguous` | More than one target FQ name; `target_fqname` is `|`‑separated sorted candidates. |
| `missing` | No target package defines this declaration path. |

**Output.** `mappings/mapping-{source compilerVersion}-to-{target compilerVersion}.csv`, with columns: `source_klib`, `source_package`, `declaration`, `status`, `target_fqname`. Compiler versions are read from each prebuilt’s `konan/konan.properties` (`compilerVersion`), using the path layout expected by `get_compiler_version()` (platform klib dir → prebuilt root → `konan/konan.properties`).

**Configuration.** Paths and the `klib` binary are set in `config.py` (`KLIB`, `SOURCE_KLIBS`, `TARGET_KLIBS`). Set `SOURCE_SYSROOT` to a sysroot that **actually contains** the header files referenced by manifest tokens (for example `usr/include/...` relative to that root), and ensure Universal Ctags is on `PATH` (or set `CTAGS_BIN`). If no listed headers exist as files under the sysroot, disambiguation cannot resolve that row. If `SOURCE_SYSROOT` is missing or not a directory, or `ctags` is not found, disambiguation is skipped and ambiguous rows are left unchanged. Manifests that list only 64-character snapshot tokens in `includedHeaders` (no `.` in the token) cannot be used for this step.

## Related scripts

- **`declarations.py`** — Same dump pipeline; can aggregate unique declaration paths and package lists into `declarations.csv` (target tree only, per its `main`).
- **`source_paths.py`** — `collect()` for Kotlin source path collection (see that file for scope).

## Running

Requires a working `klib` on `PATH` or at `config.KLIB`, and Python 3 with dependencies from `requirements.txt` (`tqdm` is used by `declarations` for parallel dumps).

From the `klib/` directory (after adjusting `config.py` to your machine):

```bash
python mapping.py
```

From the repository root (parent of `klib/`):

```bash
python -m unittest discover -s klib/tests -t .
```

`-t .` sets the import top-level directory so tests load as the `klib.tests` package (and `klib/tests/__init__.py` can extend `sys.path` for the existing flat `import config` / `import manifest` style in `klib/*.py`).
