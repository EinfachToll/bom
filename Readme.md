# bom -- a simple bookmark manager for the Zsh

```bash
bom add my_project ~/programming_stuff/even/more/stuff/

cd ~my_project
cp file ~my_project
...
```

The Zsh has a handy feature called *named directory hashes* which can be seen as abbreviations for arbitrary directories. In contrast to simple
aliases, they can be used at any place in a command.

However, typing this to add a new bookmark

```bash
echo 'hash -d blu="/etc/"' >> ~/.zshrc && source ~/.zshrc
```

is a bit cumbersome, so this little script helps managing your bookmarks.

## Usage

```
bom                       displays this help
bom show                  shows all bookmarks
bom add foo /over/there/  creates a new bookmark ~foo for the directory /over/there/
bom add foo               creates a new bookmark ~foo for the current directory
bom add /over/there/      creates a new bookmark ~there (i.e. the last component) for the directory /over/there/
bom add                   creates a new bookmark for the current direcory, the name is the path's last component
bom rm foo bar            removes the bookmarks ~foo and ~bar
```

## Installation
Don't call bom.py directly, instead, put it anywhere you like and put this in your `.zshrc`:

```bash
bom() {
    local BOM_PATH="/path/to/bom.py"
    OUTPUT="$(python3 "$BOM_PATH" $@)"
    COMMAND=$(echo "$OUTPUT" | grep "^zshexec: " | sed 's/^zshexec: //')
    PRINT=$(echo "$OUTPUT" | grep -v "^zshexec: ")
    echo "$PRINT"
    eval "$COMMAND"
}
```

------
A small warning: this messes around with your `.zshrc` (but tries not to break stuff). If you don't want that, you can change the constant ZSHRC in
bom.py to whatever you want.
