
keywords = ["word", "words", "findstring", "strip", "subst", "sort", "dir",
        "suffix", "basename", "addsuffix", "addprefix", "join", "wildcard",
        "realpath", "abspath", "foreach", "file", "call", "value"]

def is_expression_balanced(expression):
    """Check if an expression is balanced
    Return index array(start,end) of sub-expression
    Return None if not balanced
    $(word $(words $(sources)), $(shell ls /tmp)) is balanced"""
    import queue
    _queue = queue.LifoQueue()
    index = 0
    matchers = []
    start = "$("
    end = ')'
    index = 0
    length = len(expression)
    for i in expression:
        if index <= length-2:
            # check if the 2 characters are equal to start
            comp = i+expression[index+1]
            if comp == start:
                # push index if a opening match is found
                _queue.put(index)

        if i == end:
            if _queue.empty():
                return None

            # pop index if a closing match is found
            _ind = _queue.get()
            matchers.append((_ind,index))
        index += 1

    # if queue is empty means the expression is balanced
    if _queue.empty():
        return matchers

    return None

def contains_delimiter(start, end, matchers):
    """Check if the expression contains a delimiter
    e.g $(words $(sources)) contains a delimiter which is $(sources)"""
    assert(start < end)
    assert(len(matchers)>0)

    delimiters = []
    for m in matchers:
        if m[0] > start and m[1] < end:
            delimiters.append((start,end))
    return delimiters

def is_variable(start, end, expression):
    """Check if sub expression in delimiters is a variable
    assume the sub expression does not have delimiters inside"""
    word = expression[start+2:end-1].strip()
    # if contains space => it is not a variable
    if word.find(" ") >= 0:
        return False

    if word in keywords:
        return False
    return True

def find_variables_position(expression):
    """Find all positions that match a value expression"""
    matchers = is_expression_balanced(expression)
    positions = []

    for m in matchers:
        is_var = is_variable(m[0], m[1], expression)
        if is_var:
            positions.append(m)

    return positions

def _replace_variable(start, end, new_variable, expression):
    """Replace a substring at given position in an expression"""
    new_expression = expression[0:start]+new_variable+expression[end:]
    return new_variable, expression[start:end], new_expression

def _replace_variables(positions, expression):
    """Replace multiple variables in an expression"""
    # map which stores temporary variable as key and variable sustituted as
    # value
    variables_subst_map = {}
    # assume that position container is sorted in great order
    exp = expression
    index = 0
    # start by the end
    positions.reverse()
    for pos in positions:
        temp_value = "__%s" % index
        tmp_value, value, exp = _replace_variable(pos[0], pos[1], temp_value, exp)
        variables_subst_map[tmp_value] = value
        index += 1

    return exp, variables_subst_map
