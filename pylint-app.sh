#! /bin/bash
# Simple shell script to run the git RCS keywords programs through pylint

# $Author$
# $Date$
# $Source$

generate_lint()
{
  local app="${1}"
  local logfile="${app%.*}.lint"
  
  if [[ -z "${1}" ]] ; then
    echo "No application name provided to generate_lint"
  else
    echo "Processing file: ${app}"
    {
      echo "Processing file: ${app}"
      echo " "
      echo " "
      echo "pycodestyle:"
      echo " "
      pycodestyle -v --show-source --statistics "${app}"
      echo " "
      echo " "
      echo "pylint:"
      echo " "
      pylint "${app}"
    } > "${logfile}" 2>&1
  fi
}

if [[ -z "${1}" ]] ; then
  for app_file in *.py ; do
    generate_lint "${app_file}"
  done
else
  generate_lint "${1}"
fi
