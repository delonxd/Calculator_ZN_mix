# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(1000000)

resources = [("src\parameter_pkl", "src\parameter_pkl")]

block_cipher = None


a = Analysis(['MainCalculator_ZN_mix_beta_v01.py'],
             pathex=['D:\\PycharmProjects\\Calculator_ZN_mix'],
             binaries=[],
             datas=resources,
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
          name='邻线干扰单独核算-normal-V1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)
