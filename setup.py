from cx_Freeze import setup, Executable

setup(name="Batch text file word replacer", executables=[Executable("Batch text file word replacer script.py")], options={"build_exe": {"excludes": ["tkinter"]}})
