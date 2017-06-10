#/bin/env python3

import os
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


def convert_variables():
    """convert all makefile variable style to cmake style"""
    pass

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

def set_variables():
    """set variables using cmake style """
    pass

def call_tree():
    """Identify all nodes and how they related
    kind of dependency tree"""
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    files = locate_all_files(path)
    print(files)

