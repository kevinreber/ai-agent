import subprocess
import os

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
        # Run the Python file with proper configuration
        result = subprocess.run(
            commands,
            capture_output=True, # Capture both stdout and stderr
            text=True, # Return strings instead of bytes
            timeout=TIMEOUT,
            cwd=working_directory,
        )
        # Build the output string
        output_parts = []
        
        # Add stdout if present
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        
        # Add stderr if present
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        
        # Add exit code information if non-zero
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        # Return formatted output or "No output produced" message
        if output_parts:
            return "\n".join(output_parts)
        else:
            return "No output produced."
            
    except subprocess.TimeoutExpired:
        return f'Error: executing Python file: Timeout after {TIMEOUT} seconds'
    except subprocess.CalledProcessError as e:
        return f'Error: executing Python file: {e}'
    except Exception as e:
        return f'Error: executing Python file: {e}'