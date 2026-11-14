<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/DLB_Atms_UI_rgb_wht_@2x.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/DLB_Atms_UI_rgb_blk_@2x.png">
    <img alt="Dolby Atmos" src="assets/DLB_Atms_UI_rgb_blk_@2x.png" width="260">
  </picture>

  <br>
  <br>
  
  Bring Dolby EQ & Dolby Audio codec support to your Android build.
</div>

---

Dolby Atmos from the Sony with LunarisDolby
settings app and AC3 • EAC3 • EAC3-JOC • AC4 codecs.

## Setup

Clone into your source tree:

```bash
git clone -b 17 https://github.com/paulblazer15/vendor_sony_dolby.git vendor/sony/dolby
```

Inherit it in your device configuration:

```makefile
$(call inherit-product, vendor/sony/dolby/dolby-setup.mk)
```

## Audio Effects

Add these to your `audio_effects_config.xml`.

Libraries:

```xml
<!-- DOLBY START -->
<library name="dap" path="libswdapaidl.so"/>
<library name="dvl" path="libdlbvolaidl.so"/>
<library name="gamedap" path="libswgamedapaidl.so"/>
<!-- DOLBY END -->
```

Effects:

```xml
<!-- DOLBY START -->
<effect name="dap" library="dap" uuid="9d4921da-8225-4f29-aefa-39537a04bcaa" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_music_listener" library="dvl" uuid="40f66c8b-5aa5-4345-8919-53ec431aaa98" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_ring_listener" library="dvl" uuid="21d14087-558a-4f21-94a9-5002dce64bce" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_alarm_listener" library="dvl" uuid="6aff229c-30c6-4cc8-9957-dbfe5c1bd7f6" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_notification_listener" library="dvl" uuid="1f0091e3-6ad8-40fe-9b09-5948f9a26e7e" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="gamedap" library="gamedap" uuid="3783c334-d3a0-4d13-874f-0032e5fb80e2" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<!-- DOLBY END -->
```

## Updating Blobs

With `tools/extract-utils` synced, run from this repository:

```bash
./extract-files.py <path-to-firmware-dump>
```

## Credits

* [Dolby Laboratories](https://www.dolby.com/en-in/)
* [Ghosuto/hardware_dolby](https://github.com/Ghosuto/hardware_dolby) for LunarisDolby
