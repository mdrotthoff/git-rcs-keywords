#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$

import sys
import os
import errno
import subprocess
import time

# Set the debugging flag
DEBUG_FLAG = bool(True)
TIMING_FLAG = bool(False)
if DEBUG_FLAG:
    TIMING_FLAG = bool(True)
VERBOSE_FLAG = bool(True)
if TIMING_FLAG:
    VERBOSE_FLAG = bool(True)
SUMMARY_FLAG = bool(True)
if VERBOSE_FLAG:
    SUMMARY_FLAG = bool(True)

def main(argv):
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    # Set the start time for calculating elapsed time
    if TIMING_FLAG:
        start_time = time.clock()
    
    # Parameter processing
    program_name = str(sys.argv[0])
    (hook_path, hook_name) = os.path.split(program_name)
    if DEBUG_FLAG:
        sys.stderr.write('************ START **************\n')
        sys.stderr.write('Hook program: %s\n' % str(program_name))
        sys.stderr.write('Hook path: %s\n' % str(hook_path))
        sys.stderr.write('Hook name: %s\n' % str(hook_name))
        sys.stderr.write('*********************************\n')
    
    # Output the program name start
    if SUMMARY_FLAG:
        program_name = str(sys.argv[0])
        sys.stderr.write('Start program name: %s\n' % str(program_name))
    
    if VERBOSE_FLAG:
        sys.stderr.write('  Entered module main\n')

    # List the provided parameters
    if VERBOSE_FLAG:
        sys.stderr.write("  Parameter list\n")
        param_num = 0
        for param in sys.argv:
            sys.stderr.write('    Param[%d]: %s\n' % (param_num, param))
            param_num = param_num + 1
    
    # If argv[3] is zero (file checkout rather than branch checkout), then exit the hook 
    if sys.argv[3] == '0':
        if SUMMARY_FLAG:
            sys.stderr.write('Exiting for file checkout: %s\n' % sys.argv[3])
            sys.stderr.write('End program name: %s\n' % str(program_name))
            sys.stderr.write("\n")
        elif DEBUG_FLAG:
            sys.stderr.write('************ END ****************\n')
            sys.stderr.write('Hook path: %s\n' % str(hook_path))
            sys.stderr.write('Hook name: %s\n' % str(hook_name))
            sys.stderr.write('*********************************\n')
            sys.stderr.write("\n")
            sys.stderr.write("\n")
            sys.stderr.write("\n")
        exit(0)
    elif SUMMARY_FLAG:
        sys.stderr.write('Continuing for branch checkout: %s\n' % sys.argv[3])
    
    # Show the OS environment variables
    if DEBUG_FLAG:
        sys.stderr.write('  Environment variables defined\n')
        for key, value in sorted(os.environ.items()):
            sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
        sys.stderr.write("\n")
    
    # Get the list of files impacted.  If argv[1] and argv[2] are the same commit, then pass the 
    # value only once otherwise the file list is not returned
    if sys.argv[1] == sys.argv[2]:
        git_diff_tree_cmd = 'git diff-tree -r --name-only --no-commit-id --diff-filter=ACMRT %s' % sys.argv[1]
    else:
        git_diff_tree_cmd = 'git diff-tree -r --name-only --no-commit-id --diff-filter=ACMRT %s %s' % (sys.argv[1], sys.argv[2])
    if VERBOSE_FLAG:
        sys.stderr.write('  git diff-tree cmd: %s\n' % str(git_diff_tree_cmd))
    
    # Process the git diff-tree command
    git_return = subprocess.Popen([git_diff_tree_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (git_stdout, git_stderr) = git_return.communicate()
    if DEBUG_FLAG:
        sys.stderr.write('git exit code: %s\n' % str(git_return.returncode))
        sys.stderr.write('stdout length: %s\n' % str(len(git_stdout)))
        sys.stderr.write('stderr length: %s\n' % str(len(git_stderr)))
        sys.stderr.write("\n")
    
    # If an error occurred, display the command output and exit with the returned exit code 
    if git_return.returncode != 0:
        sys.stderr.write("Exiting -- git diff-tree return code: %s\n" % str(git_return.returncode))
        sys.stderr.write("Output text: %s\n" % git_stdout.strip().decode("utf-8"))
        sys.stderr.write("Error message: %s\n" % git_stderr.strip().decode("utf-8"))
        exit(git_return.returncode)
    elif len(git_stderr) > 0:
        sys.stdout.write('STDERR from git diff-tree\n')
        sys.stderr.write(git_stderr.strip().decode("utf-8"))
        sys.stderr.write("\n") 
    
    # Calculate the setup elapsed time
    if TIMING_FLAG:
        setup_time = time.clock()
    
    # Process each of the files listed by forcing a fresh check-out of the file
    files_processed = 0
    if len(git_stdout) > 0:
        # Create a sorted, unique list file names from the returned values
        git_log = git_stdout.strip().decode("utf-8")
        git_log = sorted(set(git_log.strip().split("\n")))
    
        # Process each of the file names returned
        for file_name in git_log:
            # Format the git checkout command
            files_processed = files_processed + 1
            git_checkout_cmd = 'git checkout -- "%s"' % file_name
            if VERBOSE_FLAG:
                sys.stderr.write('  git checkout cmd: %s\n' % str(git_checkout_cmd))
    
            # Remove the file if it currently exists
            try:
                os.remove(file_name)
            except OSError as err:
                # If the file does not exist, it was removed so loop to the next file
                if err.errno != errno.ENOENT:
                    raise

            # Execute the git checkout command
            git_return = subprocess.Popen([git_checkout_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (git_stdout, git_stderr) = git_return.communicate()
            if DEBUG_FLAG:
                sys.stderr.write('git exit code: %s\n' % str(git_return.returncode))
                sys.stderr.write('stdout length: %s\n' % str(len(git_stdout)))
                sys.stderr.write('stderr length: %s\n' % str(len(git_stderr)))
    
            # If an error occurred, display the command output and exit with the returned exit code 
            if git_return.returncode != 0:
                sys.stderr.write("Exiting -- git checkout return code: %s\n" % str(git_return.returncode))
                sys.stderr.write("Output text: %s\n" % git_stdout.strip().decode("utf-8"))
                sys.stderr.write("Error message: %s\n" % git_stderr.strip().decode("utf-8"))
                exit(git_return.returncode)
            else:
                if len(git_stdout) > 0:
                    sys.stdout.write(git_stdout.strip().decode("utf-8"))
                    sys.stdout.write("\n")
                if len(git_stderr) > 0:
                    sys.stderr.write(git_stderr.strip().decode("utf-8"))
                    sys.stderr.write("\n")
    
    # Calculate the elapsed times
    if TIMING_FLAG:
        end_time = time.clock()
        sys.stderr.write('Setup elapsed time: %s\n' % str(setup_time - start_time))
        sys.stderr.write('Execution elapsed time: %s\n' % str(end_time - setup_time))
        sys.stderr.write('Total elapsed time: %s\n' % str(end_time - start_time))
        sys.stderr.write('Files processed: %s\n' % str(files_processed))
    
    # Display a processing summary
    if VERBOSE_FLAG:
        sys.stderr.write('Files processed: %s\n' % str(files_processed))
    
    # Output the program name end
    if VERBOSE_FLAG:
        sys.stderr.write('End program name: %s\n' % str(program_name))
        sys.stderr.write("\n")
    elif DEBUG_FLAG:
        sys.stderr.write('************ END ****************\n')
        sys.stderr.write('Hook path: %s\n' % str(hook_path))
        sys.stderr.write('Hook name: %s\n' % str(hook_name))
        sys.stderr.write('*********************************\n')
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("\n")

    # Return from the function
    if VERBOSE_FLAG:
        sys.stderr.write('  Leaving module check_out_file\n')
    return


# Execute the main function
if __name__ == '__main__':
    main(argv=sys.argv)
