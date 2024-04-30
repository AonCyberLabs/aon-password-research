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
from complex_password_filter import is_complex

if __name__=="__main__":
    parser =argparse.ArgumentParser(description="This program takes a (debug-mode=1) hashcat log file and a (-o) hashcat output file from hashcat and divides the logged rule hits into different output files based on applicable password policies.",add_help=True)
    parser.add_argument("-l", "--log", required=True, help="The log file from hashcat debug-mode=1")
    parser.add_argument("-c", "--cracked", required=True, help="The output file from using -o with hashcat.")
    parser.add_argument("-o", "--output_prefix", required=True, help="The prefix to use for the output log files.")
    parser.add_argument("-t", "--time", required=False, default=False, action='store_true', help="Clock the execution time.")
    args = parser.parse_args()

    if args.time: start_time = time.time()

    rule_hits = []
    plaintexts = []

    with open(args.log,"r") as logfile:
        for rule in logfile.readlines():
            rule_hits.append(rule)
    with open(args.cracked, "r") as crackedfile:
        for line in crackedfile.readlines():
            plaintext = line.rstrip().split(":")[1]
            plaintexts.append(plaintext)
    
    r_len = len(rule_hits)
    if r_len != len(plaintexts):
        print("Error: --logged and --cracked must be the same length. Exiting!")
        exit()

    simple_8_hits = []
    simple_10_hits = [] 
    simple_12_hits = [] 
    simple_14_hits = [] 
    complex_8_hits = []
    complex_10_hits = [] 
    complex_12_hits = [] 
    complex_14_hits = []


    for i in range(r_len):
        pw_len = len(plaintexts[i])
        is_complex = is_complex(plaintexts[i])
        if is_complex:
            if pw_len > 7:
                complex_8_hits.append(rule_hits[i])
            if pw_len > 9:
                complex_10_hits.append(rule_hits[i])
            if pw_len > 11:
                complex_12_hits.append(rule_hits[i])
            if pw_len > 13:
                complex_14_hits.append(rule_hits[i])
        else:
            if pw_len > 7:
                simple_8_hits.append(rule_hits[i])
            if pw_len > 9:
                simple_10_hits.append(rule_hits[i])
            if pw_len > 11:
                simple_12_hits.append(rule_hits[i])
            if pw_len > 13:
                simple_14_hits.append(rule_hits[i])

    with open(args.output_prefix + "8-simple.log", "w") as simple_8:
        simple_8.writelines(simple_8_hits)

    with open(args.output_prefix + "8-complex.log", "w") as complex_8:
        complex_8.writelines(complex_8_hits)

    with open(args.output_prefix + "10-simple.log", "w") as simple_10:
        simple_10.writelines(simple_10_hits)

    with open(args.output_prefix + "10-complex.log", "w") as complex_10:
        complex_10.writelines(complex_10_hits)

    with open(args.output_prefix + "12-simple.log", "w") as simple_12:
        simple_12.writelines(simple_12_hits)

    with open(args.output_prefix + "12-complex.log", "w") as complex_12:
        complex_12.writelines(complex_12_hits)

    with open(args.output_prefix + "14-simple.log", "w") as simple_14:
        simple_14.writelines(simple_14_hits)

    with open(args.output_prefix + "14-complex.log", "w") as complex_14:
        complex_14.writelines(complex_14_hits)

    
    print("Stats:")
    print(f"8-simple hits: {len(simple_8_hits)}")
    print(f"8-complex hits: {len(complex_8_hits)}")
    print(f"10-simple hits: {len(simple_10_hits)}")
    print(f"10-complex hits: {len(complex_10_hits)}")
    print(f"12-simple hits: {len(simple_12_hits)}")
    print(f"12-complex hits: {len(complex_12_hits)}")
    print(f"14-simple hits: {len(simple_14_hits)}")
    print(f"14-complex hits: {len(complex_14_hits)}")


    if args.time:
        runtime = time.time() - start_time
        print(f"Execution took {runtime} seconds.")