package demo

import platform.ohos.napi_env
import platform.ohos.napi_value

fun wildcardImportSample(env: napi_env?, value: napi_value?) {
    val tag = (env?.hashCode() ?: 0) xor (value?.hashCode() ?: 0)
    if (tag == Int.MIN_VALUE) error("unreachable")
}
