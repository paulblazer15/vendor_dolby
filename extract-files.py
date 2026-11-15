#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2024-2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
from pathlib import Path
import sys

# Locate the source tree independently of checkout depth and working directory.
SCRIPT_DIR = Path(__file__).resolve().parent
for root in SCRIPT_DIR.parents:
    extract_utils_path = root / 'tools/extract-utils'
    if (extract_utils_path / 'extract_utils').is_dir():
        ANDROID_ROOT = root
        sys.path.insert(0, str(extract_utils_path))
        break
else:
    sys.exit('Cannot find tools/extract-utils in the parent source tree. '
             'Sync tools/extract-utils before running this script.')

DEVICE_REL_PATH = SCRIPT_DIR.relative_to(ANDROID_ROOT).as_posix()
if not DEVICE_REL_PATH.startswith('vendor/'):
    sys.exit('This repository must be checked out under the source tree vendor/ directory.')
VENDOR_SUBDIR = DEVICE_REL_PATH.removeprefix('vendor/')

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    f'{DEVICE_REL_PATH}/prebuilts',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    if partition.startswith('_'):
        partition = partition[1:]  # Remove leading underscore

    if partition not in ('vendor', 'system'):
        return None

    return f'{lib}_{partition}'


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    # (
    # ): lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib64/soundfx/libswdapaidl.so',
        'vendor/lib64/soundfx/libswgamedapaidl.so',
    ): blob_fixup().binary_regex_replace(
        # DlbGenClass2::propIsMatched: mov w0, w19 -> mov w0, #1.
        rb'\x1f\x01\x09\xeb\x41\x01\x00\x54\xe0\x03\x13\x2a\xf4\x4f\x58\xa9\xfc\xab\x40\xf9',
        b'\x1f\x01\x09\xeb\x41\x01\x00\x54\x20\x00\x80\x52\xf4\x4f\x58\xa9\xfc\xab\x40\xf9',
    ),
    'vendor/etc/dolby/dax-default.xml': blob_fixup().regex_replace(
        '<volume-leveler-enable value="true"',
        '<volume-leveler-enable value="false"',
    ),
    'vendor/etc/init/dms-service.rc': blob_fixup().regex_replace(
        r'(    class hal\n)(?!    interface aidl vendor\.dolby\.dms\.IDms/default\n)',
        r'\1    interface aidl vendor.dolby.dms.IDms/default\n',
    ),
}

module = ExtractUtilsModule(
    'prebuilts',
    VENDOR_SUBDIR,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    device_rel_path=DEVICE_REL_PATH,
)

# The constructor derives output paths from the vendor argument. Keep those
# paths, but use the original owner metadata when generating build rules.
module.vendor = 'dolby'

# --- Cleanup Unlisted Blobs ---
PROP_DIR = SCRIPT_DIR / 'prebuilts/proprietary'
PROP_FILES_TXT = SCRIPT_DIR / 'proprietary-files.txt'
PREBUILTS_VENDOR_MK = SCRIPT_DIR / 'prebuilts/prebuilts-vendor.mk'
PREBUILTS_ANDROID_BP = SCRIPT_DIR / 'prebuilts/Android.bp'


def get_expected_files():
    """Read proprietary-files.txt and return a set of expected file paths, ignoring SHA1SUM values and metadata."""
    expected_files = set()

    if not os.path.exists(PROP_FILES_TXT):
        print(f'Warning: {PROP_FILES_TXT} not found.')
        return expected_files

    with open(PROP_FILES_TXT, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Ignore empty lines and comments

            # Extract part before | (to remove SHA1SUM) and before ; (to remove metadata)
            file_paths = line.split('|')[0].split(';')[0]

            # Split multiple paths by ':'
            for path in file_paths.split(':'):
                expected_files.add(
                    path.lstrip('-')
                )  # Remove leading '-' if present

    return expected_files


def cleanup_unlisted_blobs():
    """Remove unlisted blobs from the proprietary folder."""
    if not os.path.exists(PROP_DIR):
        return

    expected_files = get_expected_files()

    for root, _, files in os.walk(PROP_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, PROP_DIR)

            # Ignore .part files silently
            if '.part' in file:
                continue

            if rel_path not in expected_files:
                print(f'Removing unlisted blob: {file_path}')
                os.remove(file_path)



def patch_generated_makefiles():
    """Apply local makefile tweaks not expressible in proprietary-files.txt."""
    if os.path.exists(PREBUILTS_ANDROID_BP):
        with open(PREBUILTS_ANDROID_BP, 'r', encoding='utf-8') as f:
            data = f.read()

        data = data.replace(
            '                "libaudio_aidl_conversion_common_ndk",\n',
            '',
        )

        with open(PREBUILTS_ANDROID_BP, 'w', encoding='utf-8') as f:
            f.write(data)

    if not os.path.exists(PREBUILTS_VENDOR_MK):
        return

    with open(PREBUILTS_VENDOR_MK, 'r', encoding='utf-8') as f:
        data = f.read()

    if 'libaudio_aidl_conversion_common_ndk' not in data:
        anchor = '    libdlbvolaidl \\\n'
        replacement = anchor + '    libaudio_aidl_conversion_common_ndk \\\n'
        if anchor not in data:
            raise RuntimeError(
                f'Failed to patch {PREBUILTS_VENDOR_MK}: missing libdlbvolaidl anchor'
            )
        data = data.replace(anchor, replacement, 1)

    with open(PREBUILTS_VENDOR_MK, 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
    patch_generated_makefiles()
    cleanup_unlisted_blobs()  # Run cleanup after extraction
