import sys
import os
from pathlib import Path
import time

def main(args=None):
    """The main routine."""
    file_name = None
    if args is None:
        try:
            file_name = sys.argv[1]
        except Exception:
            print("please specify a file name")
            return 
    import time

    t_end = time.monotonic() + 100
    files_found = False
    for root, dirs, files in os.walk("C:\\"):
        if(files_found and time.monotonic() > t_end):
            return 
        for curr_file in files:
            if curr_file ==  file_name:
                print(str(Path(root) / curr_file))
                files_found= True
                break


