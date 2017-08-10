import pytest
import expression_checker as ec

def test_is_expression_balanced():
    expression = "$(word $(words $(sources)), $(shell ls /tmp))"
    matchers = ec.is_expression_balanced(expression)
    assert(len(matchers) == 4)
    assert(matchers == [(15, 24), (7, 25), (28, 43), (0, 44)])

    expression = "$(word $(words $(sources)), shell ls /tmp))"
    matchers = ec.is_expression_balanced(expression)
    assert(not matchers)

    expression = "$(var)"
    matchers = ec.is_expression_balanced(expression)
    assert(len(matchers) == 1)
    assert(matchers == [(0,5)])


def test_contains_delimiter():
    expression = "$(word $(words $(sources)), $(shell ls /tmp))"
    matchers = ec.is_expression_balanced(expression)
    assert(matchers)

    delimiters = ec.contains_delimiter(0,44,matchers)
    assert(len(delimiters) == 3)

    delimiters = ec.contains_delimiter(28,43,matchers)
    assert(len(delimiters) == 0)

    delimiters = ec.contains_delimiter(7,25,matchers)
    assert(len(delimiters)>0)

def test_is_variable():
    expression = "$(word $(words $(sources)), $(shell ls /tmp))"
    variable = ec.is_variable(28,43, expression)
    assert(not variable)

    variable = ec.is_variable(15, 24, expression)
    assert(variable)

    expression = "$(word n, text)"
    l = len(expression)
    variable = ec.is_variable(0, l, expression)
    assert(not variable)

    expression = "$(word)"
    l = len(expression)
    variable = ec.is_variable(0, l, expression)
    assert(not variable)

def test_is_builtin_keyword():
    expression = "$(subst ee, EE, feet in the street)"
    l = len(expression)
    result = ec.is_builtin_function(expression)
    assert True == result

    expression = "ln -s $(    subst ee,EE,street)"
    l = len(expression)
    result = ec.is_builtin_function(expression[6:])
    assert True == result

def test_replace_variable():
    expression = " $(var) "
    matchers = ec.is_expression_balanced(expression)
    start = matchers[0][0]
    end = matchers[0][1]
    assert(start == 1)
    assert(end == 6)
    tmp, var, new_exp = ec._replace_variable(start,end,"__0", expression)
    assert(tmp == "__0")
    assert(var == "$(var)")
    assert(new_exp == " __0 ")

    expression = "$(word $(words $(sources)), $(shell ls /tmp))"
    tmp, original, _= ec._replace_variable(15,24,"_1", expression)
    assert(tmp == "_1")
    assert(original == "$(sources)")

    positions = [(15,24)]
    expected = "$(word $(words __0), $(shell ls /tmp))"
    result, subst = ec._replace_variables(positions,expression)
    assert(expected == result)
    assert(len(subst) == 1)

    expression = "this is $(a) $(var)"
    positions = [(8,11), (13,19)]
    expected = "this is __1 __0"
    result, subst = ec._replace_variables(positions,expression)
    assert(expected == result)
    assert(len(subst) == 2)

def test_find_variables_position():
    expression = "$(word $(words $(sources)), $(var2))"
    positions = ec._find_variables_position(expression)
    assert(positions == [(15,24), (28,34)])

    expression = "this has no $(valide value)"
    positions = ec._find_variables_position(expression)
    assert(len(positions) == 0)

def test_find_builtin_function_position():
    expression = "$(word $(words $(sources)), $(var2))"
    positions = ec._find_builtin_function_position(expression)
    assert positions == [(7,25), (0,35)]

def test_find_and_replace_variables():
    expression = "$(word $(words $(sources)), $(var2))"
    expr, map_found = ec.find_and_replace_variables(expression)
    assert(expr == "$(word $(words __1), __0)")

def test_replace_builtin_function():
    expression = "$(subst ee, EE, feet on the street)"
    result = ec._replace_builtin_function(expression)

    expect = ("set(output \"\")\n"
            "string(REPLACE \"ee\" \"EE\" ${output} \"feet on the street\")")
    assert expect == result[0]

