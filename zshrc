function commit_msg() {
  if [ -z "$(git diff)" ]; then
     echo "feat: Minor changes"

  else
       git diff | pytgpt generate --intro "Provided is a diff file. Make concise commit message from it. Each change should occupy one line only. For each line, ensure you start with category of changes made followed by full colon such as 'feat:', 'fix:', 'patch:' or any other reasonable word. Do not format the response in markdown but rather a plain text." -n -fp '/tmp/commit_message.txt' --whole "\n{{stream}}"
  fi

}

function commit_msg_file(){
  save_to="/tmp/latest_commit_msg"
  echo "$(commit_msg)" > $save_to
  echo $save_to
}

function ai_commit(){
     push . -F "$(commit_msg_file)"
}