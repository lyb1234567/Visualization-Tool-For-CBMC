import os
import time
import re
bin_op=["<","<=",">",">=","=="]
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

def extract_variables(statement):
    # Define the keywords to be excluded
    keywords = ["assertion", "NULL"]

    # Find array names and indices
    array_variables = re.findall(r'([a-zA-Z_][a-zA-Z_0-9]*)\[\s*([a-zA-Z_][a-zA-Z_0-9]*)(?:\s*[+\-*/]\s*[a-zA-Z_0-9]*)?\s*\]', statement)
    array_names = [name for name, _ in array_variables]
    array_indices = [index for _, index in array_variables]

    # Find all variables
    all_variables = re.findall(r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', statement)

    # Exclude keywords, array names and ensure unique variables
    variables = [var for var in all_variables if var not in keywords + array_names]

    # Add array indices back into the variables list
    variables += array_indices

    # Ensure unique variables
    variables = list(set(variables))

    return variables

def is_trace_file(filename):
    pattern = r"^(.*_)?trace_\d+\.json$"  # 匹配以可选的任何字符串（后面接着 "_"）开头，接着是 "trace_"，然后是一或多个数字，最后是 ".json"
    return re.match(pattern, filename) is not None
