#!/usr/bin/python

def find_files():
    import os
    files = os.listdir()

    for file in files:
        print(str(file))