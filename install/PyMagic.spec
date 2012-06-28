# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '../gui.py', '../plugins/exporters/mac_pkg/__init__.py'],
             pathex=['/Users/john/src/pymagic/install'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/PyMagic', 'PyMagic'),
          debug=False,
          strip=False,
          upx=False,
          console=1 )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name=os.path.join('dist', 'PyMagic'))
import sys
if sys.platform.startswith("darwin"):
        app = BUNDLE(exe, appname='PyMagic', version='1.0')

