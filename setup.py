from cx_Freeze import setup, Executable
import sys

build_options = {
    'packages': ['multiprocessing'],
    'excludes': ['tkinter'],
    'includes': ['ServiceHandler', 'cx_Logging'],
    'include_files':['lib/']
}

executables = [Executable('stellwerksimstatus.py', base=None)]
if sys.platform == "win32":
    executables.append(Executable("config.py", base="Win32Service", target_name="cx_FreezeSampleService.exe",))

setup(name='stellwerksimstatus',
      version = '1.0.0',
      description = 'Discord Status for Stellwerksim.de',
      options = {'build_exe': build_options},
      executables = executables)
