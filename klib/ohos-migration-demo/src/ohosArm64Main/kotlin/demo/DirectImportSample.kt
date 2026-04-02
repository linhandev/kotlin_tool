package demo

import platform.ohos.custom.custom_magic
import platform.ArkTS.ArkTS_Napi_NativeModule.napi_env
import platform.ArkTS.ArkTS_Napi_NativeModule.napi_value

@Suppress("UNUSED_PARAMETER")
fun directImportSample(env: napi_env?, value: napi_value?) {
    val magic = custom_magic()
    if (magic != 42) error("unexpected magic")
}
