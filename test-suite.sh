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
#section_name="Test basic smudge / clean operations"
#(log_section_start "${section_name}") >> "${output_log}" 2>&1

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
#(log_section_finish "${section_name}" "Param 2" "Param 3") >> "${output_log}" 2>&1


# Run tests to exercise all the hooks and filters
section_name="Detailed test all operations"
(log_section_start "${section_name}") >> "${output_log}" 2>&1

#01: Make sure we are on the development branch
step_num="01"
git_status "${step_num}.01: Make sure we are on the development branch"

#02: Create test files
step_num="02"
file_name="${test_dir}/old-01.txt"
build_test_file "${file_name}" "${step_num}.01: Build test file ${file_name}"
file_name="${test_dir}/old-02.txt"
build_test_file "${file_name}" "${step_num}.02: Build test file ${file_name}"
file_name="${test_dir}/old-03.txt"
build_test_file "${file_name}" "${step_num}.03: Build test file ${file_name}"
list_dir "${test_dir}" "${step_num}.04: List the test files on directory ${test_dir}"

#03: Add the test files to the repository
step_num="03"
git_add_file "${test_dir}/old-*.txt" "${step_num}.01: Add test files ${test_dir}/old-*.txt to the repository"
list_dir "${test_dir}" "${step_num}.02: List the test files on directory ${test_dir}"

#04: Update one test files
step_num="04"
file_name="${test_dir}/old-03.txt"
append_test_file "${file_name}" "${step_num}.01: Append data to test file ${file_name} to prevent committing"

#05: Commit the changes & display the files
step_num="05"
git_commit "${step_num}.01: Commit the test files to the repository"
file_name="${test_dir}/old-01.txt"
display_file_contents "${file_name}" "${step_num}.02: Display contents of test file ${file_name}"
file_name="${test_dir}/old-02.txt"
display_file_contents "${file_name}" "${step_num}.03: Display contents of test file ${file_name}"
file_name="${test_dir}/old-03.txt"
display_file_contents "${file_name}" "${step_num}.04: Display contents of test file ${file_name}"
list_dir "${test_dir}" "${step_num}.05: List the test files on directory ${test_dir}"

#06: Add and commit the updated log files
step_num="06"
git_add_file "${test_dir}/old-*.txt" "${step_num}.01: Add test files ${test_dir}/old-*.txt to the repository"
git_commit "${step_num}.02: Commit the test files to the repository"
git_push "${step_num}.03: Push the changes"
list_dir "${test_dir}" "${step_num}.04: List the test files on directory ${test_dir}"

#07: Display the files
step_num="07"
file_name="${test_dir}/old-01.txt"
display_file_contents "${file_name}" "${step_num}.01: Display contents of test file ${file_name}"
file_name="${test_dir}/old-02.txt"
display_file_contents "${file_name}" "${step_num}.02: Display contents of test file ${file_name}"
file_name="${test_dir}/old-03.txt"
display_file_contents "${file_name}" "${step_num}.03: Display contents of test file ${file_name}"

#08: Checkout the master branch
step_num="08"
git_branch_checkout "master" "${step_num}.01: Checkout the master branch"
list_dir "${test_dir}" "${step_num}.02: List the test files on directory ${test_dir}"

#09: Merge development changes into the master branch
step_num="09"
git_branch_list "${step_num}.01: List the branches"
git_branch_checkout "master" "${step_num}.02: Checkout the master branch"
git_branch_list "${step_num}.03: List the branches"
git_branch_merge "development" "${step_num}.04: Merge development changes into the master branch"
list_dir "${test_dir}" "${step_num}.05: List the test files on directory ${test_dir} after merge"
git_commit "${step_num}.06: Commit the changes"
git_push "${step_num}.07: Push the changes"
list_dir "${test_dir}" "${step_num}.08: List the test files on directory ${test_dir} after push"

#10: Display the files
step_num="10"
file_name="${test_dir}/old-01.txt"
display_file_contents "${file_name}" "${step_num}.01: Display contents of test file ${file_name}"
file_name="${test_dir}/old-02.txt"
display_file_contents "${file_name}" "${step_num}.02: Display contents of test file ${file_name}"
file_name="${test_dir}/old-03.txt"
display_file_contents "${file_name}" "${step_num}.03: Display contents of test file ${file_name}"

