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
import errno
import subprocess
import time

# Set the debugging flag
summary_flag = bool(True)
verbose_flag = bool(True)
timing_flag = bool(False)
debug_flag = bool(False)
if debug_flag:
    timing_flag = bool(True)
if timing_flag:
    verbose_flag = bool(True)
if verbose_flag:
    summary_flag = bool(True)


def checkfor(cmd):
    """Make sure that a program necessary for using this script is
    available.

    Arguments:
    args -- string or list of strings of commands. A single string may
            not contain spaces.
    """
    if verbose_flag:
        sys.stderr.write('  Entered module checkfor\n')
    if debug_flag:
        sys.stderr.write('  cmd: %s\n' % str(cmd))

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str):
        if ' ' in cmd:
            raise ValueError('No spaces in single command allowed.')

    try:
        # Execute the command
        cmd_return = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_return.communicate()

    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError or OSError:
        print("Required program '{}' not found! -- Exiting.".format(args[0]))
        if debug_flag:
            sys.stderr.write('    git exit code: %s\n' % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n' % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n' % str(len(cmd_stderr)))
            if len(cmd_stdout) > 0:
                sys.stdout.write('STDOUR from checkfor\n')
                sys.stderr.write(cmd_stdout.strip().decode("utf-8"))
                sys.stderr.write("\n")
            if len(cmd_stderr) > 0:
                sys.stdout.write('STDERR from checkfor\n')
                sys.stderr.write(cmd_stderr.strip().decode("utf-8"))
                sys.stderr.write("\n")
        sys.exit(1)

    # Dump debugging variables
    if debug_flag:
        sys.stderr.write('    git exit code: %s\n' % str(cmd_return.returncode))
        sys.stderr.write('    stdout length: %s\n' % str(len(cmd_stdout)))
        sys.stderr.write('    stderr length: %s\n' % str(len(cmd_stderr)))
        if len(cmd_stdout) > 0:
            sys.stdout.write('STDOUR from checkfor\n')
            sys.stderr.write(cmd_stdout.strip().decode("utf-8"))
            sys.stderr.write("\n")
        if len(cmd_stderr) > 0:
            sys.stdout.write('STDERR from checkfor\n')
            sys.stderr.write(cmd_stderr.strip().decode("utf-8"))
            sys.stderr.write("\n")

    # Return from the function
    if verbose_flag:
        sys.stderr.write('  Leaving module checkfor\n')
    return

