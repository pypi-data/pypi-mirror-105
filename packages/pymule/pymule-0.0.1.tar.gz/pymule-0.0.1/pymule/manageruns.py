from .PathType import PathType
import argparse
import os
import shutil
import subprocess
import re


try:
    input = raw_input
except NameError:
    pass


def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input('%s (%s) ' % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values


def create_dup_parser(subparsers):
    parser = subparsers.add_parser(
        'cp',
        description='Copies a set run with or without data to a '
                    'new location relative to pwd'
    )
    parser.add_argument('src', type=PathType(
        type='dir', dash_ok=False
    ))
    parser.add_argument('dest', type=PathType(
        type='dir', dash_ok=False, exists=False
    ))
    parser.add_argument('--keep', action='store_true')
    parser.add_argument('--dry', action='store_true')
    parser.add_argument('-i', action='store_true')

    parser.set_defaults(func=dup_main)


def dup_main(parsed):
    def check(msg, opt=False):
        if parsed.dry:
            print(msg)
            return False
        if parsed.i:
            ans = yn_choice(msg)
            if ans:
                return True
            else:
                if opt:
                    return False
                else:
                    raise argparse.ArgumentError('Aborting. This was not negotiable')
        else:
            return True

    toolspath = os.path.dirname(os.path.realpath(__file__))

    files = set(
        i
        for i in os.listdir(parsed.src)
        if os.path.isfile(os.path.join(parsed.src, i))
    )

    runfiles = set(
        i
        for i in files
        if os.path.splitext(i)[1] in ['.menu', '.sh', '.conf']
    )

    if check('Create directory %s' % parsed.dest):
        os.mkdir(parsed.dest)
    if check('Create directory %s/out/' % parsed.dest):
        os.mkdir(os.path.join(parsed.dest, 'out'))
    if 'afs' in toolspath:
        print('You are running on AFS, won\'t fix permissions')
    else:
        if check('Fixing permissions', opt=True):
            os.chmod(parsed.dest, 0o2775)
            os.chmod(os.path.join(parsed.dest, 'out'), 0o2775)

    for f in runfiles:
        if check('cp %s %s' % (os.path.join(parsed.src, f), os.path.join(parsed.dest, f)), opt=True):
            with open(os.path.join(parsed.src, f)) as fp:
                fc = fp.read()
            with open(os.path.join(parsed.dest, f), 'w') as fp:
                fp.write(
                    fc.replace(parsed.src, parsed.dest)
                )

            if os.path.splitext(f)[1] == '.sh':
                os.chmod(os.path.join(parsed.dest, f), 0o775)
            else:
                os.chmod(os.path.join(parsed.dest, f), 0o664)

    if parsed.keep:
        for f in files - runfiles:
            if check('cp %s %s' % (
                os.path.join(parsed.src, f), os.path.join(parsed.dest, f)
            ), opt=True):
                shutil.copy(os.path.join(parsed.src, f), os.path.join(parsed.dest, f))
        for f in os.listdir(os.path.join(parsed.src, 'out')):
            if check('cp %s %s' % (
                os.path.join(parsed.src, 'out', f), os.path.join(parsed.dest, 'out', f)
            ), opt=True):
                shutil.copy(
                    os.path.join(parsed.src, 'out',f), os.path.join(parsed.dest, 'out', f)
                )


def create_rm_parser(subparsers):
    parser = subparsers.add_parser(
        'rm',
        description='Removes all results from run'
    )
    parser.add_argument('dir', type=PathType(
        type='dir', dash_ok=False
    ))
    parser.add_argument('-f', action='store_true')

    parser.set_defaults(func=rm_main)


def rm_main(parsed):
    files = set(
        i
        for i in os.listdir(parsed.dir)
        if os.path.isfile(os.path.join(parsed.dir, i))
    )
    files.update(set(
        os.path.join('out', i) for i in os.listdir(os.path.join(parsed.dir, 'out'))
        if os.path.isfile(os.path.join(parsed.dir, 'out', i))
    ))

    runfiles = set(
        i
        for i in files
        if os.path.splitext(i)[1] in ['.menu', '.sh', '.conf', '.f95']
    )

    for fn in files - runfiles:
        f = os.path.join(parsed.dir, fn)
        if parsed.f or yn_choice('remove file %s' % f):
            os.remove(f)
        else:
            print('Skipping %s.' % f)


def create_backup_parser(subparsers):
    parser = subparsers.add_parser(
        'tar',
        description='Creates a tar file from a run folder'
    )
    parser.add_argument('dir', type=PathType(
        type='dir', dash_ok=False
    ))
    parser.add_argument(
        '-o', type=argparse.FileType('wb'), help='output file'
    )
    parser.add_argument(
        '-lib', action='store_true', help='prepare for addition to user library'
    )
    parser.add_argument(
        '--compression',
        choices=(
            ['gzip-%d' % i for i in range(1,10)] +
            ['xz-%d' % i for i in range(1,10)] +
            ['bzip2-%d' % i for i in range(1,10)]
        ),
        default='gzip-6',
        metavar='{gzip-{1-9}, xz-{1-9}, bzip2-{1-9}}'
    )

    parser.set_defaults(func=backup_main)


def backup_main(parsed):
    compr, level = re.match(
        '(gzip|xz|bzip2)-(\d)',
        parsed.compression
    ).groups()

    if parsed.o is None:
        ext = {
            'gzip': 'gz', 'xz': 'xz', 'bzip2': 'bz2'
        }[compr]

        tarfile = parsed.dir
        if tarfile.endswith('/'):
            tarfile = tarfile[:-1]
        tarfile = tarfile + '.tar.' + ext
        fp = open(tarfile, 'wb')
    else:
        fp = parsed.o

    if parsed.lib:
        tarforlib(fp, parsed.dir)
    else:
        tardir(fp, parsed.dir, compr, level)


def tardir(fp, folder, compr, level):
    pcompr = subprocess.Popen([
        compr, '-' + level
    ], stdout=fp, stdin=subprocess.PIPE)

    ptar = subprocess.Popen([
        'tar', 'cvf', '-', folder
    ], stdout=pcompr.stdin)
    ptar.wait()

    pcompr.stdin.close()
    pcompr.wait()


def tarforlib(fp, folder):
    import tarfile
    import io

    fx = io.BytesIO()
    tar = tarfile.open(fileobj=fx, mode='w|')
    for f in os.listdir(os.path.join(folder, 'out')):
        tar.add(os.path.join(folder, 'out', f), os.path.join('out', f))
    presize = [i.size for i in tar]
    n = len(presize)
    presize = sum(presize)
    tar.close()

    proc = subprocess.Popen(
        ['bzip2', '-9'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    out = proc.communicate(fx.getvalue())[0]
    print('Compressed %d out files (%d byte/%d byte = %0.2f)' % (
        n, len(out), presize, float(len(out))/float(presize)
    ))

    fx = io.BytesIO()
    tar = tarfile.open(fileobj=fx, mode='w|')
    for f in os.listdir(folder):
        if 'worker' not in f:
            continue
        tar.add(os.path.join(folder, f), os.path.join('workers', f))
    presize = [i.size for i in tar]
    n = len(presize)
    presize = sum(presize)
    tar.close()
    proc = subprocess.Popen(
        ['xz', '-9'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    workers = proc.communicate(fx.getvalue())[0]
    print('Compressed %d workers (%d byte/%d byte = %0.2f)' % (
        n, len(workers), presize, float(len(workers))/float(presize)
    ))

    tar = tarfile.open(fileobj=fp, mode='w:gz')
    for f in os.listdir(folder):
        ext = os.path.splitext(f)[1]
        if ext == '.menu' or ext == '.conf' \
           or f.endswith('patch.gz') or f.startswith('user-'):
            print('Adding %s.' % f)
            tar.add(os.path.join(folder, f))

    def addsubtar(name, s):
        t = tarfile.TarInfo(os.path.join(folder, name))
        t.size = len(s)
        t.uid = os.getuid()
        t.gid = os.getgid()
        try:
            import pwd
            import grp
            t.uname = pwd.getpwuid(t.uid)[0]
            t.gname = grp.getgrgid(t.gid)[0]
        except ImportError:
            pass
        tar.addfile(t, io.BytesIO(s))

    addsubtar('out.tar.bz2', out)
    addsubtar('workers.tar.xz', workers)

    tar.close()
