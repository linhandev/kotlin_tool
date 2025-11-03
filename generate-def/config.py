from local_config import sdk_folder, ohos_platform_lib_fdr

from pathlib import Path

# script will be generating def based on headers in sysroots
ohos_sysroot_fdr = Path(sdk_folder) / "default/openharmony/native/sysroot/usr/"
hms_sysroot_fdr = Path(sdk_folder) / "default/hms/native/sysroot/usr/"

# info that we know for fact is wrong so we provide the corrected one
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
    "multimedia/drm_framework/native_drm_common.h": "libnative_drm.so",
}

group_info = {
    "syscap_ndk.h": "Init",
    "multimedia/image_framework/image/image_source_native.h": "Image_NativeModule",
    "multimedia/image_framework/image/image_common.h": "Image_NativeModule",
    "multimedia/image_framework/image/image_receiver_native.h": "Image_NativeModule",
    "multimedia/image_framework/image/image_packer_native.h": "Image_NativeModule",
    "multimedia/image_framework/image/image_native.h": "Image_NativeModule",
    "multimedia/image_framework/image/pixelmap_native.h": "Image_NativeModule",
    "multimedia/image_framework/image/picture_native.h": "Image_NativeModule",
    "arkui/native_render.h": "ArkUI_NativeModule",
    "usb_serial/usb_serial_api.h": "SerialDDK",
    "usb_serial/usb_serial_types.h": "SerialDDK",
    "usb/usb_ddk_api.h": "UsbDDK",
    "usb/usb_ddk_types.h": "UsbDDK",
    "scsi_peripheral/scsi_peripheral_types.h": "SCSIPeripheralDDK",
    "scsi_peripheral/scsi_peripheral_api.h": "SCSIPeripheralDDK",
    "database/preferences/oh_preferences_err_code.h": "Preferences",
    "database/preferences/oh_preferences_option.h": "Preferences",
    "database/preferences/oh_preferences.h": "Preferences",
    "database/preferences/oh_preferences_value.h": "Preferences",
    "window_manager/oh_window_pip.h": "WindowManager",
    "window_manager/oh_display_info.h": "OH_DisplayManager",
    "window_manager/oh_display_capture.h": "OH_DisplayManager",
    "multimedia/native_audio_channel_layout.h": "Core",
    "multimedia/image_framework/image_mdk.h": "Image",
    "multimedia/image_framework/image_source_mdk.h": "Image",
    "multimedia/image_framework/image_pixel_map_napi.h": "Image",
    "multimedia/image_framework/image_receiver_mdk.h": "Image",
    "multimedia/image_framework/image_pixel_map_mdk.h": "Image",
    "multimedia/image_framework/image_mdk_common.h": "Image",
    "multimedia/image_framework/image_packer_mdk.h": "Image",
    "native_buffer/buffer_common.h": "BufferCommon",
}

# when headerFilter is specified, some cpp stdlib types can be missing
additional_headers = {
    "WindowManager": ["cstddef"],
    "netstack": ["cstddef", "cstdint"],
    "ArkUI_NativeModule": ["arkui/ui_input_event.h"], # resolve circular dependency
}
additional_compilerOpts = {}
ohos_platform_lib_fdr = Path(ohos_platform_lib_fdr)