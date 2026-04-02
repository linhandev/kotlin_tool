package demo

import platform.DriverDevelopmentKit.BaseDdk.DDK_FAILURE

fun ddkFailureSample() {
    val ret = DDK_FAILURE
    if (ret.hashCode() == Int.MIN_VALUE) error("unreachable")
}
