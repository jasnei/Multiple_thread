# Example 1
import subprocess
# Enable these lines to make this example work on Windows
# import os
# os.environ['COMSPEC'] = 'powershell'

# result = subprocess.run(
#     ['echo', 'Hello from the child!'],
#     capture_output=True,
#     # Enable this line to make this example work on Windows
#     shell=True,
#     encoding='utf-8')

# result.check_returncode()  # No exception means it exited cleanly
# print(result.stdout)

# # Example 2
# # Use this line instead to make this example work on Windows
# import time
# proc = subprocess.Popen(['timeout', '1'])
# while proc.poll() is None:
#     print('Working...')
#     # Some time-consuming work here
#     time.sleep(0.3)

# print('Exit status', proc.poll())

import time


start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['timeout', '1'])
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()

end = time.time()
elapse = end - start
print(f"Finished in {elapse:.3} seconds")
