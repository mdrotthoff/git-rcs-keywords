#! /bin/bash
if ! [[ -d .git ]] ; then
   echo "Current directory is not a repository root"
   echo "*** Aborting ***"
   exit 1
fi

git stash save
rm .git/index
git checkout HEAD -- "$(git rev-parse --show-toplevel)"
git stash pop
