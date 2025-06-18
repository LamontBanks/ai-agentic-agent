import os
import subprocess

"""Runs the Python file in the given working directory"""
def run_python_file(working_directory, file_path):
    target_python_file = os.path.abspath(os.path.join(working_directory, file_path))

    # CRITICAL: Ensure the file is *not* outside the working directory
    if not target_python_file.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_python_file):
        return f'Error: File "{file_path}" not found.'

    if not target_python_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # Run the file
    try:
        completed_process = subprocess.run(["python3", target_python_file], text=True, cwd=os.path.abspath(working_directory), capture_output=True, timeout=30)
        output = f'STDOUT: {completed_process.stdout}'
        output += f'STDERR: {completed_process.stderr}'

        if completed_process.stderr != 0:
            output += f"Process exited with code {completed_process.stderr}"

        if completed_process.stdout == "":
            return  "No output produced."
        else:
            return output
    except Exception as e:
        return f"Error: executing Python file: {e}"