#11: Remove the test files from the development branch
step_num="11"
git_branch_list "${step_num}.01: List the branches"
git_branch_checkout "development" "${step_num}.02: Checkout the development branch"
git_branch_list "${step_num}.03: List the branches"
list_dir "${test_dir}" "${step_num}.04: List the test files on directory ${test_dir} prior to removal"
git_rm_file "${test_dir}/old-*.txt" "${step_num}.05: Remove the test files from the development branch"
list_dir "${test_dir}" "${step_num}.06: List the test files on directory ${test_dir} after removal"
git_commit "${step_num}.07: Commit the changes"
git_push "${step_num}.08: Push the changes"
list_dir "${test_dir}" "${step_num}.09: List the test files on directory ${test_dir} after push"

#12: Merge development changes into the master branch
step_num="12"
git_branch_list "${step_num}.01: List the branches"
git_branch_checkout "master" "${step_num}.02: Checkout the master branch"
git_branch_list "${step_num}.03: List the branches"
list_dir "${test_dir}" "${step_num}.04: List the test files on directory ${test_dir} prior to removal"
git_branch_merge "development" "${step_num}.05: Merge development changes into the master branch"
list_dir "${test_dir}" "${step_num}.06: List the test files on directory ${test_dir} prior to removal"
git_commit "${step_num}.07: Commit the changes"
git_push "${step_num}.08: Push the changes"

#13: Checkout the development branch
step_num="13"
git_branch_list "${step_num}.01: List the branches"
git_branch_checkout "master" "${step_num}.02: Checkout the master branch"
git_branch_list "${step_num}.03: List the branches"
list_dir "${test_dir}" "${step_num}.04: List the test files on directory ${test_dir} after checkout"
git_commit "${step_num}.05: Commit any changes"
git_push "${step_num}.06: Push the changes"



step_num="15"
(log_message "${step_num}: Add test data to trace log") >> "${output_log}" 2>&1
step_num="16"
(log_message "${step_num}: Show the status") >> "${output_log}" 2>&1
step_num="17"
(log_message "${step_num}: Add additional test data") >> "${output_log}" 2>&1
step_num="18"
(log_message "${step_num}: Show the status") >> "${output_log}" 2>&1

#19: Commit the additional test data
step_num="19"
git_commit "${step_num}.01: Commit the additional test data"

step_num="20"
(log_message "${step_num}: Push the changes") >> "${output_log}" 2>&1
step_num="21"
(log_message "${step_num}: List the branches") >> "${output_log}" 2>&1
step_num="22"
(log_message "${step_num}: Checkout the development branch") >> "${output_log}" 2>&1
step_num="23"
(log_message "${step_num}: Merge the master branch") >> "${output_log}" 2>&1
step_num="24"
(log_message "${step_num}: Add trace logs") >> "${output_log}" 2>&1

#25: Commit & push changes
step_num="25"
git_commit "${step_num}.01: Commit changes"
git_push "${step_num}.02: Push changes"

step_num="27"
(log_message "${step_num}: Pull development") >> "${output_log}" 2>&1
step_num="28"
(log_message "${step_num}: Checkout master") >> "${output_log}" 2>&1
step_num="29"
(log_message "${step_num}: Pull master") >> "${output_log}" 2>&1
step_num="30"
(log_message "${step_num}: Merge development") >> "${output_log}" 2>&1

#31: Merge master changes into the development branch
step_num="31"
git_branch_list "${step_num}.01: List the branches"
git_branch_checkout "development" "${step_num}.02: Checkout the development branch"
git_branch_list "${step_num}.03: List the branches"
git_pull "${step_num}.04: Pull the development branch"
git_branch_merge "master" "${step_num}.05: Merge master changes into the development branch"
git_commit "${step_num}.06: Commit the changes"

#32: Merge development changes into the master branch
step_num="32"
git_branch_list "${step_num}.01: List the branches"
git_branch_checkout "master" "${step_num}.02: Checkout the master branch"
git_branch_list "${step_num}.03: List the branches"
git_pull "${step_num}.04: Pull the master branch"
git_branch_merge "master" "${step_num}.05: Merge development changes into the master branch"
git_commit "${step_num}.06: Commit the changes"

#33: Push changes
step_num="33"
git_push "${step_num}.01: Push changes"

step_num="36"
(log_message "${step_num}: Checkout development") >> "${output_log}" 2>&1
step_num="37"
(log_message "${step_num}: Merge master") >> "${output_log}" 2>&1

#38: Commit & push changes
step_num="38"
git_commit "${step_num}.01: Commit changes"
git_push "${step_num}.02: Push changes"

#40: Checkout master
step_num="40"
git_branch_checkout "master" "${step_num}.01: Checkout master"

#41: Checkout development
step_num="41"
git_branch_checkout "development" "${step_num}.01: Checkout development"

(log_section_finish "${section_name}" "Param 2" "Param 3") >> "${output_log}" 2>&1

