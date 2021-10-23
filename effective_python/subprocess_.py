# Example 1
import subprocess
# Enable these lines to make this example work on Windows
# import os
# os.environ['COMSPEC'] = 'powershell'

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    # Enable this line to make this example work on Windows
    shell=True,
    encoding='utf-8')

result.check_returncode()  # No exception means it exited cleanly
print(result.stdout)
