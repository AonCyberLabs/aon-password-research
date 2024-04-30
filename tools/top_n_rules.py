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
from heapq import nlargest
from tabulate import tabulate
from os import walk
from os.path import join

rule_hits = {} # dictionary to build rule counts in

def add_log_data(filepath):
    with open(filepath, 'r') as file:
        for line in file.readlines():
            rule = line.rstrip()
            if rule in rule_hits.keys():
                rule_hits[rule] += 1
            else:
                rule_hits[rule] = 1

if __name__ == "__main__":
    parser =argparse.ArgumentParser(description="This program takes a hashcat debug mode 1 log and outputs the n best performing rules from that log.",add_help=True)
    parser.add_argument("-t", "--time", required=False, default=False, action='store_true', help="Clock the execution time.")
    parser.add_argument("-l", "--log", required=True, help="The hashcat debug mode 1 log file (or directory if using -r).")
    parser.add_argument("-o", "--output", required=True, help="Output file for the resulting rules list.")
    parser.add_argument("-r","--recursive",required=False,help="Input all .log files in the specified directory and its subdirectories.",action='store_true',default=False)
    parser.add_argument("-n", required=True, type=int, help="The number of top performing rules to output. ")
    parser.add_argument("-c","--count", required=False, action='store_true', default=False, help="I have had issues in the past with python failing to process the entirety of large files. Use this flag to output the total count of all rules processed. This can be compared against the output of 'wc -l *.log' or similar to make sure every logged rule was processed.")
    args = parser.parse_args()

    if args.time: start_time = time.time()

    if args.recursive:
        for root, _, files in walk(args.log):
            for file in files:
                if file.endswith(".log"):
                    path = join (root, file)
                    add_log_data(path)
                    print(f"processed log data for {path}")
    else:
        add_log_data(args.log)
        
    
    ordered_rule_counts = sorted(rule_hits.items(), key=lambda x: x[1], reverse=True)

    with open(args.output, "w") as outfile:
        for i in range(args.n): 
            outfile.write(ordered_rule_counts[i][0] + "\n")

    
    if args.time:
        runtime = time.time() - start_time
        print(f"Execution took {runtime} seconds.")

    if args.count:
        total = sum(rule_hits.values())
        print(f"A total of {total} log entries were processed.")