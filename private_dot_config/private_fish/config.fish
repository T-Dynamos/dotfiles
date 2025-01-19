if status is-interactive
    # Commands to run in interactive sessions can go here
  set fish_greeting
end

export PATH="$PATH:/home/tdynamos/nchat/build/bin:/home/tdynamos/.local/bin:/home/tdynamos/woomer/target/release/:/home/tdynamos/.local/share/gem/ruby/3.0.0/bin"
alias clear='printf "\e[H\e[3J"'
zoxide init fish | source
alias cd="z"
alias feh="swayimg"
