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




