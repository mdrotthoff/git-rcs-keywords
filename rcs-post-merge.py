#! /usr/bin/env python3
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash:     "ce6f6d53540aa85c30264deab1a47016232ff0e8 $

"""rcs-keywords-post-merge

This module provides code to act as an event hook for the git
post-merge event.  It detects which files have been changed
and forces the file to be checked back out within the
repository.

"""

import sys
import os
import errno
import subprocess
import time

# Set the debugging flag
DEBUG_FLAG = bool(False)
TIMING_FLAG = bool(False)
if DEBUG_FLAG:
    TIMING_FLAG = bool(True)
VERBOSE_FLAG = bool(False)
if TIMING_FLAG:
    VERBOSE_FLAG = bool(True)
SUMMARY_FLAG = bool(True)
if VERBOSE_FLAG:
    SUMMARY_FLAG = bool(True)


def main(argv):
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    function_name = 'main'

    # Set the start time for calculating elapsed time
    start_time = time.clock()
    setup_time = None

    # Display the startup message
    startup_message(argv)

    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # List the provided parameters
    if VERBOSE_FLAG:
        dump_list(list_values=argv,
                  list_description='Param',
                  list_message='Parameter list')

    # Show the OS environment variables
    if DEBUG_FLAG:
        sys.stderr.write('  Environment variables defined\n')
        for key, value in sorted(os.environ.items()):
            sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
        sys.stderr.write("\n")

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of modified files
    files = get_modified_files()
    if VERBOSE_FLAG:
        dump_list(list_values=files,
                  list_description='File',
                  list_message='Files not checked in')

    # Filter the list of modified files to exclude those modified since
    # the commit
    files = git_not_checked_in(files=files)

    # Calculate the setup elapsed time
    setup_time = time.clock()

    # Process the remaining file list
    files_processed = 0
    if files:
        files.sort()
        for file_name in files:
            if DEBUG_FLAG:
                sys.stderr.write('  Checking out file %s\n' % file_name)
            check_out_file(file_name=file_name)
            files_processed = files_processed + 1

    # Calculate the elapsed times
    if TIMING_FLAG:
        display_timing(start_time=start_time,
                       setup_time=setup_time)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    shutdown_message(argv=argv,
                     files_processed=files_processed,
                     return_code=0)


def startup_message(argv):
    """Function display any startup messages

    Arguments:
        argv -- Command line parameters

    Returns:
        Nothing
    """
    function_name = 'startup_message'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Capture source executable information
    program_name = str(argv[0])
    (hook_path, hook_name) = os.path.split(program_name)
    if DEBUG_FLAG:
        sys.stderr.write('************ START **************\n')
        sys.stderr.write('Hook program: %s\n' % str(program_name))
        sys.stderr.write('Hook path: %s\n' % str(hook_path))
        sys.stderr.write('Hook name: %s\n' % str(hook_name))
        sys.stderr.write('*********************************\n')

    # Output the program name start
    if SUMMARY_FLAG:
        sys.stderr.write('Start program name: %s\n' % str(program_name))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def shutdown_message(argv, return_code=0, files_processed=0):
    """Function display any shutdown messages and
    the program.

    Arguments:
        argv -- Command line parameters
        files_processed -- The number of files checked out
                           by the hook
        return_code - the return code to be used when the
                      program s

    Returns:
        Nothing
    """
    function_name = 'shutdown_message'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    program_name = str(argv[0])
    (hook_path, hook_name) = os.path.split(program_name)

    # Display a processing summary
    if SUMMARY_FLAG:
        sys.stderr.write('  Files processed: %d\n' % files_processed)
        sys.stderr.write('End program name: %s\n' % program_name)

    if DEBUG_FLAG:
        sys.stderr.write('************ END ****************\n')
        sys.stderr.write('Hook path: %s\n' % hook_path)
        sys.stderr.write('Hook name: %s\n' % hook_name)
        sys.stderr.write('Return code: %d\n' % return_code)
        sys.stderr.write('*********************************\n')
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("\n")

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    exit(return_code)


