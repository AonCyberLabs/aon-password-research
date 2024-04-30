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

def get_mask(password):
    mask = ""
    for char in password: 
        if char.islower(): mask += "l"
        elif char.isupper(): mask += "u"
        elif char.isdigit(): mask += "d"
        else: mask += "s"
    return mask


if __name__ == "__main__":
    parser =argparse.ArgumentParser(description="This program collects mask statistics on a password list.",add_help=True)
    parser.add_argument("-t", "--time", required=False, default=False, action='store_true', help="Clock the execution time.")
    parser.add_argument("-p", "--passwords", required=True, help="File containing the passwords.")
    parser.add_argument("-n", required=False, default=20, type=int, help="Display the n most frequently occurring masks.")
    args = parser.parse_args()

    if args.time: start_time = time.time()

    masks = {}
    with open(args.passwords, 'r') as file:
        for line in file.readlines():
            mask = get_mask(line.rstrip())
            if mask in masks.keys():
                masks[mask] += 1
            else:
                masks[mask] = 1
    
    results_table = [["MASK", "COUNT", "PERCENT"]]
    top_masks = nlargest(args.n, masks, key = masks.get)
    total_percentage = 0
    total_count = sum(masks.values())
    eighty_percent = 0

    for m in top_masks:
        count = masks[m]
        percent = 100 * count / total_count
        if total_percentage < 80: eighty_percent += 1
        total_percentage += percent
        results_table.append([m,count,percent])

    print(tabulate(results_table, headers='firstrow', tablefmt='fancy_grid'))

    print(f"The top {args.n} masks make up {total_percentage} of all the masks for this password set.")
    if total_percentage > 80:
        print(f"The top {eighty_percent} of the masks account for 80%+ of all passwords in the list.")

    
    if args.time:
        runtime = time.time() - start_time
        print(f"Execution took {runtime} seconds.")