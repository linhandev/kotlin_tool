---
name: klib-platform-import-migration-playbook
description: End-to-end OHOS platform import migration using the kotlin_tool klib/ Python pipeline — generate mapping CSV from paired platform klibs (mapping.py), migrate Kotlin imports in OH source sets (migrate.py), README-first build discovery, wildcard normalization with IntelliJ IDEA, ambiguous-row triage via CSV and mapping.py disambiguation hooks, dry-run completion checks, and target-version rebuild. Use when migrating a KMP project between Kotlin/Native OH platform snapshots or when operating mapping.py / migrate.py in this repository.
---

# Klib platform import migration playbook

Use this skill when a user wants a practical, low-risk migration for **Kotlin/Native OH platform** `import` lines between two compiler snapshots, using the **`klib/`** tooling in **kotlin_tool** (not the standalone `platform-import-migrator` binary unless the user switches to that workflow explicitly).

## Background to explain briefly

- Platform `.klib` **package layout** can change between downstream Kotlin/Native builds (umbrella packages split into kit-specific packages, nested cinterop names, etc.).
- **`mapping.py`** compares **source** vs **target** platform klib trees (`dump-metadata-signatures`) and writes a CSV of `source_package` + `declaration` → `target_package` (+ optional `target_declaration` for `::` nested names).
- **`migrate.py`** rewrites **single** import lines in **OH-scoped** `.kt` files using that CSV. Wildcard imports that match a **mapping `source_package`** are **not** auto-expanded — they must be normalized first (same constraint as the migrator kexe playbook).
- A small fraction of rows stay **`ambiguous`** or **`missing`** until you fix mapping generation (sysroot + ctags, `config.HARDCODED_*`) or fix imports manually.

## Tools in this repo (do not confuse with the standalone migrator)

| Piece | Role |
|--------|------|
| `klib/config.py` | `MIGRATING_PROJECT`, `SOURCE_SET_NAMES`, `SOURCE_COMPILER_VERSION` / `TARGET_COMPILER_VERSION`, `KLIB`, `SOURCE_KLIBS`, `TARGET_KLIBS`, `SOURCE_SYSROOT`, `CTAGS_BIN`, hardcoded disambiguation pairs |
| `klib/mapping.py` | Generate `klib/mappings/mapping-{sourceVer}-to-{targetVer}.csv` from the two klib trees |
| `klib/migrate.py` | Apply (or dry-run) import rewrites under the project root for paths matching `SOURCE_SET_NAMES` |
| `klib/README.md` | Mapping pipeline semantics (dump → normalize → join → disambiguation) |

**Run Python commands with `klib/` as the working directory** so `import config` resolves (`cd klib && python …`).

## Before you start

Ask for or set in `config.py` if unclear:

1. **`MIGRATING_PROJECT`** — absolute path to the KMP project root.
2. **`TARGET_VERSION`** — the Kotlin/Native **compilerVersion** string for the migration target (must match the target prebuilt’s `konan/konan.properties` and `migrate.py --target-version` if you override defaults).
3. **Klib inputs** — `KLIB` binary path, `SOURCE_KLIBS` and `TARGET_KLIBS` directories (each should be the **`ohos_arm64` platform leaf** containing one subdirectory per platform klib, as expected by `declarations.collect_from_klibs`).
4. **Optional disambiguation** — `SOURCE_SYSROOT` (headers that match manifest tokens) and Universal **Ctags** on `PATH` (or `CTAGS_BIN`) so `mapping.py` can shrink `ambiguous` rows.
5. **Build** — ensure the migrating project’s Gradle/Maven repos are configured for **`TARGET_VERSION`** before the final verification build.

**Critical:** the final verification build must use the **target** Kotlin/Native toolchain, not the source one.

Discover the migrating project in this order:

1. Read **README** and any `SCENARIOS.md`-style docs for build commands.
2. Inspect scripts (`test.sh`, `build*.sh`).
3. Inspect Gradle tasks if still unclear.

Identify:

- Project build command.
- Where Kotlin/KMP version is pinned.
- OH source-set **directory** names (for example `ohosMain`, `ohosArm64Main`, `ohosX64Main`, `nativeOhos`) — they must match **`SOURCE_SET_NAMES`** in `config.py` (used by `migrate.collect`).

