from json import loads
from urllib3 import PoolManager
from sys import stdin, stdout, stderr, argv
from argparse import ArgumentParser
from re import finditer, search, sub

usage = f"{argv[0].split('/')[-1]} regex [file] [-h] [-V] [-o] [-a] [-c MARKER] [-t TEXT] [-s SUBSTITUTE] [-d]"
parser = ArgumentParser(description = "print lines that match (Python) regex patterns", usage=usage)
parser.add_argument('-V', '--version', action="store_true", help='display the current version')
parser.add_argument('-o', '--only-match', action="store_true", help='display only (nonempty) match')
parser.add_argument('-a', '--all', action="store_true", help="include lines that don't match, but highlight matches")
parser.add_argument('-c', '--color', '--colour', metavar="MARKER", help='highlight marker. Options: red, blue, green... Default: red', default='red')
parser.add_argument('-t', '--text', help="match from text instead of file", default='')
parser.add_argument('-s', '--substitute', help="substitute/replace. Support \\1 \\2...", default=False)
parser.add_argument('-d', '--delete', action="store_true", help="delete matched")
parser.add_argument('regex', nargs='?', help='regular expression', default=None)
parser.add_argument('file', nargs='?', help='path of file to read')
args = parser.parse_args()

def errout(string):
    print('error:', string.rstrip('\n'), file=stderr)
    exit(1)

highlights = {
    'bl':        '\x1b[1;30m',
    'black':    '\x1b[1;30m',
    'r':        '\x1b[1;31m',
    'red':      '\x1b[1;31m',
    'g':        '\x1b[1;32m',
    'green':    '\x1b[1;32m',
    'y':        '\x1b[1;33m',
    'yellow':   '\x1b[1;33m',
    'b':        '\x1b[1;34m',
    'blue':     '\x1b[1;34m',
    'm':        '\x1b[1;35m',
    'magenta':  '\x1b[1;35m',
    'c':        '\x1b[1;36m',
    'cyan':     '\x1b[1;36m',
    'w':        '\x1b[1;37m',
    'white':    '\x1b[1;37m',
    'n':        '\x1b[0m',
    'none':     '\x1b[0m',
}

colr = str(args.color).lower()
if colr not in highlights:
    hl = highlights
    highlights = ", ".join([(f"{hl[c]}[bl]ack" if c == "black" else hl[c] + "[" + c[0] + "]" + c[1:]) + hl["n"]
        for c in tuple(hl)[:-1] if len(c) > 2])
    errout(f'Incorrect highlight, choose from {highlights}, or [n]one\n')

colr, rst = highlights[colr], highlights['none']
def start(data, tty = stdout.isatty()):
    try:
        for line in data:
            if search(args.regex, line):
                iterfind = finditer(args.regex, line)
                if iterfind:
                    output = out = None
                    for found in iterfind:
                        group = found.group()
                        if args.delete:
                            out = print(line.replace(group, ''))
                        elif args.substitute:
                            out = print(sub(args.regex, args.substitute, line).rstrip('\n'))
                        elif args.only_match:
                            out = print(found.group().replace(group, colr+group+rst if tty else group).rstrip('\n'))
                        else:
                            output = found.string.replace(group, colr+group+rst if tty else group)
                    
                    # rstrip because full lines have \n at the end
                    not out and output and print(output.rstrip('\n'))
            else:
                args.all and print(line.rstrip('\n'))
    except Exception as error:
        errout(error)

if args.version:
    version, repo = '0.8', 'https://github.com/Glitchii/command-line-tools'
    api = 'https://api.github.com/repos/Glitchii/command-line-tools'
    about = loads(PoolManager().request('GET', api).data)

    if about.get('description'):
        description = about.get('description')
        commits = loads(PoolManager().request('GET', f'{api}/commits').data)
        commits = str(len(commits))
        available_version = commits[:len(commits)-1]+'.'+commits[-1] if len(commits) > 1 else '0.' + commits
        update_message = 'An update may be available.'
        print(description,
            f"\nRepository: {repo}",
            f"Current version: {version}",
            f"Github version: {available_version}",
            sep='\n')
        if version != available_version:
            print(f'\n\x1b[2;37m{update_message}\x1b[0m' if stdout.isatty() else update_message)
    else:
        print(f"Current version: {version}\nRepository: {repo}")
    


elif not args.regex:
    print('usage:', usage)
    print('regex is required. Use --help or -h parameter for help')
elif args.text or not stdin.isatty():
    start(args.text.splitlines() or stdin)
else:
    if not args.file:
        errout("specify a file path, or use --text/-t for text")
    try:
        with open(args.file) as file:
            start(file.readlines())
    except FileNotFoundError:
        errout(f'{args.file}: no such file')
    except IsADirectoryError:
        errout(f'{args.file}: expected a file, got directory')

stderr.close()

# TODO:
# prep: option to return only first, last, or nth matches
# prep: add match invert