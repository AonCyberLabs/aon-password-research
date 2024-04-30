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

import random
import argparse
import time

def reservoir_sampling(file_path, sample_size):
    reservoir = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file):
            if line_number < sample_size:
                reservoir.append(line.rstrip())
            else:
                # Randomly replace an existing item in the reservoir with the new line
                replace_index = random.randint(0, line_number)
                if replace_index < sample_size:
                    reservoir[replace_index] = line.strip()

    return reservoir


if __name__=="__main__":
    parser =argparse.ArgumentParser(description="This program generates random samples of n lines from the input file.",add_help=True)
    parser.add_argument("-i", "--input", required=True, help="The file to sample from.")
    parser.add_argument("-o", "--output", required=True, help="The file to output to.")
    parser.add_argument("-s", "--size", required=True, help="The sample size in number of lines.", type=int)
    parser.add_argument("-t", "--time", required=False, default=False, action='store_true', help="Clock the execution time.")
    args = parser.parse_args()

    if args.time: start_time = time.time()

    random_sample = reservoir_sampling(args.input, args.size)
    print(f"Random sample is size {len(random_sample)}. Make sure output file matches.")
    with open(args.output, 'w') as file:
        for password in random_sample:
            file.write(password + '\n')
    
    if args.time:
        runtime = time.time() - start_time
        print(f"Execution took {runtime} seconds.")