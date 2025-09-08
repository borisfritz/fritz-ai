import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_target.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    directory = os.path.dirname(abs_target)

    try:    
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(abs_target, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file inside the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Write or overwrite to a the file inside the working directory",
            ),
        },
        required=["file_path", "content"],
    ),
)
