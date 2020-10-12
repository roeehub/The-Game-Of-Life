import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
    script="The Game Of Life.py",
    icon="assets/virus_red.ico"
    )


setup(  name = "The Game Of Life",
        version = "0.1",
        description = "Conway's Game Of Life",
        options = {"build_exe": build_exe_options},
        executables = [Executable("The Game Of Life.py", base=base), target])
