#! /usr/bin/env python
# # -*- coding: utf-8 -*

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
import logging
import pprint

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-04 09:10:44"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__credits__ = []
__status__ = "Production"
# __license__ = "Python"


def shutdown_message(return_code=0):
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
    exit(return_code)


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
        sys.stderr.write(
            "{0} - Program {1} called by {2} not found! -- Exiting."
            .format(str(err), str(cmd[0]), str(' '.join(cmd)))
        )
        shutdown_message(return_code=err.returncode)
    except OSError as err:
        sys.stderr.write(
            "{0} - Program {1} called by {2} not found! -- Exiting."
            .format(str(err), str(cmd[0]), str(' '.join(cmd)))
        )
        shutdown_message(return_code=err.errno)

    # If an error occurred, display the command output and exit
    # with the returned exit code
    if cmd_handle.returncode != 0:
        sys.stderr.write("Exiting -- git log return code: %s\n"
                         % str(cmd_handle.returncode))
        sys.stderr.write("Output text: %s\n"
                         % cmd_stdout.strip().decode("utf-8"))
        shutdown_message(return_code=cmd_handle.returncode)

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
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        filename='git-hook.dmr.log')

    # Calculate the source file being smudged
    file_full_name = sys.argv[1]
    file_name = os.path.basename(file_full_name)

    # Log the file being processed
    logging.debug('processing file %s' % file_full_name)

    # Define the fields to be extracted from the commit log
    git_field_name = ['hash', 'author_name', 'author_email', 'commit_date']
    git_field_log = ['%H', '%an', '%ae', '%ci']

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
        # log_git_author = git_log[0]['author_name'].split('\\')[-1]
        # log_git_author = git_log[0]['author_name'].replace('\\', '\\\\')
        # git_log[0]['author_name'].replace('\\', '\\\\')
        # git_hash = '$Hash:     %s $' % str(git_log[0]['hash'])
        # # git_author = '$Author:   %s <%s> $' % (str(log_git_author),
        # #                                        str(git_log[0]['author_email']))
        # git_author = '$Author:   %s <%s> $' % (str(git_log[0]['author_name']),
        #                                        str(git_log[0]['author_email']))
        # git_date = '$Date:     %s $' % str(git_log[0]['commit_date'])
        # git_rev = '$Rev:      %s $' % str(git_log[0]['commit_date'])
        # git_revision = '$Revision: %s $' % str(git_log[0]['commit_date'])
        # git_file = '$File:     %s $' % str(file_name)
        # git_source = '$Source:   %s $' % str(file_full_name)
        # # git_id = '$Id:       %s | %s | %s $' % (str(file_name),
        # #                                         str(git_log[0]['commit_date']),
        # #                                         str(log_git_author))
        # git_id = '$Id:       %s | %s | %s $' % (str(file_name),
        #                                         str(git_log[0]['commit_date']),
        #                                         str(git_log[0]['author_name']))

        git_hash = re.escape('$Hash:     %s $' % str(git_log[0]['hash']))
        git_author = re.escape('$Author:   %s <%s> $' % (str(git_log[0]['author_name']),
                                                         str(git_log[0]['author_email'])))
        git_date = re.escape('$Date:     %s $' % str(git_log[0]['commit_date']))
        git_rev = re.escape('$Rev:      %s $' % str(git_log[0]['commit_date']))
        git_revision = re.escape('$Revision: %s $' % str(git_log[0]['commit_date']))
        git_file = re.escape('$File:     %s $' % str(file_name))
        git_source = re.escape('$Source:   %s $' % str(file_full_name))
        git_id = re.escape('$Id:       %s | %s | %s $' % (str(file_name),
                                                          str(git_log[0]['commit_date']),
                                                          str(git_log[0]['author_name'])))

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

    # Process each of the rows found on stdin
    line_count = 0
    exception_occurred = 0
    for line in sys.stdin:
        try:
            line_count += 1
            source_line = line
            line = author_regex.sub(git_author, line)
            line = id_regex.sub(git_id, line)
            line = date_regex.sub(git_date, line)
            line = source_regex.sub(git_source, line)
            line = file_regex.sub(git_file, line)
            line = revision_regex.sub(git_revision, line)
            line = rev_regex.sub(git_rev, line)
            line = hash_regex.sub(git_hash, line)
            sys.stdout.write(line)
        # except Exception as err:
        except:
            # logging.error('KeyError on file %s' % file_full_name)
            # err.args += ('filename', file_full_name)
            # logging.error('Exception smudging file %s' % file_full_name, exc_info=True)
            # logging.error('Author name from git log %s' % str(git_log[0]['author_name']))
            if exception_occurred == 0:
                # logging.error('Author name from git log %s' % str(git_log[0]['author_name']))
                # logging.error('Author name: %s' % log_git_author)
                # logging.error('Exception smudging file %s' % file_full_name)
                logging.error('Exception smudging file %s' % file_full_name, exc_info=True)
                logging.info('git log attributes: %s' % git_log)
            # logging.exception('Exception processing file %s' % file_full_name, exc_info=True)
            # raise
            # exit(2)
            sys.stdout.write(source_line)
            exception_occurred = 1

    # Return from the function
    # shutdown_message(return_code=0, lines_processed=line_count)
    shutdown_message(return_code=0)


# Execute the main function
if __name__ == '__main__':
    main()
