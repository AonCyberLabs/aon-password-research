#############################################################################
#   Copyright 2024 Aon plc
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#############################################################################

import argparse
import time

def is_complex(password):
    conditions_met = 0

    if any(char.isupper() for char in password):
        conditions_met += 1
    if any(char.islower() for char in password):
        conditions_met += 1
    if any(char.isdigit() for char in password):
        conditions_met += 1
    if any(char in '!@#$%^&*()_+{}|:"<>?~-[]/\\;\'.,=-' for char in password):
        conditions_met += 1

    return conditions_met >= 3

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Filter a password list based on the AD complex requirements.")
    parser.add_argument("-i", "--input", required=True, help="Input password list.")
    parser.add_argument("-o", "--output",required=True, help="Output file for segmented and labeled passwords.")
    parser.add_argument("-t", "--time", required=False, default=False, action='store_true', help="Clock the execution time.")
    args = parser.parse_args()

    if args.time: start_time = time.time()

    with open(args.input, 'r') as file:
        passwords = [line.rstrip() for line in file]

    print(f"Length of passwords is {len(passwords)}. This should match input file length.")

    # Filter passwords that meet the requirements
    filtered_passwords = [password for password in passwords if is_complex(password)]
    print(f"Length of complex passwords is {len(filtered_passwords)}. This should match output file length.")

    # Save the filtered passwords to a new file
    with open(args.output, 'w') as file:
        for password in filtered_passwords:
            file.write(password + '\n')

    if args.time:
        runtime = time.time() - start_time
        print(f"Execution took {runtime} seconds.")