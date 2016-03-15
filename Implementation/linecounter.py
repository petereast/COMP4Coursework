# A little script for totalling up the number of lines of code in a directory

import os

def code_list():
    complete_code = []
    total = 0
    dir = os.listdir(os.getcwd())
    for fi in dir:
        if fi[-2:] == "py" and fi not in  ["linecounter.py", "all.py"]:
            with open(fi) as f:
                li = f.readlines()
                c = ["# file - {0} - {1} lines\n".format(fi, len(li))]+li
                complete_code += c
                total += len(li)
                print("Read {0}".format(fi))
    print("".join(complete_code), file=open("all.py", "w"))
    return total
print(code_list(), "Lines of code")
