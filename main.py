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

def find_and_replace_variables(line):
    matches = identify_variables(line)
    return convert_variable(line, matches)

def set_variable(name, value):
    """Define an cmake style variable"""
    return "set({0} \"{1}\")".format(name.strip(), value.strip())

def identify_multilines_command():
    """Multilines command ends with a backslash '\'"""
    pass

def identify_multiple_commands():
    """Multiple commands are separated by a semi-colon ';'"""
    pass

def identify_include(line):
    """Include is used to insert a script command in makefile"""
    return line.strip().startswith("include")

def replace_include(line):
    """Replace include expression by a cmake one"""
    len_include = len("include")
    return "include(%s)" % line[len_include:].strip()


def identify_target():
    """check if the line define a target"""
    pass

def identify_ifelse_block():
    """identify if else block"""
    pass

def is_comment(line):
    """Check if the line is a comment"""
    return line.strip().startswith('#')

def is_variable_assignement(line):
    """ Affectation contains '=' or ':='
    If so, return (variable, value)"""

    variable = ""
    value = ""
    symbols = [":=", "::=", "+="]
    for symbol in symbols:
        index = line.find(symbol)
        if(index >= 0):
            variable = line[:index-1]
            value = "${%s} " %variable.strip()
            index = index + len(symbol)
            value += line[index:].strip()
            return (variable, value)

    index = line.find('=')
    if(index >=0):
        if not is_comparison(line):
            variable = line[:index]
            value = line[index+1:]
            return (variable, value)

    return None

def is_conditional_variable_assignement(line):
    variable = ""
    value = ""
    index = line.find("?=")
    if(index >= 0):
        variable = line[:index]
        index = index + 2
        value = line[index:].strip()
        return (variable, value)

    return None

def set_conditional_variable(name, value):
    var_def = set_variable(name, value)
    _line = "if(NOT DEFINED {0})\n {1}\nendif()".format(name.strip(), var_def)
    return _line

def is_comparison(line):
    """ Check if there is comparison symbol"""
    index = line.find("==")
    if(index >= 0):
        return True
    return False

def get_all_system_command():
    """ Retrieve all executable callable by the system"""
    pass

def identify_ifndef(line):
    """ Identify it it is an ifndef block """
    return line.strip().startswith("ifndef")

def replace_ifndef(expression):
    ifndef = "ifndef"
    index = expression.find(ifndef)
    expression = expression[index+len(ifndef):]
    expression = expression.strip()

    return "if(NOT DEFINED {0})".format(expression)

def identify_else(line):
    """ Identify 'else' syntax """
    return line.strip().startswith("else")

def identify_endif(line):
    """ Identify an 'endif' instruction """
    return line.strip().startswith("endif")

def call_tree():
    """Identify all nodes and how they related
    kind of dependency tree"""
    pass

def process_line(line):
    if is_comment(line):
        return line
    line =  find_and_replace_variables(line)
    if identify_include(line):
        return replace_include(line)
    if identify_ifndef(line):
        return replace_ifndef(line)
    if identify_endif(line):
        return "endif()"
    if identify_else(line):
        return "else()"
    cond_assignement = is_conditional_variable_assignement(line)
    if cond_assignement:
        name = cond_assignement[0]
        value = cond_assignement[1]
        return set_conditional_variable(name, value)
    assignement = is_variable_assignement(line)
    if assignement:
        name = assignement[0]
        value = assignement[1]
        return set_variable(name,value)

    return line.strip()

if __name__ == '__main__':
    with open("test.mk") as makefile:
        for line in makefile.readlines():
            line = process_line(line)
            print(line)

    exit()
    print(replace_ifndef("var"))
    print(is_affectation("hello=world"))
    print(is_affectation("hello :=world"))
    print(is_affectation("hello ==world"))
    exit()
    path = sys.argv[1]
    files = locate_all_files(path)
    print(files)
    print(set_variable("CXX_FLAGS", "-Werror"))

    line = "hello $(world) $one"
    matches = identify_variables(line)
    print(matches)
    print(line)
    print(convert_variable(line, matches))


