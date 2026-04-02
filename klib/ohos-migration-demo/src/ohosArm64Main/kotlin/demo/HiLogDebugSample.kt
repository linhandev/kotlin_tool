package demo

import platform.PerformanceAnalysisKit.HiLog.LOG_DEBUG

fun hiLogDebugSample() {
    val level = LOG_DEBUG
    if (level.hashCode() == Int.MIN_VALUE) error("unreachable")
}
