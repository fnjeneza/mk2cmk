#/bin/env python3

import os
import re
import sys


class node:
    top = []
    bottom = []

def locate_all_files(path):
    """Locate all files with .mk or Makefile"""
    path = os.path.abspath(path)
    # store file found
    files_found = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename[-3:] == ".mk":
                filepath = os.path.join(dirpath, filename)
                files_found.append(filepath)

            if filename == "Makefile":
                filepath = os.path.join(dirpath, filename)
                files_found.append(filepath)

    return files_found

def identify_variables(line):
    """Identify makefile variables
    return a list of tuple (first, last, name) which corresponds to the
    first and last variable position and name of the variable"""

    # list of match tuple
    matches = []
    # macthes $(variable) or $variable
    reg = re.compile('\$\(?(\w+)\)?')
    iterator = reg.finditer(line);
    for match in iterator:
        # start and end position
        start, end = match.span()
        # raw name. Name without deleimiters
        raw_name = match.group()
        # name of  the varialbe
        name = match.group(1)
        # start, name , variable tuple
        matches.append((start,end,raw_name,name))
    return matches

def convert_variable(line, matches):
    """convert all makefile variable style to cmake style
    matches: a list of tuple (start, end, raw_name, name)"""
    for _,_,raw_name,name in matches:
        new_raw_name= "${%s}" % name
        line = line.replace(raw_name, new_raw_name)

    return line

def define_variable(name, value):
    """Define an cmake style variable"""
    return "set({0} \"{1}\")".format(name, value)

def identify_multilines_command():
    """Multilines command ends with a backslash '\'"""
    pass

def identify_multiple_commands():
    """Multiple commands are separated by a semi-colon ';'"""
    pass

def identify_include():
    """Include is used to insert a script command in makefile"""
    pass

def identify_target():
    """check if the line define a target"""
    pass

def identify_ifelse_block():
    """identify if else block"""
    pass

def is_comment(line):
    """Check if the line is a comment"""
    return line.strip().startswith('#')

def get_all_system_command():
    """ Retrieve all executable callable by the system"""
    pass

def identify_ifndef(line):
    """ Identify it it is an ifndef block """
    return line.strip().starswith("ifndef")

def identify_endif(line):
    """ Identify an 'endif' instruction """
    return line.strip().starswith("endif")

def call_tree():
    """Identify all nodes and how they related
    kind of dependency tree"""
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    files = locate_all_files(path)
    print(files)
    print(define_variable("CXX_FLAGS", "-Werror"))

    line = "hello $(world) $one"
    matches = identify_variables(line)
    print(matches)
    print(line)
    print(convert_variable(line, matches))

