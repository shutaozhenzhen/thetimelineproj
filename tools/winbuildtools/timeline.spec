# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['../../source/timeline.py'],
             pathex=['C:\\Projects\\Timeline\\thetimelineproj-py3\\source'],
             binaries=[],
             datas= [ ('../../icons/*.png', 'icons' ), 
                      ('../../icons/event_icons/*.png', 'icons/event_icons' ),
                      ('../../translations', 'translations' )],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='timeline',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, 
          icon='../../icons/timeline.ico' )