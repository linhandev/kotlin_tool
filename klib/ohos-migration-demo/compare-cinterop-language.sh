#!/usr/bin/env bash
# Rebuild cinterop with language = C vs C++ and grep klib metadata (default: function-pointer typedef).
#
# Does not require editing hiappevent.h or custom_api.h. Override the grep pattern if you compare
# another symbol, e.g. CINT_DUMP_GREP='OH_HiAppEvent_OnReceive' when dumping a klib built from SDK headers.
#
# Usage: CINT_DUMP_GREP='demo_void_callback' ./compare-cinterop-language.sh [kotlinVersion]
# Requires: ~/.konan/.../bin/klib for the same -PkotlinVersion as Gradle.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

KOTLIN_VERSION="${1:-2.0.21-KBA-014}"
KLIB_BIN="${KLIB_BIN:-$HOME/.konan/kotlin-native-prebuilt-macos-aarch64-${KOTLIN_VERSION}/bin/klib}"
DEF_FILE="$SCRIPT_DIR/src/ohosArm64Main/cinterop/custom.def"
CINT_KLIB="$SCRIPT_DIR/build/classes/kotlin/ohosArm64/main/cinterop/ohos-migration-demo-cinterop-custom.klib"

if [[ ! -x "$KLIB_BIN" ]]; then
  echo "klib not found: $KLIB_BIN (set KLIB_BIN or install Kotlin/Native $KOTLIN_VERSION)" >&2
  exit 1
fi

CINT_DUMP_GREP="${CINT_DUMP_GREP:-demo_after_extern_c_block}"

dump_filtered() {
  # grep exits 1 when there are no matches; do not fail the whole script under set -e
  if ! "$KLIB_BIN" dump-metadata "$CINT_KLIB" 2>&1 | grep "$CINT_DUMP_GREP"; then
    echo "(no lines matching ${CINT_DUMP_GREP})"
  fi
}

run_with_lang() {
  local lang="$1"
  sed -i.bak -e "s/^language = .*/language = $lang/" "$DEF_FILE"
  ./gradlew -q -PkotlinVersion="$KOTLIN_VERSION" clean cinteropCustomOhosArm64
  echo "=== language = $lang ==="
  dump_filtered
  mv "$DEF_FILE.bak" "$DEF_FILE"
}


run_with_lang C
echo ""
run_with_lang 'C++'

echo ""
echo "Restore default language in custom.def (C++):"
sed -i.bak -e 's/^language = .*/language = C++/' "$DEF_FILE"
rm -f "$DEF_FILE.bak"
echo "Done. Edit custom.def if you want a different default."
