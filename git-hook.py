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

    # Parameter processing
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
#        program_name = str(argv[0])
        sys.stderr.write('Start program name: %s\n' % program_name)

    # List the provided parameters
    if VERBOSE_FLAG:
        sys.stderr.write("  Parameter list\n")
        param_num = 0
        for param in argv:
            sys.stderr.write('    Param[%d]: %s\n'
                             % (param_num, param))
            param_num = param_num + 1

    # Show the OS environment variables
    if DEBUG_FLAG:
        sys.stderr.write('  Environment variables defined\n')
        for key, value in sorted(os.environ.items()):
            sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
        sys.stderr.write("\n")

    # Verify that the named hook directory is a directory
    list_dir = program_name + '.d'
    if not os.path.isdir(list_dir):
        sys.stderr.write('The hook directory %s is not a directory\n'
                         % list_dir)
        exit(0)
    elif DEBUG_FLAG:
        sys.stderr.write('The hook directory %s is a directory\n' % list_dir)
        sys.stderr.write("\n")

    # Calculate the setup elapsed time
    if TIMING_FLAG:
        setup_time = time.clock()

    # Show the OS files in the hook named directory
    if DEBUG_FLAG:
        sys.stderr.write('OS Files existing in the hook named directory %s\n'
                         % list_dir)
        for file_name in sorted(os.listdir(list_dir)):
            file_stat = os.lstat(os.path.join(list_dir,
                                              file_name))
            file_mtime = str(time.strftime('%x %X', \
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
                sys.stderr.write('  Executing hook program %s\n' % hook_program)
            hook_call = subprocess.call([hook_program], shell=True)
            if DEBUG_FLAG:
                sys.stderr.write('Hook return code %s\n' % hook_call)
            if hook_call > 0:
                exit(hook_call)

    # Calculate the elapsed times
    if TIMING_FLAG:
        end_time = time.clock()
        sys.stderr.write('Setup elapsed time: %s\n'
                         % str(setup_time - start_time))
        sys.stderr.write('Execution elapsed time: %s\n'
                         % str(end_time - setup_time))
        sys.stderr.write('Total elapsed time: %s\n'
                         % str(end_time - start_time))

    # Display a processing summary
    if VERBOSE_FLAG:
        sys.stderr.write('Hooks seen: %d\n' % hook_count)
        sys.stderr.write('Hooks executed: %d\n' % hook_executed)
        sys.stderr.write("\n")

    # Output the program end
    if SUMMARY_FLAG:
        sys.stderr.write('End program name: %s\n' % program_name)
        sys.stderr.write("\n")
    elif DEBUG_FLAG:
        sys.stderr.write('************ END ****************\n')
        sys.stderr.write('Hook path: %s\n' % hook_path)
        sys.stderr.write('Hook name: %s\n' % hook_name)
        sys.stderr.write('*********************************\n')
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("\n")

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('    Leaving module dump_file_stream\n')
    return


# Execute the main function
if __name__ == '__main__':
    main(argv=sys.argv)
