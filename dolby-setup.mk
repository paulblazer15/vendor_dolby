# Product configuration can be parsed before the my-dir helper is defined.
# Capture this file's directory before inheriting any other makefiles.
DOLBY_PATH := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

# SEPolicy
BOARD_VENDOR_SEPOLICY_DIRS += $(DOLBY_PATH)/sepolicy/vendor

# AIDL manifests
DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE += $(DOLBY_PATH)/hidl/dolby_framework_matrix.xml
PRODUCT_PACKAGES += \
	dms-service.xml

# Dolby Audio media codecs (AC3, EAC3, EAC3-JOC, AC4)
PRODUCT_PACKAGES += \
    vendor.dolby.media.c2-default-service-dax.xml
PRODUCT_COPY_FILES += \
    $(DOLBY_PATH)/media/media_codecs_vendor.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs.xml

# Inherit proprietary targets
$(call inherit-product, $(DOLBY_PATH)/prebuilts/prebuilts-vendor.mk)

# Dolby props
PRODUCT_VENDOR_PROPERTIES += \
    ro.vendor.dolby.dax.version=DAX3_3.7.0.8_r1

# Dolby UI
PRODUCT_PACKAGES += \
	LunarisDolby
