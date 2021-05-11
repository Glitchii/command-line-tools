from sys import stdin, stdout, stderr
from argparse import ArgumentParser
from re import finditer

arg = ArgumentParser(description = "print lines that match (Python) regex patterns")
arg.add_argument('-o', '--only-match', action="store_true", help='show only (nonempty) match')
arg.add_argument('-c', '--color', '--colour', metavar="MARKER", help='highlight marker. Options: red, blue, green... Default: red', default='red')
arg.add_argument('-t', '--text', help="match from text instead of file", default='')
arg.add_argument('regex', help='regular expression')
arg.add_argument('file', nargs='?', default=None, help='path of file to read')

highlights = {
    'black':    '\x1b[1;30m',
    'red':      '\x1b[1;31m',
    'green':    '\x1b[1;32m',
    'yellow':   '\x1b[1;33m',
    'blue':     '\x1b[1;34m',
    'magenta':  '\x1b[1;35m',
    'cyan':     '\x1b[1;36m',
    'white':    '\x1b[1;37m',
    'none':     '\x1b[0m'
}

args = arg.parse_args()

colr = str(args.color).lower()
if colr not in highlights:
    # stderr.write(f'Incorrect highlight, choose from {", ".join(list(highlights)[:-1])}, or {list(highlights)[-1]}\n')
    stderr.write(f'Incorrect highlight, choose from {", ".join([highlights[c]+c+highlights["none"] for c in tuple(highlights)[:-1]])}, or {tuple(highlights)[-1]}\n')
    exit(1)

colr, rst = highlights[colr], highlights['none']

def start(data, tty = stdout.isatty()):
    for line in data:
        if iterfind := finditer(args.regex, line):
            output = None
            for found in iterfind:
                match = found.group()
                if args.only_match:
                    print(found.group().replace(match, colr+match+rst).rstrip('\n'))
                else:
                    output = found.string.replace(match, colr+match+rst if tty else match)
            # rstrip because full lines have \n at the end
            not args.only_match and output and print(output.rstrip('\n'))

# If text is recieved from argument --text/-t or is piped
# print(args.text or stdin)
if args.text or not stdin.isatty():
    start(args.text.splitlines() or stdin)
else:
    if not args.file:
        print("Please provide a file path at the end", file=stderr)
    else:
        try:
            with open(args.file) as file:
                start(file.readlines())
        except FileNotFoundError:
            print(f'{args.file}: no such file', file=stderr)
        except IsADirectoryError:
            print(f'{args.file}: expected a file, got directory', file=stderr)

stderr.close()

# TODO:
# prep: add replace functionality
# prep: option to return only first and last matches