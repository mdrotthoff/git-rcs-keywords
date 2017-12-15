#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$

import sys
import os
import stat
import subprocess
import time

# Set the debugging flag
debug_flag = bool(sys.flags.debug)
debug_flag = bool(True)
verbose_flag = bool(True)

# Set the start time for calculating elapsed time
if debug_flag:
    start_time = time.clock()

# Parameter processing
(hook_path, hook_name) = os.path.split(sys.argv[0])
if debug_flag:
    sys.stderr.write('Hook path: ' + str(hook_path) + '\n')
    sys.stderr.write('Hook name: ' + str(hook_name) + '\n')

# List the provided parameters
if verbose_flag:
    if len(sys.argv) > 0:
        program_name = str(sys.argv[0])
        sys.stderr.write('Program name: ' + str(program_name) + '\n')
if debug_flag:
    sys.stderr.write("Parameter list\n")
    param_num = 0
    for param in sys.argv:
        sys.stderr.write('  Param[%d]: %s\n' % (param_num, sys.argv[param_num]))
        param_num = param_num + 1
    sys.stderr.write("\n")

# Show the OS environment variables
if verbose_flag:
    sys.stderr.write('Environment variables defined\n')
    for key, value in sorted(os.environ.items()):
        sys.stderr.write('  Key: %s  Value: %s\n' % (key, value))
    sys.stderr.write("\n")
        
# Verify that the named hook directory is a dictory
list_dir = program_name + '.d'
if not os.path.isdir(list_dir):
    sys.stderr.write('The hook directory %s is not a directory\n' % list_dir)
    exit(1)
else:
    if debug_flag:
        sys.stderr.write('The hook directory %s is a directory\n' % list_dir)
        sys.stderr.write("\n")

# Show the OS files in the hook named directory
if verbose_flag:
    sys.stderr.write('OS Files existing in the hook named directory %s\n' % list_dir)
    for file_name in sorted(os.listdir(list_dir)):
        file_stat = os.lstat(os.path.join(list_dir, file_name))
        file_mtime = str(time.strftime('%x %X', time.localtime(file_stat.st_mtime)))
        file_size = str(file_stat.st_size)
        file_mode = str(oct(stat.S_IMODE(file_stat.st_mode)))
        file_type = ''
        if stat.S_ISLNK(file_stat.st_mode) > 0:
            file_type = file_type + ' Symlink'
        if stat.S_ISDIR(file_stat.st_mode) > 0:
            file_type = file_type + ' Directory'
        if stat.S_ISREG(file_stat.st_mode) > 0:
            file_type = file_type + ' Regular'
        sys.stderr.write('  File: %s   %s  %s bytes  %s  %s\n' % (file_name, file_mtime, file_size, file_mode, file_type.strip()))
    sys.stderr.write("\n")

# Calculate the setup elapsed time
if debug_flag:
    setup_time = time.clock()
    sys.stderr.write('Setup elapsed time: ' + str(setup_time - start_time) + '\n')
    sys.stderr.write("\n")

# Execute each of the hooks found in the relevant directory
hook_count = 0
hook_executed = 0
for file_name in sorted(os.listdir(list_dir)):
    hook_count = hook_count + 1
    hook_program = os.path.join(list_dir, file_name)
    if debug_flag:
        sys.stderr.write('hook program %s seen\n' % hook_program)
    if os.path.isfile(hook_program) and os.access(hook_program, os.X_OK):
        hook_executed = hook_executed + 1
        if debug_flag or verbose_flag:
            sys.stderr.write('Executing hook program %s\n' % hook_program)
        hook_call = subprocess.call([hook_program], shell=True)
# TODO: Add error handling if hook_call is not zero after execution
#       Also consider using Popen and capturing stdout and stderr?
#        print(hook_call)
        if debug_flag or verbose_flag:
            sys.stderr.write("\n")
sys.stderr.write("\n")


if debug_flag:
    end_time = time.clock()
    sys.stderr.write('Execution elapsed time: ' + str(end_time - setup_time) + '\n')
    sys.stderr.write('Total elapsed time: ' + str(end_time - start_time) + '\n')
    sys.stderr.write('Hooks seen: ' + str(hook_count) + '\n')
    sys.stderr.write('Hooks executed: ' + str(hook_executed) + '\n')
    sys.stderr.write("\n")
elif verbose_flag:
    sys.stderr.write('Hooks seen: ' + str(hook_count) + '\n')
    sys.stderr.write('Hooks executed: ' + str(hook_executed) + '\n')
    sys.stderr.write("\n")

if debug_flag or verbose_flag:
    sys.stderr.write("\n")
    sys.stderr.write("\n")
    sys.stderr.write("\n")
