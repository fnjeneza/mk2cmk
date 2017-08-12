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

def ifdef_(arg):
    """ convert ifdef expression """
    pass

def wildcard_(arg):
    pass

def subst_(expression):
    """Return subst cmake equivalent"""
    _from, _to, _text = _extract_subst_argument(expression)
    output_var = "${output}"
    expr = ("set(output \"\")\n"
            "string(REPLACE \"{}\" \"{}\" {} \"{}\")".format(_from,
                                                             _to,
                                                             output_var,
                                                             _text))
    return expr, output_var

def _extract_subst_argument(expression):
    """ extract substring argument from subst expression
        $(subst _1, _2, _3)
        $(subst ee, EE, feet on the street)
        return _1, _2, _3
    """
    import re
    reg = re.compile("\$\( *subst +(\w+), *(\w+), *([ \w]+) *\)")
    index = reg.search(expression)
    return index.group(1), index.group(2), index.group(3)

def strip_(expression):
    """Return a cmake strip equivqlent"""
    key = "strip"
    # extract argument
    expression = expression[2:].lstrip()
    index = expression.find(key)

    if index != 0:
        return None

    expression = expression[index+len(key):len(expression)-1].strip()
    output_var =  "${output}"
    expr = "string(STRIP \"{}\" {})".format(expression, output_var)
    return expr, output_var

def filter_out_(expression):
    """Return a cmake filter-out equivalent"""
    key = "filter-out"
    #extract argument
    expression = expression[2:].lstrip()
    index = expression.find(key)

    if index != 0:
        return None

    expression = expression[index+len(key):len(expression)-1].strip()
    comma = expression.find(',')
    lhs = expression[:comma]
    rhs = expression[comma+1:]
    var = "${var}"

    expr = ("foreach(var IN {})\n"
            "  list(REMOVE_ITEM {} {})\n"
            "endforeach(var)".format(var, rhs, lhs))

    return expr

def word_(expression):
