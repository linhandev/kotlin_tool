from pathlib import Path

sysroot_fdr = Path("/Users/user/Desktop/software/command-line-tools-6.0.0.858/sdk/default/openharmony/native/sysroot-ohos-aarch64-6.0.0.858/usr/")
# sysroot_fdr = Path("/Users/user/Desktop/software/command-line-tools-6.0.0.858/sdk/default/hms/native/sysroot/usr/")
llvm_bin_fdr = Path("/Users/user/.konan/dependencies/llvm-19-aarch64-macos-dev-75/bin")

include_fdr = sysroot_fdr / "include"
binary_fdr = sysroot_fdr / "lib" / "aarch64-linux-ohos"
