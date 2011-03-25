#!/usr/bin/env python
from cx_Freeze import setup, Executable

exe = Executable(
    script = "simpledbfbrowser.py",
    base = "Win32GUI"
)
setup(
    name = "SimpleDBFBrowser",
    version = "1.0.0-20110326_0036",
    description = "Simple DBF Browser",
    executables = [exe],
    options = {
        "build_exe": {
            "include_files": [
                "resources/logo.png",
                "gtkrc",
                "gpg.exe",
                "iconv.dll",
                ("gtk+_2.22.1-1_win32/share/themes", "share/themes"),
                ("gtk+_2.22.1-1_win32/lib", "lib"),
                ("gtk+_2.22.1-1_win32/etc", "etc"),
            ],
            "icon": "resources/icon.ico"
        }
    }
)