def display_timing(start_time=None, setup_time=None):
    """Function displays the elapsed time for various stages of the
    the program.

    Arguments:
        start_time -- Time the program started
        setup_time -- Time the setup stage of the program completed

    Returns:
        Nothing
    """
    function_name = 'display_timing'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Calculate the elapsed times
    if TIMING_FLAG:
        end_time = time.clock()
        if setup_time is None:
            setup_time = end_time
        if start_time is None:
            start_time = end_time
        sys.stderr.write('    Setup elapsed time: %s\n'
                         % str(setup_time - start_time))
        sys.stderr.write('    Execution elapsed time: %s\n'
                         % str(end_time - setup_time))
        sys.stderr.write('    Total elapsed time: %s\n'
                         % str(end_time - start_time))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def print_file_stream(stream_handle):
    """Function to print the byte stream handle from Popen
    to STDERR.

    Arguments:
        steam_handle -- a stream handle returned by the Popen
                        communicate function.

    Returns:
        Nothing
    """
    function_name = 'print_file_stream'
    if DEBUG_FLAG:
        sys.stderr.write('      Entered module %s\n' % function_name)

    # Output the contents of the stream handle if any exists
    if stream_handle:
        for line in stream_handle.strip().decode("utf-8").splitlines():
            sys.stderr.write("%s\n" % line)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('      Leaving module %s\n' % function_name)
    return


def dump_file_stream(stream_handle, stream_description):
    """Function to dump the byte stream handle from Popen
    to STDERR.

    Arguments:
        steam_handle -- a stream handle returned by the Popen
                        communicate function.
        stream_descrition -- a text description of the stream handle

    Returns:
        Nothing
    """
    function_name = 'dump_file_stream'
    if DEBUG_FLAG:
        sys.stderr.write('      Entered module %s\n' % function_name)

    # Output the stream handle description
    sys.stderr.write('        %s\n' % stream_description)

    # Output the contents of the stream handle if any exists
    if stream_handle:
        sys.stderr.write(stream_handle.strip().decode("utf-8"))
        sys.stderr.write("\n")

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('      Leaving module %s\n' % function_name)
    return


def dump_list(list_values, list_description, list_message):
    """Function to dump the byte stream handle from Popen
    to STDERR.

    Arguments:
        list_values -- a list of files to be output
        list_descrition -- a text description of the file being output

    Returns:
        Nothing
    """
    function_name = 'dump_list'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    sys.stderr.write("    %s\n" % list_message)
    list_num = 0
    for value in list_values:
        sys.stderr.write('      %s[%d]: %s\n'
                         % (list_description, list_num, value))
        list_num = list_num + 1

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def execute_cmd(cmd):
    """Execute the supplied program
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Process Popen handle
        Process stdout file handle
        Process stderr file handle
    """
    function_name = 'execute_cmd'
    if DEBUG_FLAG:
        sys.stderr.write('    Entered module %s\n' % function_name)
        sys.stderr.write('      cmd: %s\n' % str(cmd))

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        shutdown_message(argv=sys.argv,
                         return_code=1,
                         files_processed=0)

    # Execute the command
    sys.stderr.flush()
    cmd_handle = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
    if DEBUG_FLAG:
        sys.stderr.write('        cmd return code: %d\n'
                         % cmd_handle.returncode)
        sys.stderr.write('        stdout length: %d\n'
                         % len(cmd_stdout))
        sys.stderr.write('        stderr length: %s\n'
                         % len(cmd_stderr))
        dump_file_stream(stream_handle=cmd_stdout,
                         stream_description='STDOUT from check_for_cmd')
        dump_file_stream(stream_handle=cmd_stderr,
                         stream_description='STDERR from check_for_cmd')
    if cmd_stderr:
        print_file_stream(cmd_stderr)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('    Leaving module %s\n' % function_name)
    return cmd_stdout


