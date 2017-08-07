def basename_():
    """ return basename of path in args """
    assert(isinstance(args, list))
    basenames = []
    for arg in args:
        filename = os.path.basename(arg).split('.')[0]
        basenames.append(os.path.join(os.path.dirname(arg), filename))

    return basenames

def ifeq_(arg1, arg2):
    """ convert ifeq expression
    ifeq (arg1, arg2)
    ifeq 'arg1', 'arg2'
    ifeq "arg1", "arg2"
    ifeq "arg1", 'arg2'
    ifeq 'arg1', "arg2"
    endif
    """
    return "if({} EQUAL {})".format(arg1, arg2)

def ifneq_(arg1, arg2):
    """Return ifneq cmake equivalent"""
    return "if({} NOT EQUAL {})".format(arg1, arg2)

def strip_(arg):
    """ convert strip function """
def ifdef_(arg):
    """ convert ifdef expression """
    pass

def wildcard_(arg):
    pass

def subst_(arg):
    pass
