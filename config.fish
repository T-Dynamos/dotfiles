if status is-interactive
  set fish_greeting  
  python3 -c "import os;print(\"Happy Birthday!\nWhere are you?\") if '21 April' in os.popen(\"date\").read() else print"
  # Commands to run in interactive sessions can go here
end

set PATH "$PATH:$HOME/.local/bin"

export ANDROID_HOME='/opt/android-sdk'
export PATH="$PATH:$ANDROID_HOME/emulator"
