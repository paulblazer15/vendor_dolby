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

## Clone the Repository

Clone the Dolby vendor repository into your source tree:

```bash
git clone https://github.com/paulblazer15/vendor_dolby.git vendor/dolby
```

---

## Device Tree Integration

For a checkout at `vendor/sony/dolby`, use that path instead of
`vendor/dolby` in the inherit-product line below.

Inherit Dolby Atmos in your device configuration:

```makefile
$(call inherit-product, vendor/dolby/dolby-setup.mk)
```

---

## Extracting Blobs

The repository must be inside your Android source tree under `vendor/`, with
the tree's `tools/extract-utils` checked out. The script locates it relative
to its own location, including nested paths such as `vendor/sony/dolby`.

From this repository, run:

```bash
./extract-files.py /home/paul/Downloads/Sony_Xperia_1_VII_XQ-FS54_dump
```

When intentionally updating to a different dump, add `--kang` to replace the
pinned blobs and update their hashes. Extraction regenerates the build files
for the current checkout path and reapplies the local DMS init and volume
leveler changes. Keep manually maintained build definitions outside `prebuilts/`,
which the extractor regenerates.

---

## Audio Effects Configuration

Add the following entries to your `audio_effects.xml`.

### Load the Libraries

```xml
<library name="dap" path="libswdapaidl.so"/>
<library name="dvl" path="libdlbvolaidl.so"/>
<library name="gamedap" path="libswgamedapaidl.so"/>
```

### Load the Effects

```xml
<effect name="dap" library="dap" uuid="9d4921da-8225-4f29-aefa-39537a04bcaa" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_music_listener" library="dvl" uuid="40f66c8b-5aa5-4345-8919-53ec431aaa98" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_ring_listener" library="dvl" uuid="21d14087-558a-4f21-94a9-5002dce64bce" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_alarm_listener" library="dvl" uuid="6aff229c-30c6-4cc8-9957-dbfe5c1bd7f6" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="dlb_notification_listener" library="dvl" uuid="1f0091e3-6ad8-40fe-9b09-5948f9a26e7e" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
<effect name="gamedap" library="gamedap" uuid="3783c334-d3a0-4d13-874f-0032e5fb80e2" type="fa81de0e-588b-11ed-9b6a-0242ac120002"/>
```

---

## Dolby Codec Support

This repository includes **Dolby Audio codecs** unconditionally.

<div align="center">

**Supported Codecs**

AC3 • EAC3 • EAC3-JOC • AC4

> Dolby Audio media codecs require Android 15 or later. Binaries for Android versions below 15 are not compatible.

</div>

---

## Credits

* [Dolby Laboratories](https://www.dolby.com/en-in/)
