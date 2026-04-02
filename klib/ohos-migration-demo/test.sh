#!/usr/bin/env bash
# 0) restore demo Kotlin sources  1) from-version demo build  2) build migration tool
# 3) scan (mapping file)  4) migrate (mapping file dry-run + apply)
# 5) to-version rebuild must succeed
# Usage: ./demo/ohos-migration-demo/test.sh [to-kotlin-version]
# Optional: KLIB_BIN, CURRENT_KLIBS, TARGET_KLIBS, FROM_KOTLIN_VERSION
# Optional: SWITCHING_PLATFORM_BUILD=release|debug (default debug) — which CLI binary to build/use

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEMO_DIR="$SCRIPT_DIR"
TO_VERSION="${1:-2.2.21-EZ.0.2.0-03}"
FROM_VERSION="${FROM_KOTLIN_VERSION:-2.0.21-KBA-014}"

KLIB_BIN="${KLIB_BIN:-$HOME/git/kmp/cpf-kotlin-cinterop/kotlin-native/dist/bin/klib}"
CURRENT_KLIBS="${CURRENT_KLIBS:-$HOME/.konan/kotlin-native-prebuilt-macos-aarch64-${FROM_VERSION}/klib/platform/ohos_arm64}"
TARGET_KLIBS="${TARGET_KLIBS:-$HOME/git/kmp/cpf-kotlin-cinterop/kotlin-native/dist/klib/platform/ohos_arm64}"

gradle_demo() { "$REPO_ROOT/gradlew" -p "$DEMO_DIR" "$@"; }

echo "== 0) Restore demo Kotlin sources (from-version baseline; e.g. KBA) =="
git -C "$REPO_ROOT" restore -- "demo/ohos-migration-demo/src/ohosArm64Main/kotlin/demo"

echo "== 1) Demo (from-version; e.g. KBA) =="
gradle_demo -PkotlinVersion="$FROM_VERSION" clean linkDebugSharedOhosArm64

echo "== 2) Migration tool =="
if [[ "${SWITCHING_PLATFORM_BUILD:-debug}" == "release" ]]; then
  (cd "$REPO_ROOT" && ./gradlew clean linkReleaseExecutableMacosArm64)
  KEXE="$REPO_ROOT/build/bin/macosArm64/releaseExecutable/platform-import-migrator.kexe"
else
  (cd "$REPO_ROOT" && ./gradlew clean linkDebugExecutableMacosArm64)
  KEXE="$REPO_ROOT/build/bin/macosArm64/debugExecutable/platform-import-migrator.kexe"
fi

[[ -f "$KLIB_BIN" && -d "$CURRENT_KLIBS" && -d "$TARGET_KLIBS" ]] || {
  echo "Set KLIB_BIN, CURRENT_KLIBS, TARGET_KLIBS (missing path)" >&2
  exit 1
}

echo "== 3) map export (developer CSV) =="
# Run `map` from repo root so relative output paths are stable regardless of caller cwd.
MAP_OUTPUT="$(cd "$REPO_ROOT" && "$KEXE" map \
  --klib-bin "$KLIB_BIN" \
  --current-klibs "$CURRENT_KLIBS" \
  --target-klibs "$TARGET_KLIBS")"
echo "$MAP_OUTPUT"

MAPPING_CSV="$(printf '%s\n' "$MAP_OUTPUT" | awk -F'=' '/^mappingOut=/{print $2; exit}')"
if [[ -n "$MAPPING_CSV" && "${MAPPING_CSV:0:1}" != "/" ]]; then
  MAPPING_CSV="$REPO_ROOT/$MAPPING_CSV"
fi

if [[ -z "$MAPPING_CSV" || ! -f "$MAPPING_CSV" ]]; then
  echo "Expected mapping CSV not found after map command" >&2
  exit 1
fi

echo "== 3.1) scan with mapping-file =="
"$KEXE" scan \
  --mapping-file "$MAPPING_CSV" \
  --target-project "$DEMO_DIR"

echo "== 4.1) migrate with mapping-file (dry-run) =="
"$KEXE" migrate \
  --dry-run \
  --mapping-file "$MAPPING_CSV" \
  --target-project "$DEMO_DIR"

echo "== 4.2) migrate with mapping-file (apply) =="
MIGRATE_APPLY_OUTPUT="$("$KEXE" migrate \
  --mapping-file "$MAPPING_CSV" \
  --target-project "$DEMO_DIR")"
