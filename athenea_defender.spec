# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['athenea_defender.py'],
    pathex=[],
    binaries=[],
    datas=[('Bauhaus93.ttf', '.'), ('athenea_idle1.png', '.'), ('athenea_idle2.png', '.'), ('athenea_alert.png', '.'), ('athenea_sleep.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='athenea_defender',
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
    icon=['athenea.ico'],
)
