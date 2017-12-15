#! /bin/bash
# Simple shell script to install the rcs keywords filter
# $Author$
# $Date$
# $Source$

curr_dir=$(pwd)
exec_dir=$(dirname "${0}")
exec_dir=$(realpath "${exec_dir}")
filter_ext="sql txt yml xml pl sh md ora"

#################################
#  Register extensions          #
#################################
register_extension ()
{
  local attribute_file="${1}"
  local filter_ext="*.${2}"
  local filter_count

# Check to see if the file extenstion is already registered
  if [[ -f ${attribute_file} ]] ; then
    filter_count=$(grep -Ec "^[[:blank:]]*\\${filter_ext}[[:blank:]][[:blank:]]*filter=rcs-keywords" "${attribute_file}")
  else
    filter_count=0
  fi

# Register the file extension for the rcs-keywords filter if it is not
# already registered.
  if [[ ${filter_count} -eq 0 ]] ; then
    echo "${filter_ext}   filter=rcs-keywords" >> "${attribute_file}"
    echo "${filter_ext} now associated with the rcs-keywords filter"
  else
    echo "${filter_ext} already associated with the rcs-keywords filter"
  fi
}

#################################
#  Prompt yes or no             #
#################################
prompt_yes_no ()
{
  local answer=''
  local prompt="${1}"

  while true ; do
    read -pr "${prompt} (Y/N)? " answer
    case $answer in
      Y) return 1
         ;;
      y) return 1
         ;;
      N) return 0
         ;;
      n) return 0
         ;;
      *) echo "Valid response is Y(es) or N(o)"
    esac
  done
}

#################################
#  Ask Owerwrite                #
#################################
ask_overwrite ()
{
  local filename="${1}"

  prompt_yes_no "Overwrite the file ${filename}?"
  return $?
}

#################################
#  Ask Install Submodule        #
#################################
ask_install_submodule ()
{
  local submodule="${1}"

  prompt_yes_no "Install to submodule ${submodule}?"
  return $?
}

