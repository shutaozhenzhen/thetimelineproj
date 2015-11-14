from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": ".\\source\\timeline.py",
            "icon_resources": [(1, ".\\icons\\timeline.ico")]
        }
    ],
)