## Non-negotiable safety rules

- Refuse to proceed if **`MIGRATING_PROJECT`** has uncommitted changes (unless the user explicitly accepts a throwaway branch).
- Keep mechanical edits to **OH source sets** only; `migrate.py` already filters by `SOURCE_SET_NAMES`, but **wildcard expansion / IDE optimize** can touch other trees — restore non-OH paths if needed.
- If wildcard import expansion is required, **back up** `.idea/codeStyles/Project.xml` (and `codeStyleConfig.xml` if edited); restore after cleanup unless the user wants to keep IDE settings.
- No destructive cleanup; use path-scoped `git restore` (or explicit reverts) for stray changes.
- Never push to remote unless explicitly instructed.

## Progress checklist

```text
Migration Progress (klib/)
- [ ] 1) config.py inputs (project, versions, klib paths, source sets, optional sysroot/ctags)
- [ ] 2) Project exploration (build command, version pin, OH folder names)
- [ ] 3) Baseline build on source/current toolchain
- [ ] 4) Generate or obtain mapping CSV (mapping.py → klib/mappings/…)
- [ ] 5) Pre-migrate dry-run (migrate.py --dry-run) — note wildcards & blocked imports
- [ ] 6) Wildcard handling in IntelliJ IDEA (if needed)
- [ ] 7) Scope cleanup to OH source sets (if IDE touched other paths)
- [ ] 8) migrate.py apply (after dry-run review)
- [ ] 9) Manual fixes for ambiguous/missing + exotic import syntax
- [ ] 10) Post-migrate dry-run completion gate
- [ ] 11) Rebuild on target toolchain
- [ ] 12) Report results
```

## Mapping generation (`mapping.py`)

From `klib/` after editing `config.py`:

```shell
cd /path/to/kotlin_tool/klib
python mapping.py
```

This writes:

`mappings/mapping-{SOURCE_VER}-to-{TARGET_VER}.csv`

with columns: `source_package`, `declaration`, `status`, `target_package`, `target_declaration`.

- **`mapped`** — migrate can rewrite exact `import source_package.declaration` lines.
- **`ambiguous`** — multiple target packages; migrate **will not** change those imports until you improve disambiguation (sysroot/ctags, GLES rules, `HARDCODED_SOURCE_FQNAME_TO_TARGET_FQNAME` in `config.py`) or fix the CSV / code manually.
- **`missing`** — no target declaration path; needs manual mapping or code change.

If `ambiguous`/`missing` counts are high, fix **inputs** (correct `TARGET_KLIBS` tree, sysroot paths, ctags) before blaming application code.

## Migrate commands (`migrate.py`)

`migrate.py` resolves the CSV by **`--source-version`** and **`--target-version`** (defaults from `config.py`), searching **`klib/mappings/`** then **`klib/`**.

### Pre-migrate and post-migrate “scan” (dry-run)

There is no separate `scan` subcommand. Use **`--dry-run`** and read stderr:

- **`Wildcard imports (warnings)`** — lines like `import <source_package>.*` for a package that appears in the mapping; these **must** be expanded to explicit imports (same as the kexe playbook).
- **`FQ imports not updated (missing/ambiguous)`** — file:line reasons for rows the CSV did not resolve as `mapped`.

```shell
cd /path/to/kotlin_tool/klib
python migrate.py --dry-run --project "$MIGRATING_PROJECT"
# Optional explicit versions if they differ from config.py:
python migrate.py --dry-run --project "$MIGRATING_PROJECT" \
  --source-version "2.0.21-KBA-014" --target-version "2.2.21-EZ.0.2.0-05"
```

### Apply migration

Always **`--dry-run`** first, then apply:

```shell
cd /path/to/kotlin_tool/klib
python migrate.py --dry-run --project "$MIGRATING_PROJECT"
python migrate.py --project "$MIGRATING_PROJECT"
```

`migrate.py` only edits `.kt` files whose path contains `/<sourceSetName>/` for some name in `SOURCE_SET_NAMES`.

### Post-migrate completion gate (dry-run)

