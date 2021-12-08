# import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
# base = None
# if sys.platform == "win32":
base = "Win32GUI"

executables = [
    Executable(
        "E:/WEB/_python/space_invader/space_invader.py",
        icon="E:/WEB/_python/flappy_bird/icon.ico",
        base=base,
    ),
    Executable(
        "E:/WEB/_python/space_invader/space_invader_singlemode.py",
        icon="E:/WEB/_python/flappy_bird/icon.ico",
        base=base,
    ),
]

setup(
    name="Space_Invader",
    version="1.0",
    descripton="devloper : Rupesh Anand , last_updated : 3 - 2020",
    options={"build_exe": build_exe_options},
    executables=executables,
)

# python setup.py build
