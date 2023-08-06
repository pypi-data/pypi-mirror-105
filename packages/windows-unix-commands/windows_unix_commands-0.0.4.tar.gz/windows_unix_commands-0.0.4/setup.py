from setuptools import setup, find_packages

setup(
    name = "windows_unix_commands",
    version = "0.0.4",
    description = "hey",
    py_modules=["ls", "locate_file"], 
    entry_points = {
        'console_scripts': [
            'ls = ls:find_files',
            'locate = locate_file:main'
        ],
    }
)