import os
from pathlib import Path

"""Reads the first 10000 characters of the given file."""
def get_file_content(working_directory, file_path):
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    # CRITICAL: Ensure the directory is a sub-directory of `working_directory` by checking the file path prefix
    # The AI Agent should NOT be allowed to access files outside of the `working_directory`
    if not target_file.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read {file_path} as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: {file_path}'
    
    # Read file
    contents = ""
    MAX_CHARS = 10000
    truncate = False

    try:
        p = Path(target_file)

        # Set truncate flag
        if os.path.getsize(target_file) > MAX_CHARS:
            truncate = True

        with p.open() as f:
            contents = f.read(MAX_CHARS)

         # Truncate to 10000 characters, print message if needed
        if truncate:
            contents += f'\n[...File "{file_path}" truncated at 10000 characters]'
            return contents
        
        return contents
    except Exception as e:
        return f'Error: Cannot read {target_file}: {e}'
