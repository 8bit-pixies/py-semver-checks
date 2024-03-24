"""
Generate unittest runner for function definition generated from ast2dict
"""

from functools import reduce
from typing import Any, List, Tuple

from verger.ast2dict import get_info_by_key_value
from verger.base_test_generator import BaseTestGenerator


class FunctionDefTestGenerator(BaseTestGenerator):
    reference_ast_dict: dict = {}
    target_ask_dict: dict = {}

    def _get_function_def(self, ast_dict: dict) -> List[Tuple[str, List[Any]]]:
        return get_info_by_key_value(ast_dict, "_type", "FunctionDef")

    def _get_canonical_function_name(self, ast_dict: dict, function_def_key: List[str]) -> str:
        module_name_list = []
        for indx in range(1, len(function_def_key) + 1):
            name_part = reduce(dict.get, function_def_key[:indx], ast_dict).get("name")
            if name_part is not None:
                module_name_list.append(name_part)
        return ".".join(module_name_list)

    def _get_function_arguments(self, ast_dict: dict, function_def_key: List[Any]):
        function_node = reduce(dict.get, function_def_key, ast_dict)["args"]
        # go through each type of args and format it nicely so it can be compared, in order
        info = {}
        for arg_type in ["args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults"]:
            arg_type_keys = function_node[arg_type].keys() if function_node.get(arg_type) is not None else None
            if arg_type_keys is None:
                continue

            arg_info_base = [function_node[arg_type][indx] for indx in sorted(arg_type_keys)]
            arg_info = [arg_info["arg"] for arg_info in arg_info_base if arg_info["_type"] == "arg"]
            info[arg_type] = arg_info
        return info

    def test_function_def_canonical_name(self):
        reference_function_def = self._get_function_def(self.reference_ast_dict)
        reference_canonical_names = [
            self._get_canonical_function_name(self.reference_ast_dict, function_def)
            for _, function_def in reference_function_def
        ]
        target_function_def = self._get_function_def(self.target_ask_dict)
        target_canonical_names = [
            self._get_canonical_function_name(self.target_ask_dict, function_def)
            for _, function_def in target_function_def
        ]

        for reference_name in reference_canonical_names:
            with self.subTest(reference_name):
                self.assertTrue(reference_name in target_canonical_names)

        for target_name in target_canonical_names:
            with self.subTest(target_name):
                self.assertTrue(target_name in reference_canonical_names)

    def test_function_def_signature(self):
        # checks that the function signatures are the same
        reference_function_def = self._get_function_def(self.reference_ast_dict)
        reference_function_arg_def = {
            self._get_canonical_function_name(self.reference_ast_dict, function_def): self._get_function_arguments(
                self.reference_ast_dict, function_def
            )
            for _, function_def in reference_function_def
        }
        target_function_def = self._get_function_def(self.target_ask_dict)
        target_function_arg_def = {
            self._get_canonical_function_name(self.target_ask_dict, function_def): self._get_function_arguments(
                self.target_ask_dict, function_def
            )
            for _, function_def in target_function_def
        }

        for reference_name in reference_function_arg_def:
            if reference_name in target_function_arg_def:
                # check the argument names are precisely the same
                reference_info = reference_function_arg_def[reference_name]
                target_info = target_function_arg_def[reference_name]
                for arg_type in ["args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults"]:
                    with self.subTest(f"{reference_name}-{arg_type}"):
                        self.assertListEqual(reference_info["args"], target_info["args"])
