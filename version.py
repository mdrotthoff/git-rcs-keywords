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
  author_string:  '__author__ ='
  email_string:   '__email__ ='
  status_string:  '__status__'
  version_string: '__version__'

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
import fnmatch
import fileinput
import re
import datetime

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = '0.9.0'
__date__ = "2018-06-08 15:26 CDT"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__status__ = "Production"

exit_invalid_directory = 1
exit_invalid_file = 3



def save_yaml_data(yaml_data, dir_name, file_name):
    """save_yaml_data

    Save the supplied YAML data into a dictionary

    Arguments:
        dir_name  - name of the directory where the file should be located
        file_name - name of the YAML data file

    Returns:
        Dictionary of YAML supplied parameters
    """

    with open(os.path.join(dir_name, file_name), 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=False)


def update_source_file(file_name, yaml_dictionary):
    """update_source_file

    Update the program file with the configured values

    Arguments:
        file_name       - name of the program file to be modified
        yaml_dictionary - YAML dictionary of the values to use
    Returns:
        None
    """

    # Define the author regular expression
    author_regex = None
    if 'author' in yaml_dictionary:
        regex_string = r'^ *' + yaml_dictionary['author_string'] + '.*'
        author_regex = re.compile(regex_string, re.IGNORECASE)
        author_string = '{} "{}"'.format(yaml_dictionary['author_string'], yaml_dictionary['author'])

    # Define the status regular expression
    status_regex = None
    if 'status' in yaml_dictionary:
        regex_string = r'^ *' + yaml_dictionary['status_string'] + '.*'
        status_regex = re.compile(regex_string, re.IGNORECASE)
        status_string = '{} = "{}"'.format(yaml_dictionary['status_string'], yaml_dictionary['status'])

    # Define the e-mail regular expression
    email_regex = None
    if 'email' in yaml_dictionary:
        regex_string = r'^ *' + yaml_dictionary['email_string'] + '.*'
        email_regex = re.compile(regex_string, re.IGNORECASE)
        email_string = '{} = "{}"'.format(yaml_dictionary['email_string'], yaml_dictionary['email'])

    # Define the date regular expression
    date_regex = None
    if 'date_string' in yaml_dictionary:
        regex_string = r'^ *' + yaml_dictionary['date_string'] + '.*'
        date_regex = re.compile(regex_string, re.IGNORECASE)
        date_string = '{} = "{}"'.format(yaml_dictionary['date_string'],
                                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Define the version regular expression
    version_regex = None
    if 'version' in yaml_dictionary:
        regex_string = r'^ *' + yaml_dictionary['version_string'] + '.*'
        version_regex = re.compile(regex_string, re.IGNORECASE)
        prefix_string = None
        if 'prefix' in yaml_dictionary['version']:
            prefix_string = yaml_dictionary['version']['prefix'] + '-'
        version_string = '{} = "{}{}.{}.{}"'.format(yaml_dictionary['version_string'],
                                                    prefix_string,
                                                    yaml_dictionary['version']['major'],
                                                    yaml_dictionary['version']['minor'],
                                                    yaml_dictionary['version']['build'])

    # Process the file, replacing the desired lines
    for line in fileinput.input(file_name, inplace=1, backup='.bak'):
        if author_regex:
            line = author_regex.sub(author_string, line)
        if status_regex:
            line = status_regex.sub(status_string, line)
        if email_regex:
            line = email_regex.sub(email_string, line)
        if version_regex:
            line = version_regex.sub(version_string, line)
        if date_regex:
            line = date_regex.sub(date_string, line)
        print(line.rstrip())

    return


def load_source_file_names(dir_name, file_pattern='*.py'):
    """load_souce_file_names

    Find and load the Python program file names from the supplied directory

    Arguments:
        dir_name     - name of the directory where the file should be located
        file_pattern - file name patter to search for
    Returns:
        List of Python program file names
    """

    files_found = []
    for dir_root, dir_names, file_names in os.walk(dir_name):
        for file_name in fnmatch.filter(file_names, file_pattern):
            files_found.append(os.path.join(dir_root, file_name))

    return files_found


def load_yaml_data(dir_name, file_name):
    """load_yaml_data

    Load the supplied YAML data into a dictionary

    Arguments:
        dir_name  - name of the directory where the file should be located
        file_name - name of the YAML data file

    Returns:
        Dictionary of YAML supplied parameters
    """

    yaml_stream = file(os.path.join(dir_name, file_name), 'r')
    yaml_dictionary = yaml.load(yaml_stream)
    yaml_stream.close()

    if not 'version_string' in yaml_dictionary:
        yaml_dictionary.update({'version_string' : '__version__'})

    if not 'author_string' in yaml_dictionary:
        yaml_dictionary.update({'author_string' : '__author__'})

    if not 'email_string' in yaml_dictionary:
        yaml_dictionary.update({'email_string' : '__email__'})

    if not 'status_string' in yaml_dictionary:
        yaml_dictionary.update({'status_string' : '__status__'})

    if not 'date_string' in yaml_dictionary:
        yaml_dictionary.update({'date_string' : '__date__'})

    print(str(yaml_dictionary))

    return(yaml_dictionary)


def validate_file(dir_name, file_name):
    """validate_file

    Validate that the provided directory has the specified file

    Arguments:
        dir_name  - name of the directory where the file should be located
        file_name - name of the file to check

    Returns:
        Boolean
    """

    return os.path.isfile(os.path.join(dir_name, file_name))


def validate_directory(dir_name):
    """validate_directory

    Validate that the provided directory is an actual OS directory

    Arguments:
        dir_name - name of the directory to validate

    Returns:
        Boolean
    """

    return os.path.isdir(dir_name)


def parse_params():
    """parse_params

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
    parser.add_argument('--pattern',
                        action='store',
                        metavar='SOURCE FILE PATTERN',
                        type=str,
                        default='*.py',
                        help='File pattern for the source files to version')
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
    # print('Parameters: {}'.format(parameters))

    # Verify that the supplied directory is valid
    if not validate_directory(dir_name=parameters.dir):
        print('Invalid directory name provided')
        exit(exit_invalid_directory)

    # Verify that the supplied data file is valid
    if not validate_file(dir_name=parameters.dir,
                         file_name=parameters.data):
        print('Invalid data file name provided')
        exit(exit_invalid_file)

    # Verify that the program file is valid if supplied
    if parameters.file:
        if not validate_file(dir_name=parameters.dir,
                             file_name=parameters.file):
            print('Invalid program file name provided')
            exit(exit_invalid_file)

    # Check for a version.yml file in the target directory


    # Load the YAML version data from version.yml
    yaml_data = load_yaml_data(dir_name=parameters.dir,
                               file_name=parameters.data)

    # Find all of the Python source code but exclude the running program
    if parameters.file:
        sources_found = [ os.path.join(parameters.dir, parameters.file) ]
    else:
        sources_found = load_source_file_names(dir_name=parameters.dir,
                                               file_pattern=parameters.pattern)

#    print('Sources found:')
#    for file_name in sources_found:
#        print('\t{}'.format(file_name))

    # Cycle through each source program and adjust the four defined
    # replacement strings based on the configured values.  If a value
    # is not configured, do NOT make any replacement for that value.
    for file_name in sources_found:
        update_source_file(file_name, yaml_data)

    # Increment the version.build value
    yaml_data['version']['build'] += 1


    # Re-write the version.yml file with the updated values
    save_yaml_data(yaml_data=yaml_data,
                   dir_name=parameters.dir,
                   file_name=parameters.data)


    # Exit the program
    exit(0)


# Execute the main function
if __name__ == '__main__':
    main()
