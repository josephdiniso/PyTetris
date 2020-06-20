import cx_Freeze

executables = [cx_Freeze.Executable("game_main.py")]

cx_Freeze.setup(
    name="PyTetris",
    options={"build_exe": {"packages":["pygame", "winsound", ],
                           "include_files":["airtone.mp3", "remove.wav", "dead.wav"]}},
    executables = executables

    )