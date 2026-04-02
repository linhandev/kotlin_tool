# OHOS Migration Demo Scenarios

This demo focuses on OHOS source-set import patterns observed in `~/git/ci`, especially `src/ohosArm64Main`.

It is a single buildable Kotlin/Native OHOS demo project configured to produce a shared library (`.so`).
The demo also includes a cinterop `.def` that generates `platform.ohos.custom` for migration-strength testing.

## Scenario Summary

1. Direct platform import
   - Pattern: `import platform.ohos.<symbol>`
   - Seen in multiple OHOS entry points (for example `napi_env`, `napi_value`).
   - Migration expectation: rewrite when mapping is certain.
   - Extra check: direct call to `platform.ohos.custom.custom_magic()` from cinterop-generated custom platform package.

2. Wildcard platform import
   - Pattern: `import platform.ohos.*`
   - Seen in interop-heavy modules where symbol fan-out is broad.
   - Fixture note: wildcard-imported symbols are actually referenced (for example `napi_env`, `napi_value`).
   - Migration expectation: stays unchanged; current tool does not upgrade wildcard imports.

3. Mixed import style in one file
   - Pattern: direct + wildcard imports together.
   - Fixture note: file uses both a directly imported symbol (`napi_ref`) and a wildcard-resolved symbol (`napi_value`).
   - Fixture note: also imports `platform.ohos.custom.*` and calls `custom_magic()`.
   - Migration expectation: direct import rewritten when certain, wildcard import stays unchanged.

4. Non-platform wildcard import (reference only)
   - Pattern: `import kotlin.collections.*`
   - Included to mirror wildcard usage style without extra dependencies; not rewritten because migration target scope is `platform.*`.

5. Nested cinterop type vs from-version umbrella "flat" import (`Rdb_KeyData`)
   - **Context:** In native headers, a type can be nested in C (example: `union Rdb_KeyData` inside `typedef struct Rdb_KeyInfo` in relational DB APIs). A to-version split cinterop can keep that as nested Kotlin metadata (`Rdb_KeyInfo::Rdb_KeyData` in `klib dump-metadata-signatures`), while a from-version umbrella klib exposes it as a **top-level** `platform.framework.Rdb_KeyData`.
   - **Fixture:** `src/ohosArm64Main/kotlin/demo/RdbNestedTypeSample.kt` imports `platform.framework.Rdb_KeyData` and uses `CPointer<Rdb_KeyData>?` (wired from `App.kt` with `null`, same style as other samples). Requires a from-version OHOS toolchain (for example KBA in `gradle.properties`) so the `framework` platform klib is on the compile classpath.
   - **Migration expectation:** With from/to platform klib indexes, the tool matches the from-version simple name to the to-version nested declaration (trailing-name alias) and rewrites to the **`kotlinImportTarget`** import `import platform.ArkData.RDB.`Rdb_KeyInfo::Rdb_KeyData`` (not `import platform.ArkData.RDB.Rdb_KeyData`). The tool then inserts ``typealias Rdb_KeyData = `Rdb_KeyInfo::Rdb_KeyData` `` **immediately after the last `import`** so old simple-name type positions remain valid.

6. Hardcoded fallback constants (`LOG_DEBUG`, `LOG_INFO`)
   - **Context:** These constants can remain ambiguous after evidence-based disambiguation.
   - **Fixture:** `src/ohosArm64Main/kotlin/demo/HiLogDebugSample.kt` and `src/ohosArm64Main/kotlin/demo/HiLogInfoSample.kt` import `platform.ohos.LOG_DEBUG` / `platform.ohos.LOG_INFO`.
   - **Migration expectation:** when ambiguity persists, fallback resolves to `platform.PerformanceAnalysisKit.HiLog.LOG_DEBUG` and `platform.PerformanceAnalysisKit.HiLog.LOG_INFO`.

7. Hardcoded fallback constants for DDK (`DDK_FAILURE`, `DDK_SUCCESS`)
   - **Context:** Device DDK return-code symbols can remain ambiguous between BaseDdk and UsbDDK after evidence-based disambiguation.
   - **Fixture:** `src/ohosArm64Main/kotlin/demo/DdkFailureSample.kt` and `src/ohosArm64Main/kotlin/demo/DdkSuccessSample.kt` import `platform.devices.DDK_FAILURE` / `platform.devices.DDK_SUCCESS`.
   - **Migration expectation:** when ambiguity persists, fallback resolves to `platform.DriverDevelopmentKit.BaseDdk.DDK_FAILURE` and `platform.DriverDevelopmentKit.BaseDdk.DDK_SUCCESS`.

8. Hardcoded fallback function for ioctl (`platform.ohos.ioctl`)
   - **Context:** `ioctl` can remain ambiguous after evidence-based disambiguation (`platform.linux.ioctl` vs `platform.posix.ioctl`).
   - **Fixture:** `src/ohosArm64Main/kotlin/demo/IoctlSample.kt` imports `platform.ohos.ioctl`.
   - **Migration expectation:** when ambiguity persists, fallback resolves to `platform.posix.ioctl`.

9. Hardcoded fallback sdk-info symbols (`platform.ohos.*` -> `platform.info.*`)
   - **Context:** Version constants and sdk-target helpers can remain ambiguous between `platform.info` and `platform.posix`.
   - **Fixture:** `src/ohosArm64Main/kotlin/demo/SdkInfoSample.kt` imports and uses:
     - `platform.ohos.get_application_target_sdk_version`
     - `platform.ohos.OH_API_VERSION_10` ~ `OH_API_VERSION_15`
     - `platform.ohos.OH_CURRENT_API_VERSION`
     - `platform.ohos.SDK_VERSION_7` ~ `SDK_VERSION_9`
     - `platform.ohos.SDK_VERSION_FUTURE`
     - `platform.ohos.set_application_target_sdk_version`
   - **Migration expectation:** when ambiguity persists, each import resolves to the matching `platform.info.*` symbol.

10. Post-migration completion check (`scan`)
   - **Context:** After import rewrites, `scan` should report migration completion from mapping scope.
   - **Fixture flow:** `klib/test.sh` (repo root: `./klib/test.sh`) runs the migration demo pipeline (see that script).
   - **Expectation:** `totalCurrentVersionImports=0`, `wildcardImportsInOhSourceset=0`, and `isMigrationComplete=yes` before the to-version rebuild step.

11. Mapping-file-only workflow (`scan` / `migrate`)
   - **Context:** the main workflow commands are mapping-driven and no longer accept redundant klib-path analysis inputs.
   - **Fixture flow:**
     - `scan` runs with `--mapping-file` and `--target-project`.
     - `migrate` runs as mapping-file `--dry-run`, then apply-mode with the same mapping file.
   - **Expectation:** both commands execute successfully in mapping-only mode and apply-mode migration rewrites imports correctly.
