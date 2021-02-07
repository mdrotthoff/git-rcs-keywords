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

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"


def process_hooks():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    # Verify that the named hook directory is a directory
    list_dir = sys.argv[0] + '.d'
    if not os.path.isdir(list_dir):
        sys.stderr.write('The hook directory %s is not a directory\n'
                         % list_dir)
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
            hook_call = subprocess.call([hook_program], shell=True)
            if hook_call > 0:
                exit(hook_call)

    # # Return from the function
    # exit(0)


# Execute the main function
if __name__ == '__main__':
    process_hooks()
