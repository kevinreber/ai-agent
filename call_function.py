from google.genai import types
from functions.get_files_info import SCHEMA_GET_FILES_INFO, get_files_info
from functions.get_file_content import SCHEMA_GET_FILE_CONTENT, get_file_content
from functions.run_python_file import SCHEMA_RUN_PYTHON_FILE, run_python_file
from functions.write_file_content import SCHEMA_WRITE_FILE, write_file
from config import WORKING_DIR


AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[
        SCHEMA_GET_FILES_INFO,
        SCHEMA_GET_FILE_CONTENT,
        SCHEMA_RUN_PYTHON_FILE,
        SCHEMA_WRITE_FILE,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )