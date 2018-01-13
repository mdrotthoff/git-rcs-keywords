#! /bin/bash
# Simple shell script to install the rcs keywords filter
# $Author$
# $Date$
# $Source$

curr_dir="$(pwd)"
exec_dir="$(dirname "${0}")"
exec_dir="$(realpath "${exec_dir}")"
filter_ext="sql txt yml xml pl sh md ora"
# git_debug_flag values:
# 0: no debugging
# 1: debug
git_debug_flag=1

#################################
#  Debug print                  #
#################################
debug_print ()
{
# Params:
# 1: Message to print

  if [[ ${git_debug_flag} -eq 0 ]] ; then
    return
  fi

  if [[ -z "${1}" ]] ; then
    echo 'Subroutine requires one parameter'
    exit 1
  fi
  
  echo "${1}"
}

#################################
#  Register extensions          #
#################################
register_extension ()
{
# Params:
# 1: Attribute file name
# 2: File extension

  local attribute_file
  local filter_ext
  local filter_count

  if [[ -z "${2}" ]] ; then
    echo 'Subroutine requires two parameters'
    exit 1
  fi

  attribute_file="${1}"
  filter_ext="*.${2}"

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
# Params:
# 1: Prompt message

  if [[ ${git_debug_flag} -eq 1 ]] ; then
    return 0
  fi

  local answer
  local prompt

  if [[ -z "${1}" ]] ; then
    echo 'Subroutine requires one parameter'
    exit 1
  fi

  answer=''
  prompt="${1}"

  while true ; do
    read -pr "${prompt} (Y/N)? " answer
    case $answer in
      Y) return 0
         ;;
      y) return 0
         ;;
      N) return 1
         ;;
      n) return 1
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
# Params:
# 1: File name

  local filename

  if [[ -z "${1}" ]] ; then
    echo 'Subroutine requires one parameter'
    exit 1
  fi

  filename="${1}"

  prompt_yes_no "Overwrite the file ${filename}?"
  return $?
}

#################################
#  Ask Install Submodule        #
#################################
ask_install_submodule ()
{
# Params:
# 1: Submodule name

  local submodule

  if [[ -z "${1}" ]] ; then
    echo 'Subroutine requires one parameter'
    exit 1
  fi

  submodule="${1}"
  
  prompt_yes_no "Install to submodule ${submodule}?"
  return $?
}

#################################
#  Install hook manager         #
#################################
install_hook_manager ()
{
# Params:
# 1: Hook dir
# 2: Hook manager name
# 3: Hook manager file to install

  local hook_dir
  local hook_manager_name
  local hook_install_source

  # Validate the required parameters are present
  if [[ -z "${3}" ]] ; then
    echo 'Subroutine requires three parameters'
    exit 1
  fi
  
  hook_dir="${1}"
  hook_manager_name="${2}"
  hook_install_source="${3}"
  
  debug_print "Hook dir: ${hook_dir}"
  debug_print "Hook manager name: ${hook_manager_name}"
  debug_print "Hook install source: ${hook_install_source}"

  # Verify the hook directory exists  
  if ! [[ -d "${hook_dir}" ]] ; then
    echo "Hook directory ${hook_dir} does not exist"
    exit 2
  fi
  debug_print "Hook directory ${hook_dir} exists"

  # Make sure there is not a git-hook-manager present
  if [[ -x "${hook_dir}/${hook_manager_name}" ]] ; then
    echo "git hook manager already exists as ${hook_dir}/${hook_manager_name}"
    if [[ $(ask_overwrite "${hook_manager_name}") -eq 0 ]] ; then
      if ! cp -f "${exec_dir}/${git_hook_manager}" "${hook_dir}/${hook_manager_name}" ; then
        echo "Unable to overwrite hook manager ${git_hook_manager} to ${hook_dir}/${hook_manager_name}"
        exit 1
      fi
      echo "git hook manager installed to ${hook_dir}/${hook_manager_name}."
    else
      echo "*** Assuming the existing git-hook-manager provides the required"
      echo "functionality of chaining multiple hooks of a given type. ***"
    fi
  else
    if ! cp "${exec_dir}/${git_hook_manager}" "${hook_dir}/${hook_manager_name}" ; then
      echo "Failed to install git hook manager ${hook_manager_name} to ${hook_dir}/${hook_manager_name}"
      exit 1
    fi
    echo "git hook manager ${hook_manager_name} installed to ${hook_dir}/${hook_manager_name}"
  fi
}

