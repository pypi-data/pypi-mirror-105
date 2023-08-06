import random
from datetime import datetime
import os
import subprocess
import inspect
import argparse
import sys
import re

try:
    input = raw_input
except NameError:
    pass


def parsestat(s):
    return int(s.
               replace('k','').
               replace('M','000').
               replace('G','000000'))


def getref():
    try:
        rev = subprocess.check_output([
            'git', 'rev-parse', '--short', 'HEAD'
        ], stderr=subprocess.PIPE).splitlines()[0]
        return rev
    except subprocess.CalledProcessError:
        return 'not on git'


def getbranch():
    try:
        rev = subprocess.check_output([
            'git', 'rev-parse', '--abbrev-ref', 'HEAD'
        ], stderr=subprocess.PIPE).splitlines()[0]
        return rev
    except subprocess.CalledProcessError:
        return 'not on git'


def rerunconfig(
  flavour='mu-e', genprocess='m2enn',
  seeds=5, xicuts=[.5, .25, .125],
  stats={
    '0': (10000, 20, 100000, 100),
    'V': (10000, 20, 100000, 100),
    'F': (10000, 20, 100000, 100),
    'C': (10000, 20, 100000, 100),
    'R': (20000, 20, 500000, 100)
  }, folder='', binary='mcmule'
):
    if len(folder) == 0:
        folder = genprocess + flavour

    cargs = [
       '--seeds %s' % ' '.join(str(i) for i in seeds),
       '-xi %s' % ' '.join(str(i) for i in xicuts),
       '--flavour %s' % flavour,
       '--genprocess %s' % genprocess,
       '--output-dir %s' % folder,
       '--prog %s' % binary
    ]
    for part, stat in stats.items():
        if len(stat) == 5:
            cargs.append('--stat %s,%d,%d,%d,%d,%d' % (
                part, stat[0], stat[1], stat[2], stat[3], stat[4])
            )
        else:
            cargs.append('--stat %s,%d,%d,%d,%d' % (
                part, stat[0], stat[1], stat[2], stat[3])
            )

    return cargs


