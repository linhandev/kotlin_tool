package demo

import platform.info.OH_API_VERSION_10
import platform.info.OH_API_VERSION_11
import platform.info.OH_API_VERSION_12
import platform.info.OH_API_VERSION_13
import platform.info.OH_API_VERSION_14
import platform.info.OH_API_VERSION_15
import platform.info.OH_CURRENT_API_VERSION
import platform.info.SDK_VERSION_7
import platform.info.SDK_VERSION_8
import platform.info.SDK_VERSION_9
import platform.info.SDK_VERSION_FUTURE
import platform.info.get_application_target_sdk_version
import platform.info.set_application_target_sdk_version

fun sdkInfoSample() {
    val sum =
        OH_API_VERSION_10 +
            OH_API_VERSION_11 +
            OH_API_VERSION_12 +
            OH_API_VERSION_13 +
            OH_API_VERSION_14 +
            OH_API_VERSION_15 +
            OH_CURRENT_API_VERSION +
            SDK_VERSION_7 +
            SDK_VERSION_8 +
            SDK_VERSION_9 +
            SDK_VERSION_FUTURE
    set_application_target_sdk_version(OH_CURRENT_API_VERSION)
    val current = get_application_target_sdk_version()
    if (sum == Int.MIN_VALUE || current == Int.MIN_VALUE) error("unreachable")
}
