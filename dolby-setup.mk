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
# media_codecs_c2.xml is parsed by the framework on every device, whether or
# not a codec list is selected via ro.media.xml_variant.codecs (e.g. QTI SoCs,
# where the plain media_codecs.xml under /vendor/etc is never read). Installing
# only this file avoids clobbering a device's main media_codecs.xml list.
PRODUCT_COPY_FILES += \
    $(DOLBY_PATH)/media/media_codecs_c2.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_c2.xml

# Inherit proprietary targets
$(call inherit-product, $(DOLBY_PATH)/prebuilts/prebuilts-vendor.mk)

# Dolby props
PRODUCT_VENDOR_PROPERTIES += \
    ro.vendor.dolby.dax.version=DAX3_3.7.0.8_r1

# Dolby UI
PRODUCT_PACKAGES += \
	LunarisDolby
