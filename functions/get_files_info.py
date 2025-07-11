import os

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
