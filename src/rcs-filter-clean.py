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
__project__ = "git-rcs-keywords"
__version__ = "1.1.1-dev1-4"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"

# LOGGING_CONSOLE_LEVEL = None
# LOGGING_CONSOLE_LEVEL = logging.DEBUG
# LOGGING_CONSOLE_LEVEL = logging.INFO
# LOGGING_CONSOLE_LEVEL = logging.WARNING
LOGGING_CONSOLE_LEVEL = logging.ERROR
# LOGGING_CONSOLE_LEVEL = logging.CRITICAL
LOGGING_CONSOLE_MSG_FORMAT = \
    '%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(lineno)s: %(message)s'
LOGGING_CONSOLE_DATE_FORMAT = '%Y-%m-%d %H.%M.%S'

# LOGGING_FILE_LEVEL = None
LOGGING_FILE_LEVEL = logging.DEBUG
# LOGGING_FILE_LEVEL = logging.INFO
# LOGGING_FILE_LEVEL = logging.WARNING
# LOGGING_FILE_LEVEL = logging.ERROR
# LOGGING_FILE_LEVEL = logging.CRITICAL
LOGGING_FILE_MSG_FORMAT = LOGGING_CONSOLE_MSG_FORMAT
LOGGING_FILE_DATE_FORMAT = LOGGING_CONSOLE_DATE_FORMAT
# LOGGING_FILE_NAME = '.git-hook.clean.log'
LOGGING_FILE_NAME = '.git-hook.log'

# Conditionally map a time function for performance measurement
# depending on the version of Python used
if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
    from time import perf_counter as get_clock
else:
    from time import clock as get_clock


def configure_logging():
    """Configure the logging service"""

    # Configure the console logger
    if LOGGING_CONSOLE_LEVEL:
        console = logging.StreamHandler()
        console.setLevel(LOGGING_CONSOLE_LEVEL)
        console_formatter = logging.Formatter(
            fmt=LOGGING_CONSOLE_MSG_FORMAT,
            datefmt=LOGGING_CONSOLE_DATE_FORMAT,
        )
        console.setFormatter(console_formatter)

    # Create an file based logger if a LOGGING_FILE_LEVEL is defined
    if LOGGING_FILE_LEVEL:
        logging.basicConfig(
            level=LOGGING_FILE_LEVEL,
            format=LOGGING_FILE_MSG_FORMAT,
            datefmt=LOGGING_FILE_DATE_FORMAT,
            filename=LOGGING_FILE_NAME,
        )

    # Basic logger configuration
    if LOGGING_CONSOLE_LEVEL or LOGGING_FILE_LEVEL:
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)
        if LOGGING_CONSOLE_LEVEL:
            # Add the console logger to default logger
            logger.addHandler(console)


def clean():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """

    # Display the parameters passed on the command line
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('sys.argv parameter count %d', len(sys.argv))
    logging.debug('sys.argv parameters %s', sys.argv)

    # Calculate the source file being cleaned
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = '<Unknown file>'
    logging.info('Processing file: %s', file_name)

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
    except Exception as err:
        logging.info('Exception cleaning file %s',
                     file_name,
                     exc_info=True)
        logging.debug('Generic exception variables: %s', vars(err))
        logging.error('Exception smudging file %s - Keywords not replaced',
                      file_name)
        exit(2)

    end_time = get_clock()
    logging.debug('Line count: %d', line_count)
    logging.info('Elapsed time: %f', (end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    configure_logging()

    START_TIME = get_clock()
    logging.debug('Entered module')

    clean()

    END_TIME = get_clock()
    logging.info('Elapsed time: %f', (END_TIME - START_TIME))
