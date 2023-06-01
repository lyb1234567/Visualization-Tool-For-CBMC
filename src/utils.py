import os

def extract_file_name(file_address):
    file_name = os.path.basename(file_address)
    return file_name

def check_file_exists(filename):
    return os.path.isfile(filename)