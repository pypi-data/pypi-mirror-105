import argparse
import re
import sys


def parsedec(line):
    if '::' in line:
        line = line.split('::')[-1]
    else:
        line = line.split('(kind=prec)')[-1]
    line = line.split('=')[0]
    return [
        re.sub(
            '\(.*?\)',
            '',
            i.strip()
        ) for i in line.split(',')]


def expand_switch(block):
    prec = re.sub(
        'END FUNCTION (.*)', r'END FUNCTION \1prec',
        re.sub(
            '^( *)FUNCTION (.*?)\((.*?)\)',
            r'\1FUNCTION \2prec(\3) result(\2)',
            block,
            flags=re.S | re.M
        )
    )

    cond = re.findall(
        '!BEGIN SWITCHEROO\n(.*?)\n!CODE',
        block, flags=re.M | re.S
    )
    if len(cond) == 1:
        cond = cond[0]
        prec = prec.replace('!BEGIN SWITCHEROO\n'+cond+'\n!CODE', '')
    else:
        cond = '.false.'

    interfaces = []
    for func, args, body in re.findall(
        '^ *FUNCTION (.*?)\((.*?)\)(.*?)END FUNCTION',
        block,flags=re.M | re.S
    ):
        iface = '  FUNCTION %s(%s)\n' % (func, args)
        lines = body.splitlines()
        realvars = []
        cmplxvars = []
        while len(lines) > 0:
            line = lines.pop(0).strip()
            if len(line) == 0:
                continue
            if line.startswith('implicit ') or line.startswith('use '):
                iface += '  ' + line + '\n'
            elif line.startswith('real(kind=prec)'):
                iface += '  ' + line + '\n'
                realvars += parsedec(line)
            elif line.startswith('complex(kind=prec)'):
                iface += '  ' + line + '\n'
                cmplxvars += parsedec(line)
            elif line.startswith('integer'):
                iface += '  ' + line + '\n'
            else:
                break

        argsex = re.sub('[&\n ]','',args).split(',')
        if not all([i in realvars or i in cmplxvars for i in argsex]):
            sys.stderr.write(
                'Some args are not defined. Please check your code\n'
            )
        args16 = [
            (
                'real(%s, kind=16)' if i in realvars else 'cmplx(%s, kind=16)'
            ) % i
            for i in argsex
        ]
        ind = ', &\n ' + (' '*len('    %s = %s16' % (func, func)))
        iface += '  if(%s) then\n' % cond
        iface += '    %s = real(%s16(%s), kind=prec)\n' % (func, func, ind.join(args16))
        iface += '  else\n'
        iface += '    %s = real(%s8 (%s), kind=prec)\n' % (func, func, args)
        iface += '  endif\n'
        iface += '  END FUNCTION '+func
        interfaces.append(iface)
    return (
        prec.replace('prec', '16') + '\n\n' +
        prec.replace('prec', '8') + '\n\n\n' +
        '\n\n'.join(interfaces)
    )


def create_parser(subparsers):
    parser = subparsers.add_parser(
        'preproc',
        description='runs the switching pre-processor'
    )
    parser.add_argument(
        'src', nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    parser.add_argument(
        'dest', nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout
    )
    parser.set_defaults(func=main)


def main(parsed):
    buf = parsed.src.read()

    parsed.dest.write(re.sub(
        '!BEGIN SWITCHEROO.*?!END SWITCHEROO',
        lambda m: expand_switch(m.group()),
        buf,
        flags=re.M | re.S
    ))
