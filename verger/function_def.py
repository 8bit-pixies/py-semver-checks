"""
Generate unittest runner for function definition generated from ast2dict
"""

from functools import reduce
from typing import Any, Dict, List, Tuple

from verger.ast2dict import get_info_by_key_value


class FunctionDefChecker:
    @classmethod
    def _get_function_def(cls, ast_dict: dict) -> List[Tuple[str, List[Any]]]:
        return get_info_by_key_value(ast_dict, "_type", "FunctionDef")

    @classmethod
    def _get_canonical_function_name(cls, ast_dict: dict, function_def_key: List[str]) -> str:
        module_name_list = []
        for indx in range(1, len(function_def_key) + 1):
            name_part = reduce(dict.get, function_def_key[:indx], ast_dict).get("name")
            if name_part is not None:
                module_name_list.append(name_part)
        return ".".join(module_name_list)

    @classmethod
    def _get_function_arguments(cls, ast_dict: dict, function_def_key: List[Any]):
        def _build_info(info_dict):
            return {key: value for key, value in info_dict.items() if key in ["arg", "lineno", "col_offset"]}

        function_node = reduce(dict.get, function_def_key, ast_dict)
        function_node_args = function_node["args"]
        # go through each type of args and format it nicely so it can be compared, in order
        info = {"lineno": function_node["lineno"], "col_offset": function_node["col_offset"]}
        for arg_type in ["args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults"]:
            arg_type_keys = (
                function_node_args[arg_type].keys() if function_node_args.get(arg_type) is not None else None
            )
            if arg_type_keys is None:
                continue
            arg_info_base = [function_node_args[arg_type][indx] for indx in sorted(arg_type_keys)]
            arg_info = [_build_info(arg_info) for arg_info in arg_info_base if arg_info["_type"] == "arg"]
            if len(arg_info) > 0:
                info[arg_type] = arg_info
        return info

    @classmethod
    def generate_function_def_signature(cls, ast_dict: dict) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """
        ```
        def add_one(a, b):
            return a+1
        ```
        Generates --> {"add_one": {"args": [{"arg": "a", ...}, {"arg": "b", ...}]}}
        """
        function_def = cls._get_function_def(ast_dict)
        return {
            cls._get_canonical_function_name(ast_dict, function_def): cls._get_function_arguments(
                ast_dict, function_def
            )
            for _, function_def in function_def
        }
