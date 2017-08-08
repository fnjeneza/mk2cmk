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

def subst_(subst_expression):
    """Return subst cmake equivalent"""
    expr = """
    set(output "")
    string(REPLACE "{}" "{}" ${output} {})""".format(arg1, arg2, text)
    return expr

def _extract_subst_argument(expression):
    """ extract substring argument from subst expression
        $(subst _1,_2,_3)
    """
    space_position = expression.find(' ')
    first_comma_position = expression.find(',')
    second_comma_position = expression[first_comma_position+1:].find(',') +\
                            first_comma_position
    print(first_comma_position)
    print(second_comma_position)

    from_ = expression[space_position:first_comma_position]
    to_ = expression[first_comma_position+1:second_comma_position+1]
    length = len(expression)
    text = expression[second_comma_position+2:length-1]

    return (from_.strip(), to_.strip(), text.strip())
