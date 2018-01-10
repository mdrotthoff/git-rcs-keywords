This module provides a means to add keyword expansion of the following
standard RCS tags to your git projects:

|----------|-----------------------------------------------------------|
| Keyword  | Value used |
|----------|-----------------------------------------------------------|
| Id       | Composition of the file name, commit date, and author name |
| Date     | Date the change was committed to the repository |
| Author   | Author's name and e-mail address from the commit log |
| Rev      | Date the change was commited |
| Revision | Date the change was commited |
| File     | Name of the file |
| Source   | Name of the file complete with relative path |
| Hash     | Commit hash of the change |
|----------|-----------------------------------------------------------|


The mechanism used is a combination of git filters and git event hooks.

There are two filters programs registered with the git repository.  The clean filter
is registered to convert the RCS keyword from an expanded state to a keyword state.
This allows the keyword without expansion to be stored in the git repository.  The
clean filter is run whenever a file is added to the git change log prior to
committing the change to the local git repository. The smudge filter is registered
to convert the RCS keywords into an expanded state for storage in the local copy
of the repository.  The smudge filter is run whenever a file is checked out
as the result of a commit, branch change, or any other time the file is created
from the git repository.

Additionally, there are three git event hooks registered to ensure that the data used
in expanding the RCS keywords is accurate and consistent.  Due to the method git uses
to manage pulling changes from the remote copy of the repository, the events are used
to trigger a fresh checkout of the modified files under specific conditions.  The three
event hooks registered are:

1. post-checkout event - re-processes files found during a git checkout that may not
have had up-to-date commit information at the time of the checkout

2. post-commit event - re-processes files which were just added to the local repository
as a part of a git commit action so that the keyword data is re-expanded for the latest
commit

3. post-merge event - re-process files found during the latest git merge action as the
result of a git pull or git merge action


To install the rcs keyword expansion support, execute the install.py program in the
repository.  This may either be done at the root of the git repository or by
providing the directory path of the repository root on the command line.  The installer
will copy the two filter programs into the .git/filters folder of the repository.
Additionally, the three event hook programs will be copied into the relevant event
subfolder (named <event>.d) in the .git/hooks folder.  A git hook manager will be also
be copied into the .git/hooks folder to act as a control program to allow multiple
event hooks to exist for each event being registered.  Next, the installer will
register the filters in the .git/config file so that they will be called as needed by git.
The installer will also register the (hard-coded) file patterns into the file
.git/info/attributes to control which files in the repository are managed by the
filters.  Finally, if the repository has any sub-modules, the filters will also be
installed into the submodules.
