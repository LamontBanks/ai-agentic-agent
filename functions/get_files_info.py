import os
from pathlib import Path

def get_files_info(working_directory, directory=None):
    """Returns a string of metadata of files in the directory.

        Will return regular string "error" messages instead of raising formal Errors
        so the AI Agent can process the text and "know" there is an error

        Args:
            working_directory: The base directory
            directory: The sub-directory of working_directory to read

        Returns:
            A string containing metadata for all the files in the directory, or an error message

        Example:
        - Directory contents
        ```
        - README.md: file_size=1032 bytes, is_dir=False
        - src: file_size=128 bytes, is_dir=True
        - package.json: file_size=1234 bytes, is_dir=False
        ```
    """
    
    # Set target directory
    target_dir = os.path.abspath(working_directory)
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # Check that the working_directory + directory is an actual sub dir
    if not os.path.isdir(target_dir):
        return f"Error: {os.path.join(working_directory, directory)} is not a directory"

    # CRITICAL: Ensure the directory is a sub-directory of `working_directory` by checking the file path prefix
    # The AI Agent should NOT be allowed to access files outside of the `working_directory`
    if not target_dir.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list {directory} as it is outside the permitted working directory'
    
    # Compile file metadata
    contents_metadata = ""
    directory_contents = sorted(os.listdir(target_dir))   # Sorted for unit tests

    # Get the size, is_directory status of each item
    # Append into a singular, newline-seperated string
    # try-except in case of file errors
    try:
        for file_or_folder in directory_contents:
            is_dir = not os.path.isfile(file_or_folder)
            file_or_folder_size_bytes = os.path.getsize(os.path.join(target_dir, file_or_folder))

            contents_metadata += f"- {file_or_folder}: file_size={file_or_folder_size_bytes} bytes, is_dir={is_dir}\n"
        return contents_metadata.rstrip()
    except Exception as e:
        return f"Error reading files in {target_dir}: {e}"

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
