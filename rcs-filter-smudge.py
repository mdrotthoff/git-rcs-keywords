#! /usr/bin/env python
# # -*- coding: utf-8 -*

# $Author$
# $Date$
# $File$
# $Rev$
# $Revision$
# $Source$
# $Hash$

"""
rcs-keywords-filter-smudge

This module provides the code to smudge the local copy of the
file retreived from the git repository performing the various
keyword substitutions.
"""

import sys
import os
import re
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
ENVIRONMENT_DUMP_FLAG = False
VARIABLE_DUMP_FLAG = False


if CALL_GRAPH:
    from pycallgraph import PyCallGraph
    from pycallgraph.output import GraphvizOutput


def variable_dump(descriotion=None, globals=globals(), locals=locals()):
    """Function to dumps the contents pf the Python
    global and local varaibles.

    Arguments:
        globals - Global variable dictionary to dump
        locals  - Local variable dictionary to dump

    Returns:
        Nothing
    """

    # Dump the supplied variable dictionaries
    if VARIABLE_DUMP_FLAG:
        sys.stderr.write('Program: %s\n' % sys.argv[0])
        sys.stderr.write('Program global variables\n')
        for var_name in globals:
            sys.stderr.write('Name: %s   Value: %s\n' % (var_name, globals[var_name]))
        sys.stderr.write('\n\n')
        sys.stderr.write('Program local variables\n')
        for var_name in globals:
            sys.stderr.write('Name: %s   Value: %s\n' % (var_name, globals[var_name]))
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
            sys.stderr.write('Variable: %s   Value: %s\n' % (var, os.getenv(var)))
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


def git_log_attributes(git_field_log, full_file_name, git_field_name):
    """Function to dump the git log associated with the provided
    file name.

    Arguments:
        git_field_log -- a list of git log fields to capture
        full_file_name -- The full file name to be examined
        git_field_name -- Name of the attributes fields for the dictionary

    Returns:
        git_log -- Array of defined attribute dictionaries
    """
    # Format the git log command
    git_field_format = '%x1f'.join(git_field_log) + '%x1e'
    cmd = ['git',
           'log',
           '--date=iso8601',
           '--max-count=1',
           '--format=%s' % git_field_format,
           '--',
           str(full_file_name)]

    # Process the git log command
    try:
        cmd_handle = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
        if cmd_stderr:
            for line in cmd_stderr.strip().decode("utf-8").splitlines():
                sys.stderr.write("%s\n" % line)
    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        sys.stderr.write("CalledProcessError - Program {0} called by {1} not found! -- Exiting."
                         .format(str(cmd), str(cmd_source)))
        shutdown_message(return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        sys.stderr.write("OSError - Program {0} called by {1} not found! -- Exiting."
                         .format(str(cmd), str(cmd_source)))
        shutdown_message(return_code=err.errno,
                         files_processed=0)

    # If an error occurred, display the command output and exit
    # with the returned exit code
    if cmd_handle.returncode != 0:
        sys.stderr.write("Exiting -- git log return code: %s\n"
                         % str(cmd_handle.returncode))
        sys.stderr.write("Output text: %s\n"
                         % cmd_stdout.strip().decode("utf-8"))
        shutdown_message(return_code=cmd_handle.returncode, lines_processed=0)

    # Calculate replacement strings based on the git log results
    if cmd_stdout:
        # Convert returned values to a list of dictionaries
        git_log = cmd_stdout.strip().decode("utf-8")
        git_log = git_log.strip().split("\x1e")
        git_log = [row.strip().split("\x1f") for row in git_log]
        git_log = [dict(zip(git_field_name, row)) for row in git_log]
    else:
        git_log = []

    # Return from the function
    return git_log


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

    # Display the startup message
    if SUMMARY_FLAG:
        sys.stderr.write('Start %s: %s\n' % (sys.argv[0], sys.argv[1]))

    # Calculate the source file being smudged
    file_full_name = sys.argv[1]
    file_name = os.path.basename(file_full_name)

    # Define the fields to be extracted from the commit log
    git_field_name = ['hash', 'author_name', 'author_email', 'commit_date']
    git_field_log = ['%H', '%an', '%ae', '%ci']

    # List the provided parameters
    if VERBOSE_FLAG:
        dump_list(list_values=sys.argv,
                  list_description='Param',
                  list_message='Parameter list')

    # Define the various substitution regular expressions
    author_regex = re.compile(r"\$Author: +[.\w@<> ]+ +\$|\$Author\$",
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

    # Format the git log command
    git_log = git_log_attributes(git_field_log=git_field_log,
                                 full_file_name=file_full_name,
                                 git_field_name=git_field_name)

    if git_log:
        # Calculate the replacement strings based on the git log results
        git_hash = '$Hash:     %s $' % str(git_log[0]['hash'])
        git_author = '$Author:   %s <%s> $' % (str(git_log[0]['author_name']),
                                               str(git_log[0]['author_email']))
        git_date = '$Date:     %s $' % str(git_log[0]['commit_date'])
        git_rev = '$Rev:      %s $' % str(git_log[0]['commit_date'])
        git_revision = '$Revision: %s $' % str(git_log[0]['commit_date'])
        git_file = '$File:     %s $' % str(file_name)
        git_source = '$Source:   %s $' % str(file_full_name)
        git_id = '$Id:       %s | %s | %s $' % (str(file_name),
                                                str(git_log[0]['commit_date']),
                                                str(git_log[0]['author_name']))
    else:
        # Build a empty keyword list if no source data was found
        # Note: the unusual means of building the list is to keep
        #       the code from being modified while using keywords!
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
