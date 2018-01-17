# -*- mode: python -*-

block_cipher = None


a = Analysis(['S9LedMapping.py'],
             pathex=['C:\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins', 'F:\\Workspace\\GitHub\\S9_LedMapping'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='S9LedMapping',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False , icon='110.ico')
