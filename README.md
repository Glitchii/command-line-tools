# Commandline Tools
Simple tools I made because I find myself to need them quite a lot.  
The scripts are in the scripts directory. You can compile them (recommended) by running `compile.sh` or run them straight with python.
Change directory to where `compile.sh` is before running it.

## Tools

## PREP - Python  Regular Expression Print:
Similar to, and inspired by grep. I find myself to use grep quite a lot, but along with some other issues, the regular expression was not quite advanced and so I made this.


```sh
$ prep '/home/\w+' -t "$PATH"       # Find /home/anyuser in path.
$ cat users.txt | prep "John Doe"   # prep data from pipe
$ prep "John Doe" users.txt         # prep data from file
$ prep -o "John Doe" users.txt      # print only the matches (not full lines)
$ prep -a "\d" users.txt            # print all lines but with digits highlighted
```

##  CLYP:
Clyp allows to copy text or file content to clipboard, or pasting from clipboard


```sh
# Copy file outpup to clipboard:
$ clyp file.txt                 # Copy content of file.txt to clipboard
$ cat file.txt | clyp           # Copy from pipe
$ cat file.txt | python clyp.py # If not compiled from python

# Copy text to clipboard:
$ clyp 'Hello world'            # Copy 'Hello world' to clipboard
$ echo 'Hello world' | clyp     # Copy from pipe echo

# Paste from clipboard to terminal (clyp --paste/-p):
$ echo "$(clyp -p)"             # print the output of 'clyp -p' (clipboard data)
$ clyp -p | cat                 # cat instead of echo because echo accepts no stdin
```