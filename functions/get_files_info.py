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
    target_dir = os.path.abspath(working_directory)
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # Check that the `directory` is an actual subdir
    if not os.path.isdir(target_dir):
        return f"Error: {os.path.join(working_directory, directory)} is not a directory"

    # CRITICAL: Ensure the directory is a sub-directory of `working_directory`
    # The AI Agent should NOT be allowed to access files outside of the `working_directory`
    if not target_dir.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list {directory} as it is outside the permitted working directory'
    
    # Compile file metadata
    contents_metadata = ""
    full_path_prefix = os.path.join(working_directory, directory)
    directory_contents = sorted(os.listdir(full_path_prefix))   # Sorted for unit tests

    # Get the size, is_directory status of each item
    # Append into a singular, newline-seperated string
    try:
        for file_or_folder in directory_contents:
            file_or_folder_name = file_or_folder

            file_or_folder_abs_path = os.path.join(full_path_prefix, file_or_folder)
            file_or_folder_size_bytes = os.path.getsize(file_or_folder_abs_path)

            is_dir = not os.path.isfile(file_or_folder)

            contents_metadata += f"- {file_or_folder_name}: file_size={file_or_folder_size_bytes} bytes, is_dir={is_dir}\n"
        return contents_metadata.rstrip()
    except Exception as e:
        return f"Error reading files in {target_dir}: {e}"