echo "$MIGRATE_APPLY_OUTPUT"
if ! printf '%s\n' "$MIGRATE_APPLY_OUTPUT" | rg -q '^blocked=0$'; then
  echo "migrate apply must report blocked=0 (no blocked imports)" >&2
  exit 1
fi

echo "== 4.3) verify nested import + typealias from CSV mapping =="
RDB_FILE="$DEMO_DIR/src/ohosArm64Main/kotlin/demo/RdbNestedTypeSample.kt"
if ! rg -n 'import platform\.ArkData\.RDB\.`Rdb_KeyInfo::Rdb_KeyData`' "$RDB_FILE" >/dev/null; then
  echo "Expected nested to-version import not found in $RDB_FILE" >&2
  exit 1
fi
if ! rg -n 'typealias Rdb_KeyData = `Rdb_KeyInfo::Rdb_KeyData`' "$RDB_FILE" >/dev/null; then
  echo "Expected nested typealias not found in $RDB_FILE" >&2
  exit 1
fi

echo "== 4.4) verify DDK fallback import rewrites =="
DDK_FAILURE_FILE="$DEMO_DIR/src/ohosArm64Main/kotlin/demo/DdkFailureSample.kt"
DDK_SUCCESS_FILE="$DEMO_DIR/src/ohosArm64Main/kotlin/demo/DdkSuccessSample.kt"
if ! rg -n 'import platform\.DriverDevelopmentKit\.BaseDdk\.DDK_FAILURE' "$DDK_FAILURE_FILE" >/dev/null; then
  echo "Expected BaseDdk DDK_FAILURE import not found in $DDK_FAILURE_FILE" >&2
  exit 1
fi
if ! rg -n 'import platform\.DriverDevelopmentKit\.BaseDdk\.DDK_SUCCESS' "$DDK_SUCCESS_FILE" >/dev/null; then
  echo "Expected BaseDdk DDK_SUCCESS import not found in $DDK_SUCCESS_FILE" >&2
  exit 1
fi

echo "== 4.5) verify ioctl fallback import rewrite =="
IOCTL_FILE="$DEMO_DIR/src/ohosArm64Main/kotlin/demo/IoctlSample.kt"
if ! rg -n 'import platform\.posix\.ioctl' "$IOCTL_FILE" >/dev/null; then
  echo "Expected posix ioctl import not found in $IOCTL_FILE" >&2
  exit 1
fi

echo "== 4.6) verify sdk-info fallback import rewrites =="
SDK_INFO_FILE="$DEMO_DIR/src/ohosArm64Main/kotlin/demo/SdkInfoSample.kt"
for sym in \
  get_application_target_sdk_version \
  OH_API_VERSION_10 \
  OH_API_VERSION_11 \
  OH_API_VERSION_12 \
  OH_API_VERSION_13 \
  OH_API_VERSION_14 \
  OH_API_VERSION_15 \
  OH_CURRENT_API_VERSION \
  SDK_VERSION_7 \
  SDK_VERSION_8 \
  SDK_VERSION_9 \
  SDK_VERSION_FUTURE \
  set_application_target_sdk_version
do
  if ! rg -n "import platform\\.info\\.${sym}" "$SDK_INFO_FILE" >/dev/null; then
    echo "Expected platform.info.${sym} import not found in $SDK_INFO_FILE" >&2
    exit 1
  fi
done

echo "== 4.7) scan completion check after migrate apply =="
POST_SCAN_OUTPUT="$("$KEXE" scan \
  --mapping-file "$MAPPING_CSV" \
  --target-project "$DEMO_DIR")"
echo "$POST_SCAN_OUTPUT"
for key in filesScanned totalCurrentVersionImports autoMigratableImports wildcardImportsInOhSourceset isMigrationComplete
do
  if ! printf '%s\n' "$POST_SCAN_OUTPUT" | rg -q "^${key}="; then
    echo "Expected ${key}=... in scan summary" >&2
    exit 1
  fi
done
if ! printf '%s\n' "$POST_SCAN_OUTPUT" | rg -q '^isMigrationComplete=(yes|no)$'; then
  echo "Expected isMigrationComplete=yes|no in scan summary" >&2
  exit 1
fi

echo "== 5) rebuild (-PkotlinVersion=${TO_VERSION}; expect success after migrate) =="
gradle_demo -PkotlinVersion="$TO_VERSION" clean linkDebugSharedOhosArm64
echo "OK: rebuild succeeded after upgrade"
