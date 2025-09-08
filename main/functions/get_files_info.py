import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, directory))
    
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        entries = os.listdir(abs_target)
        lines = []
        for name in entries:
            p = os.path.join(abs_target, name)
            is_dir = os.path.isdir(p)
            size = os.path.getsize(p)
            lines.append(f'- {name}: file_size={size} bytes, is_dir={str(is_dir)}')
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
