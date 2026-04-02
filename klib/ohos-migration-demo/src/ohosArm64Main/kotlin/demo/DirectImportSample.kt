package demo

import platform.ohos.custom.custom_magic
import platform.ohos.napi_env
import platform.ohos.napi_value

@Suppress("UNUSED_PARAMETER")
fun directImportSample(env: napi_env?, value: napi_value?) {
    val magic = custom_magic()
    if (magic != 42) error("unexpected magic")
}
