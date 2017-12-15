This module provides a means to add keyword expansion of the following
standard RCS tags to your git projects:

	 $Id$
	 $Date$
	 $File$
	 $Author$
	 $Rev$
	 $Source$
	 $Hash$

The mechanism used are git filters.  The smudge filter is run on checkout and commit.
The clean filter is run on commit.  The tags are only expanded on the local disk,
not in the repository itself.

*NOTE:* The revision used is the date the file was last commit to the git repository as
        git does not have a true revision number.

The install the rcs keyword expansion, change directory to the root of the git
repository and run the install.sh script.  It will make all of the necessary changes
to the git repository configuration.  Additionally, if there are git submodules
defined in the repository, you will be prompted as to wheter or not the functionality
should be installed into the submodules as well.

The install script will make the following changes to each git repository / submodule
into which it installs the rcs keywords functionality.  First in the <git_dir>/config
file, the following section will be added:

	[filter "rcs-keywords"]
		clean  = .git/filters/rcs-keywords-filter-clean.py %f
		smudge = .git/filters/rcs-keywords-filter-smudge.py %f

*NOTE:* Each of the filters installed has a filter_debug which by default is set to
        False (debugging not enabled).  If set to True, select information will be displayed
        to the standard error output for debugging purposes.

Next, a hook manager will be installed into the hooks directory by copying the python
module git-hook.py.  This provides the capability of having multiple hooks for the
same git event. The same code will support running hooks for other events if required
by looking for a folder of the <event name>.d. The only requirement for supporting an
additional event is to create a symbolic link to the relevent event name in the hooks
directory.

	ln -s <git_dir>/hooks/git-hook.py <git_dir>/hooks/<event name>
	mkdir <git_dir>/hooks/<event name>.d

Finally, file patterns need to be registered to be managed by filters in the file:

	<git_dir>/info/attributes

Each registration is composed of a line in the attributes file of the following pattern:

	<file pattern>		filter=rcs-keywords
