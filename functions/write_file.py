import os

"""Writes content to the given file"""
def write_file(working_directory, file_path, content):
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    # CRITICAL: Ensure the file is *not* outside the working directory
    if not target_file.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    

    # Overwrite the existing file (or create a new file)
    try:
        # "w" overwrites, creating the file if needed
        with open(target_file, mode="w") as f:
            print(content, file=f)
    except Exception as e:
        return f'ERROR: Unable to write/create the file {target_file}: {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