#################################
#  Install hook                 #
#################################
install_hook ()
{
# Params:
# 1: Hook dir
# 2: Hook name
# 3: Hook manager name
# 4: Hook file to install

  local hook_dir
  local hook_event
  local hook_event_dir
  local hook_manager_name
  local hook_install_source
  local hook_install_file
  local init_dir
  local hook_event_alternate

  # Validate the required parameters are present
  if [[ -z "${4}" ]] ; then
    echo 'Subroutine requires four parameters'
    exit 1
  fi
  
  hook_dir="${1}"
  hook_event="${2}"
  hook_event_dir="${hook_event}.d"
  hook_manager_name="${3}"
  hook_install_source="${4}"
  hook_install_file="$(basename "${hook_install_source}")"

  debug_print "Hook dir: ${hook_dir}"
  debug_print "Hook event: ${hook_event}"
  debug_print "Hook event dir: ${hook_event_dir}"
  debug_print "Hook manager name: ${hook_manager_name}"
  debug_print "Hook install source: ${hook_install_source}"
  debug_print "Hook install file: ${hook_install_file}"

  init_dir="$(pwd)"

  # Change to the hook directory  
  if ! cd "${hook_dir}" ; then
    echo "Unable to change to the hook directory ${hook_dir}"
    exit 2
  fi
  debug_print "Pwd: $(pwd) (should be ${hook_dir}"

  # Make sure the hook manager is installed
  if ! [[ -f "${hook_manager_name}" ]] ; then
    echo "Hook manager ${hook_manager_name} not found"
    exit 1
  fi
  
  # Make sure the hook event directory exists
  if [[ -e "${hook_event_dir}" ]] ; then
    if ! [[ -d "${hook_event_dir}" ]] ; then
      echo "Hook directory ${hook_event_dir} exists but is not a sub-directory"
      exit 1
    fi
  else
    if ! mkdir "${hook_event_dir}" ; then
      echo "Unable to create directory ${hook_dir}/${hook_event_dir}"
      exit 1
    fi 
  fi

  # If the hook event file exists
  debug_print "$(ls -l "${hook_event}")"
  if [[ -e "${hook_event}" ]] ; then
    if ! [[ -L "${hook_event}" ]] ; then

      # Move any existing hook into the hook event directory
      hook_event_alternate="${hook_event_dir}/zz-${hook_event}${RANDOM}"
      if ! mv "${hook_event}" "${hook_event_alternate}" ; then
        echo "Unable to move existing hook ${hook_dir}/${hook_event} to ${hook_event_alternate}"
        exit 1
      fi
      debug_print "Move existing hook ${hook_dir}/${hook_event} to ${hook_event_alternate}"

      debug_print "ln -s ${hook_manager_name} ${hook_event}"
      # Link the hook manager to the hook event
      if ! ln -s "${hook_manager_name}" "${hook_event}" ; then
        echo "Unable to link ${hook_event} to hook manager ${hook_manager_name}"
        exit 1
      fi 
      echo "Linked ${hook_event} to hook manager ${hook_manager_name}"
    fi
  else
    # Link the hook manager to the hook event
    if ! ln -s "${hook_manager_name}" "${hook_event}" ; then
      echo "Unable to link ${hook_event} to hook manager ${hook_manager_name}"
      exit 1
    fi 
    echo "Linked ${hook_event} to hook manager ${hook_manager_name}"
  fi

  # Copy the hook file to the hook event directory
  if ! cp "${hook_install_source}" "${hook_event_dir}/${hook_install_file}" ; then
    echo "Unable to copy the hook file to directory ${hook_event_dir}"
    exit 1
  fi 

  # Return to the original directory  
  if ! cd "${init_dir}" ; then
    echo "Unable to return to source directory ${init_dir}"
    exit 2
  fi
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
  local curr_dir
#  local post_commit_file
  local git_hook_manager
#  local git_hook_manager_name
#  local hooks_manager
  local smudge_filter
  local clean_filter
  local hook_list

  curr_dir="$(pwd)"
  git_hook_manager='git-hook-manager.pl'

  # Install the git hook manager
  install_hook_manager "${hooks_dir}" "${git_hook_manager}" "${exec_dir}/${git_hook_manager}" 
  echo " "

  # Install the git hooks
  hook_list="pre-commit prepare-commit-msg commit-msg applypatch-msg pre-applypatch pre-rebase post-rewrite post-checkout"
  hook_list="${hook_list} post-merge pre-push pre-auto-gc pre-receive update post-receive"
  for hook_entry in ${hook_list} ; do
    install_hook "${hooks_dir}" "${hook_entry}" "git-hook-manager.pl" "${exec_dir}/git-hook-test.sh"
  done
  # install_hook "${hooks_dir}" "post-commit" "git-hook-manager.pl" "${exec_dir}/git_hook_test"
  echo " "


# Create the filters directory
  if [[ -d ${filters_dir} ]] ; then
    echo "filters directory already exists.  rcs-keywords filters will be added to the"
    echo "existing directory."
  else
    if ! mkdir "${filters_dir}" ; then
      echo "Unable to create filter directory ${filters_dir}"
      exit 1
    fi
    echo "filters directory created."
  fi
  echo " "

# Copy the clean filter into the target directory
  clean_filter="${filters_dir}/rcs-keywords.clean.pl"
  if [[ -f ${clean_filter} ]] ; then
    echo "rcs-keywords clean filter ${clean_filter} already exists."
    if [[ $(ask_overwrite "${clean_filter}") -eq 0 ]] ; then
      if ! cp -f "${exec_dir}/rcs-keywords.clean.pl" "${clean_filter}" ; then
        echo "Unable to overwrite clean filter ${clean_filter}"
        exit 1
      fi
      echo "rcs-keywords clean filter ${clean_filter} over written."
    else
      echo "rcs-keywords clean filter assumed to already be installed."
    fi
  else
    if ! cp "${exec_dir}/rcs-keywords.clean.pl" "${clean_filter}" ; then
      echo "Unable to copy clean filter ${clean_filter}"
      exit 1
    fi
    echo "rcs-keywords clean filter ${clean_filter} installed."
  fi
  echo " "

# Copy the smudge filter into the target directory
  smudge_filter="${filters_dir}/rcs-keywords.smudge.pl"
  if [[ -f ${smudge_filter} ]] ; then
    echo "rcs-keywords smudge filter ${smudge_filter} already exists."
    if [[ $(ask_overwrite "${smudge_filter}") -eq 0 ]] ; then
      if ! cp -f "${exec_dir}/rcs-keywords.smudge.pl" "${smudge_filter}" ; then
        echo "Unable to overwrite smudge filter ${smudge_filter}"
        exit 1
      fi
      echo "rcs-keywords smudge filter ${smudge_filter} installed."
    else
      echo "rcs-keywords smudge filter assumed to already be installed."
    fi
    echo " "
  else
    if ! cp "${exec_dir}/rcs-keywords.smudge.pl" "${smudge_filter}" ; then
      echo "Unable to copy smudge filter ${smudge_filter}"
      exit 1
    fi
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
  local curr_dir
  local submodule_list
  local git_dir
  local work_dir

  curr_dir="$(pwd)"
  submodule_list="$(find .git/modules -name config -print)"

# Prompt about installed rcs-keywords to submodules
  for submodule in $submodule_list ; do
    echo "Found submodule ${submodule}"
    git_dir="$(dirname "${submodule}")"
    if ! cd "${git_dir}" ; then
    echo "Unable to change directory to git directory ${git_dir}"
      exit 2
    fi
    work_dir="$(grep worktree config | awk '{ print \$3 }')"
    if ! [[ -z ${work_dir} ]] ; then
      if [[ $(ask_install_submodule "$(dirname "${submodule}")") -eq 0 ]] ; then
        if ! cd "${work_dir}" ; then
          echo "Unable to change directory to work directory ${work_dir}"
          exit 2
        fi
        if [[ -f .git ]] ; then
          install_filter "$(awk '{ print $2 }' < .git)"
          echo "rcs-keywords filter installed to submodule ${git_dir} "
        fi
      else
        echo "rcs-keywords filter NOT installed to submodule ${git_dir} "
      fi
    fi
    if ! cd "${curr_dir}" ; then
      echo "Unable to return to current directory ${curr_dir}"
      exit 2
    fi
    echo " "
  done
}

#################################
#  Main line                    #
#################################
# If .git is a file, we are in a submodule.  Set vars accordingly.
if [[ -f .git ]] ; then
  install_filter "$(awk '{ print $2 }' < .git)"
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
