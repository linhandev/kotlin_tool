from pathlib import Path

sysroot_fdr = Path("/Volumes/disk/cache/konan/dependencies/sysroot-ohos-aarch64-6.0.0.858/usr/")
# sysroot_fdr = Path("/Users/user/Desktop/software/command-line-tools-6.0.0.858/sdk/default/hms/native/sysroot/usr/")
llvm_bin_fdr = Path("/Volumes/disk/cache/konan/dependencies/llvm-19-aarch64-macos-dev-75/bin")
# llvm_bin_fdr = Path("/Users/user/.konan/dependencies/llvm-19-aarch64-macos-dev-75/bin")
out_fdr = Path("/Volumes/disk/work/temp/check_def ")

include_fdr = sysroot_fdr / "include"
binary_fdr = sysroot_fdr / "lib" / "aarch64-linux-ohos"

# info that we know for a fact is wrong so we provide our own
library_info = {
    "database/rdb/oh_values_bucket.h": "libnative_rdb_ndk.z.so",
    "database/rdb/relational_store_error_code.h": "libnative_rdb_ndk.z.so",
    "database/rdb/oh_cursor.h": "libnative_rdb_ndk.z.so",
    "database/rdb/oh_value_object.h": "libnative_rdb_ndk.z.so",
    "database/rdb/relational_store.h": "libnative_rdb_ndk.z.so",
    "database/rdb/oh_predicates.h": "libnative_rdb_ndk.z.so",
    "database/data/data_asset.h": "libnative_rdb_ndk.z.so",
    "syscap_ndk.h": "libdeviceinfo_ndk.z.so",
    "ConnectivityKit/bluetooth/oh_bluetooth.h": "libbluetooth_ndk.so",
    "hilog/log.h": "libhilog_ndk.z.so",
    "accesstoken/ability_access_control.h": "libability_access_control.so",
    "hitrace/trace.h": "libhitrace_ndk.z.so",
    "usb_serial/usb_serial_api.h": "libusb_serial_ndk.z.so",
    "usb_serial/usb_serial_types.h": "libusb_serial_ndk.z.so",
    "multimodalinput/oh_input_manager.h": "libohinput.so",
    "multimodalinput/oh_axis_type.h": "libohinput.so",
    "purgeable_memory/purgeable_memory.h": "libpurgeable_memory_ndk.z.so",
    "multimedia/image_framework/image_pixel_map_napi.h": "libpixelmap_ndk.z.so",
    "multimedia/image_framework/image_pixel_map_mdk.h": "libpixelmap_ndk.z.so",
    "multimedia/drm_framework/native_drm_err.h": "libnative_drm.so",
    "multimedia/drm_framework/native_mediakeysession.h": "libnative_drm.so",
    "multimedia/drm_framework/native_mediakeysystem.h": "libnative_drm.so",
    "multimedia/drm_framework/native_drm_common.h": "libnative_drm.so"
}
group_info = {"syscap_ndk.h": "Init",
"multimedia/image_framework/image/image_source_native.h": "Image_NativeModule",
"multimedia/image_framework/image/image_common.h": "Image_NativeModule",
"multimedia/image_framework/image/image_receiver_native.h": "Image_NativeModule",
"multimedia/image_framework/image/image_packer_native.h": "Image_NativeModule",
"multimedia/image_framework/image/image_native.h": "Image_NativeModule",
"multimedia/image_framework/image/pixelmap_native.h": "Image_NativeModule",
"multimedia/image_framework/image/picture_native.h": "Image_NativeModule"
}
# when specifying headerFilter, some stdlib types can be missing
additional_headers = {"WindowManager": ["cstddef"], "netstack": ["cstdint", "cstddef"]}
additional_compilerOpts = {"TeeTrusted": "-ITEEKit/tee -fpermissive"}