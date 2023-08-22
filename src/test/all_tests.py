import os

def find_test_files(root_dir):
    test_file_paths = []

    # 遍历root_dir目录下的所有文件和文件夹
    for dirpath, dirnames, filenames in os.walk(root_dir):
        
        # 如果当前文件夹是以"test_"开头的
        if os.path.basename(dirpath).startswith('test_'):
            
            # 遍历当前文件夹中的所有文件
            for filename in filenames:
                
                # 如果文件名以"test_"开头并且是.py文件
                if filename.startswith('test_') and filename.endswith('.py'):
                    abs_path = os.path.abspath(os.path.join(dirpath, filename))
                    test_file_paths.append(abs_path)

    return test_file_paths
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import subprocess
    current_directory = os.getcwd()
    files_to_run = find_test_files(current_directory)
    for file in files_to_run:
        subprocess.call(['coverage','run', file])
        subprocess.call(['coverage','report'])

    
    