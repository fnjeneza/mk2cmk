import os

def _ifeq(arg1, arg2):
    """Return ifeq cmake equivalent"""
    return "if({} EQUAL {})".format(arg1, arg2)

def _ifneq(arg1, arg2):
    """Return ifneq cmake equivalent"""
    return "if({} NOT EQUAL {})".format(arg1, arg2)

def _endif():
    return "endif"

def _basename(args):
    """ return basename of path in args """
    assert(isinstance(args, list))
    basenames = []
    for arg in args:
        filename = os.path.basename(arg).split('.')[0]
        basenames.append(os.path.join(os.path.dirname(arg), filename))

    return basenames
