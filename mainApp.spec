# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mainApp.py'],
             pathex=['D:\\PythonBranch\\PyLocal_master\\autoTest'],
             binaries=[],
             datas=[('app_src/templates', 'app_src/templates'), ('app_src/static', 'app_src/static'), ('app_src/sqliteDB', 'app_src/sqliteDB')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy', 'scipy', 'matplotlib'],
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
          name='mainApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='docs\\coverIcon.ico')
