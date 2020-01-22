# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['compatibilityCore.py'],
             pathex=['E:\\IBProjects\\ArmorPorts\\LabComparison\\IBConverter'],
             binaries=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             datas=[
					(r"E:\IBProjects\ArmorPorts\LabComparison\IBConverter\icon","./icon"),
					(r"E:\IBProjects\ArmorPorts\LabComparison\IBConverter\Master_MtList_i.mrl3","."),
					],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
		  Tree('E:\IBProjects\ArmorPorts\LabComparison\IBConverter\evxx_resources', "."),
          a.datas,
          [],
          name='Compatibilizer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
		  icon='icon\\DodoSama.ico',
		  )
		  

					
			 