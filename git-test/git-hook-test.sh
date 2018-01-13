#! /bin/bash

git_hook_name=$(basename "${0}")
if [[ -z ${log_file} ]] ; then
  log_file="${HOME}/${git_hook_name}.log"	
  echo " " > "${log_file}"
fi

echo "git_hook_name: ${git_hook_name}"
echo "log_file: ${log_file}"

write_log()
{
   echo "$(date +"%Y-%m-%d %T") ${1}" >> "${log_file}"
}

write_log_blank()
{
   echo " " >> "${log_file}"
}

write_log "**** Executing test for ${git_hook_name} ****"
write_log "Log file: ${log_file}"
write_log_blank

write_log "Input parameters"
args=("$@") 
ELEMENTS=${#args[@]} 
for (( i=0;i<ELEMENTS;i++)); do 
  write_log "Param $((i + 1)): ${args[${i}]}"
done
write_log_blank

write_log "GIT environment"
env | grep -E '^GIT|^vauto_git' >> "${log_file}" 2>&1
write_log_blank

#write_log "Shell environment"
#env >> "${log_file}" 2>&1
#write_log_blank

write_log "Exiting test for ${git_hook_name} ****"
write_log_blank
write_log_blank
write_log_blank
