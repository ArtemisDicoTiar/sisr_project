# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None


a = Analysis(['frontend_ui/src/UI_ProgramSetting.py',
              'frontend_ui/src/components/file_browser.py',
              'frontend_ui/src/components/image_result.py',
              'frontend_ui/src/components/processing.py',
              'backend_api/processor/pre_process/downsampling.py',
              'backend_api/processor/processor/DeepLearningProcessor.py',
              'backend_api/processor/processor/EdgePreserveProcessor.py',
              'backend_api/processor/processor/InterpolationProcessor.py',
              'backend_api/settings/ProgramSetting.py',
              'backend_api/settings/configs/ProgramConfig.py',
             ],
             pathex=['/Users/JohnJongyoonKim/OneDrive - University of Bristol/!Third Year (2021)/project/Codes/sisr_project/src'],
             binaries=[],
             datas=[('frontend_ui/ui/ProcessBar.ui', 'frontend_ui/ui'),
                    ('frontend_ui/ui/ProgramSetting.ui', 'frontend_ui/ui'),
                    ('frontend_ui/ui/result_window.ui', 'frontend_ui/ui'),
                    ('backend_api/settings/configs/config.json', 'backend_api/settings/configs'),
                    ('resource/*','resource')
             ],
             hiddenimports=collect_submodules('tensorflow_core'),
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
          [],
          name='UI_ProgramSetting',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

app = BUNDLE(exe,
         name='myscript.app',
         icon=None,
         bundle_identifier=None)