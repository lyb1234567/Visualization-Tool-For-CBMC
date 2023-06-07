import subprocess

result = subprocess.run(['cbmc test.c --bounds-check --pointer-check --trace --xml-ui > output.xml '], shell=True, capture_output=True, text=True)

print('returncode:', result.returncode)
print('Have error:', result.stderr)
print('output:', result.stdout)