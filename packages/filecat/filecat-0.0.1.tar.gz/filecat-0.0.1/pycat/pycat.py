import sys


def cat_files(files):
    for file in files:
        print("-- Printing contents of {file} --".format(file=file))
        for line in open(file, 'r'):
            print(line)


def cat_files_main():
    if len(sys.argv) == 1:
        print("Please provide file names!")
    else:
        cat_files(sys.argv[1:])
