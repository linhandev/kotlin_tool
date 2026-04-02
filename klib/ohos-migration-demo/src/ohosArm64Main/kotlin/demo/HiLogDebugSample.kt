package demo

import platform.ohos.LOG_DEBUG

fun hiLogDebugSample() {
    val level = LOG_DEBUG
    if (level.hashCode() == Int.MIN_VALUE) error("unreachable")
}
