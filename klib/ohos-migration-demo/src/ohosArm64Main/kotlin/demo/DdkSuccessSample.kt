package demo

import platform.DriverDevelopmentKit.BaseDdk.DDK_SUCCESS

fun ddkSuccessSample() {
    val ret = DDK_SUCCESS
    if (ret.hashCode() == Int.MIN_VALUE) error("unreachable")
}
