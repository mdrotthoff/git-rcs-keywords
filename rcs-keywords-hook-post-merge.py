#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$

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
DEBUG_FLAG = bool(True)
TIMING_FLAG = bool(False)
if DEBUG_FLAG:
    TIMING_FLAG = bool(True)
VERBOSE_FLAG = bool(True)
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
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module main\n')

    # Set the start time for calculating elapsed time
    if TIMING_FLAG:
        start_time = time.clock()

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

    # List the provided parameters
    if VERBOSE_FLAG:
        sys.stderr.write("  Parameter list\n")
        dump_list(list_values=argv,
                  list_description='    Param')
##        param_num = 0
#        for param in argv:
#            sys.stderr.write('    Param[%d]: %s\n'
#                             % (param, argv[param]))
##            param_num = param_num + 1

    # Show the OS environment variables
    if DEBUG_FLAG:
        sys.stderr.write('  Environment variables defined\n')
        for key, value in sorted(os.environ.items()):
            sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
        sys.stderr.write("\n")

    # Check if git is available.
    if DEBUG_FLAG:
        sys.stderr.write('  Validating git is installed\n')
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of modified files
    if DEBUG_FLAG:
        sys.stderr.write('  Getting list of files modified\n')
    files = get_modified_files()

    # If no files are returned, there is no work to be done
    if len(files) == 0:
        if VERBOSE_FLAG:
            sys.stderr.write('  %d files found for processing\n' % len(files))
            sys.stderr.write('  Exiting')
        sys.exit(0)

    # Get the list of modified files to exclude from the list of files
    # to process
    modified_files_list = git_not_checked_in()
    if len(modified_files_list) > 0:
        if DEBUG_FLAG:
            sys.stderr.write('  Removing non-committed modified files\n')
            for file_name in files:
                sys.stderr.write('    Checking File name %s\n' % file_name)
                if file_name not in modified_files_list:
                    sys.stderr.write('    File name %s not in modified file list\n'
                                     % file_name)
                else:
                    sys.stderr.write('    File name %s IS in modified file list\n'
                                     % file_name)
        files = [f for f in files if f not in modified_files_list]
    elif DEBUG_FLAG:
        sys.stderr.write('  Modified files list length: %d\n'
                         % len(modified_files_list))

    # If no files remain, there is no work to be done
    if len(files) == 0:
        if VERBOSE_FLAG:
            sys.stderr.write('  %d files remain for processing\n' % len(files))
            sys.stderr.write('  Exiting')
        sys.exit(0)

    # TODO:  Add code to restrict files based on attribite file?
    # TODO:  Add code to limit files based on keyword contents?
    #for fn in kwfn:

    # Calculate the setup elapsed time
    if TIMING_FLAG:
        setup_time = time.clock()

    # Process the remaining file list
    if DEBUG_FLAG:
        sys.stderr.write('  Processing the remaining file list\n')
    files_processed = 0
    files.sort()
    for file_name in files:
        if DEBUG_FLAG:
            sys.stderr.write('  Checking out file %s\n' % file_name)
        check_out_file(file_name=file_name)
        files_processed = files_processed + 1

    # Calculate the elapsed times
    if TIMING_FLAG:
        end_time = time.clock()
        sys.stderr.write('Setup elapsed time: %s\n'
                         % str(setup_time - start_time))
        sys.stderr.write('Execution elapsed time: %s\n'
                         % str(end_time - setup_time))
        sys.stderr.write('Total elapsed time: %s\n'
                         % str(end_time - start_time))
        sys.stderr.write('Files processed: %s\n'
                         % str(files_processed))

    # Display a processing summary
    if SUMMARY_FLAG:
        sys.stderr.write('Files processed: %s\n' % str(files_processed))

    # Output the program end
    if VERBOSE_FLAG:
        sys.stderr.write('End program name: %s\n' % str(program_name))
        sys.stderr.write("\n")
    elif DEBUG_FLAG:
        sys.stderr.write('************ END ****************\n')
        sys.stderr.write('Hook path: %s\n' % str(hook_path))
        sys.stderr.write('Hook name: %s\n' % str(hook_name))
        sys.stderr.write('*********************************\n')
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("\n")

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module main\n')
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
    if VERBOSE_FLAG:
        sys.stderr.write('    Entered module dump_file_stream\n')

    # Output the stream handle description
    sys.stderr.write('      %s\n' % stream_description)

    # Output the contents of the stream handle if any exists
    if len(stream_handle) > 0:
        sys.stderr.write(stream_handle.strip().decode("utf-8"))
        sys.stderr.write("\n")

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('    Leaving module dump_file_stream\n')
    return


