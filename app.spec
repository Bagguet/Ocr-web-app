# app.spec
# -*- mode: python ; -*-

block_cipher = None

a = Analysis(['app.py'],
             pathex=['C:\\Users\\maksy\\Documents\\Programowanie\\Python_Scripts\\TextFromPicture'],
             binaries=[],
             datas=[
                 ('templates', 'templates'),
                 ('tesseract_bin', 'tesseract_bin'),
                 ('tessdata', 'tessdata')
             ],
             hiddenimports=['flask', 'pytesseract', 'Pillow'],
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
          name='OcrWebApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_info=None,
          console=False,
          disable_windowed_mode=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )