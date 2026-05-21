# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = []
datas += collect_data_files('customtkinter')
datas += collect_data_files('faster_whisper')
datas += collect_data_files('ctranslate2')
datas += [('image/*', 'image')]
datas += [('audio/*', 'audio')]

hiddenimports = []
hiddenimports += collect_submodules('customtkinter')
hiddenimports += collect_submodules('faster_whisper')
hiddenimports += collect_submodules('ctranslate2')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('pynput')
hiddenimports += ['pyperclip', 'keyboard', 'pyaudio', 'PIL', 'PIL.Image', 'PIL.ImageOps', 'PIL.ImageTk',
                   'pynput', 'pynput.keyboard', 'pynput.keyboard._xorg', 'pynput.keyboard._win32',
                   'pynput.mouse', 'pynput.mouse._xorg', 'pynput.mouse._win32']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LazyAudio',
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
    icon=['image/logodoappicone.ico'],
)
