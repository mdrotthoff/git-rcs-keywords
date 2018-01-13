#! /bin/bash
echo "Running git-exec"

write_log()
{
   echo "$(date +"%Y-%m-%d %T") ${1}" >> "${log_file}"
}

write_log_blank()
{
   echo " " >> "${log_file}"
}

git-exec-log="$(basename "${0}")-test"
if [[ -z ${log_file} ]] ; then
  export log_file="${HOME}/${git-exec-log}.log"
  echo " " > "${log_file}"
fi

write_log "**** Executing test for ${git-exec-log} ****"
write_log "Log file: ${log_file}"
write_log_blank

write_log "Input parameters"
args=("$@") 
ELEMENTS=${#args[@]}
for (( i=0;i<ELEMENTS;i++)); do
  write_log "Param $((i + 1)): ${args[${i}]}"
done
write_log_blank

export vauto_git_start_head
vauto_git_start_head=$(git log --pretty=format:'%H' -n 1)
write_log "vauto_git_start_head: ${vauto_git_start_head}"
write_log_blank

write_log "GIT environment"
env | grep -E '^GIT|^vauto_git' >> "${log_file}" 2>&1
write_log_blank

#write_log "Shell environment"
#env >> "${log_file}" 2>&1
#write_log_blank

write_log "Executing git commands from command line"
for i in "$@"; do 
  write_log "Executing command: git $i"
  git "$i" >> "${log_file}" 2>&1
  write_log_blank
done
write_log_blank

export vauto_git_end_head
vauto_git_end_head=$(git log --pretty=format:'%H' -n 1)
write_log "vauto_git_end_head: ${vauto_git_end_head}"
write_log_blank

if [[ "${vauto_git_start_head}" != "${vauto_git_end_head}" ]] ; then
  write_log "Files changed:"
  git diff --name-status "${vauto_git_start_head}" "${vauto_git_end_head}" >> "${log_file}" 2>&1
  write_log_blank

  write_log "Files added/updated:"
  git diff --name-only --diff-filter=ACMR "${vauto_git_start_head}" "${vauto_git_end_head}" >> "${log_file}" 2>&1
  write_log_blank
fi 
write_log_blank
write_log_blank
write_log_blank
