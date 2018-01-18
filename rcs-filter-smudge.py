#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Revision$
# $Source$
# $Hash$

"""rcs-keywords-filter-smudge

This module provides the code to smudge the local copy of the
file retreived from the git repository performing the various
keyword substitutions.

"""

import sys
import os
import re
import subprocess
import time
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


# Set the debugging flag
CALL_GRAPH_FLAG = bool(True)
DEBUG_FLAG = bool(False)
TIMING_FLAG = bool(False)
VERBOSE_FLAG = bool(False)
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
    if VERBOSE_FLAG:
        sys.stderr.write('Start program name: %s\n' % str(program_name))

    # Output the program name start
    if SUMMARY_FLAG:
        sys.stderr.write('%s: %s\n' % (str(program_name), sys.argv[1]))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


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
    function_name = 'shutdown_message'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    program_name = str(sys.argv[0])
    (hook_path, hook_name) = os.path.split(program_name)

    # Display a processing summary
    if SUMMARY_FLAG:
        sys.stderr.write('  Lines processed: %d\n' % lines_processed)
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
    function_name = 'git_log_attributes'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Format the git log command
    git_field_format = '%x1f'.join(git_field_log) + '%x1e'
    cmd = ['git',
           'log',
           '--date=iso8601',
           '--max-count=1',
           '--format=%s' % git_field_format,
           '--',
           str(full_file_name)]
#           '%s' % str(full_file_name)]
    if DEBUG_FLAG:
        sys.stderr.write('  git log cmd: %s\n' % str(cmd))

    # Process the git log command
    cmd_return = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = cmd_return.communicate()
    if DEBUG_FLAG:
        sys.stderr.write('  git exit code: %s\n' % str(cmd_return.returncode))
        sys.stderr.write('  stdout length: %s\n' % str(len(cmd_stdout)))
        sys.stderr.write('  stderr length: %s\n' % str(len(cmd_stderr)))

    # If an error occurred, display the command output and exit
    # with the returned exit code
    if cmd_return.returncode != 0:
        sys.stderr.write("Exiting -- git log return code: %s\n"
                         % str(cmd_return.returncode))
        sys.stderr.write("Output text: %s\n"
                         % cmd_stdout.strip().decode("utf-8"))
        sys.stderr.write("Error message: %s\n"
                         % cmd_stderr.strip().decode("utf-8"))
        shutdown_message(return_code=cmd_return.returncode, lines_processed=0)

    if cmd_stderr:
        sys.stderr.write('STDERR from command %s\n' % str(cmd))
        sys.stderr.write(cmd_stderr.strip().decode("utf-8"))
        sys.stderr.write("\n")

    # Calculate replacement strings based on the git log results
    if cmd_stdout:
        if DEBUG_FLAG:
            sys.stderr.write('STDOUT from command %s\n' % str(cmd))
            sys.stderr.write(cmd_stdout.strip().decode("utf-8"))
            sys.stderr.write("\n")
        # Convert returned values to a list of dictionaries
        git_log = cmd_stdout.strip().decode("utf-8")
        git_log = git_log.strip().split("\x1e")
        git_log = [row.strip().split("\x1f") for row in git_log]
        git_log = [dict(zip(git_field_name, row)) for row in git_log]
    else:
        git_log = []

    if DEBUG_FLAG:
        sys.stderr.write('git_log: %s\n' % str(git_log))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return git_log


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
    startup_message()

    # Calculate the source file being smudged
    file_full_name = argv[1]
    file_name = os.path.basename(file_full_name)

    # Define the fields to be extracted from the commit log
    git_field_name = ['hash', 'author_name', 'author_email', 'commit_date']
    git_field_log = ['%H', '%an', '%ae', '%ci']

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

    # Display the name of the file being smudged
    if VERBOSE_FLAG or DEBUG_FLAG:
        sys.stderr.write('  Smudge file full name: %s\n' % str(file_full_name))

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

    # Display the smudging values (debugging)
    if DEBUG_FLAG:
        sys.stderr.write('git hash:     %s\n' % git_hash)
        sys.stderr.write('git author:   %s\n' % git_author)
        sys.stderr.write('git date:     %s\n' % git_date)
        sys.stderr.write('git rev:      %s\n' % git_rev)
        sys.stderr.write('git revision: %s\n' % git_revision)
        sys.stderr.write('git file:     %s\n' % git_file)
        sys.stderr.write('git source:   %s\n' % git_source)
        sys.stderr.write('git id:       %s\n' % git_id)
        sys.stderr.write("\n")

    # Calculate the setup elapsed time
    setup_time = time.clock()

    # Process each of the rows found on stdin
    line_count = 0
    for line in sys.stdin:
        line_count = line_count + 1
        line = author_regex.sub(git_author, line)
        line = id_regex.sub(git_id, line)
        line = date_regex.sub(git_date, line)
        line = source_regex.sub(git_source, line)
        line = file_regex.sub(git_file, line)
        line = revision_regex.sub(git_revision, line)
        line = rev_regex.sub(git_rev, line)
        line = hash_regex.sub(git_hash, line)
        sys.stdout.write(line)
        if DEBUG_FLAG:
            sys.stderr.write(line)

    # Calculate the elapsed times
    if TIMING_FLAG:
        display_timing(start_time=start_time,
                       setup_time=setup_time)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    shutdown_message(return_code=0, lines_processed=line_count)
    return


# Execute the main function
if __name__ == '__main__':
    if CALL_GRAPH_FLAG:
        graphviz = GraphvizOutput()
        graphviz.output_type = 'pdf'
        graphviz.output_file = {os.path.basename(sys.argv[0])
                                + '.' + graphviz.output_type}
        sys.stderr.write('Writing %s file: %s\n'
                         % (graphviz.output_type, graphviz.output_file))
        with PyCallGraph(output=graphviz):
            main(argv=sys.argv)
    else:
        main(argv=sys.argv)
