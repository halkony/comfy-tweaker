# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['./src/comfy_tweaker/gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[('./src/comfy_tweaker/icons', 'icons')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='comfy-tweaker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./src/comfy_tweaker/icons/favicon.ico'  # Set the icon here
)
