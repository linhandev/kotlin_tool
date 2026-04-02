package demo

import platform.ohos.custom.custom_magic
import platform.ohos.napi_ref
import platform.ohos.napi_value

@Suppress("UNUSED_PARAMETER")
fun mixedImportSample(ref: napi_ref?, valueFromWildcard: napi_value?) {
    val values: MutableList<napi_value?> = mutableListOf(valueFromWildcard)
    val magic = custom_magic()
    // Direct import + wildcard platform imports + custom cinterop platform package.
    if (values.isNotEmpty() && ref != null) values.add(null)
    val sizes: List<Int> = values.map { it?.hashCode() ?: 0 }
    var sum = 0
    for (n in sizes) sum += n
    if (sum == 0 && values.size > 1) error("unexpected")
    if (magic != 42) error("unexpected magic")
}