def dump_list(list_values, list_description):
    """Function to dump the byte stream handle from Popen
    to STDERR.

    Arguments:
        list_values -- a list of files to be output
        list_descrition -- a text description of the file being output

    Returns:
        Nothing
    """
    if VERBOSE_FLAG:
        sys.stderr.write('    Entered module dump_file_list\n')

    list_num = 0
    for value in list_values:
        sys.stderr.write('      %s[%d]: %s\n'
                         % (list_description, list_num, value))
        list_num = list_num + 1

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('    Leaving module dump_file_list\n')
    return


def check_for_cmd(cmd):
    """Make sure that a program necessary for using this script is
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Nothing
    """
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module check_for_cmd\n')
    if DEBUG_FLAG:
        sys.stderr.write('  cmd: %s\n' % str(cmd))

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str):
        if ' ' in cmd:
            raise ValueError('No spaces in single command allowed.')

    # Execute the command
    try:
        if DEBUG_FLAG:
            sys.stderr.write('  cmd: %s\n' % str(cmd))

        cmd_return = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_return.communicate()
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description='STDOUT from check_for_cmd')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description='STDERR from check_for_cmd')

    # If the command fails, notify the user and exit immediately
    except (subprocess.CalledProcessError, OSError):
        print "Required program '{}' not found! -- Exiting.".format(cmd)
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from check_for_cmd error')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from check_for_cmd error')
#        sys.exit(1)
        raise

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module check_for_cmd\n')
    return


def git_ls_files():
    """Find files that are relevant based on all files for the
       repository branch.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module git_ls_files\n')

    # Get a list of all files in the current repository branch
    try:
        cmd = ['git', 'ls-files']
        if DEBUG_FLAG:
            sys.stderr.write('  git_cmd: %s\n' % str(cmd))

        cmd_return = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_return.communicate()
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from git_ls_files')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from git_ls_files')

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError:
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from git_ls_files error')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from git_ls_files error')
        if VERBOSE_FLAG:
            sys.stderr.write('  Leaving module git_ls_files\n')
#        sys.exit(1)
        raise

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module git_ls_files\n')
    return cmd_stdout


def get_modified_files():
    """Find files that were modified bby the merge.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module get_modified_files\n')
    file_list = []

    # Fetch the list of files modified by the last commit
    try:
        cmd = ['git', 'diff-tree', 'ORIG_HEAD', 'HEAD', '--name-only', '-r',
               '--diff-filter=ACMRT']
        if DEBUG_FLAG:
            sys.stderr.write('  git_cmd: %s\n' % str(cmd))

        # Get the list of files modified during the last commit
        cmd_return = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_return.communicate()
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from get_modified_files')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from get_modified_files')

    # if an exception occurs, get a full list of all files or raise
    # it to the caller
    except subprocess.CalledProcessError as err:
        # This is a new repository, so get a list of all files
        if err.returncode == 128:  # new repository
            cmd_stdout = git_ls_files()
        else:
            if DEBUG_FLAG:
                sys.stderr.write('    git exit code: %s\n'
                                 % str(cmd_return.returncode))
                sys.stderr.write('    stdout length: %s\n'
                                 % str(len(cmd_stdout)))
                sys.stderr.write('    stderr length: %s\n'
                                 % str(len(cmd_stderr)))
                dump_file_stream(stream_handle=cmd_stdout,
                                 stream_description=
                                 'STDOUT from get_modified_files error')
                dump_file_stream(stream_handle=cmd_stderr,
                                 stream_description=
                                 'STDERR from get_modified_files error')
            raise

    # Convert the stdout stream to a list of files
    file_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if len(file_list) == 1 and file_list[0] is 'clean':
        if DEBUG_FLAG:
            sys.stderr.write('  No files found to process\n')
            sys.stderr.write('  Leaving module get_modified_files\n')
        return []

    # List the files found
    if DEBUG_FLAG:
        sys.stderr.write('    File list length: %d\n' % len(file_list))
        sys.stderr.write('    List files found\n')
        dump_list(list_values=file_list,
                  list_description='      file found')

    # Only return regular files.
    file_list = [i for i in file_list if os.path.isfile(i)]
    if DEBUG_FLAG:
        sys.stderr.write('    List real files found\n')
        dump_list(list_values=file_list,
                  list_description='      Real file found')

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module get_modified_files\n')
    return file_list


