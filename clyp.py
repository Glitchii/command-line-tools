from sys import stdin, stderr
from argparse import ArgumentParser
from pyperclip import copy, paste

arg = ArgumentParser(description = "copy out put or output text from clipboard",)
arg.add_argument('-p', '--paste', action="store_true", help='output instead of copying')
arg.add_argument('text', nargs='?', default=None, help='text to copy or paste if not piped')
args = arg.parse_args()

def start():
    if not args.text and not args.paste:
        if stdin.isatty():
            return print('please provice text if not piped', file=stderr)

    print(paste()) if args.paste else copy(args.text or stdin.read())

start()

"""
Examples:
    Copy file outpup to clipboard:
        $ cat file | clyp               # If clyp is compiled
        $ cat file | python clyp.py -p  # From Python file
        $ clyp.py 'Hello world'         # Copy 'Hello world' to clipboard
    
    Paste from clipboard to terminal (clyp --paste):
        $ echo "$(clyp -p)"             # print the output of 'clyp -p' (clipboard data)
        $ clyp -p | cat                 # cat prints stdin data opposed to echo which does not print piped data
"""