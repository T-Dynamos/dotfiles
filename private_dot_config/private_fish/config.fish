if status is-interactive
    # Commands to run in interactive sessions can go here
  set fish_greeting
end

source "$HOME/.cargo/env.fish"
export PATH="$PATH:/home/tdynamos/nchat/build/bin:/home/tdynamos/.local/bin:/home/tdynamos/woomer/target/release/"
alias clear='printf "\e[H\e[3J"'
