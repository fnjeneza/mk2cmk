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
    # macthes $(variable)
    reg = re.compile('\$\(?\W+\)?')
    iterator = reg.finditer(line);
    for match in iterator:
        matches.append(match.span());
    return matches

def convert_variable(name, value):
    """convert all makefile variable style to cmake style"""
    pass

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

def identify_targets():
    """check if the line define a target"""
    pass

def identify_ifelse_block():
    """identify if else block"""
    pass

def is_comment():
    """Check if the line is a comment"""
    pass

def get_all_system_command():
    """ Retrieve all executable callable by the system"""
    pass

def call_tree():
    """Identify all nodes and how they related
    kind of dependency tree"""
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    files = locate_all_files(path)
    print(files)
    print(define_variable("CXX_FLAGS", "-Werror"))

    line = "hello $(world)"
    print(identify_variables(line))

