package demo

import platform.devices.DDK_SUCCESS

fun ddkSuccessSample() {
    val ret = DDK_SUCCESS
    if (ret.hashCode() == Int.MIN_VALUE) error("unreachable")
}
