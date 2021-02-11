#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
git-hook

This module acts as a MCP for each git hook event it is registered
against.  A symlink is created between the hook name and the program
that tells it what event is executing.  The corresponding .d
directory is read and all executable programs are run.  All parameters
received by the module are passed along to each of the executed
programs.
"""

import sys
import os
import subprocess
import logging

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__project__ = "git-rcs-keywords"
__version__ = "1.1.1-beta1-15"
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
# LOGGING_FILE_LEVEL = logging.DEBUG
LOGGING_FILE_LEVEL = logging.INFO
# LOGGING_FILE_LEVEL = logging.WARNING
# LOGGING_FILE_LEVEL = logging.ERROR
# LOGGING_FILE_LEVEL = logging.CRITICAL
LOGGING_FILE_MSG_FORMAT = LOGGING_CONSOLE_MSG_FORMAT
LOGGING_FILE_DATE_FORMAT = LOGGING_CONSOLE_DATE_FORMAT
# LOGGING_FILE_NAME = '.git-hook.manager.log'
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
        if LOGGING_CONSOLE_LEVEL:
            # Add the console logger to default logger
            logger.addHandler(console)


def process_hooks():
    """Main program.

    Returns:
        Nothing
    """
    # Display the parameters passed on the command line
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('sys.argv parameter count %d', len(sys.argv))
    logging.debug('sys.argv parameters %s', sys.argv)

    # Verify that the named hook directory is a directory
    list_dir = sys.argv[0] + '.d'
    if not os.path.isdir(list_dir):
        logging.info('The hook directory %s is not a directory', list_dir)
        exit(0)

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
                hook_program = '"%s" %s' \
                               % (hook_program,
                                  ' '.join('"%s"' % param
                                           for param in sys.argv[1:]))
            hook_executed += 1
            logging.info('Executing hook %s', hook_program)
            hook_call = subprocess.call([hook_program], shell=True)
            if hook_call > 0:
                end_time = get_clock()
                logging.info('Exiting - Hook program failed with error %s',
                             hook_call)
                logging.info('Elapsed time: %f', (end_time - start_time))
                exit(hook_call)

    end_time = get_clock()
    logging.debug('Hooks examined: %d', hook_count)
    logging.debug('Hooks executed: %d', hook_executed)
    logging.info('Elapsed time: %f', (end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    configure_logging()

    START_TIME = get_clock()
    logging.debug('Entered module')

    process_hooks()

    END_TIME = get_clock()
    logging.info('Elapsed time: %f', (END_TIME - START_TIME))