def git_not_checked_in():
    """Find files that are modified but are not checked in.

    Arguments:
        None

    Returns:
        A list of modified files that are not checked in.
    """
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module git_not_checked_in\n')

    # Get the list of files that are modified but not checked in
    try:
        cmd = ['git', 'status', '-s']
        if DEBUG_FLAG:
            sys.stderr.write('  git_cmd: %s\n' % str(cmd))
        cmd_return = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_return.communicate()
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from git_not_checked_in')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from git_not_checked_in')

    # If an exception occurs, just re-raise the exception
    except (subprocess.CalledProcessError, OSError):
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from git_not_checked_in error')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from git_not_checked_in error')
        raise

    # Convert the stream output to a list of output lines
    modified_files_list = cmd_stdout.decode('utf8').splitlines()
    if DEBUG_FLAG:
        sys.stderr.write('    Status files found\n')
#        for file_name in modified_files_list:
#            sys.stderr.write('      status file found: %s\n' % str(file_name))
        dump_list(list_values=modified_files_list,
                  list_description='      status file found')

    # Deal with unmodified repositories
    if len(modified_files_list) == 0:
        if DEBUG_FLAG:
            sys.stderr.write('  No modified files found to process\n')
            sys.stderr.write('  Leaving module git_not_checked_in\n')
        return []

    # Pull the file name (second field) of the output line and
    # remove any double quotes
    modified_files_list = [l.split(None, 1)[-1].strip('"')
                           for l in modified_files_list]
    if DEBUG_FLAG:
        sys.stderr.write('    Modified files found\n')
#        for file_name in modified_files_list:
#            sys.stderr.write('      modified file found: %s\n' % str(file_name))
        dump_list(list_values=modified_files_list,
                  list_description='      modified file found')

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module git_not_checked_in\n')
    return modified_files_list


def check_out_file(file_name):
    """Checkout file that has been modified by the latest commit.

    Arguments:
        file_name -- the file name to be checked out for smudging

    Returns:
        Nothing.
    """
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module check_out_file\n')

    # Remove the file if it currently exists
    try:
        if DEBUG_FLAG:
            sys.stderr.write('  os file %s exists: %s\n'
                             % (file_name, str(os.path.isfile(file_name))))
        os.remove(file_name)
    except OSError as err:
        # Ignore a file not found error, it was being removed anyway
        if err.errno == errno.ENOENT:
            if DEBUG_FLAG:
                sys.stderr.write('Unable to remove file: %s  Error code: %d\n'
                                 % (file_name, err.errno))
        else:
            raise
    if DEBUG_FLAG:
        sys.stderr.write('  Removed os file %s exists: %s\n'
                         % (file_name, str(os.path.isfile(file_name))))

    # Check out the file so that it is smudged
    try:
        cmd = ['git', 'checkout', '-f', '%s' % file_name]
        if DEBUG_FLAG:
            sys.stderr.write('  git_cmd: %s\n' % str(cmd))
        cmd_return = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_return.communicate()
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from check_out_file')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from check_out_file')

    except (subprocess.CalledProcessError, OSError):
        if DEBUG_FLAG:
            sys.stderr.write('    git exit code: %s\n'
                             % str(cmd_return.returncode))
            sys.stderr.write('    stdout length: %s\n'
                             % str(len(cmd_stdout)))
            sys.stderr.write('    stderr length: %s\n'
                             % str(len(cmd_stderr)))
            dump_file_stream(stream_handle=cmd_stdout,
                             stream_description=
                             'STDOUT from check_out_file')
            dump_file_stream(stream_handle=cmd_stderr,
                             stream_description=
                             'STDERR from check_out_file')
#        sys.exit(1)
        raise

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module check_out_file\n')
    return


# Execute the main function
if __name__ == '__main__':
    main(argv=sys.argv)
