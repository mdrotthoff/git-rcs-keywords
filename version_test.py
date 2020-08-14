#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
version_test

Unit test for the version module.
"""

import sys
import os
import version
import unittest
import yaml

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
param_pattern_default = '*.py'
param_pattern_unused = '*.asdasasd'

exit_success = 0
exit_invalid_directory = 1
exit_invalid_param = 2
exit_invalid_file = 3

yaml_status =         'Development'
yaml_author =         'David Rotthoff'
yaml_email =          'drotthoff@gmail.com'
yaml_version_prefix = 'git-rcs-keywords'
yaml_version_major =  0
yaml_version_minor =  9
yaml_version_build =  0
yaml_string_author =  '__author__'
yaml_string_email =   '__email__'
yaml_string_status =  '__status__'
yaml_string_version = '__version__'

class Test_0100_ParseArgs(unittest.TestCase):
    def test_0100_parse_args_path_data(self):
        """The parse_params should return the supplied path and data file"""
        testargs = ["prog",
                    '--dir', param_path_cwd,
                    '--data', param_file_default]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == None
            assert parameters.pattern == param_pattern_default

    def test_0110_parse_args_path_data_file(self):
        """The parse_params should return the supplied path, program and data file"""
        testargs = ["prog",
                    '--dir', param_path_cwd,
                    '--data', param_file_default,
                    '--file', param_file_program]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == param_file_program
            assert parameters.pattern == param_pattern_default

    def test_0115_parse_args_path_data_file_pattern(self):
        """The parse_params should return the supplied path, program and data file"""
        testargs = ["prog",
                    '--dir', param_path_cwd,
                    '--data', param_file_default,
                    '--file', param_file_program,
                    '--pattern', param_pattern_unused]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == param_file_program
            assert parameters.pattern == param_pattern_unused

    def test_0120_parse_args_defaults(self):
        """The parse_params should return the current working directory and default data file"""
        testargs = ["prog"]
        with patch.object(sys, 'argv', testargs):
            parameters = version.parse_params()
            assert parameters.dir == os.getcwd()
            assert parameters.data == param_file_default
            assert parameters.file == None
            assert parameters.pattern == param_pattern_default

    def test_0130_parse_args_invalid_parameter(self):
        """The parse_params should exit with status code 2 when provided an invalid parameter"""
        testargs = ["prog", '--no-such-param']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                parameters = version.parse_params()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0140_parse_args_dir_param_missing(self):
        """The parse_params should exit with status code 2 when dir parameter is not provided a valued"""
        testargs = ["prog", '--dir']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                parameters = version.parse_params()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0150_parse_args_data_param_missing(self):
        """The parse_params should exit with status code 2 when data parameter is not provided a valued"""
        testargs = ["prog", '--data']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                parameters = version.parse_params()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0160_parse_args_file_param_missing(self):
        """The parse_params should exit with status code 2 when data parameter is not provided a valued"""
        testargs = ["prog", '--file']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                parameters = version.parse_params()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_0170_parse_args_file_param_missing(self):
        """The parse_params should exit with status code 2 when pattern parameter is not provided a valued"""
        testargs = ["prog", '--pattern']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                parameters = version.parse_params()
            self.assertEqual(cm.exception.code, exit_invalid_param)


class Test_0200_ValidateDir(unittest.TestCase):
    def test_0200_validate_dir_cwd(self):
        """The validate_directory should return true when handed the current working directory"""
        assert version.validate_directory(os.getcwd())

    def test_0210_validate_dir_none_existent(self):
        """The validate_directory should return false when handed an invalid directory"""
        assert not version.validate_directory(param_path_invalid)


class Test_0300_ValidateFile(unittest.TestCase):
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


class Test_0400_LoadYamlData(unittest.TestCase):
    def test_0400_load_yaml_data_should_return_status(self):
        """The load_yaml_data function should return a status of Development when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['status'] == yaml_status

    def test_0405_load_yaml_data_should_return_status_string(self):
        """The load_yaml_data function should return the status string to search for"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['status_string'] == yaml_string_status

    def test_0410_load_yaml_data_should_return_author(self):
        """The load_yaml_data function should return a status of David Rotthoff when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['author'] == yaml_author

    def test_0415_load_yaml_data_should_return_author_string(self):
        """The load_yaml_data function should return the author string to search for"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['author_string'] == yaml_string_author

    def test_0420_load_yaml_data_should_return_email(self):
        """The load_yaml_data function should return a status of drotthoff@gmail.com when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['email'] == yaml_email

    def test_0425_load_yaml_data_should_return_email_string(self):
        """The load_yaml_data function should return the email string to search for"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['email_string'] == yaml_string_email

    def test_0430_load_yaml_data_should_return_version_prefix(self):
        """The load_yaml_data function should return a status of git-rcs-keywords when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['version']['prefix'] == yaml_version_prefix

    def test_0440_load_yaml_data_should_return_version_major(self):
        """The load_yaml_data function should return a status of 0 when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['version']['major'] == yaml_version_major

    def test_0450_load_yaml_data_should_return_version_minor(self):
        """The load_yaml_data function should return a status of 9 when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['version']['minor'] == yaml_version_minor

    def test_0460_load_yaml_data_should_return_version_build(self):
        """The load_yaml_data function should return a status of 0 when provided default input parameters"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['version']['build'] == yaml_version_build

    def test_0465_load_yaml_data_should_return_version_string(self):
        """The load_yaml_data function should return a version string to search for"""
        yaml_dictionary = version.load_yaml_data(os.path.join(param_path_cwd,
                                                              param_file_default))
        assert yaml_dictionary['version_string'] == yaml_string_version

    def test_0470_load_yaml_data_raise_ioerror_for_invalid_directory(self):
        """The load_yaml_data function should raise an IOError exception if passed an invalid directory"""
        with self.assertRaises(IOError) as cm:
            yaml_dictionary = version.load_yaml_data(os.path.join(param_path_invalid,
                                                                  param_file_default))
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)

    def test_0470_load_yaml_data_raise_ioerror_for_invalid_file_name(self):
        """The load_yaml_data function should raise an IOError exception if passed an invalid directory"""
        with self.assertRaises(IOError) as cm:
            yaml_dictionary = version.load_yaml_data(os.path.join(param_path_invalid,
                                                                  param_file_invalid))
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)

    def test_0470_load_yaml_data_raise_ioerror_for_invalid_yaml_file(self):
        """The load_yaml_data function should raise an IOError exception if passed an invalid directory"""
        with self.assertRaises(IOError) as cm:
            yaml_dictionary = version.load_yaml_data(os.path.join(param_path_invalid,
                                                                  'README.md'))
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)


class Test_0500_LoadSourceFileNames(unittest.TestCase):
    def test_0500_load_source_file_names_should_return_list(self):
        """The load_source_file_names function should return a list of source files from the directory"""
        source_list = version.load_source_file_names(param_path_cwd)
        assert isinstance(source_list, list)
        assert len(source_list)  > 0

    def test_0510_load_source_file_names_should_return_empty_list_unused_pattern(self):
        """The load_source_file_names function should return an empty list when an unused pattern is supplied"""
        source_list = version.load_source_file_names(param_path_cwd,
                                                     'asdasd.bniasd')
        assert isinstance(source_list, list)
        assert len(source_list)  == 0

    def test_0520_load_source_file_names_should_return_empty_list_invalid_dir(self):
        """The load_source_file_names function should return an empty list when an unused pattern is supplied"""
        source_list = version.load_source_file_names(param_path_cwd,
                                                     'asdasd.bniasd')
        assert isinstance(source_list, list)
        assert len(source_list)  == 0


class Test_0600_UpdateSourceFile(unittest.TestCase):
    def build_yaml_dictionary(self):
        """Build a YAML dictionary for testing with"""
        return version.load_yaml_data(os.path.join(param_path_cwd,
                                                   param_file_default))

    def test_6000_update_source_file_should_exit_success(self):
        """The update_source_file function should return normally when provided a valid file name"""
        if os.path.isfile(os.path.join(param_path_cwd,
                                       'test',
                                       'test.py.bak')):
            os.remove(os.path.join(param_path_cwd,
                                   'test',
                                   'test.py.bak'))
        assert not os.path.isfile(os.path.join(param_path_cwd,
                                               'test',
                                               'test.py.bak'))
        version.update_source_file(os.path.join(param_path_cwd,
                                                'test',
                                                'test.py'),
                                   self.build_yaml_dictionary())
        assert os.path.isfile(os.path.join(param_path_cwd,
                                           'test',
                                           'test.py.bak'))

    def test_6010_update_source_file_should_exit_failed(self):
        """The update_source_file function should raise an exception with an invalid file name"""
        with self.assertRaises(OSError) as cm:
            version.update_source_file(os.path.join(param_path_cwd,
                                                    'test',
                                                    'nosuch-file-test.py'),
                                       self.build_yaml_dictionary())
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)


class Test_0700_UpdateSourceFile(unittest.TestCase):
    def build_yaml_dictionary(self):
        """Build a YAML dictionary for testing with"""
        return version.load_yaml_data(file_name=os.path.join(param_path_cwd,
                                                             param_file_default))

    def test_7000_update_source_file_should_exit_success(self):
        """The update_source_file function should return normally when provided a valid file name"""
        if os.path.isfile(os.path.join(param_path_cwd,
                                       'test',
                                       'test.py.bak')):
            os.remove(os.path.join(param_path_cwd,
                                   'test',
                                   'test.py.bak'))
        assert not os.path.isfile(os.path.join(param_path_cwd,
                                               'test',
                                               'test.py.bak'))
        version.update_source_file(os.path.join(param_path_cwd,
                                                'test',
                                                'test.py'),
                                   self.build_yaml_dictionary())
        assert os.path.isfile(os.path.join(param_path_cwd,
                                           'test',
                                           'test.py.bak'))

    def test_7010_update_source_file_should_exit_failed(self):
        """The update_source_file function should raise an exception with an invalid file name"""
        with self.assertRaises(OSError) as cm:
            version.update_source_file(os.path.join(param_path_cwd,
                                                    'test',
                                                    'nosuch-file-test.py'),
                                       self.build_yaml_dictionary())
        test_exception = cm.exception
        self.assertEqual(test_exception.errno, 2)


class Test_9900_Main(unittest.TestCase):
    def test_9900_main_should_exit_success(self):
        """The main function should exit with a status code of 0 when provided valid parameters"""
        testargs = ["prog",
                    '--dir', os.path.join(param_path_cwd, 'test'),
                    '--data', param_file_default]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_success)

    def test_9910_main_should_exit_invalid_parameter(self):
        """The main function should exit with a status code of 2 when provided an invalid directory"""
        testargs = ["prog",
                    '--dir', os.path.join(param_path_cwd, 'test'),
                    '--data', param_file_default,
                    '--no-param']
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_param)

    def test_9920_main_should_exit_invalid_directory(self):
        """The main function should exit with a status code of 1 when provided an invalid directory"""
        testargs = ["prog",
                    '--dir', param_path_invalid,
                    '--data', param_file_default]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
            self.assertEqual(cm.exception.code, exit_invalid_directory)

    def test_9930_main_should_exit_invalid_data_file(self):
        """The main function should exit with a status code of 3 when provided an invalid data file"""
        testargs = ["prog",
                    '--dir', os.path.join(param_path_cwd, 'test'),
                    '--data', param_file_invalid]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
                print('Exit code: {}'.format(cm.exception_code))
            self.assertEqual(cm.exception.code, exit_invalid_file)

    def test_9940_main_should_exit_invalid_data_file(self):
        """The main function should exit with a status code of 3 when provided an invalid program file"""
        testargs = ["prog",
                    '--dir', os.path.join(param_path_cwd, 'test'),
                    '--data', param_file_default,
                    '--file', param_file_invalid]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit) as cm:
                version.main()
                print('Exit code: {}'.format(cm.exception_code))
            self.assertEqual(cm.exception.code, exit_invalid_file)


class Test_0A00_SaveYamlData(unittest.TestCase):
    def build_yaml_dictionary(self):
        """Build a YAML dictionary for testing with"""
        return version.load_yaml_data(file_name=os.path.join(param_path_cwd,
                                                             param_file_default))

    def test_A000_save_yaml_data_should_exit_success(self):
        """The save_yaml_data function should return normally when provided a valid file name and YAML dictionary"""
        version.save_yaml_data(os.path.join(param_path_cwd, 'test','version_test.yml'),
                               self.build_yaml_dictionary())
        assert os.path.isfile(os.path.join(param_path_cwd, 'test', 'version_test.yml'))

#    def test_A010_update_source_file_should_exit_failed(self):
#        """The update_source_file function should raise an exception with an invalid file name"""
#        with self.assertRaises(OSError) as cm:
#            version.update_source_file(os.path.join(param_path_cwd, 'test', 'nosuch-file-test.py'),
#                                       self.build_yaml_dictionary())
#        test_exception = cm.exception
#        self.assertEqual(test_exception.errno, 2)


# Execute the main function
if __name__ == '__main__':
    unittest.main()