#################################
#  Install filter               #
#################################
install_filter ()
{
  local git_dir="${1}"
  local hooks_dir="${1}/hooks"
  local filters_dir="${1}/filters"
  local attribute_file="${1}/info/attributes"
#  local config_file="${git_dir}/config"
  local curr_dir="$(pwd)"
  local post_commit_file
  local git_hook_manager
  local hooks_manager
  local smudge_filter
  local clean_filter

# Make sure there is not a git-hook-manager present
  git_hook_manager="git-hook-manager.pl"
  hooks_manager="${hooks_dir}/${git_hook_manager}"
  if [[ -x ${hooks_manager} ]] ; then
    echo "git hook manager already exists as ${hooks_manager}."
    ask_overwrite "${hooks_manager}"
    if [[ $? -eq 1 ]] ; then
      cp "${exec_dir}/${git_hook_manager}" "${hooks_manager}"
      echo "git hook manager installed to ${hooks_manager}."
    else
      echo "Assuming the existing git-hook-manager provides the required"
      echo "functionality of chaining multiple hooks of a given type."
    fi
  else
    cp "${exec_dir}/${git_hook_manager}" "${hooks_manager}"
    echo "git hook manager installed to ${hooks_dir}."
  fi
  echo " "

# Create the post-commit.d directory
  if [[ -d ${hooks_dir}/post-commit.d ]] ; then
    echo "post-commit.d directory already exists.  rcs-keywords hook will be added to the"
    echo "existing directory."
  else
    mkdir "${hooks_dir}/post-commit.d"
    echo "post-commit.d directory created."
  fi
  echo " "

# Link the git-hook-manager into the git post-commit event
  cd "${hooks_dir}" || exit 2
  if [[ -f post-commit ]] ; then
    if [[ -s post-commit ]] ; then
      post_commit_file=$(realpath post-commit)
      post_commit_file=$(basename "${post-commit-file}")
      if [[ ${post_commit_file} != "${git_hook_manager}" ]] ; then
        echo "post-commit symbolic link already exists.  Skipping symbolic link to"
        echo "${git_hook_manager}."
      fi
    else
      mv -n post-commit post-commit.d/99-post-commit
      if [[ -f post-commit ]] ; then
        mv post-commit post-commit.save.rcs-keywords
        echo "Existing post-commit handler saved as post-commit.save.rcs-keywords"
        echo "Move it into post-commit.d if it is still required"
      fi
      ln -s "${git_hook_manager}" post-commit
    fi
  else
    ln -s "${git_hook_manager}" post-commit
  fi
  cd "${curr_dir}" || exit 2
  echo " "

# Copy the post-commit hook into the target directory
  post_commit_hook="01-rcs-keywords.post-commit.pl"
  if [[ -f ${hooks_dir}/post-commit.d/${post_commit_hook} ]] ; then
    echo "rcs-keywords post-commit handler already exists."
    ask_overwrite "${hooks_dir}/post-commit.d/${post_commit_hook}"
    if [[ $? -eq 1 ]] ; then
      cp "${exec_dir}/${post_commit_hook}" "${hooks_dir}/post-commit.d/${post_commit_hook}"
      echo "rcs-keywords post-commit handler installed."
    else
      echo "Assuming it provides the existing rcs-keywords post-commit required"
    fi
  else
    cp "${exec_dir}/${post_commit_hook}" "${hooks_dir}/post-commit.d/${post_commit_hook}"
    echo "rcs-keywords post-commit handler installed."
  fi
  echo " "

# Create the filters directory
  if [[ -d ${filters_dir} ]] ; then
    echo "filters directory already exists.  rcs-keywords filters will be added to the"
    echo "existing directory."
  else
    mkdir "${filters_dir}"
    echo "filters directory created."
  fi
  echo " "

# Copy the clean filter into the target directory
  clean_filter="${filters_dir}/rcs-keywords.clean.pl"
  if [[ -f ${clean_filter} ]] ; then
    echo "rcs-keywords clean filter ${clean_filter} already exists."
    ask_overwrite "${clean_filter}"
    if [[ $? -eq 1 ]] ; then
      cp "${exec_dir}/rcs-keywords.clean.pl" "${clean_filter}"
      echo "rcs-keywords clean filter ${clean_filter} over written."
    else
      echo "rcs-keywords clean filter assumed to already be installed."
    fi
  else
    cp "${exec_dir}/rcs-keywords.clean.pl" "${clean_filter}"
    echo "rcs-keywords clean filter ${clean_filter} installed."
  fi
  echo " "

# Copy the smudge filter into the target directory
  smudge_filter="${filters_dir}/rcs-keywords.smudge.pl"
  if [[ -f ${smudge_filter} ]] ; then
    echo "rcs-keywords smudge filter ${smudge_filter} already exists."
    ask_overwrite "${smudge_filter}"
    if [[ $? -eq 1 ]] ; then
      cp "${exec_dir}/rcs-keywords.smudge.pl" "${smudge_filter}"
      echo "rcs-keywords smudge filter ${smudge_filter} installed."
    else
      echo "rcs-keywords smudge filter assumed to already be installed."
    fi
    echo " "
  else
    cp "${exec_dir}/rcs-keywords.smudge.pl" "${smudge_filter}"
    echo "rcs-keywords smudge filter ${smudge_filter} installed."
  fi

# Configure the filters for use
  echo "Configuring the filters for use"
  git config --local filter.rcs-keywords.clean "${clean_filter}"
  git config --local filter.rcs-keywords.smudge "${smudge_filter} %f"
  echo "rcs-keywords configuring for use"
  echo " "

# Register the file extensions to be supported
  echo "Registering file extension for rcs-keywords"
  for file_ext in ${filter_ext} ; do
    register_extension "${attribute_file}" "${file_ext}"
  done
  echo "File extension for rcs-keywords registered"
  echo " "
}

#################################
#  Process submodules           #
#################################
process_submodules ()
{
  local curr_dir=$(pwd)
  local submodule_list=$(find .git/modules -name config -print)
  local git_dir
  local work_dir

# Prompt about installed rcs-keywords to submodules
  for submodule in $submodule_list ; do
    echo "Found submodule ${submodule}"
    git_dir=$(dirname "${submodule}")
    cd "${git_dir}" || exit 2
    work_dir=$(grep worktree config | awk '{ print \$3 }')
    if ! [[ -z ${work_dir} ]] ; then
      ask_install_submodule "$(dirname \"${submodule}\")"
      if [[ $? -eq 1 ]] ; then
        cd "${work_dir}" || exit 2
        if [[ -f .git ]] ; then
          install_filter "$(awk '{ print $2 }' < .git)"
          echo "rcs-keywords filter installed to submodule ${git_dir} "
        fi
      else
        echo "rcs-keywords filter NOT installed to submodule ${git_dir} "
      fi
    fi
    cd "${curr_dir}" || exit 2
    echo " "
  done
}

#################################
#  Main line                    #
#################################
# If .git is a file, we are in a submodule.  Set vars accordingly.
if [[ -f .git ]] ; then
  install_filter "$(awk '{ print $2 } < .git')"
  exit 0
# If .git is a directory, we are in a main module.  Set vars accordingly.
elif [[ -d .git ]] ; then
  install_filter ".git"
  if [[ -d .git/modules ]] ; then
    process_submodules
  else
    echo "Repo does NOT have submodules"
  fi
  exit 0
# If .git is a directory, we are in a main module.  Set vars accordingly.
else
  echo "Installer must be run from the root of the git repository rcs-keywords should be"
  echo "installed to"
  exit 1
fi

echo " "
