#! /bin/bash
# Simple shell script to test the git RCS keywords setup

# $Author$
# $Date$
# $Source$

output_log="test-suite.log"
test_dir="testing"
#test_file1="test1.txt"
#test_file2="test 1.txt"


log_blank_line()
{
  echo -e " "
}

log_message()
{
  echo -e "${1}"
}

log_section_start()
{
  echo -e "*****************************************************************"
  echo -e "*****************************************************************"
  echo -e "***  Section Start"
  echo -e "***    Title: ${1}"
  echo -e "***    Date:  $(date '+%Y-%m-%d %T.%N')"
  echo -e "*****************************************************************"
  echo -e "*****************************************************************"
  log_blank_line
}

log_section_finish()
{
#  log_blank_line
  echo -e "*****************************************************************"
  echo -e "*****************************************************************"
  echo -e "***  Section Finish"
  echo -e "***    Title: ${1}"
  echo -e "***    Date:  $(date '+%Y-%m-%d %T.%N')"
  echo -e "*****************************************************************"
  echo -e "*****************************************************************"
  log_blank_line
  log_blank_line
  log_blank_line
}

log_step_start()
{
  echo -e "*****************************************************************"
  echo -e "***  Step Start"
  echo -e "***    Title: ${1}"
  echo -e "***    Cmd:   ${2} ${3} ${4} ${5}"
  echo -e "***    Date:  $(date '+%Y-%m-%d %T.%N')"
  echo -e "*****************************************************************"
  log_blank_line
}

log_step_finish()
{
  log_blank_line
  echo -e "*****************************************************************"
  echo -e "***  Step Finish"
  echo -e "***    Title:  ${1}"
  echo -e "***    Status: ${2}"
  echo -e "***    Date:   $(date '+%Y-%m-%d %T.%N')"
  echo -e "*****************************************************************"
  log_blank_line
}

log_step_status()
{
  echo -e "cmd status: ${1}"
}

test_file_contents()
{
  echo "\$Author\$"
  echo "\$Date\$"
  echo "\$Revision\$"
  echo "\$Rev\$"
  echo "\$File\$"
  echo "\$Source\$"
  echo "\$Hash\$"
  echo "\$Id\$"
#  echo " "
}

display_file_contents()
{
  local step_name
  local step_cmd

  step_name="Display contents of ${1}"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="cat \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (log_message "$(cat "${1}")")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
}

build_test_file()
{
  local step_name
  local step_cmd

  step_name="Build test file ${1}"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="echo >> \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (test_file_contents) > "${1}"
    (log_blank_line)
    (log_message "** ${step_name} - start file contents **")
    (log_message "$(cat "${1}")")
    (log_message "** ${step_name} - end file contents **")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
}

append_test_file()
{
  local step_name
  local step_cmd

  step_name="Append to file ${1}"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="echo >> \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (log_blank_line) >> "${1}"
    (test_file_contents) >> "${1}"
    (log_blank_line)
    (log_message "** ${step_name} - start file contents **")
    (log_message "$(cat "${1}")")
    (log_message "** ${step_name} - end file contents **")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
}

list_dir()
{
  local step_name
  local step_cmd

  step_name="Directory listing of ${1}"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="ls -lah \"${1}\""
#  (log_step_start "${step_name}" "${step_cmd}") >> "${output_log}" 2>&1
#  (test_file_contents) >> "${1}" 2>> "${output_log}"
#  (log_step_finish "${step_name}" "$?") >> "${output_log}" 2>&1
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (log_blank_line)
    (ls -lah "${1}")
    (log_blank_line)
#    (log_message "** ${step_name} - start file contents **")
#    (log_message "$(ls -lah "${1}")")
#    (log_message "** ${step_name} - end file contents **")
    (log_step_finish "${step_name}" "$?")
} >> "${output_log}" 2>&1
}


git_status()
{
  local step_name
  local step_cmd

  step_name="Show git status of the repository"
  if ! [[ -z ${1} ]] ; then
    step_name="${1}"
  fi

  step_cmd="git status"
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git status)
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
}