Treat migration as **incomplete** until a final dry-run reports:

- **`Wildcard imports (warnings): 0`**
- **`FQ imports not updated (missing/ambiguous): 0`**

(If the project intentionally has no platform imports, `FQ imports not updated` may already be zero — still confirm wildcards.)

### Agent instructions (migrate)

1. **Dry-run → apply → dry-run** for the automated part.
2. Ensure the CSV on disk matches the **`--source-version` / `--target-version`** passed to `migrate.py` (or defaults in `config.py`).
3. For blocked symbols, grep the **CSV** for `source_package` / `declaration` and inspect `status` and `target_package` columns; cross-check with `mapping.py` disambiguation and `config.HARDCODED_*`.

## Limitations (read before promising)

- **Skipped imports:** paths with **backticks**, multiline imports, broken `import` syntax — normalize by hand or with the IDE/LLM; see `migrate.py` module docstring.
- **`.def` / cinterop** in the app project are **out of scope** for `migrate.py` (same non-goal as the original playbook unless the user asks separately).

## Wildcard normalization (conditional)

Same workflow as the **platform-call-migration-playbook**: IntelliJ per-project code style, raise star-import thresholds, **Optimize Imports** (scoped to OH if possible), then **restore** `Project.xml` from backup.

Reference blocks (backup files first):

**`codeStyleConfig.xml`**

```xml
<component name="ProjectCodeStyleConfiguration">
  <state>
    <option name="USE_PER_PROJECT_SETTINGS" value="true" />
  </state>
</component>
```

**`Project.xml`** (use a `version` consistent with your IDE)

```xml
<component name="ProjectCodeStyleConfiguration">
  <code_scheme name="Project" version="173">
    <JetCodeStyleSettings>
      <option name="NAME_COUNT_TO_USE_STAR_IMPORT" value="2147483647" />
      <option name="NAME_COUNT_TO_USE_STAR_IMPORT_FOR_MEMBERS" value="2147483647" />
    </JetCodeStyleSettings>
  </code_scheme>
</component>
```

After expansion, run `migrate.py --dry-run` again until wildcard warnings are gone.

## Ambiguous / manual fixes

When the CSV lists multiple `target_package` values (`|`‑separated) or empty target:

1. Grep the mapping row for the **source** `declaration` and inspect **all** candidates.
2. Use call-site context (which kit/API is used).
3. Prefer fixes that match **header / module ownership**, not only name similarity.
4. Options: improve **`mapping.py` inputs** (sysroot, ctags), add **`HARDCODED_SOURCE_FQNAME_TO_TARGET_FQNAME`** entries if appropriate, or edit Kotlin imports / local typealiases manually.
5. Re-run **`mapping.py`** after CSV-affecting config changes; then **`migrate.py`** again.

## Rebuild on target version

1. Confirm the project resolves dependencies against **`TARGET_VERSION`**.
2. Run the project’s documented build.
3. If the compiler version in build output does not match target, stop and fix version pinning before declaring success.

## Testing this repo’s tooling

From repository root:

```shell
python -m unittest discover -s klib/tests -t .
```

## Skill iteration loop

After each real migration:

- Note friction (wildcard cleanup, ambiguous rows, migrate parser limits).
- Note any **README** drift (column names, paths).
- Update this skill when a step repeatedly fails in practice.

## Failure handling

- **Baseline build fails** — stop; fix before migration.
- **mapping.py fails** — check `KLIB` exists, `SOURCE_KLIBS` / `TARGET_KLIBS` layout, disk space, and `konan.properties` paths.
- **Wildcards persist** — re-check IDE code style and Optimize Imports scope.
- **Many `fq_not_changed`** — regenerate mapping with better disambiguation inputs or extend hardcoded pairs; grep CSV for the symbol’s `status`.

## Relationship to the standalone migrator skill

The **platform-call-migration-playbook** (external `platform-import-migrator` **`.kexe`**) and this skill describe the **same migration problem**. Use **this** skill when work happens **inside kotlin_tool `klib/`** (Python mapping + migrate). Use the **kexe** skill when the user only has published **binaries + CSV** and no local clone of kotlin_tool.
