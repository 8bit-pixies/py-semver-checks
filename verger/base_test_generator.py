"""
Generate unittest runner for function definition generated from ast2dict
"""

import json
import unittest

from verger.ast2dict import ast2dict_from_file


class BaseTestGenerator(unittest.TestCase):
    reference_ast_dict: dict = {}
    target_ask_dict: dict = {}

    @classmethod
    def from_reference_ast_dict(cls, ast_dict):
        cls.reference_ast_dict = ast_dict
        metadata = json.loads(ast_dict.get("_metadata", "{}"))
        file_name = metadata.get("file")
        cls.target_ask_dict = ast2dict_from_file(file_name) if file_name is not None else {}
        if file_name is not None:
            file_name = file_name.replace(".py", "")
            file_name = file_name.replace("/", "_")
            cls.__name__ = f"Test{file_name}"
        return cls