def modifiedfiles():
    """Find files that have been modified in the last commit.

    Returns:
        A list of filenames.
    """
    if verbose_flag:
        sys.stderr.write('  Entered module modifiedfiles\n')
    file_list = []
    try:
        git_cmd = ['git', 'diff-tree', 'ORIG_HEAD', 'HEAD', '--name-only', '-r',
                   '--diff-filter=ACMRT']
        if debug_flag:
            sys.stderr.write('  git_cmd: %s\n' % str(git_cmd))

        # Get the list of files modified during the last commit
        git_return = subprocess.Popen(git_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (git_stdout, git_stderr) = git_return.communicate()
        if debug_flag:
            sys.stderr.write('    git exit code: %s\n' % str(git_return.returncode))
            sys.stderr.write('    stdout length: %s\n' % str(len(git_stdout)))
            sys.stderr.write('    stderr length: %s\n' % str(len(git_stderr)))
        file_list = git_stdout.decode('utf8').splitlines()
        if debug_flag:
            sys.stderr.write('  File list length: %d\n' % len(file_list))

        # Deal with unmodified repositories
        if len(file_list) == 1 and file_list[0] is 'clean':
            if debug_flag:
                sys.stderr.write('  No files found to process\n')
                sys.stderr.write('  Leaving module modifiedfiles\n')
            return []
        if debug_flag:
            sys.stderr.write('    List files found\n')
            for file_name in file_list:
                sys.stderr.write('      file found: %s\n' % str(file_name))

    except subprocess.CalledProcessError as e:
        # This is a new repository, so get a list of all files
        if e.returncode == 128:  # new repository
            if debug_flag:
                sys.stderr.write('  No head commit found\n')
            git_cmd = ['git', 'ls-files']
            if debug_flag:
                sys.stderr.write('  git_cmd: %s\n' % str(git_cmd))

            git_return = subprocess.Popen(git_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (git_stdout, git_stderr) = git_return.communicate()
            if debug_flag:
                sys.stderr.write('    git exit code: %s\n' % str(git_return.returncode))
                sys.stderr.write('    stdout length: %s\n' % str(len(git_stdout)))
                sys.stderr.write('    stderr length: %s\n' % str(len(git_stderr)))
            file_list = git_stdout.decode('utf8').splitlines()
            if debug_flag:
                sys.stderr.write('    File list length: %d\n' % len(file_list))
                sys.stderr.write('    List files found\n')
                for file_name in file_list:
                    sys.stderr.write('      file found: %s\n' % str(file_name))
        else:
            raise

    # Only return regular files.
    file_list = [i for i in file_list if os.path.isfile(i)]
    if debug_flag:
        sys.stderr.write('    List real files found\n')
        for file_name in file_list:
            sys.stderr.write('      Real file found: %s\n' % str(file_name))

    # Return from the function
    if verbose_flag:
        sys.stderr.write('  Leaving module modifiedfiles\n')
    return file_list

def git_not_checkedin():
    """Find files that are modified but are not checked in.

    Returns:
        A list of modified files that are not checked in.
    """
    if verbose_flag:
        sys.stderr.write('  Entered module git_not_checkedin\n')

#    modified_files = subprocess.check_output(['git', 'status', '-s'])
    try:
        git_cmd = ['git', 'status', '-s']
        if debug_flag:
            sys.stderr.write('  git_cmd: %s\n' % str(git_cmd))
        git_return = subprocess.Popen(git_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (git_stdout, git_stderr) = git_return.communicate()
        if debug_flag:
            sys.stderr.write('    git exit code: %s\n' % str(git_return.returncode))
            sys.stderr.write('    stdout length: %s\n' % str(len(git_stdout)))
            sys.stderr.write('    stderr length: %s\n' % str(len(git_stderr)))

    except subprocess.CalledProcessError or OSError:
        if debug_flag:
            sys.stderr.write('    git exit code: %s\n' % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n' % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n' % str(len(cmd_stderr)))
            if len(cmd_stdout) > 0:
                sys.stdout.write('STDOUR from git_not_checkedin\n')
                sys.stderr.write(cmd_stdout.strip().decode("utf-8"))
                sys.stderr.write("\n")
            if len(cmd_stderr) > 0:
                sys.stdout.write('STDERR from git_not_checkedin\n')
                sys.stderr.write(cmd_stderr.strip().decode("utf-8"))
                sys.stderr.write("\n")
        sys.exit(1)

    modified_files_list = git_stdout.decode('utf8').splitlines()
    if debug_flag:
        sys.stderr.write('    Status files found\n')
        for file_name in modified_files_list:
            sys.stderr.write('      status file found: %s\n' % str(file_name))
    modified_files_list = [l.split()[-1].strip('"') for l in modified_files_list]
    if debug_flag:
        sys.stderr.write('    Modified files found\n')
        for file_name in modified_files_list:
            sys.stderr.write('      modified file found: %s\n' % str(file_name))

    if verbose_flag:
        sys.stderr.write('  Leaving module git_not_checkedin\n')

    return modified_files_list

def checkoutfile(file_name):
    """Checkout file that has been modified by the latest commit.

    Returns:
        Nothing.
    """
    if verbose_flag:
        sys.stderr.write('  Entered module checkoutfile\n')

    # Remove the file if it currently exists
    try:
        if debug_flag:
            sys.stderr.write('  os file %s exists: %s\n' % (file_name, str(os.path.isfile(file_name))))

        os.remove(file_name)
    except OSError as err:
        # If the file does not exist, it was removed so loop to the next file
        if err.errno == errno.ENOENT:
            if debug_flag:
                sys.stderr.write('Unable to remove file name: %s  Error code: %d\n' % (str(git_checkout_cmd), err.errno))
        else:
            raise
    if debug_flag:
        sys.stderr.write('  Removed os file %s exists: %s\n' % (file_name, str(os.path.isfile(file_name))))

    git_cmd = ['git', 'checkout', '-f', '%s' % file_name]
    if debug_flag:
        sys.stderr.write('  git_cmd: %s\n' % str(git_cmd))
    git_return = subprocess.Popen(git_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (git_stdout, git_stderr) = git_return.communicate()
    if debug_flag:
        sys.stderr.write('    git exit code: %s\n' % str(git_return.returncode))
        sys.stderr.write('    stdout length: %s\n' % str(len(git_stdout)))
        sys.stderr.write('    stderr length: %s\n' % str(len(git_stderr)))

    # Return from the function
    if verbose_flag:
        sys.stderr.write('  Leaving module checkoutfile\n')
    return



# Set the start time for calculating elapsed time
if timing_flag:
    start_time = time.clock()

# Parameter processing
program_name = str(sys.argv[0])
(hook_path, hook_name) = os.path.split(program_name)
if debug_flag:
    sys.stderr.write('************ START **************\n')
    sys.stderr.write('Hook program: %s\n' % str(program_name))
    sys.stderr.write('Hook path: %s\n' % str(hook_path))
    sys.stderr.write('Hook name: %s\n' % str(hook_name))
    sys.stderr.write('*********************************\n')

# Output the program name start
if summary_flag:
    program_name = str(sys.argv[0])
    sys.stderr.write('Start program name: %s\n' % str(program_name))

# List the provided parameters
if verbose_flag:
    sys.stderr.write("  Parameter list\n")
    param_num = 0
    for param in sys.argv:
        sys.stderr.write('    Param[%d]: %s\n' % (param_num, sys.argv[param_num]))
        param_num = param_num + 1

# Show the OS environment variables
if debug_flag:
    # Show the OS environment variables
    sys.stderr.write('  Environment variables defined\n')
    for key, value in sorted(os.environ.items()):
        sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
    sys.stderr.write("\n")

# Check if git is available.
if debug_flag:
    sys.stderr.write('  Validating git is installed\n')
checkfor(cmd = ['git', '--version'])

# Get the list of modified files
if debug_flag:
    sys.stderr.write('  Getting list of files modified\n')
files = modifiedfiles()
modified_files_list = git_not_checkedin()
# Remove any modified files from the list of files to process
if modified_files_list:
    if debug_flag:
        sys.stderr.write('  Removing non-committed modifications\n')
        for file_name in files:
            if file_name not in modified_files_list:
                sys.stderr.write('    File name %s not in modified file list', file_name)
            else:
                sys.stderr.write('    File name %s IS in modified file list', file_name)
    files = [f for f in files if f not in modified_files_list]
## If no files remain in the list, 
#if not files:
#    print('{}: No modified files.'.format(args[0]))
#    sys.exit(0)

## Get the list of files impacted by the action
#git_diff_tree_cmd = 'git diff-tree -r --name-only --diff-filter=ACMRT ORIG_HEAD HEAD'
#if verbose_flag:
#    sys.stderr.write('  git diff-tree cmd: %s\n' % str(git_diff_tree_cmd))

## Process the git diff-tree command
#git_return = subprocess.Popen([git_diff_tree_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#(git_stdout, git_stderr) = git_return.communicate()
#if debug_flag:
#    sys.stderr.write('git exit code: %s\n' % str(git_return.returncode))
#    sys.stderr.write('stdout length: %s\n' % str(len(git_stdout)))
#    sys.stderr.write('stderr length: %s\n' % str(len(git_stderr)))
#    sys.stderr.write("\n")

## If an error occurred, display the command output and exit with the returned exit code 
#if git_return.returncode != 0:
#    sys.stderr.write("Exiting -- git diff-tree return code: %s\n" % str(git_return.returncode))
#    sys.stderr.write("Output text: %s\n" % git_stdout.strip().decode("utf-8"))
#    sys.stderr.write("Error message: %s\n" % git_stderr.strip().decode("utf-8"))
#    exit(git_return.returncode)
#elif len(git_stderr) > 0:
#    sys.stdout.write('STDERR from git diff-tree\n')
#    sys.stderr.write(git_stderr.strip().decode("utf-8"))
#    sys.stderr.write("\n")

# Calculate the setup elapsed time
if timing_flag:
    setup_time = time.clock()

# Process the list of modified files
if debug_flag:
    sys.stderr.write('  Processing modified files list\n')
files_processed = 0
#for fn in kwfn:
if files:
    files.sort()
    for file_name in files:
        if debug_flag:
            sys.stderr.write('  Checking out file %s\n' % file_name)
        checkoutfile(file_name = file_name)
        files_processed = files_processed + 1

## Process each of the files listed by forcing a fresh check-out of the file
#files_processed = 0
#if len(git_stdout) > 0:
#    # Create a sorted, unique list file names from the returned values
#    git_log = git_stdout.strip().decode("utf-8")
#    git_log = sorted(set(git_log.strip().split("\n")))
#
#    # Process each of the file names returned
#    for file_name in git_log:
#        # Format the git checkout command
#        files_processed = files_processed + 1
#        git_checkout_cmd = 'git checkout -- "%s"' % file_name
#        if verbose_flag:
#            sys.stderr.write('  git checkout cmd: %s\n' % str(git_checkout_cmd))
#
#        # Remove the file if it currently exists
#        try:
#            os.remove(file_name)
#        except OSError as err:
#            # If the file does not exist, it was removed so loop to the next file
#            if err.errno == errno.ENOENT:
#                if debug_flag:
#                    sys.stderr.write('Unable to remove file name: %s  Error code: %d\n' % (str(git_checkout_cmd), err.errno))
#                pass

#        # Execute the git checkout command
#        git_return = subprocess.Popen([git_checkout_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#        (git_stdout, git_stderr) = git_return.communicate()
#        if debug_flag:
#            sys.stderr.write('git exit code: %s\n' % str(git_return.returncode))
#            sys.stderr.write('stdout length: %s\n' % str(len(git_stdout)))
#            sys.stderr.write('stderr length: %s\n' % str(len(git_stderr)))

#        # If an error occurred, display the command output and exit with the returned exit code 
#        if git_return.returncode != 0:
#            sys.stderr.write("Exiting -- git checkout return code: %s\n" % str(git_return.returncode))
#            sys.stderr.write("Output text: %s\n" % git_stdout.strip().decode("utf-8"))
#            sys.stderr.write("Error message: %s\n" % git_stderr.strip().decode("utf-8"))
#            exit(git_return.returncode)
#        else:
#            if len(git_stdout) > 0:
#                sys.stdout.write(git_stdout.strip().decode("utf-8"))
#                sys.stdout.write("\n")
#            if len(git_stderr) > 0:
#                sys.stderr.write(git_stderr.strip().decode("utf-8"))
#                sys.stderr.write("\n")

# Calculate the elapsed times
if timing_flag:
    end_time = time.clock()
    sys.stderr.write('Setup elapsed time: %s\n' % str(setup_time - start_time))
    sys.stderr.write('Execution elapsed time: %s\n' % str(end_time - setup_time))
    sys.stderr.write('Total elapsed time: %s\n' % str(end_time - start_time))
    sys.stderr.write('Files processed: %s\n' % str(files_processed))

# Display a processing summary
if summary_flag:
    sys.stderr.write('Files processed: %s\n' % str(files_processed))

# Output the program end
if verbose_flag:
    sys.stderr.write('End program name: %s\n' % str(program_name))
    sys.stderr.write("\n")
elif debug_flag:
    sys.stderr.write('************ END ****************\n')
    sys.stderr.write('Hook path: %s\n' % str(hook_path))
    sys.stderr.write('Hook name: %s\n' % str(hook_name))
    sys.stderr.write('*********************************\n')
    sys.stderr.write("\n")
    sys.stderr.write("\n")
    sys.stderr.write("\n")
