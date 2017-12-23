# -*- mode: python -*-

block_cipher = None


a = Analysis(['webscrape_cryptocurrency.py'],
             pathex=['C:\\Users\\nelso_8bi0ds3\\Desktop\\webscraping\\cryptocurrency-updater'],
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
          name='webscrape_cryptocurrency',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\nelso_8bi0ds3\\Desktop\\webscraping\\cryptocurrency-updater\\crypto.ico.ico')
