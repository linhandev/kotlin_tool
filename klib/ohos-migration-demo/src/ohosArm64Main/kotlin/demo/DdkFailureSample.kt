package demo

import platform.devices.DDK_FAILURE

fun ddkFailureSample() {
    val ret = DDK_FAILURE
    if (ret.hashCode() == Int.MIN_VALUE) error("unreachable")
}
