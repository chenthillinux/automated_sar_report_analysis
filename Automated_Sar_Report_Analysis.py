#!/usr/bin/env python3 -W ignore::DeprecationWarning
import subprocess
import os
import glob
import sys
import pandas as pd

print('cmd entry:', sys.argv)
directory = sys.argv[1]
print(directory)


file_type = 'sa[0-9][0-9]'
files = glob.glob(os.path.join(directory, file_type))
files.sort(key=os.path.getmtime)
#print(files)

def sar_u(directory):
    file_type = 'sa[0-9][0-9]'
    files = glob.glob(os.path.join(directory, file_type))
    files.sort(key=os.path.getmtime)
    for file_path in files:
        print(file_path)
        cmd1 = f"sar -t -f {file_path} -u"
        cmd2 = f"grep -v RESTART"
        cmd3 = f"grep -v Linux"
        cmd4 = f"grep -v Average"
        cmd5 = f"grep -v idle"
        cmd6 = f"grep -v '^\[\[:space:\]\]\*$'"
        cmd7 = f"tr -s ' ' ','"

        command = f"{cmd1} | {cmd2} | {cmd3} | {cmd4} | {cmd5} | {cmd6} | {cmd7}"
        output_file_name = f"output_{os.path.basename(file_path)}.csv"
        with open(output_file_name, 'w') as out_file:
            result = subprocess.run(command, shell=True, stdout=out_file)
            if result.returncode == 0:
                print('Command succeeded')
            else:
                print(f'Error, code {result.returncode}')

        df = pd.read_csv(output_file_name)
        df.columns = [ 'Time','AM-PM','CPU','%user','%nice','%system','%iowait','%steal','%idle' ]
        result = df.loc[df['%iowait']>=10]
        if len(result) == 0:
            print("No IOwait state found")
        else:
            print("IOwait state found")
            print(result)
            print("     ")

def sar_q(directory):
    file_type = 'sa[0-9][0-9]'
    files = glob.glob(os.path.join(directory, file_type))
    files.sort(key=os.path.getmtime)
    for file_path in files:
        print(file_path)
        cmd1 = f"sar -t -f {file_path} -q"
        cmd2 = f"grep -v RESTART"
        cmd3 = f"grep -v Linux"
        cmd4 = f"grep -v Average"
        cmd5 = f"grep -v idle"
        cmd6 = f"grep -v '^\[\[:space:\]\]\*$'"
        cmd7 = f"tr -s ' ' ','"

        command = f"{cmd1} | {cmd2} | {cmd3} | {cmd4} | {cmd5} | {cmd6} | {cmd7}"
        output_file_name = f"output_{os.path.basename(file_path)}.csv"
        with open(output_file_name, 'w') as out_file:
            result = subprocess.run(command, shell=True, stdout=out_file)
            if result.returncode == 0:
                print('Command succeeded')
            else:
                print(f'Error, code {result.returncode}')
            
            
            
        df = pd.read_csv(output_file_name)
        df.columns = [ 'Time','AM-PM','runq-sz','plist-sz','ldavg-1','ldavg-5','ldavg-15','blocked' ]
        result = df.loc[df['blocked']==0]
        if len(result) >= 2:
            print("No blocked state process")
        else:
            print("Found blocked state proces")
            print(result)
            print("     ")




#sar_u(directory)
sar_q(directory)
