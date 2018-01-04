#! /bin/bash
# Simple shell script to run the git RCS keywords programs through pylint


# $Author$
# $Date$
# $Source$

output_log="pylint-app.log"
source_apps=('install.py'  'git-hook.py' 
             'rcs-filter-clean.py' 'rcs-filter-smudge.py'
             'rcs-post-checkout.py' 'rcs-post-commit.py' 'rcs-post-merge.py')


if [[ -f "${output_log}" ]] ;then
  rm -f "${output_log}" 2> /dev/null
fi

echo "Source_apps: ${source_apps[*]}"
#exit 0

for py_app in "${source_apps[@]}" ; do
  echo "Processing ${py_app}" >> "${output_log}"
  echo " " >> "${output_log}"
  pylint "${py_app}" >> "${output_log}" 2>&1
  echo " " >> "${output_log}"
  echo " " >> "${output_log}"
done
