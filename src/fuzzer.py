#!/usr/bin/env python3
import os
import sys
import subprocess
import random
import signal
import time 

def run_binary(binary_path, input_data):

    try:
        # Can update to subprocess.Popen() for more manual control of the process
        result = subprocess.run(
                    [binary_path],
                    input=input_data,
                    capture_output=True,
                    timeout=1
                )
        
        print(f"Subprocess started for {binary_path}")

        if result.returncode != 0:
            print(f"Exited with {result}")
            return True, result.returncode
        
        return False, result.returncode
    except subprocess.TimeoutExpired:
        print("timeout > 1s")
        return False, 0
    
'''
function currently just runs all the inputs from /example_inputs against the ELF

next addition will be a mutate_input() function to alter these inputs 
'''
def fuzz_binary(binary_path, inputs_dir, output_dir, timeout=60):
    print(f"Now fuzzing {binary_path}!!!!")

    inputs = []
    for f in os.listdir(inputs_dir):
        full_path = os.path.join(inputs_dir, f)
        if os.path.isfile(full_path):
            inputs.append(full_path)

    crashes_found = []
    start_time = time.time()
    iteration = 0

    while time.time() - start_time < timeout:
        for input_path in inputs:
            iteration += 1

            if time.time() - start_time >= timeout:
                break

            with open(input_path, 'rb') as f:
                current_input = f.read()

            print(f"testing {binary_path} with input: {os.path.basename(input_path)}")
            
            crashed, exit_code = run_binary(binary_path, current_input)

            if crashed:
                print(f"Crashed at iteration {iteration}!!!! Exit code: {exit_code}")
                crashes_found.append(current_input)
                
                # save input that causes crash
                binary_name = os.path.basename(binary_path)
                output_file = os.path.join(output_dir, f"{binary_name}_crashing_input.txt")
                with open(output_file, 'wb') as f:
                    f.write(current_input)
                print(f"saved to {output_file}!!!!")
                return True
        break
        
    print(f"no crashes found for {binary_path} after {iteration} iterations")
    return False

# def mutate_input():

def main():
    binaries_dir = "/binaries"
    inputs_dir = "/example_inputs"
    output_dir = "/fuzzer_output"

    binaries = []
    for f in os.listdir(binaries_dir):  
        full_path = os.path.join(binaries_dir, f)
        if os.path.isfile(full_path):
            binaries.append(f)

    print(f'"Found {len(binaries)} binaries to fuzzzzz!')

    timeout_per_binary = 60

    for binary in binaries:
        binary_path = os.path.join(binaries_dir, binary)

        fuzz_binary(binary_path, inputs_dir, output_dir, timeout_per_binary)

    print("fuzzing all done")


if __name__ == "__main__":
    main()

