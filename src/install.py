#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
Install

This module installs the RCS keyword functionality into an
existing git repository.
"""

import sys
import os
from shutil import copy2
import subprocess
import re
import logging

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"

GIT_HOOK = 'git-hook.py'

GIT_DIRS = {'filter_dir': 'filters', 'event_dir': 'hooks'}

GIT_HOOKS = [{'event_name': 'post-commit',
              'event_code': 'rcs-post-commit.py'},
             {'event_name': 'post-checkout',
              'event_code': 'rcs-post-checkout.py'},
             {'event_name': 'post-merge',
              'event_code': 'rcs-post-merge.py'},
             {'event_name': 'post-rewrite',
              'event_code': 'rcs-post-rewrite.py'}]

GIT_FILTERS = [{'filter_type': 'clean',
                'filter_name': 'rcs-filter-clean.py'},
               {'filter_type': 'smudge',
                'filter_name': 'rcs-filter-smudge.py'}]

GIT_FILE_PATTERN = ['*.sql', '*.ora', '*.txt', '*.md', '*.yml',
                    '*.yaml', '*.hosts', '*.xml', '*.jsn',
                    '*.json', '*.pl', '*.py', '*.sh']

# Set the installation target
(PROGRAM_PATH, PROGRAM_EXECUTABLE) = os.path.split(sys.argv[0])
if len(sys.argv) > 1:
    TARGET_DIR = sys.argv[1]
else:
    TARGET_DIR = ''

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
LOGGING_FILE_NAME = '.git-hook.install.log'

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


def check_for_cmd(cmd):
    """Make sure that a program necessary for using this script is
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Nothing
    """
    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        exit(1)

    # Execute the command
    try:
        execute_cmd(cmd)

    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        print(
            "{0} - Program '{1}' not found! -- Exiting."
            .format(str(err), str(cmd))
        )
        exit(err.returncode)
    except OSError as err:
        print(
            "{0} - Required program '{1}' not found! -- Exiting."
            .format(str(cmd), str(cmd))
        )
        exit(err.errno)


def createdir(dirname):
    """Create an OS directory

    Arguments:
        dirname: Name of the subdirectory to create

    Returns:
        None
    """
    if os.path.isdir(dirname):
        return
    os.makedirs(dirname)


def copyfile(srcfile, destfile):
    """Copy an existing source file to a target file name

    Arguments:
        srcfile: Source file for use with the copy
        destfile: Destination file for use with the copy

    Returns:
        None
    """
    # Copy the source file to the destination file
    copy2(srcfile, destfile)


def execute_cmd(cmd):
    """Execute the supplied program
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Process Popen handle
        Process stdout file handle
        Process stderr file handle
    """
    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        exit(1)

    # Execute the command
    sys.stderr.flush()
    cmd_handle = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
    if cmd_stderr:
        for line in cmd_stderr.strip().decode("utf-8").splitlines():
            sys.stderr.write("%s\n" % line)

    # Return from the function
    return cmd_stdout


def registergitevent(eventdir, eventname, eventcode):
    """Register a git event in the .git/hooks folder

    Arguments:
        eventdir: Source file for use with the copy
        eventname: Destination file for use with the copy
        eventcode: Source program to be copied into the hook directory

    Returns:
        None
    """
    event_code_dir = os.path.join(eventdir, '%s.d' % eventname)
    createdir(dirname=event_code_dir)
    copyfile(srcfile=os.path.join(PROGRAM_PATH, eventcode),
             destfile=os.path.join(event_code_dir, eventcode))
    event_link = os.path.join(eventdir, eventname)
    if os.path.islink(event_link):
        os.remove(event_link)
    os.symlink(GIT_HOOK, event_link)


def registerfilter(filter_dir, filter_type, filter_name):
    """Register a git filter for rcs-keywords functionality

    Arguments:
        filter_dir: Directory to hold the filter program
        filter_type: Type of the filter program
        filter_name: Source program of the filter to be copied

    Returns:
        None
    """
    # Register the filter program to rcs-keywords filter
    cmd = ['git',
           'config',
           '--local',
           'filter.rcs-keywords.%s' % filter_type,
           '%s %s' % (os.path.join(filter_dir, filter_name), '%f')]
    execute_cmd(cmd=cmd)


def registerfilepattern(git_dir):
    """Register the relevant file patterns for rcs-keywords functionality

    Arguments:
        filter_dir: Directory to hold the filter program
        filter_type: Type of the filter program
        filter_name: Source program of the filter to be copied

    Returns:
        None
    """
    # Register the defined file patterns to the filters in the attributes files
    attribute_file = os.path.join(git_dir, 'info', 'attributes')
    attribute_backup = os.path.join(git_dir, 'info', 'attributes~')

    # If the attribute file already exists, rename the file and re-create it
    # without the rcs file patterns defined
    if os.path.exists(attribute_file):
        os.rename(attribute_file, attribute_backup)
        keyword_regex = re.compile("rcs-keywords", re.IGNORECASE)
        source = open(attribute_backup, "r")
        destination = open(attribute_file, "w")
        for line in source:
            if not keyword_regex.search(line):
                destination.write(line)
        source.close()
    else:
        destination = open(attribute_file, "w")
        destination.write('* text=auto !eol\n')

    # Write the appropriate file patterns for the filter usage
    max_len = len(max(GIT_FILE_PATTERN, key=len))
    for file_pattern in GIT_FILE_PATTERN:
        destination.write('%s filter=rcs-keywords\n'
                          % file_pattern.ljust(max_len))
    destination.close()


def validategitrepo(repo_dir, git_dir='.git'):
    """Validate that the supplied directory is a git repository

    Arguments:
        repo_dir: Source git repository folder
        git_dir:  Name of the git configuration subfolder

    Returns:
        None
    """
    # Validate that the installation target has a .git directory
    if not os.path.isdir(os.path.join(repo_dir, git_dir)):
        sys.stderr.write('  Target directory %s is not a git repository\n'
                         % repo_dir)
        sys.stderr.write('  Aborting installation!\n')
        raise Exception('Target git directory %s is not a git repository'
                        % repo_dir)


def installgitkeywords(repo_dir, git_dir='.git'):
    """Register a git event in the .git/hooks folder

    Arguments:
        eventdir: Source file for use with the copy
        eventname: Destination file for use with the copy
        eventcode: Source program to be copied into the hook directory

    Returns:
        None
    """
    # Create the core directories
    filter_dir = os.path.join(git_dir, GIT_DIRS['filter_dir'])
    createdir(dirname=filter_dir)
    event_dir = os.path.join(git_dir, GIT_DIRS['event_dir'])
    createdir(dirname=event_dir)

    # Register the defined file patterns to the filters in the attributes files
    registerfilepattern(git_dir)

    # Copy the git event manager
    copyfile(srcfile=os.path.join(PROGRAM_PATH, GIT_HOOK),
             destfile=os.path.join(event_dir, GIT_HOOK))

    # Register the git event hooks
    for git_event in GIT_HOOKS:
        registergitevent(eventdir=event_dir,
                         eventname=git_event['event_name'],
                         eventcode=git_event['event_code'])

    # Set up the filter programs for use
    for filter_def in GIT_FILTERS:
        copyfile(srcfile=os.path.join(PROGRAM_PATH, filter_def['filter_name']),
                 destfile=os.path.join(filter_dir, filter_def['filter_name']))

    # Change to the repository directory and de-register the
    # rcs-keywords filter
    local_dir = os.getcwd()
    os.chdir(os.path.abspath(repo_dir))
    cmd = ['git',
           'config',
           '--local',
           '--remove-section',
           'filter.rcs-keywords']
    execute_cmd(cmd=cmd)

    # Set up the filter programs for use
    filter_dir = os.path.join(git_dir, GIT_DIRS['filter_dir'])
    for filter_def in GIT_FILTERS:
        # Register the defined filter program
        registerfilter(filter_dir=os.path.join(git_dir,
                                               GIT_DIRS['filter_dir']),
                       filter_type=filter_def['filter_type'],
                       filter_name=filter_def['filter_name'])
    os.chdir(local_dir)


def install():
    """Main program.

    Arguments:
        None

    Returns:
        Nothing
    """
    # Capture the current working directory
    current_dir = os.getcwd()

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Install the keyword support
    try:
        # Validate that a git repository was supplied
        validategitrepo(repo_dir=TARGET_DIR)
        # Change to the repository directory
        os.chdir(os.path.abspath(TARGET_DIR))
        # Install rcs keywords support in the repo
        installgitkeywords(repo_dir='')
        # # Find any submodules registered in the repository
        # dirmodule = os.path.join('.git', 'modules')
        # field_name = ['gitdir', 'repodir']
        # submodule_list = [dict(zip(field_name, (dirpath,
        #                                         os.path.relpath(dirpath,
        #                                                         dirmodule))))
        #                   for (dirpath, _, filenames) in os.walk(dirmodule)
        #                   for name in filenames if name == 'config']
        # # Install keyword support to submodules found
        # for module in submodule_list:
        #     installgitkeywords(repo_dir=module['repodir'],
        #                        git_dir=module['gitdir'])

    except:
        sys.stderr.write('Exception caught\n')
        raise

    # Return to the initial working directory
    os.chdir(current_dir)


# Execute the main function
if __name__ == '__main__':
    configure_logging()

    START_TIME = get_clock()
    logging.debug('Entered module')

    install()

    END_TIME = get_clock()
    logging.info('Elapsed time: %f', (END_TIME - START_TIME))
