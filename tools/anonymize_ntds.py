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

if __name__=="__main__":
    parser =argparse.ArgumentParser(description="""This program takes an NTDS file as formatted by impacket-secretsdump and replaces 
                                    all the domain\\username information with user1, user2, user3, etc. and machine1, machine2, etc. 
                                    The reason for doing this instead of cut-ing out the NTLM hashes by themselves is to retain password history information. 
                                    This script assumes that all password history entries for a given user or computer are consecutive.""",add_help=True)
    parser.add_argument("-n", "--ntds", required=True, help="The ntds file to anonymize.")
    parser.add_argument("-o", "--output", required=True, help="The file to output to.")
    parser.add_argument("-u", "--users_only", required=False, default=False, action="store_true", help="Omit machine accounts from the output.")
    args = parser.parse_args()

    anonymized_user_lines = []
    anonymized_machine_lines = []

    # state tracking
    current_user = ""
    user_index = 0
    machine_index = 0


    with open(args.ntds,"r") as ntds:
        for entry in ntds.readlines():

            # step 1: figure out if it's a machine account and if it's a history entry
            tokens = entry.split(":")
            account_name = tokens[0]
            is_machine = "$" in account_name
            history_index = account_name.find("_history")

            # choose the anonymous account name based on the information from step 1
            if history_index > -1 and not is_machine:
                new_account = f"user{user_index}{account_name[history_index:]}"
            elif history_index > -1 and is_machine:
                new_account = f"machine{machine_index}{account_name[history_index:]}"
            elif history_index < 0 and not is_machine:
                user_index += 1
                new_account = f"user{user_index}"
            elif history_index < 0 and is_machine:
                machine_index += 1
                new_account = f"machine{machine_index}"

            # put the new anonymized account back into the line 
            if not is_machine:
                anonymized_user_lines.append(f"{new_account}:{':'.join(tokens[1:])}")
            if is_machine:
                anonymized_machine_lines.append(f"{new_account}:{':'.join(tokens[1:])}")

    with open(args.output, "w") as outfile:
        outfile.writelines(anonymized_user_lines)
        if not args.users_only:
            outfile.writelines(anonymized_machine_lines)
