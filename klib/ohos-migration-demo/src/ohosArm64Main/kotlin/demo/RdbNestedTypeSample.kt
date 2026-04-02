package demo

import kotlinx.cinterop.CPointer
import kotlinx.cinterop.IntVar
import kotlinx.cinterop.alloc
import kotlinx.cinterop.memScoped
import kotlinx.cinterop.ptr
import platform.ArkData.RDB.OH_Rdb_GetSupportedDbType
import platform.framework.Rdb_KeyData
import platform.ArkData.RDB.Rdb_KeyInfo

/**
 * KBA: `Rdb_KeyData` is top-level in `platform.framework`. [Rdb_KeyInfo.data] and
 * [OH_Rdb_GetSupportedDbType] are real OH RDB bindings from the same klib.
 *
 * After migrate to CPF, imports move under `platform.ArkData.RDB` and the union type becomes nested
 * (`Rdb_KeyInfo::Rdb_KeyData` / `Rdb_KeyInfo.Rdb_KeyData`); see SCENARIOS.md.
 */
fun rdbNestedTypeSample(data: CPointer<Rdb_KeyData>?) {
    val p = data ?: return
    memScoped {
        val keyInfo = alloc<Rdb_KeyInfo>()
        keyInfo.data = p
        val dbTypeOut = alloc<IntVar>()
        OH_Rdb_GetSupportedDbType(dbTypeOut.ptr)
    }
}