def check_for_cmd(cmd):
    """Make sure that a program necessary for using this script is
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Nothing
    """
    function_name = 'check_for_cmd'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)
        sys.stderr.write('    Validating command is available\n')

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        shutdown_message(argv=sys.argv,
                         return_code=1,
                         files_processed=0)


    # Execute the command
    try:
        execute_cmd(cmd)

    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        print("CalledProcessError - Program '{}' not found! -- Exiting."
              .format(cmd))
        shutdown_message(argv=sys.argv,
                         return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        print("OSError - Required program '{}' not found! -- Exiting."
              .format(cmd))
        shutdown_message(argv=sys.argv,
                         return_code=err.errno,
                         files_processed=0)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def git_ls_files():
    """Find files that are relevant based on all files for the
       repository branch.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    function_name = 'git_ls_files'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    cmd = ['git', 'ls-files']

    # Get a list of all files in the current repository branch
    try:
        cmd_stdout = execute_cmd(cmd)

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError as err:
        shutdown_message(argv=sys.argv,
                         return_code=err.returncode,
                         files_processed=0)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return cmd_stdout


def get_modified_files():
    """Find files that were modified by the merge.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    function_name = 'get_modified_files'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    modified_file_list = []
    cmd = ['git', 'diff-tree', 'ORIG_HEAD', 'HEAD', '--name-only', '-r',
           '--diff-filter=ACMRT']

    if DEBUG_FLAG:
        sys.stderr.write('    Getting list of files modified\n')

    # Fetch the list of files modified by the last commit
    try:
        cmd_stdout = execute_cmd(cmd)

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError as err:
        # This is a new repository, so get a list of all files
        if err.returncode == 128:  # new repository
            cmd_stdout = git_ls_files()
        else:
            shutdown_message(argv=sys.argv,
                             return_code=err.returncode,
                             files_processed=0)

    # Convert the stdout stream to a list of files
    modified_file_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if modified_file_list and modified_file_list[0] == 'clean':
        if DEBUG_FLAG:
            sys.stderr.write('  No files found to process\n')
            sys.stderr.write('  Leaving module get_modified_files\n')
        shutdown_message(argv=sys.argv,
                         return_code=0,
                         files_processed=0)

    # Only return regular files.
    modified_file_list = [i for i in modified_file_list if os.path.isfile(i)]
    if DEBUG_FLAG:
        dump_list(list_values=modified_file_list,
                  list_description='Modified file found',
                  list_message='List modified files found')

    if VERBOSE_FLAG:
        sys.stderr.write('  %d modified files found for processing\n'
                         % len(modified_file_list))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return modified_file_list


def git_not_checked_in(files):
    """Find files that are modified but are not checked in.

    Arguments:
        None

    Returns:
        A list of modified files that are not checked in.
    """
    function_name = 'git_not_checked_in'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    cmd = ['git', 'status', '-s']

    # Get the list of files that are modified but not checked in
    try:
        cmd_stdout = execute_cmd(cmd)

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError as err:
        sys.stderr.write('  CalledProcessError in git_not_checked_id\n')
        shutdown_message(argv=sys.argv,
                         return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        sys.stderr.write('  OSError in git_not_checked_id\n')
        shutdown_message(argv=sys.argv,
                         return_code=err.errno,
                         files_processed=0)

    # Convert the stream output to a list of output lines
    modified_files_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if not modified_files_list:
        if DEBUG_FLAG:
            sys.stderr.write('  No modified files found to exclude\n')
            sys.stderr.write('  Leaving module git_not_checked_in\n')
        return files

    # Pull the file name (second field) of the output line and
    # remove any double quotes
    modified_files_list = [l.split(None, 1)[-1].strip('"')
                           for l in modified_files_list]
    if DEBUG_FLAG and modified_files_list:
        dump_list(list_values=modified_files_list,
                  list_description='modified file found',
                  list_message='Modified files found')

     # Remove any modified files from the list of files to process
    if modified_files_list:
        if DEBUG_FLAG:
            sys.stderr.write('  Removing non-committed modified files\n')
        files = [f for f in files if f not in modified_files_list]

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return files


def check_out_file(file_name):
    """Checkout file that has been modified by the latest commit.

    Arguments:
        file_name -- the file name to be checked out for smudging

    Returns:
        Nothing.
    """
    function_name = 'check_out_file'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)
        sys.stderr.write('    os file %s exists: %s\n'
                         % (file_name, str(os.path.isfile(file_name))))

    # Remove the file if it currently exists
    try:
        sys.stderr.flush()
        os.remove(file_name)
    except OSError as err:
        # Ignore a file not found error, it was being removed anyway
        if err.errno == errno.ENOENT:
            if DEBUG_FLAG:
                sys.stderr.write('Unable to remove file: %s  Error code: %d\n'
                                 % (file_name, err.errno))
        else:
            shutdown_message(argv=sys.argv,
                             return_code=err.errno,
                             files_processed=0)
    if DEBUG_FLAG:
        sys.stderr.write('    Removed os file %s exists: %s\n'
                         % (file_name, str(os.path.isfile(file_name))))

    cmd = ['git', 'checkout', '-f', '%s' % file_name]
    if DEBUG_FLAG:
        sys.stderr.write('    git_cmd: %s\n' % str(cmd))

    # Check out the file so that it is smudged
    try:
        sys.stderr.flush()
        execute_cmd(cmd)
    except subprocess.CalledProcessError as err:
        sys.stderr.write('  CalledProcessError in check_out_file\n')
        shutdown_message(argv=sys.argv,
                         return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        sys.stderr.write('  OSError in check_out_file\n')
        shutdown_message(argv=sys.argv,
                         return_code=err.errno,
                         files_processed=0)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


# Execute the main function
if __name__ == '__main__':
    main(argv=sys.argv)
