"""
This script is used to analyze the execution times of a set of functions.

It assumes that it is given a JSON file with each line containing a JSON object
with the following structure:

{
    "key": "<module_name>.<func_name>",
    "execution_time": <float>
}

The script will then load the JSON data and extract the method names and execution
times. It will then calculate the mean and standard deviation of the execution
times for each method. Finally, it will create a plot with each method on a
different line showing the mean and standard deviation of the execution times.

The user must provide the path to the JSON file as a command line argument.
"""

import json
import numpy as np
import matplotlib.pyplot as plt

# Load the JSON data from the file
with open('<Your Path Here>', 'r') as f:
    data = [json.loads(line) for line in f.readlines()]

# Extract the method names and execution times
method_names = []
execution_times = []
for d in data:
    # method_names.append(d['method_name'])
    method_names.append(d['key'])
    execution_times.append(d['execution_time'])

# Create a dictionary to store the execution times for each method
method_times = {}
for method, time in zip(method_names, execution_times):
    if method not in method_times:
        method_times[method] = []
    method_times[method].append(time)

# Calculate the mean and standard deviation of the execution times for each method
method_means = {}
method_stds = {}
for method, times in method_times.items():
    method_means[method] = np.mean(times)
    method_stds[method] = np.std(times)

# Create a plot with each method on a different line
methods = list(method_times.keys())
means = [method_means[method] for method in methods]
stds = [method_stds[method] for method in methods]

plt.errorbar(range(len(methods)), means, yerr=stds, fmt='o-')
plt.xticks(range(len(methods)), methods, rotation=90)
plt.xlabel('Method')
plt.ylabel('Mean Execution Time (s)')
plt.title('Execution Time by Method')
plt.show()
