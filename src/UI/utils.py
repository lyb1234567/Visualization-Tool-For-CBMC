import os
import time 
def extract_file_name(file_address):
    file_name = os.path.basename(file_address)
    return file_name

def extract_file_name_without_extension(file_address):
    base_name = os.path.basename(file_address) # Extract the file name (with extension) from the file path
    file_name_without_extension = os.path.splitext(base_name)[0] # Remove the extension from the file name
    return file_name_without_extension

def check_file_exists(filename):
    return os.path.isfile(filename)

def extract_command(input_string):
    split_string = input_string.split('>')
    command = split_string[-1].strip()  # Use strip to remove leading/trailing whitespace
    return command

def print_result(result,window,command):
    if result.stdout:
        window.terminal.appendPlainText(result.stdout)
        window.terminal.process.write(b'\n')
    elif result.stderr:
        window.terminal.appendPlainText(result.stderr)
        window.terminal.process.write(b'\n')
    else:
        window.terminal.appendPlainText(command)
        window.terminal.process.write(b'\n')
def wait_for_file(file_path):
    while not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        time.sleep(0.1)
    return