package demo

import kotlinx.cinterop.CPointer
import kotlinx.cinterop.IntVar
import kotlinx.cinterop.alloc
import kotlinx.cinterop.memScoped
import kotlinx.cinterop.ptr
import platform.framework.OH_Rdb_GetSupportedDbType
import platform.framework.Rdb_KeyData
import platform.framework.Rdb_KeyInfo

/**
 * Same nested-type migration pattern as [rdbNestedTypeSample], but keeps both the flat union import
 * and [Rdb_KeyInfo] in one file so migration produces **one** backtick import plus **one** typealias
 * after the last `import` (see SCENARIOS.md scenario 5).
 */
fun rdbNestedMultiImportSample(data: CPointer<Rdb_KeyData>?) {
    val p = data ?: return
    memScoped {
        val info = alloc<Rdb_KeyInfo>()
        info.data = p
        val out = alloc<IntVar>()
        OH_Rdb_GetSupportedDbType(out.ptr)
    }
}
