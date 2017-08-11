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

def test_subst_():
    text = "$(subst ee, EE, feet on the street)"
    result, var = fc.subst_(text)

    expect = ("set(output \"\")\n"
            "string(REPLACE \"ee\" \"EE\" ${output} \"feet on the street\")")
    assert expect == result
    assert "${output}" == var

def test_strip_():
    text = "$(strip text to strip)"
    result, var = fc.strip_(text)

    assert "string(STRIP \"text to strip\" ${output})" == result
    assert "${output}" == var
