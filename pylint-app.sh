#! /bin/bash
# Simple shell script to run the git RCS keywords programs through pylint

# $Author$
# $Date$
# $Source$

generate_lint()
{
  local app="${1}"
  local logfile="${app%.*}.lint"
#  local pdffile="${app%.*}.pdf"
#  local hash=$(git log --max-count=1 --pretty=%H)

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
      echo " "
      echo " "
#      if [[ "${1}" == 'rcs-filter-clean.py' ]] ; then
#        pycallgraph -o "${pdffile}" -f pdf "${1}" "${1}"
#      elif [[ "${1}" == 'rcs-filter-smudge.py' ]] ; then
#        pycallgraph -o "${pdffile}" -f pdf "${1}" "${1}"
#      elif [[ "${1}" == 'rcs-post-checkout.py' ]] ; then
#        pycallgraph -o "${pdffile}" -f pdf "${1}" "${hash}" "${hash}" "0"
#      else
#        pycallgraph -o "${pdffile}" -f pdf "${1}"
#      fi
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
