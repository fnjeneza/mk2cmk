import pytest
import builtin_functions_converter as fc


def test_extract_subst_argument():
    text = "$(subst ee, EE, feet on the street)"
    _from, _to, _text = fc._extract_subst_argument(text)
    assert("ee" == _from)
    assert "EE" == _to
    assert "feet on the street" == _text

    text = "$(subst __1, __2, __3)"
    _from, _to, _text = fc._extract_subst_argument(text)
    assert "__1" == _from
    assert "__2" == _to
    assert "__3" == _text