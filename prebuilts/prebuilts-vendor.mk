#
# Automatically generated file. DO NOT MODIFY
#

PRODUCT_SOONG_NAMESPACES += \
    vendor/dolby/prebuilts

PRODUCT_COPY_FILES += \
    vendor/dolby/prebuilts/proprietary/vendor/etc/dolby/dax-default.xml:$(TARGET_COPY_OUT_VENDOR)/etc/dolby/dax-default.xml \
    vendor/dolby/prebuilts/proprietary/vendor/etc/init/dms-service.rc:$(TARGET_COPY_OUT_VENDOR)/etc/init/dms-service.rc \
    vendor/dolby/prebuilts/proprietary/vendor/etc/init/vendor.dolby.media.c2-default-service-dax.rc:$(TARGET_COPY_OUT_VENDOR)/etc/init/vendor.dolby.media.c2-default-service-dax.rc \
    vendor/dolby/prebuilts/proprietary/vendor/etc/media_codecs_dolby_audio.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_dolby_audio.xml

PRODUCT_PACKAGES += \
    c2.dolby.store \
    libcodec2_soft_ac4dec \
    libcodec2_soft_ddpdec \
    libcodec2_store_dolby \
    libdapparamstorage \
    libdeccfg \
    libdlbdsservice \
    libdlbpreg \
    libdmshal \
    libdlbvolaidl \
    libaudio_aidl_conversion_common_ndk \
    libswdapaidl \
    libswgamedapaidl \
    vendor.dolby.dms-V1-ndk \
    vendor.dolby.hardware.dms@2.0 \
    vendor.dolby.dms.service \
    vendor.dolby.media.c2-default-service-dax
