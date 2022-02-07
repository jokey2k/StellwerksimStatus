from cx_Freeze import setup, Executable
import sys

build_options = {
    'packages': ['multiprocessing'],
    'excludes': ['tkinter'],
    'include_files':['lib/']
}

executables = [Executable('stellwerksimstatus.py', base=None)]

setup(name='stellwerksimstatus',
      version = '1.0.0',
      description = 'Discord Status for Stellwerksim.de',
      options = {'build_exe': build_options},
      executables = executables)
