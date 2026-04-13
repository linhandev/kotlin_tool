from pathlib import Path

MIGRATING_PROJECT = "/Users/ohoskt/git/ci/kotlinx-coroutines"
SOURCE_SET_NAMES = ["ohosMain", "ohosArm64Main", "ohosX64Main", "nativeOhos"]
SOURCE_COMPILER_VERSION = "2.0.21-KBA-014"
TARGET_COMPILER_VERSION = "2.2.21-0.2.0-01"

''' used for maping generation only '''
KLIB = f"~/.konan/kotlin-native-prebuilt-macos-aarch64-{TARGET_COMPILER_VERSION}/bin/klib"
SOURCE_KLIBS = f"~/.konan/kotlin-native-prebuilt-macos-aarch64-{SOURCE_COMPILER_VERSION}/klib/platform/ohos_arm64"
SOURCE_SYSROOT = "/Applications/DevEco-Studio-5.0.11.110.app/Contents/sdk/default/openharmony/native/sysroot"
TARGET_KLIBS = f"~/.konan/kotlin-native-prebuilt-macos-aarch64-{TARGET_COMPILER_VERSION}/klib/platform/ohos_arm64"
# use universal Ctags
CTAGS_BIN = "ctags"
HARDCODED_SOURCE_FQNAME_TO_TARGET_FQNAME: dict[str, str] = {
    "platform.ohos.LOG_DEBUG": "platform.PerformanceAnalysisKit.HiLog.LOG_DEBUG",
    "platform.ohos.LOG_INFO": "platform.PerformanceAnalysisKit.HiLog.LOG_INFO",
    "platform.devices.DDK_Ashmem": "platform.DriverDevelopmentKit.BaseDdk.DDK_Ashmem",
    "platform.devices.DDK_FAILURE": "platform.DriverDevelopmentKit.BaseDdk.DDK_FAILURE",
    "platform.devices.DDK_INVALID_OPERATION": "platform.DriverDevelopmentKit.BaseDdk.DDK_INVALID_OPERATION",
    "platform.devices.DDK_INVALID_PARAMETER": "platform.DriverDevelopmentKit.BaseDdk.DDK_INVALID_PARAMETER",
    "platform.devices.DDK_NULL_PTR": "platform.DriverDevelopmentKit.BaseDdk.DDK_NULL_PTR",
    "platform.devices.DDK_RetCodeVar": "platform.DriverDevelopmentKit.BaseDdk.DDK_RetCodeVar",
    "platform.devices.DDK_RetCode": "platform.DriverDevelopmentKit.BaseDdk.DDK_RetCode",
    "platform.devices.DDK_SUCCESS": "platform.DriverDevelopmentKit.BaseDdk.DDK_SUCCESS",
    "platform.ohos.ioctl": "platform.posix.ioctl",
    "platform.ohos.get_application_target_sdk_version": "platform.info.get_application_target_sdk_version",
    "platform.ohos.OH_API_VERSION_10": "platform.info.OH_API_VERSION_10",
    "platform.ohos.OH_API_VERSION_11": "platform.info.OH_API_VERSION_11",
    "platform.ohos.OH_API_VERSION_12": "platform.info.OH_API_VERSION_12",
    "platform.ohos.OH_API_VERSION_13": "platform.info.OH_API_VERSION_13",
    "platform.ohos.OH_API_VERSION_14": "platform.info.OH_API_VERSION_14",
    "platform.ohos.OH_API_VERSION_15": "platform.info.OH_API_VERSION_15",
    "platform.ohos.OH_CURRENT_API_VERSION": "platform.info.OH_CURRENT_API_VERSION",
    "platform.ohos.SDK_VERSION_7": "platform.info.SDK_VERSION_7",
    "platform.ohos.SDK_VERSION_8": "platform.info.SDK_VERSION_8",
    "platform.ohos.SDK_VERSION_9": "platform.info.SDK_VERSION_9",
    "platform.ohos.SDK_VERSION_FUTURE": "platform.info.SDK_VERSION_FUTURE",
    "platform.ohos.set_application_target_sdk_version": "platform.info.set_application_target_sdk_version",
    "platform.ohos.htonl": "platform.posix.htonl",
    "platform.ohos.htons": "platform.posix.htons",
    "platform.ohos.ntohl": "platform.posix.ntohl",
    "platform.ohos.ntohs": "platform.posix.ntohs",
    "platform.ohos.INET6_ADDRSTRLEN": "platform.posix.INET6_ADDRSTRLEN",
    "platform.ohos.INET_ADDRSTRLEN": "platform.posix.INET_ADDRSTRLEN",
}

# process configs
KLIB_DIR = Path(__file__).resolve().parent
MIGRATING_PROJECT = Path(MIGRATING_PROJECT)
KLIB = Path(KLIB).expanduser()
SOURCE_KLIBS = Path(SOURCE_KLIBS).expanduser()
TARGET_KLIBS = Path(TARGET_KLIBS).expanduser()
IOS_KLIBS = TARGET_KLIBS.parent / "ios_arm64"
SOURCE_SYSROOT = Path(SOURCE_SYSROOT).expanduser() if SOURCE_SYSROOT.strip() else None
# ``mapping.py`` writes ``mapping-{SOURCE_COMPILER_VERSION}-to-{TARGET_COMPILER_VERSION}.csv`` here.
MAPPING_CSV = (
    KLIB_DIR
    / "mappings"
    / f"mapping-{SOURCE_COMPILER_VERSION}-to-{TARGET_COMPILER_VERSION}.csv"
)
