from setuptools import setup, find_packages

setup(
    name = "windows_unix_commands",
    version = "0.0.7",
    description = "hey",
    py_modules=["ls", "locate_file", "change_permisions"], 
    install_requires=[
          'oschmod',
      ],
    entry_points = {
        'console_scripts': [
            'ls = ls:find_files',
            'locate = locate_file:main',
            'chmod = change_permisions:change'
        ],
    }
)