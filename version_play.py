#! /usr/bin/env python
# # -*- coding: utf-8 -*

# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash:     "ce6f6d53540aa85c30264deab1a47016232ff0e8 $

"""
version

This module will read yaml data from version.yml and construct
a version string to be embedded in any Python application found
in the current sub-directory (excluding this program) and 
do a global replacement of of __version__ = '<version>' with the
current version number.

The expected structure of the yaml file is as follows:
  author:   '<author name>'
  email:    '<author email'
  status:   '<project status>'
  version:
    prefix: '<version prefix>'
    major:  0
    minor:  9
    build:  0

Immediately after making the changes to the program source, the value
of version.build will be incremented and the version.yml file re-written.

The string placed into the source code will be formatted as follows:
  1) A version_prefix is supplied:
     '<version.prefix>-<version.major>.<version.minor>'.<version.build>'
  2) A version prefix is NOT supplied:
     '<version.major>.<version.minor>'.<version.build>'
"""


import sys
import os
import errno
import subprocess
import time
import argparse
import yaml


__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = '0.9.0'
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__credits__ = []
__status__ = "Production"
# __license__ = "Python"


def parse_params():
    """get_params
    
    Read up to two parameters off of the command line for the directory
    to process and the version file to read
    
    Arguments:
        None
        
    Returns:
        Directory to process
        Version data file name
    """
    
    parser = argparse.ArgumentParser(description='Get parameters from the command line.')
    parser.add_argument('--dir',
                        action='store',
                        metavar='SOURCE DIRECTORY',
                        type=str,
                        default=os.getcwd(),
                        help='Directory where the Python source code resides')
    parser.add_argument('--file',
                        action='store',
                        metavar='PROGRAM FILE',
                        type=str,
                        default=None,
                        help='Name of the program file to version')
    parser.add_argument('--data',
                        action='store',
                        metavar='VERSION DATA',
                        type=str,
                        default='version.yml',
                        help='Name of the file containing the version data')
    parameters = parser.parse_args()

    return(parameters)


def main():
    """Main program.

    Arguments:
        None

    Returns:
        Nothing
    """
#    print('Program version is running')
#    current_dir = os.getcwd()

    # Get the parameters supplied on the command line
    parameters = parse_params()

    # Check for a version.yml file in the target directory 


    # Load the YAML version data from version.yml


    # Find all of the Python source code but exclude the running program


    # Cycle through each source program and adjust the four defined
    # replacement strings based on the configured values.  If a value
    # is not configured, do NOT make any replacement for that value. 


    # Increment the version.build value


    # Re-write the version.yml file with the updated values


    # Exit the program
    return(0)


# Execute the main function
if __name__ == '__main__':
    main()

