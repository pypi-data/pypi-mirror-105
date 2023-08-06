from calculator import calculator as calc
import pytest


def test_calc_multiple_operations():
    new_calc = calc.Calculator()
    assert new_calc.add(100) == 100
    assert new_calc.divide(2) == 50
    assert new_calc.subtract(23) == 27
    assert new_calc.nth_root(3) == 3
    assert new_calc.multiply(63) == 189


def test_calc_type_error():
    new_calc = calc.Calculator()
    assert new_calc.add(-45) == -45
    with pytest.raises(ValueError):
        new_calc.add("stuff")
    assert new_calc.divide(2) == -22.5


def test_calc_negative_root():
    new_calc = calc.Calculator()
    assert new_calc.subtract(13) == -13
    assert new_calc.multiply(-13) == 169
    assert new_calc.add(87) == 256
    assert new_calc.nth_root(-4) == 0.25


def test_calc_root_of_negative_number():
    new_calc = calc.Calculator()
    assert new_calc.subtract(4) == -4
    assert new_calc.nth_root(3) == 0.7937005259840999+1.3747296369986024j


def test_calc_divide_by_zero_error():
    new_calc = calc.Calculator()
    assert new_calc.add(34) == 34
    assert new_calc.subtract(105) == -71
    with pytest.raises(ZeroDivisionError):
        new_calc.divide(0)
    assert new_calc.divide(71) == -1


def test_calc_floats():
    new_calc = calc.Calculator()
    assert new_calc.add(42) == 42
    assert new_calc.divide(5) == 8.4
    assert new_calc.add(47.08) == 55.48
    assert new_calc.divide(2) == 27.74


def test_calc_reset():
    new_calc = calc.Calculator()
    assert new_calc.subtract(-8) == 8
    assert new_calc.multiply(4) == 32
    assert new_calc.reset() == 0
    assert new_calc.add(99) == 99
    assert new_calc.reset() == 0


def test_calc_strings():
    new_calc = calc.Calculator()
    assert new_calc.subtract(35) == -35
    with pytest.raises(ValueError):
        new_calc.add("4")
