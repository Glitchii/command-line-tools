from sys import stdin, stderr
from argparse import ArgumentParser
from pyperclip import copy, paste

arg = ArgumentParser(description = "copy out put or output text from clipboard",)
arg.add_argument('-p', '--paste', action="store_true", help='output instead of copying')
arg.add_argument('-f', '--file', help='copy/paste from file', default=False)
arg.add_argument('text', nargs='?', help='text to copy or paste if not piped', default=None)
args = arg.parse_args()

def start(txt = args.text):
    if not (txt or args.paste or args.file):
        return print('No file (-f), text, or stdin data recieved to copy from. To paste, use -p', file=stderr)
    if args.file:
        with open(args.file) as f:
            txt = f.read()
            
    print(paste()) if args.paste else copy(txt or stdin.read())

start()