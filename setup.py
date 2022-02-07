from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [],
    'excludes': ['tkinter'],
    'include_files':['lib/']
}

import sys
base = 'Win32Service' if sys.platform=='win32' else None
base = None
executables = [
    Executable('stellwerksimstatus.py', base=base)
]

setup(name='stellwerksimstatus',
      version = '1.0.0',
      description = 'Discord Status for Stellwerksim.de',
      options = {'build_exe': build_options},
      executables = executables)
