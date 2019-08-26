#! /usr/bin/env python
# # -*- coding: utf-8 -*

# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$

"""
rcs-keywords-filter-clean

This module provides the code to clean the local copy of the
file of the keyword substitutions prior to commiting changes
back to the repository.
"""

import sys
import os
import re
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
ENVIRONMENT_DUMP_FLAG = False
VARIABLE_DUMP_FLAG = False


if CALL_GRAPH:
    from pycallgraph import PyCallGraph
    from pycallgraph.output import GraphvizOutput


def variable_dump(description=None, global_var=globals(), local_var=locals()):
    """Function to dumps the contents pf the Python
    global and local variables.

    Arguments:
        globals - Global variable dictionary to dump
        locals  - Local variable dictionary to dump

    Returns:
        Nothing
    """

    # Dump the supplied variable dictionaries
    if VARIABLE_DUMP_FLAG:
        sys.stderr.write('Program: %s\n' % sys.argv[0])
        sys.stderr.write('Variables dump for %s\n' % description)
        sys.stderr.write('Program global variables\n')
        for var_name in global_var:
            sys.stderr.write('Name: %s   Value: %s\n'
                             % (var_name, global_var[var_name]))
        sys.stderr.write('\n\n')
        sys.stderr.write('Program local variables\n')
        for var_name in local_var:
            sys.stderr.write('Name: %s   Value: %s\n'
                             % (var_name, local_var[var_name]))
        sys.stderr.write('\n\n')


def environment_dump():
    """Function to dumpe the contents pf the environment
    that the program is executing under.

    Arguments:
        None

    Returns:
        Nothing
    """
    # Display a processing summary
    if ENVIRONMENT_DUMP_FLAG:
        sys.stderr.write('Program: %s\n' % sys.argv[0])
        sys.stderr.write('Environment variables\n')
        for var in os.environ:
            sys.stderr.write('Variable: %s   Value: %s\n'
                             % (var, os.getenv(var)))
        sys.stderr.write('\n\n')


def shutdown_message(return_code=0, lines_processed=0):
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
        sys.stderr.write('  Lines processed: %d\n' % lines_processed)
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


def main():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    # Set the start time for calculating elapsed time
    start_time = time.clock()

    # Dump the system environment variables
    environment_dump()

    # Calculate the source file being cleaned (if provided)
    if len(sys.argv) > 1:
        file_full_name = sys.argv[1]
    else:
        file_full_name = 'Not provided'

    # Display the startup message
    if SUMMARY_FLAG:
        sys.stderr.write('Start %s: %s\n' % (str(sys.argv[0]), file_full_name))

    # List the provided parameters
    if VERBOSE_FLAG:
        dump_list(list_values=sys.argv,
                  list_description='Param',
                  list_message='Parameter list')

    # Define the various substitution regular expressions
#    author_regex = re.compile(r"\$Author: +[\-.\w@<> ]+ +\$|\$Author\$",
#                              re.IGNORECASE)
    author_regex = re.compile(r"\$Author:.*\$",
                              re.IGNORECASE)
    id_regex = re.compile(r"\$Id: +.+ \| [-:\d ]+ \| .+ +\$|\$Id\$",
                          re.IGNORECASE)
    date_regex = re.compile(r"\$Date: +[-:\d ]+ +\$|\$Date\$",
                            re.IGNORECASE)
    source_regex = re.compile(r"\$Source: .+[.].+ \$|\$Source\$",
                              re.IGNORECASE)
    file_regex = re.compile(r"\$File: .+[.].+ \$|\$File\$",
                            re.IGNORECASE)
    revision_regex = re.compile(r"\$Revision: +[-:\d ]+ +\$|\$Revision\$",
                                re.IGNORECASE)
    rev_regex = re.compile(r"\$Rev: +[-:\d ]+ +\$|\$Rev\$",
                           re.IGNORECASE)
    hash_regex = re.compile(r"\$Hash: +\w+ +\$|\$Hash\$",
                            re.IGNORECASE)

    # Calculate empty strings based on the keyword
    git_hash = '$%s$' % 'Hash'
    git_author = '$%s$' % 'Author'
    git_date = '$%s$' % 'Date'
    git_rev = '$%s$' % 'Rev'
    git_revision = '$%s$' % 'Revision'
    git_file = '$%s$' % 'File'
    git_source = '$%s$' % 'Source'
    git_id = '$%s$' % 'Id'

    # Calculate the setup elapsed time
    setup_time = time.clock()

    # Process each of the rows found on stdin
    line_count = 0
    for line in sys.stdin:
        line_count += 1
        line = author_regex.sub(git_author, line)
        line = id_regex.sub(git_id, line)
        line = date_regex.sub(git_date, line)
        line = source_regex.sub(git_source, line)
        line = file_regex.sub(git_file, line)
        line = revision_regex.sub(git_revision, line)
        line = rev_regex.sub(git_rev, line)
        line = hash_regex.sub(git_hash, line)
        sys.stdout.write(line)

    # Calculate the elapsed times
    if TIMING_FLAG:
        display_timing(start_time=start_time,
                       setup_time=setup_time)

    # Return from the function
    shutdown_message(return_code=0, lines_processed=line_count)


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
