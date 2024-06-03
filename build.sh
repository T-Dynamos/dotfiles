for dir in sway waybar kitty;
do
    cp -r ~/.config/$dir $dir
done
rm -rf ~/.config/nvim/lua/custom
cp -r nvim/custom ~/.config/nvim/lua/custom
cp nvim/default.lua cp -r ~/.local/share/nvim/lazy/ui/lua/nvchad/statusline/default.lua

mkdir -p ~/.config/nvim/syntax
wget https://raw.githubusercontent.com/kivy/kivy/master/kivy/tools/highlight/kivy.vim -O ~/.config/nvim/syntax/kivy.vim
