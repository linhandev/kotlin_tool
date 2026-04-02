#!/usr/bin/env bash
# OH migration demo: unit tests → restore sources → Gradle (source compiler version) →
# migrate.py --dry-run → migrate.py (apply) → Gradle (target compiler version).
#
# Source/target compiler versions match klib/config.py (SOURCE_COMPILER_VERSION /
# TARGET_COMPILER_VERSION) and the mapping CSV under klib/mappings/.
#
# Run from repository root: ./klib/test.sh
# Or from this directory: ./test.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
KLIB_DIR="$SCRIPT_DIR"
DEMO_DIR="$KLIB_DIR/ohos-migration-demo"

SOURCE_COMPILER_VERSION="2.0.21-KBA-014"
TARGET_COMPILER_VERSION="2.2.21-EZ.0.2.0-05"

echo "== UT: klib unit tests =="
( cd "$REPO_ROOT" && python -m unittest discover -s klib/tests -t . )

echo "== 0) Restore demo Kotlin sources (git) =="
git -C "$REPO_ROOT" restore -- "klib/ohos-migration-demo/src"

echo "== 1) Gradle build (source compiler version ${SOURCE_COMPILER_VERSION}) =="
( cd "$DEMO_DIR" && ./gradlew -PkotlinVersion="$SOURCE_COMPILER_VERSION" clean linkDebugSharedOhosArm64 )

echo "== 2) Migrate dry-run =="
python "$KLIB_DIR/migrate.py" \
  --project "$DEMO_DIR" \
  --source-version "$SOURCE_COMPILER_VERSION" \
  --target-version "$TARGET_COMPILER_VERSION" \
  --dry-run

echo "== 3) Migrate (apply; default) =="
python "$KLIB_DIR/migrate.py" \
  --project "$DEMO_DIR" \
  --source-version "$SOURCE_COMPILER_VERSION" \
  --target-version "$TARGET_COMPILER_VERSION"

echo "== 4) Gradle build (target compiler version ${TARGET_COMPILER_VERSION}) =="
( cd "$DEMO_DIR" && ./gradlew -PkotlinVersion="$TARGET_COMPILER_VERSION" clean linkDebugSharedOhosArm64 )

echo "OK: klib/test.sh finished"