git_add_file()
{
  local step_name
  local step_cmd

  step_name="Add file ${1} to the repository"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="git add \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git add "${1}")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_rm_file()
{
  local step_name
  local step_cmd

  step_name="Remove file ${1} from the repository"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="git rm \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git rm "${1}")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_force_rm_file()
{
  local step_name
  local step_cmd

  step_name="Force remove file ${1} from the repository"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="git rm -f \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git rm -f "${1}")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_commit()
{
  local step_name
  local step_cmd

  step_name="Test post-commit handler"
  if ! [[ -z ${1} ]] ; then
    step_name="${1}"
  fi

  step_cmd="git commit -m \"Post-commit test\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git commit -m "Post-commit test")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_pull()
{
  local step_name
  local step_cmd

  step_name="Execute git pull"
  if ! [[ -z ${1} ]] ; then
    step_name="${1}"
  fi

  step_cmd="git pull"
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git push)
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_push()
{
  local step_name
  local step_cmd

  step_name="Execute git push"
  if ! [[ -z ${1} ]] ; then
    step_name="${1}"
  fi

  step_cmd="git push"
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git push)
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_branch_list()
{
  local step_name
  local step_cmd

  step_name="List all git branches"
  if ! [[ -z ${1} ]] ; then
    step_name="${1}"
  fi

  step_cmd="git branch -a"
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git branch -a)
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
}

git_branch_checkout()
{
  local step_name
  local step_cmd

  step_name="Checkout git branch ${1}"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="git checkout \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git checkout "${1}")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}

git_branch_merge()
{
  local step_name
  local step_cmd

  step_name="Merge branch ${1} into the current branch"
  if ! [[ -z ${2} ]] ; then
    step_name="${2}"
  fi

  step_cmd="git merge \"${1}\""
  {
    (log_step_start "${step_name}" "${step_cmd}")
    (git merge "${1}")
    (log_step_finish "${step_name}" "$?")
  } >> "${output_log}" 2>&1
  git_status "${step_name} - git status"
}


if [[ -f "${output_log}" ]] ;then
  rm -f "${output_log}" 2> /dev/null
fi


#list_dir "${test_dir}"
#exit 0


# Run general tests involving the clean and smudge filters
section_name="Test basic smudge / clean operations"
(log_section_start "${section_name}") >> "${output_log}" 2>&1

# Show the current branch information
git_branch_list
git_branch_checkout "development"

#build_test_file "${test_file1}"
#display_file_contents "${test_file1}"
#git_add_file "${test_file1}"
#git_rm_file "${test_file1}"
#git_force_rm_file "${test_file1}"
#build_test_file "${test_file1}"
#display_file_contents "${test_file1}"
#git_add_file "${test_file1}"
#append_test_file "${test_file1}"
#display_file_contents "${test_file1}"
#git_commit
#git_add_file "${test_file1}"
#git_commit

#build_test_file "${test_file2}"
#display_file_contents "${test_file2}"
#git_add_file "${test_file2}"
#git_rm_file "${test_file2}"
#git_force_rm_file "${test_file2}"
#build_test_file "${test_file2}"
#display_file_contents "${test_file2}"
#git_add_file "${test_file2}"
#append_test_file "${test_file2}"
#display_file_contents "${test_file2}"
#git_commit
#git_add_file "${test_file2}"
#git_commit


#git_rm_file "${test_file1}"
#git_commit
#git_rm_file "${test_file2}"
#git_commit
#git_push
#git_status

## Show the current branch information
#git_branch_list
#git_branch_checkout "master"

#(log_blank_line) >> "${output_log}"
(log_section_finish "${section_name}" "Param 2" "Param 3") >> "${output_log}" 2>&1


# Run tests to exercise all the hooks and filters
section_name="Detailed test all operations"
(log_section_start "${section_name}") >> "${output_log}" 2>&1

#01: Make sure we are on the development branch
git_status "01.01: Make sure we are on the development branch"

#02: Create test files
file_name="${test_dir}/old-01.txt"
build_test_file "${file_name}" "02.01: Build test file ${file_name}"
file_name="${test_dir}/old-02.txt"
build_test_file "${file_name}" "02.02: Build test file ${file_name}"
file_name="${test_dir}/old-03.txt"
build_test_file "${file_name}" "02.03: Build test file ${file_name}"
list_dir "${test_dir}" "02.04: List the test files on directory ${test_dir}"

#03: Add the test files to the repository
git_add_file "${test_dir}/old-*.txt" "03.01: Add test files ${test_dir}/old-*.txt to the repository"
list_dir "${test_dir}" "03.02: List the test files on directory ${test_dir}"

#04: Update one test files
file_name="${test_dir}/old-03.txt"
append_test_file "${file_name}" "04.01: Append data to test file ${file_name} to prevent committing"

#05: Commit the changes & display the files
git_commit "05.01: Commit the test files to the repository"
file_name="${test_dir}/old-01.txt"
display_file_contents "${file_name}" "05.02: Display contents of test file ${file_name}"
file_name="${test_dir}/old-02.txt"
display_file_contents "${file_name}" "05.03: Display contents of test file ${file_name}"
file_name="${test_dir}/old-03.txt"
display_file_contents "${file_name}" "05.04: Display contents of test file ${file_name}"
list_dir "${test_dir}" "05.05: List the test files on directory ${test_dir}"

#06: Add and commit the updated log files
git_add_file "${test_dir}/old-*.txt" "06.01: Add test files ${test_dir}/old-*.txt to the repository"
git_commit "06.02: Commit the test files to the repository"
git_push "06.03: Push the changes"
list_dir "${test_dir}" "06.04: List the test files on directory ${test_dir}"

#07: Display the files
file_name="${test_dir}/old-01.txt"
display_file_contents "${file_name}" "07.01: Display contents of test file ${file_name}"
file_name="${test_dir}/old-02.txt"
display_file_contents "${file_name}" "07.02: Display contents of test file ${file_name}"
file_name="${test_dir}/old-03.txt"
display_file_contents "${file_name}" "07.03: Display contents of test file ${file_name}"

#08: Checkout the master branch
git_branch_checkout "master" "08.01: Checkout the master branch"
list_dir "${test_dir}" "08.02: List the test files on directory ${test_dir}"

#09: Merge development changes into the master branch
git_branch_list "09.01: List the branches"
git_branch_checkout "master" "09.02: Checkout the master branch"
git_branch_list "09.03: List the branches"
git_branch_merge "development" "09.04: Merge development changes into the master branch"
list_dir "${test_dir}" "09.05: List the test files on directory ${test_dir} after merge"
git_commit "09.06: Commit the changes"
git_push "09.07: Push the changes"
list_dir "${test_dir}" "09.08: List the test files on directory ${test_dir} after push"

#10: Display the files
file_name="${test_dir}/old-01.txt"
display_file_contents "${file_name}" "10.01: Display contents of test file ${file_name}"
file_name="${test_dir}/old-02.txt"
display_file_contents "${file_name}" "10.02: Display contents of test file ${file_name}"
file_name="${test_dir}/old-03.txt"
display_file_contents "${file_name}" "10.03: Display contents of test file ${file_name}"

#11: Remove the test files from the development branch
git_branch_list "11.01: List the branches"
git_branch_checkout "development" "11.02: Checkout the development branch"
git_branch_list "11.03: List the branches"
list_dir "${test_dir}" "11.04: List the test files on directory ${test_dir} prior to removal"
git_rm_file "${test_dir}/old-*.txt" "11.05: Remove the test files from the development branch"
list_dir "${test_dir}" "11.06: List the test files on directory ${test_dir} after removal"
git_commit "11.07: Commit the changes"
git_push "11.08: Push the changes"
list_dir "${test_dir}" "11.09: List the test files on directory ${test_dir} after push"

#12: Merge development changes into the master branch
git_branch_list "12.01: List the branches"
git_branch_checkout "master" "12.02: Checkout the master branch"
git_branch_list "12.03: List the branches"
list_dir "${test_dir}" "12.04: List the test files on directory ${test_dir} prior to removal"
git_branch_merge "development" "12.05: Merge development changes into the master branch"
list_dir "${test_dir}" "12.06: List the test files on directory ${test_dir} prior to removal"
git_commit "12.07: Commit the changes"
git_push "12.08: Push the changes"

#13: Checkout the development branch
git_branch_list "13.01: List the branches"
git_branch_checkout "master" "13.02: Checkout the master branch"
git_branch_list "13.03: List the branches"
list_dir "${test_dir}" "13.04: List the test files on directory ${test_dir} after checkout"
git_commit "13.05: Commit any changes"
git_push "13.06: Push the changes"



(log_message "15: Add test data to trace log") >> "${output_log}" 2>&1
(log_message "16: Show the status") >> "${output_log}" 2>&1
(log_message "17: Add additional test data") >> "${output_log}" 2>&1
(log_message "18: Show the status") >> "${output_log}" 2>&1

#19: Commit the additional test data
git_commit "19.01: Commit the additional test data"

(log_message "20: Push the changes") >> "${output_log}" 2>&1
(log_message "21: List the branches") >> "${output_log}" 2>&1
(log_message "22: Checkout the development branch") >> "${output_log}" 2>&1
(log_message "23: Merge the master branch") >> "${output_log}" 2>&1
(log_message "24: Add trace logs") >> "${output_log}" 2>&1

#25: Commit & push changes
git_commit "25.01: Commit changes"
git_push "25.02: Push changes"

(log_message "27: Pull development") >> "${output_log}" 2>&1
(log_message "28: Checkout master") >> "${output_log}" 2>&1
(log_message "29: Pull master") >> "${output_log}" 2>&1
(log_message "30: Merge development") >> "${output_log}" 2>&1

#31: Merge master changes into the development branch
git_branch_list "31.01: List the branches"
git_branch_checkout "development" "31.02: Checkout the development branch"
git_branch_list "31.03: List the branches"
git_pull "31.04: Pull the development branch"
git_branch_merge "master" "31.05: Merge master changes into the development branch"
git_commit "31.06: Commit the changes"

#32: Merge development changes into the master branch
git_branch_list "32.01: List the branches"
git_branch_checkout "master" "32.02: Checkout the master branch"
git_branch_list "32.03: List the branches"
git_pull "32.04: Pull the master branch"
git_branch_merge "master" "32.05: Merge development changes into the master branch"
git_commit "32.06: Commit the changes"

#33: Push changes
git_push "33.01: Push changes"

(log_message "36: Checkout development") >> "${output_log}" 2>&1
(log_message "37: Merge master") >> "${output_log}" 2>&1

#38: Commit & push changes
git_commit "38.01: Commit changes"
git_push "38.02: Push changes"

#40: Checkout master
git_branch_checkout "master" "40.01: Checkout master"

#41: Checkout development
git_branch_checkout "development" "41.01: Checkout development"

(log_section_finish "${section_name}" "Param 2" "Param 3") >> "${output_log}" 2>&1
