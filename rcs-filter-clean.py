#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
rcs-keywords-filter-clean

This module provides the code to clean the local copy of the
file of the keyword substitutions prior to commiting changes
back to the repository.
"""

import sys
import re
import logging

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"

LOGGING_LEVEL = None
LOGGING_LEVEL = logging.DEBUG
# LOGGING_LEVEL = logging.INFO
# LOGGING_LEVEL = logging.WARNING
# LOGGING_LEVEL = logging.ERROR

# Conditionally map a time function for performance measurement
# depending on the version of Python used
if LOGGING_LEVEL:
    if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
        from time import perf_counter as get_clock
    else:
        from time import clock as get_clock
else:
    def get_clock():
        """Dummy get_clock function for when the timing flag is not set"""
        pass


def clean_input():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """

    # Display the parameters passed on the command line
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('sys.argv parameter count %d' % len(sys.argv))
        logging.debug('sys.argv parameters %s' % sys.argv)

    # Calculate the source file being cleaned
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = '<Unknown file>'

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
    try:
        for line in sys.stdin:
            line_count += 1
            if line.count('$') > 1:
                line = author_regex.sub(git_author, line)
                line = id_regex.sub(git_id, line)
                line = date_regex.sub(git_date, line)
                line = source_regex.sub(git_source, line)
                line = file_regex.sub(git_file, line)
                line = revision_regex.sub(git_revision, line)
                line = rev_regex.sub(git_rev, line)
                line = hash_regex.sub(git_hash, line)
            sys.stdout.write(line)
    except Exception:
        logging.error('Exception cleaning file %s' % file_name, exc_info=True)
        sys.stderr.write('Exception smudging file %s - Key words were not replaced\n' % file_name)
        exit(2)

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Line count in %s: %s' % (sys._getframe().f_code.co_name, line_count))
        logging.info('Elapsed for %s: %s' % (sys._getframe().f_code.co_name, end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    # Initialize logging
    if LOGGING_LEVEL:
        if LOGGING_LEVEL <= logging.INFO:
            start_time = get_clock()
        logging.basicConfig(
            level=LOGGING_LEVEL,
            format='%(levelname)s: %(message)s',
            filename='.git-hook.clean.log')
        logging.debug('')
        logging.debug('')
        logging.debug('Executing: %s' % sys.argv[0])
    clean_input()

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s' % (sys.argv[0], end_time - start_time))
