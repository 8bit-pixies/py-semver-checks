from verger.ast2dict import copy_dictionary_exclude_keys
from verger.function_def import FunctionDefChecker

LINENO = "lineno"
COLOFFSET = "col_offset"


def function_signatures(current_ast_dict, reference_ast_dict):
    """
    This is designed to check one module (file) against another module (file)
    """

    def format_reference(info):
        return f"{info[LINENO]}:{info[COLOFFSET]}"

    source_file_name = current_ast_dict["_file"]

    current_info = FunctionDefChecker.generate_function_def_signature(current_ast_dict)
    reference_info = FunctionDefChecker.generate_function_def_signature(reference_ast_dict)

    for key in current_info:
        if key not in reference_info:
            yield (
                f"{source_file_name}:{format_reference(current_info[key])}",
                f"FunctionDef {key} does not exist in reference module",
            )

    for key in reference_info:
        if key not in current_info:
            yield (
                f"{source_file_name}:{format_reference(reference_info[key])}",
                f"FunctionDef {key} does not exist in current module",
            )

    # check the reference function definitions are okay
    for key in current_info:
        if key in reference_info:
            if copy_dictionary_exclude_keys(
                current_info[key], ["lineno", "col_offset"]
            ) != copy_dictionary_exclude_keys(reference_info[key], ["lineno", "col_offset"]):
                # TODO get the specific arguments that don't match
                yield (
                    f"{source_file_name}:{format_reference(current_info[key])}",
                    f"FunctionDef {key} arguments differ from reference module",
                )
