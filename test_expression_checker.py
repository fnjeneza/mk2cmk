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

def test_replace_variable():
    expression = "$(word $(words $(sources)), $(shell ls /tmp))"
    tmp, original, _= ec._replace_variable(15,25,"_1", expression)
    assert(tmp == "_1")
    assert(original == "$(sources)")

    positions = [(15,24)]
    expected = "$(word $(words __0)), $(shell ls /tmp))"
    result, subst = ec._replace_variables(positions,expression)
    assert(expected == result)
    assert(len(subst) == 1)

    expression = "this is $(a) $(var)"
    positions = [(8,12), (13,19)]
    expected = "this is __1 __0"
    result, subst = ec._replace_variables(positions,expression)
    assert(expected == result)
    assert(len(subst) == 2)

