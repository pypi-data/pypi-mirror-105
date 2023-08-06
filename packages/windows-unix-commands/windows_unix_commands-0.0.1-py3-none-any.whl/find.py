def program(arg1):
    for root, dirs, files in os.walk("C:\\"):
        for curr_file in files:
            if curr_file ==  arg:
                print(str(Path(root) / curr_file))
                break


def main():
    import sys
    arg1= sys.argv[1]
    program(arg1)

if __name__ == "__main__":
    main()