import argparse
import re
import sys


def create_parser(subparsers):
    parser = subparsers.add_parser(
        'ffilter',
        description='returns interfaces for functions'
    )
    parser.add_argument(
        'src', nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    parser.add_argument(
        '--name', nargs='?',
        default=None
    )
    parser.add_argument(
        'dest', nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout
    )
    parser.set_defaults(func=main)


def main(parsed):
    fname = parsed.src.name
    if parsed.name:
        name = parsed.name
    else:
        name = fname.split('.')[0]

    buf = parsed.src.read()
    matches = re.findall(
        'FUNCTION ([A-Z_]+2[A-Z\d_]+)(\([^\)\n]+\))\n(( *!!.*\n)+)',
        buf,
        re.I
    )
    if len(matches) > 0:
      parsed.dest.write('  !! From file %s\n' % fname)
      parsed.dest.write('\n'.join(
          '  use %s, only: %s!!%s\n%s' % (
              name, func.lower(), args, comments
          )
          for func, args, comments, _ in matches
      ))
      parsed.dest.write('\n\n')
