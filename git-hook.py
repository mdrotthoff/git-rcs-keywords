#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$


"""git-hook

This module acts as a MPC for each git hook event it is registered
against.  A symlink is created between the hook name and the program
that tells it what event is executing.  The correspoinding .d
directory is read and all executable programs are run.  All parameters
received by the module are passed along to each of the executed
programs.

"""


import sys
import os
import stat
import subprocess
import time


# Set the debugging flag
DEBUG_FLAG = bool(False)
TIMING_FLAG = bool(False)
if DEBUG_FLAG:
    TIMING_FLAG = bool(True)
VERBOSE_FLAG = bool(True)
if TIMING_FLAG:
    VERBOSE_FLAG = bool(True)
SUMMARY_FLAG = bool(True)
if VERBOSE_FLAG:
    SUMMARY_FLAG = bool(True)


def startup_message():
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
    program_name = str(sys.argv[0])
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


def shutdown_message(return_code=0, hook_count=0, hook_executed=0):
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

    program_name = str(sys.argv[0])
    (hook_path, hook_name) = os.path.split(program_name)

    # Display a processing summary
    if SUMMARY_FLAG:
        sys.stderr.write('Hooks seen: %d\n' % hook_count)
        sys.stderr.write('Hooks executed: %d\n' % hook_executed)
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


def main(argv):
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    function_name = 'main'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Set the start time for calculating elapsed time
    start_time = time.clock()

    # Display the startup message
    if SUMMARY_FLAG or DEBUG_FLAG:
        startup_message()

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

    # Verify that the named hook directory is a directory
    list_dir = sys.argv[0] + '.d'
    if not os.path.isdir(list_dir):
        sys.stderr.write('The hook directory %s is not a directory\n'
                         % list_dir)
        exit(0)
    if DEBUG_FLAG:
        sys.stderr.write('The hook directory %s is a directory\n' % list_dir)
        sys.stderr.write("\n")

    # Calculate the setup elapsed time
    setup_time = time.clock()

    # Show the OS files in the hook named directory
    if DEBUG_FLAG:
        sys.stderr.write('OS Files existing in the hook named directory %s\n'
                         % list_dir)
        for file_name in sorted(os.listdir(list_dir)):
            file_stat = os.lstat(os.path.join(list_dir,
                                              file_name))
            file_mtime = str(time.strftime('%x %X',
                                           time.localtime(file_stat.st_mtime)))
            file_size = str(file_stat.st_size)
            file_mode = str(oct(stat.S_IMODE(file_stat.st_mode)))
            file_type = ''
            if stat.S_ISLNK(file_stat.st_mode) > 0:
                file_type = file_type + ' Symlink'
            if stat.S_ISDIR(file_stat.st_mode) > 0:
                file_type = file_type + ' Directory'
            if stat.S_ISREG(file_stat.st_mode) > 0:
                file_type = file_type + ' Regular'
            sys.stderr.write('  File: %s   %s  %s bytes  %s  %s\n'
                             % (file_name,
                                file_mtime,
                                file_size,
                                file_mode,
                                file_type.strip()))
        sys.stderr.write("\n")

    # Execute each of the hooks found in the relevant directory
    hook_count = 0
    hook_executed = 0
    for file_name in sorted(os.listdir(list_dir)):
        hook_count = hook_count + 1
        hook_program = os.path.join(list_dir, file_name)
        if DEBUG_FLAG:
            sys.stderr.write('Saw hook program %s\n' % hook_program)
        if os.path.isfile(hook_program) and os.access(hook_program, os.X_OK):
            # If parameters were supplied, pass them through to the actual
            # hook program
            if len(argv) > 1:
                hook_program = '"%s" %s' % (hook_program,
                                            ' '.join('"%s"' % param
                                                     for param in argv[1:]))
            hook_executed = hook_executed + 1
            if VERBOSE_FLAG:
                sys.stderr.write('  Executing hook program %s\n'
                                 % hook_program)
            hook_call = subprocess.call([hook_program], shell=True)
            if DEBUG_FLAG:
                sys.stderr.write('Hook return code %s\n' % hook_call)
            if hook_call > 0:
                exit(hook_call)

    # Calculate the elapsed times
    if TIMING_FLAG:
        display_timing(start_time=start_time,
                       setup_time=setup_time)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    shutdown_message(return_code=0,
                     hook_count=hook_count,
                     hook_executed=hook_executed)
    return


# Execute the main function
if __name__ == '__main__':
    main(argv=sys.argv)
