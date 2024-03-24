from textwrap import dedent

from verger.ast2dict import ast2dict_from_file, ast2dict_from_str, copy_dictionary_exclude_keys
from verger import checker
from verger.function_def import FunctionDefChecker


def test_ref_names():
    simple_code = dedent(
        """
    def add_one(a, b):
        return a+1
    """
    )
    ref_info = FunctionDefChecker.generate_function_def_signature(ast2dict_from_str(simple_code))
    assert copy_dictionary_exclude_keys(ref_info, ["lineno", "col_offset"]) == {
        "add_one": {"args": [{"arg": "a"}, {"arg": "b"}]}
    }


def test_ref_names_from_file(fixture_path):
    ref_info = FunctionDefChecker.generate_function_def_signature(
        ast2dict_from_file(fixture_path.joinpath("simple_code.py.fixture"))
    )
    assert copy_dictionary_exclude_keys(ref_info, ["lineno", "col_offset"]) == {
        "add_one": {"args": [{"arg": "a"}, {"arg": "b"}]}
    }


def test_complex_func():
    complex_types_code = dedent(
        """
    from typing import Callable

    def add_one(a:float, *, b=None, c: int=1, func=Callable[..., int]) -> float:
        test = b'asdf'
        return a+1j
    """
    )
    ref_info = FunctionDefChecker.generate_function_def_signature(ast2dict_from_str(complex_types_code))
    assert copy_dictionary_exclude_keys(ref_info, ["lineno", "col_offset"]) == {
        "add_one": {"args": [{"arg": "a"}], "kwonlyargs": [{"arg": "b"}, {"arg": "c"}, {"arg": "func"}]}
    }


def test_checker_identical():
    simple_code = dedent(
        """
    def add_one(a, b):
        return a+1
    """
    )
    report = list(checker.function_signatures(ast2dict_from_str(simple_code), ast2dict_from_str(simple_code)))
    assert len(report) == 0


def test_checker_miss():
    simple_code = dedent(
        """
    def add_one(a, b):
        return a+1
    """
    )
    simple_code2 = dedent(
        """
    def add_one2(a, b):
        return a+1
    """
    )
    report = list(checker.function_signatures(ast2dict_from_str(simple_code), ast2dict_from_str(simple_code2)))
    assert len(report) == 2