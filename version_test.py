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
version_test

Unit test for the version module.
"""

import sys
import os
import version
import unittest

try:
    # python 3.4+ should use builtin unittest.mock not mock package
    from unittest.mock import patch
except ImportError:
    from mock import patch

param_path_cwd = os.getcwd()
param_path_invalid = '/asdacc/asdascascas'
param_path_default = '.'
param_file_program = 'version_play.py'
param_file_invalid = 'asdasdasdasdacs'
param_file_default = 'version.yml'

exit_success = 0
exit_invalid_directory = 1
exit_invalid_param = 2
exit_invalid_file = 3

yaml_status = 'Development'
yaml_author = 'David Rotthoff'
yaml_email = 'drotthoff@gmail.com'
yaml_version_prefix = 'git-rcs-keywords'
yaml_version_major = 0
yaml_version_minor = 9
yaml_version_build = 0


class Test_100_ParseArgs(unittest.TestCase):
    def test_0100_parse_args_path_data(self):
        """The parse_params should return the supplied path and data file"""
        testargs = ["prog", '--dir', param_path_cwd, '--data', param_file_default]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == None

    def test_0110_parse_args_path_data_file(self):
        """The parse_params should return the supplied path, program and data file"""
        testargs = ["prog", '--dir', param_path_cwd, '--data', param_file_default, '--file', param_file_program]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == param_file_program

    def test_0120_parse_args_defaults(self):
        """The parse_params should return the current working directory and default data file"""
        testargs = ["prog"]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == None

    def test_0130_parse_args_invalid_parameter(self):
        """The parse_params should exit with status code 2 when provided an invalid parameter"""
        testargs = ["prog", '--no-such-param']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0140_parse_args_dir_param_missing(self):
        """The parse_params should exit with status code 2 when dir parameter is not provided a valued"""
        testargs = ["prog", '--dir']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0150_parse_args_data_param_missing(self):
        """The parse_params should exit with status code 2 when data parameter is not provided a valued"""
        testargs = ["prog", '--data']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0160_parse_args_file_param_missing(self):
        """The parse_params should exit with status code 2 when data parameter is not provided a valued"""
        testargs = ["prog", '--file']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_param)


class Test_200_ValidateDir(unittest.TestCase):
    def test_0200_validate_dir_cwd(self):
        """The validate_directory should return true when handed the current working directory"""
        assert version.validate_directory(os.getcwd())

    def test_0210_validate_dir_none_existent(self):
        """The validate_directory should return false when handed an invalid directory"""
        assert not version.validate_directory(param_path_invalid)


class Test_300_ValidateFile(unittest.TestCase):
    def test_0300_validate_file_default(self):
        """The validate_directory should return true when handed the current working directory and default data file"""
        assert version.validate_file(os.getcwd(), param_file_default)

    def test_0310_validate_file_no_directory(self):
        """The validate_directory should return false when handed an invalid directory and the default data file"""
        assert not version.validate_file(param_path_invalid, param_file_default)

    def test_0320_validate_dir_no_file(self):
        """The validate_directory should return false when handed the default directory and and an invalid file name"""
        assert not version.validate_file(os.getcwd(), param_file_invalid)

    def test_0330_validate_dir_no_file_directory(self):
        """The validate_directory should return false when handed an invalid directory and invalid file name"""
        assert not version.validate_file(param_path_invalid, param_file_invalid)


class Test_400_LoadYamlData(unittest.TestCase):
    def test_0400_load_yaml_data_should_return_status(self):
        """The load_yaml_data function should return a status of Development when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['status'] == yaml_status

    def test_0410_load_yaml_data_should_return_author(self):
        """The load_yaml_data function should return a status of David Rotthoff when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['author'] == yaml_author

    def test_0420_load_yaml_data_should_return_email(self):
        """The load_yaml_data function should return a status of drotthoff@gmail.com when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['email'] == yaml_email

    def test_0430_load_yaml_data_should_return_version_prefix(self):
        """The load_yaml_data function should return a status of git-rcs-keywords when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['version']['prefix'] == yaml_version_prefix

    def test_0440_load_yaml_data_should_return_version_major(self):
        """The load_yaml_data function should return a status of 0 when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['version']['major'] == yaml_version_major

    def test_0450_load_yaml_data_should_return_version_minor(self):
        """The load_yaml_data function should return a status of 9 when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['version']['minor'] == yaml_version_minor

    def test_0460_load_yaml_data_should_return_version_build(self):
        """The load_yaml_data function should return a status of 0 when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(param_path_cwd, param_file_default)
        assert yaml_dictionary['version']['build'] == yaml_version_build

    def test_0470_load_yaml_data_raise_ioerror_for_invalid_directory(self):
        """The load_yaml_data function should raise an IOError exception if passed an invalid directory"""
        with self.assertRaises(IOError) as cm:
            yaml_dictionary = version.load_yaml_data(param_path_invalid, param_file_default)
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)

    def test_0470_load_yaml_data_raise_ioerror_for_invalid_file_name(self):
        """The load_yaml_data function should raise an IOError exception if passed an invalid directory"""
        with self.assertRaises(IOError) as cm:
            yaml_dictionary = version.load_yaml_data(param_path_invalid, param_file_invalid)
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)

    def test_0470_load_yaml_data_raise_ioerror_for_invalid_yaml_file(self):
        """The load_yaml_data function should raise an IOError exception if passed an invalid directory"""
        with self.assertRaises(IOError) as cm:
            yaml_dictionary = version.load_yaml_data(param_path_invalid, 'README.md')
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)


class Test_500_LoadPythonFileNames(unittest.TestCase):
    def test_0500_load_python_file_names_should_return_list(self):
        """The load_python_file_names function should return a list of Python files from the directory"""
        python_programs = version.load_python_file_names(param_path_cwd)
        assert isinstance(python_programs, list)


'''
class Test_900_Main(unittest.TestCase):
    def test_9900_main_should_exit_success(self):
        """The main function should exit with a status code of 0 when provided valid parameters"""
        testargs = ["prog", '--dir', param_path_cwd, '--data', param_file_default]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_success)

    def test_9910_main_should_exit_invalid_parameter(self):
        """The main function should exit with a status code of 2 when provided an invalid directory"""
        testargs = ["prog", '--dir', param_path_cwd, '--data', param_file_default, '--no-param']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_9920_main_should_exit_invalid_directory(self):
        """The main function should exit with a status code of 1 when provided an invalid directory"""
        testargs = ["prog", '--dir', param_path_invalid, '--data', param_file_default]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_directory)

    def test_9930_main_should_exit_invalid_data_file(self):
        """The main function should exit with a status code of 3 when provided an invalid data file"""
        testargs = ["prog", '--dir', param_path_cwd, '--data', param_file_invalid]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
                print('Exit code: {}'.format(cm.exception_code))
            self.assertEqual(cm.exception.code, exit_invalid_file)

    def test_9940_main_should_exit_invalid_data_file(self):
        """The main function should exit with a status code of 3 when provided an invalid program file"""
        testargs = ["prog", '--dir', param_path_cwd, '--data', param_file_default, '--file', param_file_invalid]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
                print('Exit code: {}'.format(cm.exception_code))
            self.assertEqual(cm.exception.code, exit_invalid_file)
'''


# Execute the main function
if __name__ == '__main__':
    unittest.main()