def create_menu(
  flavour='mu-e', genprocess='m2enn',
  seeds=5, xicuts=[.5, .25, .125],
  stats={
    '0': (10000, 20, 100000, 100),
    'V': (10000, 20, 100000, 100),
    'F': (10000, 20, 100000, 100),
    'C': (10000, 20, 100000, 100),
    'R': (20000, 20, 500000, 100)
  }, folder='', binary='mcmule'
):
    totalstat = [0,0,0]

    # We first need to work out how many seeds we need.
    # If a number of seeds per collection is requested, we just
    # count the collections and the seeds per collection
    nseeds = 0
    for k, v in stats.items():
        if len(v) == 4:
            # number of seeds is missing
            if type(seeds) == list:
                raise ValueError('Explicit seeds require the number of seeds '
                                 'per collection to be specified!')
            stats[k] = tuple(list(v) + [seeds])

        if 'C' in k or 'R' in k or 'F' in k:
            nseeds += stats[k][4] * len(xicuts)
        else:
            nseeds += stats[k][4]

    if type(seeds) == int:
        seeds = []
        while len(seeds) < nseeds:
            r = random.randint(10000, 100000)
            if r in seeds:
                continue
            seeds.append(r)
    elif type(seeds) == list:
        if len(seeds) < nseeds:
            print('Not enough seeds provided! Will recycle seeds')
            seeds = seeds * (nseeds//len(seeds)+1)
            seeds = seeds[:nseeds]
    else:
        raise TypeError(
            'Seeds needs to be either list or int, is type '
            + str(type(seeds))
        )

    if len(folder) == 0:
        folder = genprocess + flavour

    rrc = rerunconfig(
        flavour, genprocess, seeds, xicuts,
        stats, folder, binary
    )
    print('Building files. To rerun this, execute')
    print('python %s create\\' % sys.argv[0])
    print(' \\\n'.join(
        '      ' + i for i in rrc
    ))

    header = (
      '## Generated at %s by %s\n'
      '# git version: %s (%s)\n'
      '# To re-generate, run python %s create \\\n'
    ) % (
        datetime.now().strftime('%H:%M on %B %d %Y'), os.environ['USER'],
        getbranch(), getref(), sys.argv[0]
    ) + ' \\\n'.join(
        '#      ' + i for i in rrc
    )

    menu = '\n\nconf %s/%s-%s.conf' % (folder, genprocess, flavour)
    config = ('\n\n# specify the program to run relative to `pwd`\n'
              'binary=%s\n\n'
              '# specify the output folder\n'
              'folder=%s/\n\n'
              '# Specify the variables nenter_ad, itmx_ad, nenter and itmx\n'
              '# for each piece you want to run.\n'
              'declare -A STAT=(\n') % (binary, folder)

    for part,stat in stats.items():
        config += '  [\'%s%s\']=\'%d\\n%d\\n%d\\n%d\'\n' % (
            genprocess, part, stat[0], stat[1], stat[2], stat[3]
        )
        if stat[0] < stat[1] or stat[2] < stat[3]:
            print('Warning! In part %s, calls and itmx might be swapped!' % (
                part
            ))

        xiloop = (
            'R'  in part or                      # real corrections
            'F'  in part or                      # eikonal subtracted corrections
            'C'  in part                         # explicit counter term
        )

        for xi in (xicuts if xiloop else [1.]):
            totalstat[0] += stat[4]*(stat[1] + stat[3])  # iterations
            # iterations
            totalstat[1] += 1000*stat[4]*(stat[0]*stat[1] + stat[2]*stat[3])
            # runs
            totalstat[2] += stat[4]
            menu += '\n\n'
            menu += '\n'.join(
                'run %d %f %s%s %s 0' % (seeds.pop(), xi, genprocess, part, flavour)
                for i in range(stat[4])
            )

        menu += '\n\n'
    config += ')'

    if totalstat[1] > 999999999999:
        c = 'T'
        p = float(totalstat[1])/1.e12
    elif totalstat[1] > 999999999:
        c = 'G'
        p = float(totalstat[1])/1.e9
    elif totalstat[1] > 999999:
        c = 'M'
        p = float(totalstat[1])/1.e6
    elif totalstat[1] > 999:
        c = 'k'
        p = float(totalstat[1])/1.e3
    print('Expect %d iterations, %f%s calls, and %d runs' % (
        totalstat[0], p, c, totalstat[2]
    ))
    return (
        [os.path.join(folder, 'menu-%s-%s.menu' % (genprocess, flavour)), header + menu],
        [os.path.join(folder, '%s-%s.conf' % (genprocess, flavour)), header + config],
        folder
    )


def interogate(args={}):
    specs = inspect.getargspec(create_menu)
    defaults = dict(zip(specs.args, specs.defaults))

    def basic_ask(msg, default, parser=(lambda x: x)):
        if type(default) == list:
            default = ', '.join(str(i) for i in default)
        else:
            default = str(default)
        ans = input('%s? [%s] ' % (msg, default))
        if ans == '':
            return parser(default)
        else:
            return parser(ans)

    def ask(key, msg, parser=(lambda x: x)):
        if key not in args:
            args[key] = basic_ask(msg, defaults[key], parser)

    ask('genprocess', 'What generic process')
    ask('flavour', 'Which flavour combination')
    ask('seeds', 'How many / which seeds',
        parser=lambda x: (
            int(x) if ',' not in x else [int(i) for i in x.split(',')]
        ))
    ask('xicuts', 'Which xi cuts',
        parser=lambda x: [float(i) for i in x.split(',')]
        )
    defaults['folder'] = args['genprocess'] + args['flavour']
    ask('folder', 'Where to store data')
    ask('binary', 'Which binary to run')

    if 'stats' not in args:
        pieces = basic_ask(
            'Which pieces', ['0', 'F', 'R'],
            parser=lambda x: [i.strip() for i in x.split(',')]
        )
        args['stats'] = {}
        for piece in pieces:
            args['stats'][piece] = basic_ask(
                'How much statistics for ' + piece + ' (pc, pi, c, i)',
                ['10M', '20', '100M', '100'],
                parser=lambda x: tuple(parsestat(i) for i in x.split(','))
            )
    return args


def create_parser(subparsers):
    specs = inspect.getargspec(create_menu)
    defaults = dict(zip(specs.args, specs.defaults))

    parser = subparsers.add_parser(
        'create',
        description='Generate menu and config files'
    )
    parser.add_argument(
        '-i', action='store_true',
        help='reads all arguments and questions the user about the rest'
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-ns', '--nseeds', type=int,
        help='number of random seeds to use [%d]' % defaults['seeds']
    )
    group.add_argument('--seeds', nargs='+', type=int, help='list of seeds')

    parser.add_argument(
        '-xi', nargs='+', type=float,
        help='list of xicut [%s]' % (
            ','.join(str(i) for i in defaults['xicuts'])
        )
    )

    parser.add_argument(
        '-f', '--flavour', type=str,
        help='flavour variable [%s]' % defaults['flavour']
    )
    parser.add_argument(
        '-p', '--genprocess', type=str,
        help='the generic process [%s]' % defaults['genprocess']
    )

    parser.add_argument(
        '-d', '--output-dir', help='output folder, aborts if folder exists'
    )
    parser.add_argument(
        '--force', action='store_true', help='overwrite existing files'
    )

    parser.add_argument(
        '--prog', default='mcmule', help='executable of the MC [mcmule]'
    )

    parser.add_argument(
        '-s', '--stat', action='append',
        help='comma seperated list of piece,pc,pi,c,i[,seeds to use]'
    )
    parser.set_defaults(func=main)


def parseargs(parsed):
    args = {}

    if parsed.nseeds:
        args['seeds'] = parsed.nseeds
    if parsed.seeds:
        args['seeds'] = parsed.seeds
    if parsed.xi:
        args['xicuts'] = parsed.xi

    if parsed.stat:
        args['stats'] = {}
        for stat in parsed.stat:
            s = stat.split(',')
            args['stats'][s[0]] = tuple(parsestat(i) for i in s[1:])
    elif not parsed.i:
        args['stats'] = defaults['stats']

    if parsed.flavour:
        args['flavour'] = parsed.flavour
    if parsed.genprocess:
        args['genprocess'] = parsed.genprocess

    if parsed.output_dir:
        args['folder'] = parsed.output_dir
    if parsed.prog:
        args['binary'] = parsed.prog

    if parsed.i:
        args = interogate(args)
    elif not parsed.output_dir:
        parser.error('Check your flags')

    return args, parsed.force


def save(menu, conf, folder, force=False):
    toolspath = os.path.dirname(os.path.realpath(__file__))
    if os.path.isdir(folder):
        print('The folder %s already exists.' % folder)
        if not force:
            raise SystemExit('File exists')
        else:
            print('Overwritting.')
    else:
        os.mkdir(folder)
        os.mkdir(os.path.join(folder, 'out'))
        if 'afs' in toolspath:
            print('You are running on AFS, won\'t fix permissions')
        else:
            os.chmod(folder, 0o2775)
            os.chmod(os.path.join(folder, 'out'), 0o2775)

    with open(os.path.join(toolspath, 'submit.sh')) as fp:
        submit = fp.read()

    submit = re.sub(
        '^#SBATCH --output=.*/slurm-%j.out$',
         '#SBATCH --output=%s/slurm-%%j.out' % folder,
        submit, flags=re.M
    )
    submit = re.sub(
        '^#SBATCH --input=.*$',
         '#SBATCH --input=%s' % menu[0],
        submit, flags=re.M
    )
    submit = re.sub(
        '^this=\./submit\.sh$',
         'this=%s/submit.sh' % folder,
        submit, flags=re.M
    )

    with open(menu[0], 'w') as fp:
        fp.write(menu[1])
    with open(conf[0], 'w') as fp:
        fp.write(conf[1])
    with open(os.path.join(folder, 'submit.sh'), 'w') as fp:
        fp.write(submit)

    os.chmod(menu[0], 0o664)
    os.chmod(os.path.join(folder, 'submit.sh'), 0o775)

    print('Created menu, config and submit script in %s.' % folder)
    print('Please change the ntasks and time options accordingly')


def main(parsed):
    args, force = parseargs(parsed)
    menu, config, folder = create_menu(**args)
    save(menu, config, folder, force=force)
