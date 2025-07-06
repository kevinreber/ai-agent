import subprocess
import os
from google.genai import types


TIMEOUT = 30


def _verify_file_path(working_directory: str, file_path: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found'
    if not abs_file_path.endswith(".py"):
        return f'Error: Cannot run "{file_path}" as it is not a Python file'
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside'
    if not os.path.isdir(abs_working_dir):
        return f'Error: Working directory "{working_directory}" is not a directory'
    return ''

def run_python_file(working_directory, file_path, args=None):
    error_message = _verify_file_path(working_directory, file_path)
    if error_message:
        return error_message
    
    try:
        commands = ["python", file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True, # Capture both stdout and stderr
            text=True, # Return strings instead of bytes
            timeout=TIMEOUT,
            cwd=working_directory,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"


SCHEMA_RUN_PYTHON_FILE = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)