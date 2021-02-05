#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
rcs-keywords-filter-clean

This module provides the code to clean the local copy of the
file of the keyword substitutions prior to commiting changes
back to the repository.
"""

import sys
# import os
import re

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-04 09:10:44"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__credits__ = []
__status__ = "Production"
# __license__ = "Python"


# def shutdown_message(return_code=0, lines_processed=0):
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


def main():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    # Define the various substitution regular expressions
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
    revision_regex = re.compile(r"\$Revision: +[-:\d+ ]+ +\$|\$Revision\$",
                                re.IGNORECASE)
    rev_regex = re.compile(r"\$Rev: +[-:\d+ ]+ +\$|\$Rev\$",
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

    shutdown_message(return_code=0)
    # return


# Execute the main function
if __name__ == '__main__':
    main()
