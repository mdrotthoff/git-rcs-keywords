#! /usr/bin/env python
# # -*- coding: utf-8 -*

# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$


"""
git-hook

This module acts as a MCP for each git hook event it is registered
against.  A symlink is created between the hook name and the program
that tells it what event is executing.  The correspoinding .d
directory is read and all executable programs are run.  All parameters
received by the module are passed along to each of the executed
programs.
"""


import sys
import os
import subprocess
import time


__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__credits__ = []
__status__ = "Production"
# __license__ = "Python"


# Set the debugging flag
CALL_GRAPH = False
TIMING_FLAG = False
VERBOSE_FLAG = False
SUMMARY_FLAG = False


if CALL_GRAPH:
    from pycallgraph import PyCallGraph
    from pycallgraph.output import GraphvizOutput


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
    # Display a processing summary
    if SUMMARY_FLAG:
        sys.stderr.write('Hooks seen: %d\n' % hook_count)
        sys.stderr.write('Hooks executed: %d\n' % hook_executed)
        sys.stderr.write('End program name: %s\n' % sys.argv[0])

    # Return from the function
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
    # Calculate the elapsed times
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
    sys.stderr.write("    %s\n" % list_message)
    list_num = 0
    for value in list_values:
        sys.stderr.write('      %s[%d]: %s\n'
                         % (list_description, list_num, value))
        list_num += 1

    # Return from the function
    return


def main():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    # Set the start time for calculating elapsed time
    start_time = time.clock()

    # Display the startup message
    if SUMMARY_FLAG:
        sys.stderr.write('Start program name: %s\n' % sys.argv[0])

    # List the provided parameters
    if VERBOSE_FLAG:
        dump_list(list_values=sys.argv,
                  list_description='Param',
                  list_message='Parameter list')

    # Verify that the named hook directory is a directory
    list_dir = sys.argv[0] + '.d'
    if not os.path.isdir(list_dir):
        sys.stderr.write('The hook directory %s is not a directory\n'
                         % list_dir)
        exit(0)

    # Calculate the setup elapsed time
    setup_time = time.clock()

    # Execute each of the hooks found in the relevant directory
    hook_count = 0
    hook_executed = 0
    for file_name in sorted(os.listdir(list_dir)):
        hook_count += 1
        hook_program = os.path.join(list_dir, file_name)
        if os.path.isfile(hook_program) and os.access(hook_program, os.X_OK):
            # If parameters were supplied, pass them through to the actual
            # hook program
            if len(sys.argv) > 1:
                hook_program = '"%s" %s' % (hook_program,
                                            ' '.join('"%s"' % param
                                                     for param in sys.argv[1:]))
            hook_executed += 1
            if VERBOSE_FLAG:
                sys.stderr.write('  Executing hook program %s\n'
                                 % hook_program)
            hook_call = subprocess.call([hook_program], shell=True)
            if hook_call > 0:
                exit(hook_call)

    # Calculate the elapsed times
    if TIMING_FLAG:
        display_timing(start_time=start_time,
                       setup_time=setup_time)

    # Return from the function
    shutdown_message(return_code=0,
                     hook_count=hook_count,
                     hook_executed=hook_executed)
    return


def call_graph():
    """Call_graph execution

    Arguments:
        None

    Returns:
        Nothing
    """
    graphviz = GraphvizOutput()
    graphviz.output_type = 'pdf'
    graphviz.output_file = (os.path.splitext(os.path.basename(sys.argv[0]))[0]
                            + '-' + time.strftime("%Y%m%d-%H%M%S")
                            + '.' + graphviz.output_type)
    with PyCallGraph(output=graphviz):
        main()


# Execute the main function
if __name__ == '__main__':
    if CALL_GRAPH:
        call_graph()
    else:
        main()
