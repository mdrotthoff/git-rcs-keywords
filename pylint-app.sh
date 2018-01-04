#! /bin/bash
# Simple shell script to run the git RCS keywords programs through pylint

# $Author$
# $Date$
# $Source$


for app in *.py ; do
  pylint "${app}" >> "${app}.lint" 2>&1
done
