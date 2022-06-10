#!/usr/bin/env python
import argparse
import subprocess
from sys import exit
from os import path
from os import environ
import datetime

__author__ = 'pcfeduardo'
__version__ = 1.0

backup_dir = 'backup_dir.list'
prog = 'bkp-tool'

class style():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description='bkp-tool - file backup tool using rsync', prog=f'{prog}')
parser.add_argument('src', help='specify the source directory')
parser.add_argument('dst', help='specify the destination directory')
parser.add_argument('--file', '-f', default=f'{backup_dir}', help='specify the file with the directories to backup')
parser.add_argument('--show-logs', action='store_true', help='shows the details of success as well as errors')
parser.add_argument('--show-errors', action='store_true', help='show only error details')
parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
args = parser.parse_args()

print(f'{style.HEADER}{datetime.datetime.now()} - starting {prog} {version} {style.ENDC}')
print(f'{style.HEADER}{datetime.datetime.now()} - written by {__author__}')

err = {}
logs = {}

if path.exists(args.file) == False:
    print(f'{style.WARNING}*** {style.UNDERLINE}{args.file}{style.ENDC}{style.WARNING} not found! :({style.ENDC}')
    exit(1)

rsync_fail, rsync = subprocess.getstatusoutput(f'which rsync')
if rsync_fail == 1:
    print(f'{style.WARNING}*** rsync not found! :({style.ENDC}')
    exit(1)
    
with open(args.file) as repo_backup:
    directories = repo_backup.readlines()
    if len(directories) == 0:
        print(f'{style.WARNING}*** the list for backup (file: {args.file}) is empty{style.ENDC}')
        exit(0)
    for dir in directories:
        print(f'{style.OKBLUE}{datetime.datetime.now()} - backuping {dir.strip()}...{style.ENDC}')
        backup_run = subprocess.run([rsync, '-avz', '--partial', '--ignore-errors', '--delete', f'{args.src}/{dir.strip()}', f'{args.dst}/{dir.strip()}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if backup_run.returncode == 0:
            logs.update({dir: 'success!'})
        if backup_run.returncode != 0:
            err.update({dir: backup_run.stderr})

def show_logs():
    if args.show_logs == True:
        for folder in logs:
            print(f'{style.OKGREEN}[successful] {folder.strip()} - {logs[folder].strip()}{style.ENDC}')

def show_errors():
    if args.show_logs or args.show_errors == True:
        for err_dir in err:
            print(f'{style.FAIL}[error] directory: {style.UNDERLINE}{err_dir.strip()}{style.ENDC}{style.FAIL} | details: {err[err_dir].strip()}{style.ENDC}')

if len(err) == 0:
    print(f'\n{style.OKGREEN}*** congratulations! all directories have been backed up successfully!{style.ENDC}\n')
    show_logs()
else:
    print(f'\n{style.FAIL}*** problems detected when performing the backup!{style.ENDC}\n')
    show_logs()
    show_errors()
