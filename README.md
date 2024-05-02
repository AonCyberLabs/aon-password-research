# Password Cracking Tools
A repository for tools and rules useful for conducting password cracking research and data collection.

### Rule Lists
This repo contains rule lists of various sizes tailored for cracking passwords that are known to comply with common password strength requirements. The rule lists are named by 

`<minimum password length>-<complex or simple>-<number of rules>`

__Minimum Password Length:__ the minimum number of characters required for the target passwords

__Complex:__ Password policy requires at least 3 different character classes (upper case letters, lower case letters, numbers, special characters, etc.)

__Simple:__ No restrictions on character class

__Number of Rules:__ The length of the rule list

[This blog post](https://www.aon.com/en/insights/cyber-labs/cracking-into-password-requirements) describes how the rule lists were made. 

The "unrevised_top_64" folder contains copies of the *-64.rule files from before they were revised to match current years. The "Source_Rules.md" file contains a list of the public rule files that these new rule lists are based on. See the blog post for more details. 


### super_dict.txt
This is a password cracking word list designed to be an improvement on rockyou.txt with only modest size inflation. It is a deduplicated combination of the following:
1. rockyou.txt
2. https://github.com/danielmiessler/SecLists/blob/master/Passwords/xato-net-10-million-passwords.txt
3. https://github.com/danielmiessler/SecLists/blob/master/Passwords/Keyboard-Combinations.txt
4. The 5000 most common English words
5. 3000 common names (mix of first and last)
6. Various permutations of "Passsword" 


### anonymize_ntds.py

This program takes an NTDS file (as formatted by impacket-secretsdump) and replaces all the domain\username information with user1, user2, user3, etc. and machine1, machine2, etc. 
This script assumes that all password history entries for a given user or computer are consecutive.

```
options:
  -h, --help                    Show this help message and exit. 
  -n, --ntds NTDS               The ntds file to anonymize.
  -o, --output OUTPUT           The file to output to.
  -u, --users_only              Omit machine accounts from the output.
```

### complex_password_filter.py
This script takes a list of passwords and outputs a new file containing only the passwords that contain at least three of the following four character classes. 
1. upper case letter
2. lower case letter
3. number
4. One of the following special characters
```
!@#$%^&*()_+{}|:"<>?~-[]/\\;\'.,=-
```

```
  -h, --help            Show this help message and exit.
  -i, --input INPUT     Input password list.
  -o, --output OUTPUT   Output file for segmented and labeled passwords.
  -t, --time            Clock the execution time.
```

### mask_stats.py
This program collects simple mask statistics on a password list. A mask is a sequence of symbols representing the character classes used by the password.

This script uses a relatively simple mapping of 'u' for upper case letters, 'l' for lower case letters, 'd' for digits, and 's' for anything else. For example, if the input is `Password123!` then the mask will be `ulllllllddds`.


```
  -h, --help                Show this help message and exit.
  -t, --time                Clock the execution time.
  -p, --passwords PASSWORDS File containing the passwords.
  -n N                      Display the n most frequently occurring masks.
```

### per-policy-rule-hits.py
This program takes a (debug-mode=1) hashcat log file and a (-o) hashcat output file from hashcat and divides the logged rule hits into different output files based on applicable password policies.

```
  -h, --help                        Show this help message and exit.
  -l, --log LOG                     The log file from hashcat debug-mode=1
  -c, --cracked CRACKED             The output file from using -o with hashcat.
  -o, --output_prefix OUTPUT_PREFIX The prefix to use for the output log files.
  -t, --time                        Clock the execution time.
```

### reservoir_sampling.py 
This script uses the reservoir sampling method to generate random samples of a specified number of lines from the input file. 

```
  -h, --help            Show this help message and exit.
  -i, --input INPUT     The file to sample from.
  -o, --output OUTPUT   The file to output to.
  -s, --size SIZE       The sample size in number of lines.
  -t, --time            Clock the execution time.
```

### top_n_rules.py
When used with `--debug-mode=1 --debug-file out-file.log`, hashcat will log the rule that was used each time a password is recovered. This script takes these log files and counts up the highest performing n rules and outputs those rules to a new file. 

```
  -h, --help            Show this help message and exit.
  -t, --time            Clock the execution time.
  -l, --log LOG         The hashcat debug mode 1 log file (or directory if using -r).
  -o, --output OUTPUT   Output file for the resulting rules list.
  -r, --recursive       Input all .log files in the specified directory and its subdirectories.
  -n N                  The number of top performing rules to output.
  -c, --count           I have had issues in the past with python failing to process the entirety of large files. Use this flag to output the total line count of all rules processed. This can be compared against the output of 'wc -l *.log' or similar to make sure every logged rule was processed.
```

**Dependencies:** `pip3 install tabulate`

### hashgen.py

There is a great utility for converting plaintext passwords to hashes available at https://github.com/cyclone-github/hashgen-testing/tree/main/hashgen_python

Example: 
```
python3 hashgen.py -w wordlist.txt -m md5 -o output.txt
```

### Copyright
Copyright 2024 Aon plc
