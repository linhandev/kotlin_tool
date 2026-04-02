package demo

import platform.posix.ioctl

@OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)
fun ioctlSample() {
    // Exercise the imported variadic C API directly.
    val ret = ioctl(0, 0)
    if (ret == Int.MIN_VALUE) error("unreachable")
}
